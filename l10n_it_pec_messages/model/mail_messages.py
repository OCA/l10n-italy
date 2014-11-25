# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################
import base64
import copy
import re
import tempfile
import logging
from openerp.osv import fields, orm
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                                                DEFAULT_SERVER_DATETIME_FORMAT)
from openerp.tools.translate import _
from datetime import datetime,date
from lxml.etree import fromstring, tostring, ElementTree
from lxml.etree import register_namespace

_logger = logging.getLogger(__name__)

class mail_message(orm.Model):
    _inherit = "mail.message"

    _columns = {
        'pec': fields.many2one(
            'fetchmail.server', 'Server Pec',readonly=True),
        'pec_type': fields.selection([
                        ('completa', 'Pec Mail'),
                        ('accettazione', 'Reception'),
                        ('avvenuta-consegna', 'Delivery'),
                        ], 'Pec Type',readonly=True),
        'cert_datetime': fields.datetime(
            'Certified Date and Time ', readonly=True),
        'pec_msg_id': fields.char('PEC-Message-Id',
             help='Message unique identifier', select=1, readonly=1),
        'ref_msg_id': fields.char('ref-Message-Id',
             help='Ref Message unique identifier', select=1, readonly=1),
        'delivery_message_id' : fields.many2one(
            'mail.message', 'Delivery Message',readonly=True),
        'reception_message_id' : fields.many2one(
            'mail.message', 'Reception Message',readonly=True),
    }

