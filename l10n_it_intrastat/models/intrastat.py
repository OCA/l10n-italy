# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountIntrastatCustom(models.Model):
    _name = 'account.intrastat.custom'
    _description = 'Customs Sections'

    code = fields.Char(
        size=6)
    name = fields.Char()
    date_start = fields.Date(
        string="Start Date")
    date_stop = fields.Date(
        string="Stop Date")


class ReportIntrastatCode(models.Model):
    _name = "report.intrastat.code"
    _description = "Intrastat code"

    name = fields.Char(
        string="Intrastat Code")
    active = fields.Boolean(
        default=True)
    additional_unit_required = fields.Boolean(
        string="Additional Unit of Measure Required")
    additional_unit_from = fields.Selection(
        selection=[
            ('quantity', "Quantity"),
            ('weight', "Weight"),
            ('none', "None")],
        string="Additional Unit of Measure from")
    additional_unit_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="Additional Unit of Measure")
    type = fields.Selection(
        selection=[
            ('good', "Goods"),
            ('service', "Service")])
    description = fields.Char(
        string="Description",
        translate=True)

    @api.multi
    def name_get(self):
        res = []
        for code in self:
            name = "%s - %s" % (code.name, code.description)
            if len(name) > 50:
                name = name[:50] + '...'
            res.append((code.id, name))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            records = self.search([
                '|', ('name', operator, name), ('description', operator, name)
                ] + args, limit=limit)
        else:
            records = self.search(args, limit=limit)
        return records.name_get()


class ResCountry(models.Model):
    _inherit = 'res.country'

    @api.multi
    def intrastat_validate(self):
        self.ensure_one()
        if not self.code:
            raise ValidationError(
                _("State %s without ISO code") % self.display_name)
        return True


class AccountIntrastatTransport(models.Model):
    _name = 'account.intrastat.transport'
    _description = "Transport Mode"

    code = fields.Char(
        string="Code",
        size=1,
        required=True)
    name = fields.Char(
        string="Name")


class AccountIntrastatTransationNature(models.Model):
    _name = 'account.intrastat.transaction.nature'
    _description = "Transaction Nature"

    code = fields.Char(
        string="Code",
        size=1,
        required=True)
    name = fields.Char(
        string="Name")
