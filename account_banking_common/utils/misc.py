#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
def external_id_to_res_model_data(env, external_id):
    module, name = external_id.split('.')
    resource = env['ir.model.data'].search([
        ('module', '=', module),
        ('name', '=', name)
    ])
    return resource


def external_id_to_id(env, external_id):
    resource = external_id_to_res_model_data(env, external_id)
    return resource.res_id


def external_id_to_obj(env, external_id):
    resource = external_id_to_res_model_data(env, external_id)
    record = env[resource.model].browse(resource.id)
    return record
