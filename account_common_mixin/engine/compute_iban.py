def get_company_bank_account(document):

    adoc = document.adapt_document()

    if is_client_doc(adoc):

        pm_id = adoc['payment_mode_id']
        is_fixed = pm_id and bool(
            pm_id.offsetting_account == 'bank_account'
            and
            pm_id.bank_account_link == 'fixed'
        )

        if is_fixed:
            return pm_id.fixed_journal_id.bank_account_id

        elif adoc['assigned_income_bank']:
            return adoc['assigned_income_bank']

        else:
            return adoc['default_company_bank']

        # end if

    elif is_supplier_doc(adoc):

        if adoc['assigned_bank']:
            return adoc['assigned_bank']

        else:
            return adoc['default_company_bank']

        # end if

    else:
        return None
    # end if
# end get_company_bank_account


def get_counterparty_bank_account(document):

    adapted_doc = document.adapt_document()

    if adapted_doc['default_counterparty_bank']:
        return adapted_doc['default_counterparty_bank']
    else:
        return False
    # end if
# end get_counterpart_bank_account


# - - - - - - - - - - -
# Utilità
# - - - - - - - - - - -

def is_client_doc(adapted_doc):

    if adapted_doc['model'] == 'sale.order':
        return True

    elif (
        adapted_doc['model'] in ('account.invoice', 'account.move')
        and
        adapted_doc['type'] in ('out_invoice', 'out_refund')
    ):
        return True

    else:
        return False
    # end if
# _is_client_doc


def is_supplier_doc(adapted_doc):

    if adapted_doc['model'] == 'purchase.order':
        return True

    elif (
            adapted_doc['model'] in ('account.invoice', 'account.move')
            and
            adapted_doc['type'] in ('in_invoice', 'in_refund')
    ):
        return True

    else:
        return False
    # end if
# _is_client_doc
