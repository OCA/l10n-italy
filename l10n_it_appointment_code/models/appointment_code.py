# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2019 Stefano Consolaro (Associazione PNLUG - Gruppo Odoo)
# Copyright 2021 Alex Comba - Agile Business Group

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AppointmentCode(models.Model):
    _name = "appointment.code"
    _description = "Appointment Code"

    @api.constrains("code")
    def _check_code(self):
        for appointment_code in self:
            domain = [("code", "=", appointment_code.code)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise ValidationError(
                    _("The element with code %s already exists") % appointment_code.code
                )

    code = fields.Char()
    name = fields.Char()
