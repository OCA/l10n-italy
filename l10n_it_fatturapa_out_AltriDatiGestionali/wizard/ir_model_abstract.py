# -*- coding: utf-8 -*-
# © 2021 Giuseppe Stoduto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _

class IrModelAbstract(models.TransientModel):
    _name = 'ir.model.abstract'

    name = fields.Char(string='Name')
    model = fields.Char(string='Object Relation',
        help="For relationship fields, the technical name of the target model")
    ttype = fields.Selection(
                            string='Field Type',
                            selection='_get_field_types')
    field_description = fields.Char(string='Field Label')
    view_related_id = fields.Many2one('view_fields',
                            string='Relationship view_fields',
                            ondelete='cascade')

    @api.model
    def _get_field_types(self):
        # retrieve the possible field types from the field classes' metaclass
        return sorted((key, key) for key in fields.MetaField.by_type)

    @api.multi
    def add_field_name(self):
        ir_model_obj = self.env['ir.model']
        model_id = ir_model_obj.search([('model',  '=', self.model)])
        out_fields_obj = self.env['out_custom_fields']
        related_model = self.view_related_id
        if self.view_related_id.name:
            self.view_related_id.name = self.view_related_id.name + \
                                        '.'+ self.name
        else:
            self.view_related_id.name = self.name
        self.view_related_id.model_w_id = model_id.id
        return out_fields_obj.reset_view(model_id, related_model)
