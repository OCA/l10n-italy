# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountIntrastatCustom(models.Model):
    _name = 'account.intrastat.custom'
    _description = 'Account INTRASTAT - Customs'

    code = fields.Char(
        size=6)
    name = fields.Char()
    date_start = fields.Date(
        string="Date start")
    date_stop = fields.Date(
        string="Date stop")


class ReportIntrastatCode(models.Model):
    _name = "report.intrastat.code"
    _description = "Intrastat code"

    name = fields.Char(
        string="Intrastat Code")
    active = fields.Boolean(
        default=True)
    additional_unit_required = fields.Boolean(
        string="Unit of Measure Additional Required")
    additional_unit_from = fields.Selection(
        selection=[
            ('quantity', "Quantity"),
            ('weight', "Weight"),
            ('none', "None")],
        string="Additional Unit of Measure FROM")
    additional_unit_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure Additional")
    type = fields.Selection(
        selection=[
            ('good', "Good"),
            ('service', "Service")])
    description = fields.Char(
        string="Description",
        translate=True)


class ResCountry(models.Model):
    _inherit = 'res.country'

    @api.multi
    def intrastat_validate(self):
        self.ensure_one()
        if not self.code:
            raise ValidationError(
                _("Country %s without ISO code") % self.display_name)
        return True


class AccountIntrastatTransport(models.Model):
    _name = 'account.intrastat.transport'
    _description = "Account INTRASTAT - Transport"

    code = fields.Char(
        string="Code",
        size=1,
        required=True)
    name = fields.Char(
        string="Name")


class AccountIntrastatTransationNature(models.Model):
    _name = 'account.intrastat.transation.nature'
    _description = "Account INTRASTAT - Transation Nature"

    code = fields.Char(
        string="Code",
        size=1,
        required=True)
    name = fields.Char(
        string="Name")
