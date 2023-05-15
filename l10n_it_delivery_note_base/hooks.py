# Copyright 2023 Nextev Srl
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, sequence):
    """
    Create DN types and their sequences after installing the module
    if they're not already exist
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])
    for company in companies:
        env["stock.delivery.note.type"].create_dn_types(company)
