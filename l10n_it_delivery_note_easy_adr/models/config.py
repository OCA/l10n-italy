from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]
    
    virtual_mass_limit = fields.Integer(
        string="Virtual Mass Max Limit",
        config_parameter="adr_virtual_mass_limit"
    )
    limit_exceeded_message = fields.Char(
        string="Limit exceeded message",
        config_parameter="adr_limit_exceeded_message"
    )
    limit_not_exceeded_message = fields.Char(
        string="Limit not exceeded message",
        config_parameter="adr_limit_not_exceeded_message"
    )
    virtual_mass_min_limit = fields.Integer(
        string="Virtual Mass Min Limit",
        config_parameter="adr_virtual_mass_min_limit"
    )
