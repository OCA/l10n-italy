from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning


class product_category(models.Model):
    _inherit = 'product.category'

    intrastat_id = fields.Many2one('report.intrastat.code',
        string='Intrastat Code')
