# Copyright 2023 Nextev Srl


def post_init_hook(env):
    """
    Create DN types and their sequences after installing the module
    if they're not already exist
    """
    companies = env["res.company"].search([])
    for company in companies:
        env["stock.delivery.note.type"].create_dn_types(company)
