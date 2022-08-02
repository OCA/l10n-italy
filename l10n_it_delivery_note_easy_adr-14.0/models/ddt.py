from odoo import api, fields, models, _

class DDT(models.Model):
    _inherit = "stock.delivery.note"
    
    virtual_mass = fields.Html(
        string="Virtual Mass",
        compute="_compute_virtual_mass"
    )
    is_adr = fields.Boolean(
        string="Is Adr",
        compute="_compute_is_adr"
    )
    
    def _compute_is_adr(self):
        self.write({'is_adr': False})
        for record in self:
            for line in record.line_ids:
                product = line.product_id
                if product.is_adr:
                    record.is_adr = True
                    break

    def _compute_virtual_mass(self):
        self.write({'virtual_mass': _('Configuration not set.')})
        limit = self.env['ir.config_parameter'].sudo().get_param('adr_virtual_mass_limit')
        min_limit = self.env['ir.config_parameter'].sudo().get_param('adr_virtual_mass_min_limit')
        msg_exceeded = self.env['ir.config_parameter'].sudo().get_param('adr_limit_exceeded_message')
        msg_not_exceeded = self.env['ir.config_parameter'].sudo().get_param('adr_limit_not_exceeded_message')
        
        if msg_exceeded and msg_not_exceeded:
            for record in self:
                sum = 0
                msg = 'CALCOLO MASSA VIRTUALE<br/><br/>'
                for line in record.line_ids:
                    product = line.product_id
                    qty = line.product_qty
                    if product.is_adr:
                        if product.adr_weight == 'weight':
                            qty = qty * product.weight
                            
                    if product.adr_category_id and qty > float(min_limit):
                        sum += (qty * product.adr_category_id.multiplier)
                        msg += 'Cat. %s TOT. %sx%s=%s<br/>' % (
                            product.adr_category_id.name,
                            qty,
                            product.adr_category_id.multiplier,
                            qty*product.adr_category_id.multiplier
                        )
                if float(sum) <= float(limit):
                    msg += '<br/>%s' % msg_not_exceeded.format(virtual_mass=str(sum))
                else:
                    msg += '<br/>%s' % msg_exceeded.format(virtual_mass=str(sum))  
                record.virtual_mass = msg
