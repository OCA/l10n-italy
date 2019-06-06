from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountIntrastatCustom(models.Model):
    _name = 'account.intrastat.custom'
    _description = 'Customs Sections'

    code = fields.Char(string='Code', size=6)
    name = fields.Char(string='Name')
    date_start = fields.Date(string='Date start')
    date_stop = fields.Date(string='Date stop')


class ReportIntrastatCode(models.Model):

    _inherit = 'report.intrastat.code'

    active = fields.Boolean(default=True)
    additional_unit_required = fields.Boolean(
        default=False,
        string='Unit of Measure Additional Required')
    additional_unit_from = fields.Selection(
        [('quantity', 'Quantity'), ('weight', 'Weight'), ('none', 'None')],
        string='Additional Unit of Measure FROM')
    additional_unit_uom_id = fields.Many2one(
        'product.uom',
        string='Unit of Measure Additional')
    type = fields.Selection(
        [('good', 'Good'), ('service', 'Service')])
    description = fields.Char('Description', translate=True)


class ResCountry(models.Model):

    _inherit = 'res.country'

    @api.model
    def intrastat_validate(self):
        control_ISO_code = self._context.get('control_ISO_code', False)
        if not self:
            raise ValidationError(
                _('Missing Country'))
        if control_ISO_code and not self.code:
            raise ValidationError(
                _('Country %s without ISO code') % (self.name,))
        return True


class AccountIntrastatTransport(models.Model):
    _name = 'account.intrastat.transport'
    _description = 'Transport mode'

    code = fields.Char(string='Code', size=1, required=True)
    name = fields.Char(string='Name')


class AccountIntrastatTransationNature(models.Model):
    _name = 'account.intrastat.transation.nature'
    _description = 'Transaction Nature'

    code = fields.Char(string='Code', size=1, required=True)
    name = fields.Char(string='Name')
