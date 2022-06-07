#  Copyright 2021 Simone Vanin - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    MoveLine = env["account.move.line"]
    Translations = env["ir.translation"]
    source = "Split Payment Write Off"
    text_vals = {source}
    langs = Translations._get_languages()
    for lang, _lang_name in langs:
        text_val = env["ir.translation"]._get_source(
            False, "code", lang=lang, source=source
        )
        text_vals.add(text_val)
    text_vals = list(text_vals)
    line_ids = MoveLine.search([("name", "in", text_vals)]).ids
    if line_ids:
        openupgrade.logged_query(
            cr,
            """
            update account_move_line
            set is_split_payment = True
            where id in {line_ids}
            """.format(
                line_ids=tuple(line_ids)
            ),
        )
