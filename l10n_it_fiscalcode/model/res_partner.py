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

    # Constraints and onchanges
    @api.multi
    @api.onchange('is_company')
    def onchange_iscompany(self):
        """ if partner is switched from company to person,
        is_soletrader is set to False because a simple private citizen
        may not be a sole trader.
        A proper warning is displayed.
        """
        for partner in self:
            if not partner.is_company and partner.is_soletrader:
                # prevoius soletrader partner changed to person partner
                partner.is_soletrader = False
                title = _('Partner type changed')
                message = _('WARNING:\n'
                            'Changing partner type from company to '
                            'person will remove the "Sole Trader" selection '
                            'in the Accounting tab.\nFiscal code may need '
                            'to be changed accordingly.')
                result = {
                    'warning': {'title': title,
                                'message': message, }, }
                return result

    @api.multi
    @api.onchange('fiscalcode', 'parent_id')
    def onchange_fiscalcode(self):
        """ Partners not in same parent/child relationship should
        have different fiscal code.
        A proper warning is displayed.
        """
        self.ensure_one()
        if not self.fiscalcode:
            # fiscalcode empty
            return {}
        # search any partner with same fiscal code in this compamy
        same_fiscalcode_partners = self.search([
            ('fiscalcode', '=', self.fiscalcode),
            ('fiscalcode', '!=', False),
            ('company_id', '=', self.company_id.id),
            ])
        if not same_fiscalcode_partners:
            # there is no partner with same fiscalcode.
            # Safe condition. return
            return {}

        if isinstance(self.id, models.NewId) and not self.parent_id:
            # new record with no parent BUT there are other partners
            # with same fiscal code
            is_fc_present = True
        else:
            # new or old record with parent
            # get first parent to start searching
            parent = self
            while parent.parent_id:
                parent = parent.parent_id
            # all partners in our family tree
            related_partners = self.search([
                ('id', 'child_of', parent.id),
                ('company_id', '=', self.company_id.id),
                ])
            # any partner with same fiscal code OUT of our family tree ?
            is_fc_present = self.search([
                ('id', 'in', same_fiscalcode_partners.ids),
                ('id', 'not in', related_partners.ids),
                ('company_id', '=', self.company_id.id),
                ])

        if is_fc_present:
            title = _('Partner fiscal code is not unique')
            message = _('WARNING:\n'
                        'Partner fiscal code must be unique per'
                        ' company except for partner with'
                        ' parent/child relationship.'
                        ' Partners with same fiscal code'
                        ' and not related, are:\n %s!') % (
                            ', '.join(x.name for x in
                                      same_fiscalcode_partners))
            result = {
                'warning': {'title': title,
                            'message': message, }, }
        else:
            result = {}
        return result

    @api.multi
    @api.constrains('fiscalcode', 'is_soletrader')
    def _check_fiscalcode_constraint(self):
        """ verify fiscalcode content, lenght and isnumeric/isalphanum
        depending if self is private citizen,
        business company or sole trader
        """
        for self in self:
            if not self.fiscalcode:
                # fiscalcode empty. Nothing to check..
                is_fc_ok = True
            elif (not self.is_company or
                  self.is_company and self.is_soletrader):
                # self is a private citizen
                # or a sole trader operating in Italy
                # should have an Italian valid fiscalcode
                if is_valid(self.fiscalcode):
                    is_fc_ok = True
                else:
                    is_fc_ok = False
                    msg = _("The Fiscal Code is invalid")
            elif self.is_company and not self.is_soletrader:
                # self is a business company
                # should have the fiscal code of the same kind of VAT code
                if (self.fiscalcode.isdigit() and
                        len(self.fiscalcode) == 11):
                    is_fc_ok = True
                else:
                    is_fc_ok = False
                    msg = _("The Fiscal Code must be a numeric code "
                            " of length 11")
        if not is_fc_ok:
            raise ValidationError(msg)
