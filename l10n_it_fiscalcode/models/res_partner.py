# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

try:
    import codicefiscale
except ImportError:
    codicefiscale = False
    _logger.warning(
        'codicefiscale library not found. '
        'If you plan to use advanced verification for italian ssn, please install the codicefiscale library '
        'from https://pypi.python.org/pypi/codicefiscale')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_individual = fields.Boolean(default=True)
    fiscalcode = fields.Char(
        string='Fiscal Code', size=16, help="""For non-italian partners, this can be used as a SSN field.""")

    company_type = fields.Selection(selection_add=[('nominal_company', 'Nominal Company')],
        compute='_compute_company_type', inverse='_write_company_type')

    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            if partner.is_company:
                partner.company_type = (partner.is_individual and 'nominal_company') or 'company'
                continue
            partner.company_type = 'person'

    def _write_company_type(self):
        for partner in self:
            partner.is_company = (partner.company_type in ['company', 'nominal_company'])
            partner.is_individual = (partner.company_type in ['person', 'nominal_company'])

    @api.onchange('company_type')
    def onchange_company_type(self):
        self.update({
            'is_company': True if (self.company_type in ['company', 'nominal_company']) else False,
            'is_individual': True if (self.company_type in ['person', 'nominal_company']) else False
        })

    @api.model
    def _commercial_fields(self):
        """ Returns the list of fields that are managed by the commercial entity
        to which a partner belongs. These fields are meant to be hidden on
        partners that aren't `commercial entities` themselves, and will be
        delegated to the parent `commercial entity`. The list is meant to be
        extended by inheriting classes. """
        return super(ResPartner,self)._commercial_fields() + ['fiscalcode']

    @api.constrains('fiscalcode', 'is_individual', 'is_company')
    def _check_fiscalcode(self):
        for partner in self:
            if (not partner.country_id) or (partner.commercial_partner_id.id != partner.id):  # We can't check on country-less partners, and shouldn't be too strict on partners with no commercial implications.
                continue
            check_func = getattr(partner, '_{}_check_fiscalcode'.format(partner.country_id.code.lower()), False)
            if not check_func:
                continue
            check_func()
            
    def _it_check_fiscalcode(self):
        if self.fiscalcode:
            if self.is_individual:
                if len(self.fiscalcode) != 16:
                    raise ValidationError(
                        _("Italian fiscal code for individuals must be exactly 16 characters.")
                    )
                if codicefiscale and (not codicefiscale.isvalid(self.fiscalcode)):
                    raise ValidationError(
                        _("Advanced fiscal code verification failed.")
                    )
            elif self.is_company:
                if len(self.fiscalcode) != 11:
                    raise ValidationError(
                        _("Italian fiscal code for juridic entities must be exactly 11 characters.")
                    )