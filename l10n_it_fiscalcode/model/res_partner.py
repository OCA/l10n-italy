# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

try:
    from stdnum.it.codicefiscale import is_valid
except ImportError:
    _logger.warning(
        'stdnum library not found. '
        'If you plan to use it, please install the python-stdnum library '
        'for Fiscal Code validation '
        'from https://pypi.python.org/pypi/python-stdnum/')


class ResPartner(models.Model):
    """ Extends res.partner to add Italian Fiscal Code
    """
    # Private attributes
    _inherit = 'res.partner'

    # Fields declaration
    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")
    is_soletrader = fields.Boolean(
        string='Sole Trader',
        default=False,
        readonly=False,
        help="Checked if company is a sole trader")

    @api.multi
    @api.onchange('is_company')
    def onchange_iscompany(self):
        """ if partner is switched from company to person,
        is_soletrader is set to False because a simple private citizen
        may not be a sole trader
        """
        for partner in self:
            if partner.is_company is False:
                partner.is_soletrader = False
        return {
            'warning': {
                'title': _('Partner type changed'),
                'message': _('Warning: the partner has been changed'
                             ' from company to private citizen.\n'
                             'Sole trader selection remove.'
                             ' Please verify fiscal code'),
                },
                }

    # Constraints and onchanges
    @api.multi
    @api.constrains('fiscalcode')
    def _check_fiscalcode_constraint(self):
        """ verify fiscalcode content, lenght and isnumeric/isalphanum
        depending if partner is private citizen,
        business company or sole trader
        """
        for partner in self:
            if not partner.fiscalcode:
                # fiscalcode empty. Nothing to check..
                is_fc_ok = True
            elif partner.country_id.code != "IT":
                # partners outside Italy cannot have an Italian fiscalcode
                is_fc_ok = False
                msg = _("The Fiscal Code can only belong to "
                        "Italian citizens/companies")
            elif (not partner.is_company or
                  partner.is_company and partner.is_soletrader):
                # partner is a private citizen resident in Italy
                # or a sole trader resident in Italy
                # should have an Italian standard fiscalcode
                if is_valid(partner.fiscalcode):
                    is_fc_ok = True
                else:
                    is_fc_ok = False
                    msg = _("The Fiscal Code is not correct")
            elif partner.is_company and not partner.is_soletrader:
                # partner is an Italian business company
                # should have the fiscal code of the same kind of VAT code
                if (partner.fiscalcode.isnumeric() and
                        len(partner.fiscalcode) == 11):
                    is_fc_ok = True
                else:
                    is_fc_ok = False
                    msg = _("The Fiscal Code must be numeric and"
                            " of length 11")
        if not is_fc_ok:
            raise ValidationError(msg)
