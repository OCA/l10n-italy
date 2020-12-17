from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PaymentReason(models.Model):
    _name = "payment.reason"
    _description = "Payment Reason"

    @api.constrains("code")
    def _check_code(self):
        for reason in self:
            domain = [("code", "=", reason.code)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise ValidationError(
                    _("The element with code %s already exists") % reason.code
                )

    def name_get(self):
        res = []
        for cau in self:
            name = "{} - {}".format(cau.code, cau.name)
            if len(name) > 50:
                name = name[:50] + "..."
            res.append((cau.id, name))
        return res

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Text(string="Description", required=True)
