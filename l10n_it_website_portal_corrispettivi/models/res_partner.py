from odoo import models, api


class Partner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def write(self, vals):
        if "use_invoices" in vals:
            del vals["use_invoices"]
        res = super(Partner, self).write(vals)
        if "use_corrispettivi" in vals:
            for p in self:
                p.onchange_use_corrispettivi()
                vals = p._convert_to_write(p._cache)
                del vals["use_corrispettivi"]
                p.write(vals)
        return res
