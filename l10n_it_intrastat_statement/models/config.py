# -*- coding: utf-8 -*-
#
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
#

from openerp import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'
    
    intrastat_custom_id = fields.Many2one(
        'account.intrastat.custom', string='Custom'
        )
    
