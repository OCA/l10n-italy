# -*- coding: utf-8 -*-
# © 2021 Giuseppe Stoduto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
from openerp.addons.product import product as addons_product
import openerp.addons.decimal_precision as dp

class ViewFields(models.TransientModel):
    _name = 'view_fields'
    _description = 'View Fields'

    name = fields.Char(string='Field name')
    model_w_id = fields.Many2one('ir.model', string='Model', readonly=True,
                                    ondelete='restrict')
    list_fields = fields.One2many('ir.model.abstract', 'view_related_id',
                                    string='List model fields',
                                    readonly=True
                                )
    out_custom_field_id = fields.Many2one(
        string='out_custom_field_id',
        comodel_name='out_custom_fields',
        ondelete='cascade',
        copy=False
    )

    def display_error(self, item):
        raise UserError(_("Error! The '%s' field is not valid.")
                                    % item)

    @api.multi
    def reset_name(self):
        ir_model_obj = self.env['ir.model']
        model = ir_model_obj.search([('model',  '=', 'account.invoice.line')])
        out_fields_obj = self.env['out_custom_fields']
        self.name = ""
        self.model_w_id= model.id
        return out_fields_obj.reset_view(model, self)

    @api.multi
    def confirm_name(self):
        inv_line_obj = self.env['account.invoice.line']
        list_fields = self.name.split(".")
        for item in list_fields:
            if not hasattr(inv_line_obj, item):
                self.display_error(item)
            field = getattr(inv_line_obj, item)
            type_field = inv_line_obj._fields.get(item).type
            if hasattr(inv_line_obj, item) and type_field in ['many2one']:
                inv_line_obj = self.env[field._name]
                if list_fields.index(item) == (len(list_fields) - 1):
                    raise UserError(_("Error! The last '%s' field must "
                                    "have a value other than Many2one.")
                                    % item)
            elif hasattr(inv_line_obj, item) \
                        and type_field in ['one2many', 'many2many']:
                self.display_error(item)
        self.out_custom_field_id.field_ref = self.name
        return True
