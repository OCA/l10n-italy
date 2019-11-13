from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    fiscalcode = fields.Char(
        string="Fiscal Code",
        help="Italian Fiscal Code")

    @api.multi
    def _create_lead_partner(self):
        """Add fiscal code to partner."""
        return (super(Lead, self.with_context(
            default_fiscalcode=self.fiscalcode))._create_lead_partner())

    def _onchange_partner_id_values(self, partner_id):
        """Recover fiscal code from partner if available."""
        result = super(Lead, self)._onchange_partner_id_values(partner_id)
        if not partner_id:
            return result
        partner = self.env['res.partner'].browse(partner_id)
        if partner.fiscalcode:
            result['fiscalcode'] = partner.fiscalcode
        return result
