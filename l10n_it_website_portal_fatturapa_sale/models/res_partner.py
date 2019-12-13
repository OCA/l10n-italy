from odoo.addons.sale.models.res_partner import ResPartner


def can_edit_vat(self):
    can_edit_vat = super(ResPartner, self).can_edit_vat()
    if not can_edit_vat:
        return can_edit_vat
    SaleOrder = self.env['sale.order']
    has_so = SaleOrder.search([
        ('partner_id', 'child_of', self.commercial_partner_id.id),
        ('state', 'in', ['sale', 'done'])  # removing 'sent'
    ], limit=1)
    return can_edit_vat and not bool(has_so)


ResPartner.can_edit_vat = can_edit_vat
