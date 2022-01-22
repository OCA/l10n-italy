#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from . import misc


BANK_EXPENSES_ACCOUNT_EXTERNAL_ID = 'account.data_account_type_expenses'

CURRENT_ASSETS_ACCOUNT_EXTERNAL_ID = 'account.data_account_type_current_assets'
LIQUIDITY_ACCOUNT_EXTERNAL_ID = 'account.data_account_type_liquidity'
CURRENT_LIABILITIES_ACCOUNT_EXTERNAL_ID = \
    'account.data_account_type_current_liabilities'


transfer_journal = [
    ('type', 'not in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])
]
sezionale = transfer_journal

transfer_account = [
    ('user_type_id.type', '=', 'receivable')
]
conto_effetti_attivi = transfer_account

banca_conto_effetti = [
    ('user_type_id.type', 'in', ['bank', 'receivable'])
]

effetti_allo_sconto = [
    ('user_type_id.type', 'in', ['bank', 'receivable'])
]


def get_bank_expenses_account(env):
    acct_type_id = misc.external_id_to_id(
        env, BANK_EXPENSES_ACCOUNT_EXTERNAL_ID
    )
    return [('user_type_id', '=', acct_type_id)]


def domain_effetti_allo_sconto(env):
    # acct_type_ids = list()
    #
    # acct_type_ids.append(misc.external_id_to_id(
    #     env, CURRENT_ASSETS_ACCOUNT_EXTERNAL_ID
    # ))
    # acct_type_ids.append(misc.external_id_to_id(
    #     env, LIQUIDITY_ACCOUNT_EXTERNAL_ID
    # ))
    # acct_type_ids.append(misc.external_id_to_id(
    #     env, CURRENT_LIABILITIES_ACCOUNT_EXTERNAL_ID
    # ))
    #
    # return [('user_type_id', 'in', acct_type_ids)]
    return [('nature', '=', 'A')]


def domain_portafoglio_sbf():
    return ['|', ('nature', '=', 'P'), ('user_type_id.type', '=', 'liquidity')]


get_expenses_account = get_bank_expenses_account
