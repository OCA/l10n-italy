# -*- coding: utf-8 -*-
# © 2021 Giuseppe Stoduto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
from openerp.addons.product import product as addons_product


class OutCustomField(models.Model):
    """Use custom field to save in the e-bill product line on
    AltiDatiGestionali.
    """
    _name = 'out_custom_fields'
    _description = u'Custom field for out e-bill'
    _order = 'sequence'

    name = fields.Char('Name', size=10, required=True)
    sequence = fields.Integer(string='Sequence', help="Assigns the priority to the list of fields.")
    field_ref = fields.Char(string='Reference Field')
    force_text = fields.Boolean(string="Force export in 'RiferimentoTesto'")
    active = fields.Boolean(string='Active', default=True)

    def set_default_data(self, model):
        view_data = {
            'name': '',
            'model_w_id': model.id,
            'out_custom_field_id': self.id,
            'list_fields': False
        }
        return view_data

    def set_line_data(self, item, model):
        line_data = {
            'name': item.name,
            'model': item.relation,
            'ttype': item.ttype,
            'field_description': item.field_description,
            'view_related_id': model.id,
        }
        return line_data

    def _view(self, view_model, model):
        return {
            'name': _('List fields'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'view_fields',
            'view_id': view_model.id,
            'res_id': model.id,
            'target': 'new',
        }

    def reset_view(self, model, related_model):
        view_model = self.env.ref(
                'l10n_it_fatturapa_out_AltriDatiGestionali.wizard_view_field_form'
                )
        lines = [(5, 0, 0)]
        for line in model.field_id:
            lines.append((0, 0, self.set_line_data(line,
                                                    related_model)))
        related_model.write({'list_fields': lines})
        return self._view(view_model, related_model)

    @api.multi
    def set_fields(self):
        ir_model_abstract_obj = self.env['ir.model.abstract']
        ir_model_obj = self.env['ir.model']
        view_field_obj = self.env['view_fields']
        view_model = self.env.ref(
                'l10n_it_fatturapa_out_AltriDatiGestionali.wizard_view_field_form'
            )
        model = ir_model_obj.search([('model',  '=', 'account.invoice.line')])
        view_data = self.set_default_data(model)
        view_fields_id = view_field_obj.create(view_data)
        view_model_line_ids = []
        for item in model.field_id:
            abstract_data = self.set_line_data(item, view_fields_id)
            view_model_line_ids.append(ir_model_abstract_obj.create(abstract_data).id)

        view_fields_id.write({'list_fields': [(6, 0, view_model_line_ids)]})
        return self._view(view_model, view_fields_id)
