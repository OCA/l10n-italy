# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    # Private attributes
    _inherit = 'res.partner'

    # Fields declaration
    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")

    # Constraints and onchanges
    @api.multi
    @api.constrains('fiscalcode')
    def _check_fiscalcode_constraint(self):
        is_fc_ok=True
        msg=""
        for partner in self:
            if not partner.fiscalcode: is_fc_ok = True
                # fiscalcode empty. Nothing  o check..
            elif partner.is_company:
                # fiscalcode not empty and partner is a company
                if partner.country_id.name == u"Italia":
                    if len(partner.fiscalcode) == 13:
                        is_fc_ok = True 
                    else:
                         is_fc_ok = False
                         msg =u"For Italian companies and organizations the ficalcode must be the same of the VAT code"
                else:
                    # not Italian company with Italian fiscal code ???
                    is_fc_ok = False
                    msg =u"A Company outside Italy cannot have a fiscalcode"
            else:
                # fiscalcode not empty and partner is a person 
                if len(partner.fiscalcode) == 16 and partner.country_id.name == u"Italia":
                    is_fc_ok = True
                else:
                    is_fc_ok = False
                    msg=u"Wrong fiscalcode length or not Italian address"
                    # we test only length and not also CRC, because of possible code collision (omocodia)
                    # false if italian person with fiscal code of wrong length or a non Italian address

        if not is_fc_ok:
                raise ValidationError(msg)
