from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning


class product_category(models.Model):
    _inherit = 'product.category'

    intrastat_code_id = fields.Many2one('report.intrastat.code',
        string='Intrastat Code')


class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    def get_intrastat_id(self):
        '''
        It Returns the intrastat code with the following priority:
        - Intrastat Code on product template
        - Intrastat Code on product category
        '''
        intrastat_id = False
        # From Product
        if self.intrastat_id:
            intrastat_id = self.intrastat_id.id
        elif self.categ_id and self.categ_id.intrastat_code_id: 
            intrastat_id = self.intrastat_code_id.id
        
        return intrastat_id