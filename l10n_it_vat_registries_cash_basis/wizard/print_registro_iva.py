# -*- coding: utf-8 -*-
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://www.linkgroup.it/>)
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"

    def _get_cash_basis_move_ids(self, wizard):
        move_cash_move_ids = {}
        move_ids = []
        SQL_MOVES = """
        with moves_cash_moves as (
        -- prendo solo i movimenti di giroconto, che identificano la parte
        -- pagata delle fatture sotto regime di cassa.
        -- tramite la tabella account_partial_reconcile, risalgo al movimento
        -- della fattura relativa (che potrebbe essere in un periodo diverso
        -- dal pagamento.
        SELECT
            i.date,
            i.number as protocollo,
            ml2.move_id move_id,
            array_agg(distinct m.id) as cash_move_ids
        FROM  account_move m
        INNER JOIN account_move_line ml on (ml.move_id = m.id)
        INNER JOIN account_partial_reconcile r on
                (tax_cash_basis_rec_id = r.id),
        account_move_line ml2, account_invoice i
        WHERE
            (
                (ml2.id = r.debit_move_id and ml2.invoice_id is not null
                and i.id = ml2.invoice_id)
            OR
                (ml2.id = r.credit_move_id and ml2.invoice_id is not null
                and i.id = ml2.invoice_id)
        )
        AND ml.tax_exigible is True
        AND m.state = 'posted'
        AND ml.date >= %(from_date)s
        AND ml.date <= %(to_date)s
        AND ml.company_id = %(company_id)s
        AND ml2.journal_id in %(journals)s
        GROUP BY 1, 2, 3
        ),
        moves as (
        -- query che identifica solo i movimenti delle fatture, escludendo
        -- quelle a regime di cassa.
        SELECT m.date, m.name as protocollo, m.id as move_id,
            ARRAY[]::integer[] as cash_move_ids
        FROM account_move m
        INNER JOIN account_move_line ml on (ml.move_id = m.id)
        WHERE
        ml.tax_exigible is True
        AND ml.tax_line_id  is not null
        AND ml.invoice_id is not null
        AND m.state = 'posted'
        AND ml.date >= %(from_date)s
        AND ml.date <= %(to_date)s
        AND ml.company_id = %(company_id)s
        AND ml.journal_id in %(journals)s
        )
        -- Unisco tutti i movimenti delle fatture NON per cassa, con
        -- quelle che ho trovato partendo dai giroconti e ordino
        -- per data, protocollo
        SELECT *
        FROM
         (
          SELECT * FROM moves_cash_moves
            UNION
          SELECT * FROM moves
          ) as moves
        ORDER BY date, protocollo
        """
        params = {'from_date': wizard.from_date,
                  'to_date': wizard.to_date,
                  'journals': tuple([j.id for j in wizard.journal_ids]),
                  'company_id': self.env.user.company_id.id}

        self.env.cr.execute(SQL_MOVES, params)
        res = self.env.cr.fetchall()

        for date, protocollo, move_id, c_move_ids in res:
            move_ids.append(move_id)
            if c_move_ids:
                move_cash_move_ids[move_id] = c_move_ids

        return move_ids, move_cash_move_ids

    def print_registro(self):
        """
        Non verrà chiamato il super poiché la query che torna i movimenti, si
        preoccupa di tornare oltre agli id dei movimenti anche gli id dei
        movimenti di cassa associati.
        """
        wizard = self
        cash_move_ids = {}
        move_ids = []
        # controllare se la contabilità è in regime di cassa
        move_ids, cash_move_ids = self._get_cash_basis_move_ids(wizard)

        if not move_ids:
            raise UserError(_('No documents found in the current selection'))

        datas_form = {}
        datas_form['from_date'] = wizard.from_date
        datas_form['to_date'] = wizard.to_date
        datas_form['journal_ids'] = [j.id for j in wizard.journal_ids]
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['registry_type'] = wizard.layout_type
        datas_form['cash_move_ids'] = cash_move_ids

        lang_code = self.env.user.company_id.partner_id.lang
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        datas_form['date_format'] = date_format

        if wizard.tax_registry_id:
            datas_form['tax_registry_name'] = wizard.tax_registry_id.name
        else:
            datas_form['tax_registry_name'] = ''
        datas_form['only_totals'] = wizard.only_totals
        report_name = 'l10n_it_vat_registries.report_registro_iva'
        datas = {
            'ids': move_ids,
            'model': 'account.move',
            'form': datas_form
        }
        return self.env['report'].get_action([], report_name, data=datas)
