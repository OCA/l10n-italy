# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from osv import fields, osv, orm
from tools.translate import _
#from ir_mail_server import extract_rfc2822_addresses

def extract_rfc2822_addresses(text):
    """Returns a list of valid RFC2822 addresses
       that can be found in ``source``, ignoring 
       malformed ones and non-ASCII ones.
    """
    if not text: return []
    candidates = address_pattern.findall(tools.ustr(text).encode('utf-8'))
    return filter(try_coerce_ascii, candidates)


SDI_CHANNELS = [
    ('pec', 'PEC'),
    # ('web', 'Web service'), # not implemented
    # ('sftp', 'SFTP'), # not implemented
]


class SdiChannel(osv.osv):
    _name = "sdi.channel"
    _description = "SdI channel"

    _columns = {
        'name': fields.char('Name', required=True, size=32),
        'company_id': fields.many2one('res.company', string='Company', required=True),
    }

    _defaults = {
        'company_id': lambda self, cr, uid, ctx: self.pool.get('res.company')._company_default_get(
            cr, uid, 'sdi.channel', context=ctx),
    }
SdiChannel()


class SdiChannelPEC(osv.osv):
    _inherit = "sdi.channel"

    def _check_pec_server_id(self, cr, uid, ids, context=None):
        for channel in self.browse(cr, uid, ids, context):
            domain = [('pec_server_id', '=', channel.pec_server_id.id)]
            channel_ids = self.search(cr, uid, domain, context=context)
            if len(channel_ids) > 1:
                return False
        return True

    def _check_email_validity(self, cr, uid, ids, context=None):
        for channel in self.browse(cr, uid, ids, context):
            if not extract_rfc2822_addresses(channel.email_exchange_system):
                return False
        return True

    _columns = {
        'channel_type': fields.selection(SDI_CHANNELS, string='SdI channel type', required=True,
            help='PEC is the only implemented channel in this module. Other '
                 'channels (Web, Sftp) could be provided by external modules.'),
        'pec_server_id': fields.many2one('email.server', string='Pec mail server', required=False,
            domain=[('is_fatturapa_pec', '=', True)]),
        'email_exchange_system': fields.char('Exchange System Email Address', size=250),
    }

    _constraints = [
        (_check_pec_server_id, _("The channel %s with pec server %s already exists"), ['pec_server_id']),
        (_check_email_validity, _("Email %s is not valid"), ['email_exchange_system']),
    ]
SdiChannelPEC()


class SdiChannelWEB(osv.osv):
    _inherit = "sdi.channel"

    _columns = {
        'web_server_address': fields.char('Web server address', size=250),
        'web_server_login': fields.char('Web server login', size=32),
        'web_server_password': fields.char('Web server password', size=32),
        'web_server_token': fields.char('Web server token', size=250),
    }
SdiChannelWEB()
