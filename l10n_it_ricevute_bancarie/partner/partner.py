# -*- coding: utf-8 -*-
##############################################################################
#    
# Copyright (C) 2016 Andrea Cometa (Apulia Software)
# Email: a.cometa@apuliasoftware.it
# Web site: http://www.apuliasoftware.it
# Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
# Copyright (C) 2012 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo.osv import fields, orm

class res_partner(orm.Model):

    _name = "res.partner"
    _inherit = "res.partner"

    _columns = {
        'group_riba' : fields.boolean("Group Ri.Ba.", 
            help="Group Ri.Ba. by customer while issuing"),
    }

