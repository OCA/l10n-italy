# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # soglie intrastat
    intrastat_goods_sale_threshold = fields.Monetary(
        string="Soglia Cessioni Intra-UE (beni)"
    )
    intrastat_goods_purchase_threshold = fields.Monetary(
        string="Soglia Acquisti Intra-UE (beni)"
    )
    intrastat_service_sale_threshold = fields.Monetary(
        string="Soglia Prestazioni Rese a soggetti UE (servizi)"
    )
    intrastat_service_purchase_threshold = fields.Monetary(
        string="Soglia Prestazioni Ricevute da soggetti UE (servizi)"
    )
    intrastat_email_recipients = fields.Char(string="Destinatari Email Intrastat")
    # posizioni fiscali intrastat
    fiscal_position_goods_sale_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Vendite Beni"
    )
    fiscal_position_goods_purchase_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Acquisti Beni"
    )
    fiscal_position_service_sale_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Vendite Servizi"
    )
    fiscal_position_service_purchase_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Acquisti Servizi"
    )

    # enable email notification
    intrastat_email_enabled = fields.Boolean(
        string="Enable Intrastat Email Notification",
        default=False,
        help="Enable email notification when Intrastat threshold is exceeded.",
    )
