# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Addebito diretto SEPA per l'Italia",
    "summary": "Crea file SEPA per l'addebito diretto",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Carlo Vettore, berim, Ooops404, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "category": "Banking addons",
    "external_dependencies": {"python": ["fintech>=7.2.10"]},
    "depends": ["account_banking_sepa_credit_transfer", "account_payment_order"],
    "data": [
        "data/account_payment_method.xml",
        "views/account_payment_line.xml",
        "views/res_partner_bank.xml",
    ],
    "installable": True,
    "auto_install": False,
}
