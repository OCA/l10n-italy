# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta 
# version 0.1 - changed method check_fiscalcode() to consider multiple situation
#             - removed local "individual" field, to use "is_company" original res.partner.is_compamy field
#             - prefixed (_) constrain method, to adhere with OCA convention 
#             - https://github.com/OCA/maintainer-tools/blob/master/CONTRIBUTING.md#oca-guidelines  
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# 1: imports of python lib
# 2: import of known third party lib
# 3:  imports of openerp
from odoo import models, fields, api


class ResPartner(models.Model):
    # Private attributes
    _inherit = 'res.partner'
    
    # Fields declaration
    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")
   
    # Constraints and onchanges
    @api.multi
    def _check_fiscalcode(self):
        for partner in self:
            if not partner.fiscalcode:
                #fiscalcode empty. Nothing  o check...
                return True
            elif partner.is_company :
                #fiscalcode not empty and partner is a company
                if partner.country_id.name == u"Italia":
                    if len(partner.fiscalcode) == 13:
                        #Italian company with fiscal code long 13 (as VAT ITxx)
                        return True
                    else:
                        #wrong fiscalcode length for an Italian company  
                        return False
                else:
                    # not Italian company with Italian fiscal code ???
                    return False
            else:
                #fiscalcode not empty and partner is a person
                if len(partner.fiscalcode) == 16 and partner.country_id.name == u"Italia":
                # we test only length and not also CRC, because of possible code collision (omocodia)
                    return True
                else :
                    #italian person with fiscal code of wrong length or a non Italian address
                    return False   
  
    _constraints = [
        (check_fiscalcode,"The fiscal code doesn't seem to be correct.", ["fiscalcode"])


    ]
