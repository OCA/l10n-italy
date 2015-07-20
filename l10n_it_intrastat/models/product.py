from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning


class product_category(models.Model):
    _inherit = 'product.category'

    intrastat_code_good = fields.Many2one('account.intrastat.code.good',
        string='INTRASTAT Code for goods')
    intrastat_code_service = fields.Many2one('account.intrastat.code.service',
        string='INTRASTAT Code for services')


class product_template(models.Model):
    _inherit = 'product.template'

    intrastat_code_good = fields.Many2one('account.intrastat.code.good',
        string='INTRASTAT Code for goods')
    intrastat_code_service = fields.Many2one('account.intrastat.code.service',
        string='INTRASTAT Code for services')
