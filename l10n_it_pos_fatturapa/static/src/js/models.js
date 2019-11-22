odoo.define('l10n_it_pos_fatturapa.models', function (require) {
    "use strict";

  var pos_models = require('point_of_sale.models');

  pos_models.load_fields("res.partner",
    ["electronic_invoice_subjected", "eori_code",
     "codice_destinatario", "pec_destinatario",
     "pa_partner_code"]);

});
