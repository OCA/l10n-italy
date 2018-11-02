# -*- coding: utf-8 -*-
# Copyright 2014 KTec S.r.l.
# (<http://www.ktec.it>).
# Copyright 2014 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Andrea Cometa <a.cometa@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import orm, fields


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'ipa_code': fields.char("IPA Code", size=6),
        'is_pa': fields.boolean("Public administration"),
    }
