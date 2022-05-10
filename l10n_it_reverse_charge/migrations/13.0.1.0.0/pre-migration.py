#  Copyright 2021 Simone Vanin - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    cr = env.cr

    # list of account_move fields for further insert
    openupgrade.logged_query(
        cr,
        """
        SELECT STRING_AGG(column_name, ', ')
        FROM information_schema.columns
        WHERE table_name = 'account_move'
        AND table_schema = 'public'
        AND column_name NOT IN('id')
        ;
        """,
    )

    move_fields = "".join(cr.fetchone())
    query_move = (
        "select "
        + move_fields.replace("create_date", "NOW()").replace("write_date", "NOW()")
        + " from account_move "
    )

    # List of rc invoices
    openupgrade.logged_query(
        cr,
        """
        select
        am.company_id,
        full_reconcile_id,
        am.id,
        inv.rc_purchase_invoice_id,
        aml.account_id
        from account_move_line aml
        join account_move am
        on am.id = aml.move_id
        join account_invoice inv
        on inv.move_id = am.id
        join account_full_reconcile afr
        on afr.id = aml.full_reconcile_id
        where inv.rc_purchase_invoice_id is not null
        and aml.move_id not in (select move_id from account_payment);
    """,
    )

    res = cr.fetchall()

    for r in res:
        company_id, fr_id, rc_inv, supp_inv, rc_dest_acc_id = r
        openupgrade.logged_query(
            cr,
            """
            select am.currency_id, am.partner_id, am.create_uid, aml.account_id
            from account_move am join account_move_line aml
            on am.id = aml.move_id
            where am.id = {supp_inv}
            and aml.account_id in (
                select aa.id from account_account aa
                where aa.internal_type = 'payable'
            );
            """.format(
                supp_inv=supp_inv
            ),
        )
        payment_vals = cr.fetchall()[0]
        currency_id = payment_vals[0]
        partner_id = payment_vals[1]
        create_uid = payment_vals[2]
        supp_dest_acc_id = payment_vals[3]

        openupgrade.logged_query(
            cr,
            """
                select move_id, full_reconcile_id, id, abs(amount_currency)
                from account_move_line
                where move_id in (
                select move_id from account_move_line
        where full_reconcile_id = {fr_id}
        and journal_id in (
            select payment_journal_id
            from account_rc_type
            where method = 'selfinvoice'
        ))
        order by full_reconcile_id;
        """.format(
                fr_id=fr_id
            ),
        )

        # split payment move in two moves
        move_vals = {}
        # format [(inv_move, payment_move)]
        move_ids = []
        supp_amount = 0
        rc_amount = 0
        for m, k, v, amnt in cr.fetchall():
            if k == fr_id:
                k = rc_inv
                rc_amount = amnt
            else:
                if rc_amount and rc_amount == amnt:
                    k = rc_inv
                else:
                    k = supp_inv
                    supp_amount = amnt
            if not move_ids:
                move_ids = [(k, m)]
            move_vals[k] = [v] if k not in move_vals else move_vals[k] + [v]

        # clone payment move and append to list
        openupgrade.logged_query(
            cr,
            """
            insert into account_move ({move_fields})
            {query_move} where id = {move_id}
            returning id;
            """.format(
                move_fields=move_fields, query_move=query_move, move_id=move_ids[0][1]
            ),
        )
        move_ids.append(
            (supp_inv if move_ids[0] == rc_inv else rc_inv, cr.fetchone()[0])
        )

        # create an account_payment record for every payment move
        # update move lines with new move id
        for inv, move_id in move_ids:
            openupgrade.logged_query(
                cr,
                """
                insert into account_payment
                (move_id, is_reconciled, is_matched, is_internal_transfer,
                payment_method_id, amount, payment_type, partner_type,
                currency_id, partner_id, destination_account_id, create_uid,
                create_date, write_uid, write_date)
                values
                ({move_id}, 't', 't', 'f', {method}, {amount}, {payment_type},
                {partner_type}, {currency_id}, {partner_id}, {dest_acc_id},
                {create_uid}, NOW(), {write_uid}, NOW())
                returning id;
                """.format(
                    move_id=move_id,
                    method=1 if inv == supp_inv else 2,
                    amount=supp_amount if inv == supp_inv else rc_amount,
                    payment_type="'outbound'" if inv == supp_inv else "'inbound'",
                    partner_type="'supplier'" if inv == supp_inv else "'customer'",
                    currency_id=currency_id,
                    partner_id=partner_id,
                    dest_acc_id=supp_dest_acc_id if inv == supp_inv else rc_dest_acc_id,
                    create_uid=create_uid,
                    write_uid=create_uid,
                ),
            )
            payment_id = cr.fetchone()[0]

            line_ids = ",".join([str(line_id) for line_id in move_vals[inv]])
            openupgrade.logged_query(
                cr,
                """
                update account_move_line
                set move_id = {move_id},
                    payment_id = {payment_id}
                where id in ({line_ids});
                """.format(
                    move_id=move_id, payment_id=payment_id, line_ids=line_ids
                ),
            )

            openupgrade.logged_query(
                cr,
                """
                update account_move
                set payment_id = {payment_id}
                where id = {move_id};
                """.format(
                    payment_id=payment_id, move_id=move_id
                ),
            )
