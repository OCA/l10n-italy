odoo.define('l10n_it_pos_fatturapa.models', function(require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('res.partner', ['pec_destinatario', 'electronic_invoice_subjected',
                                        'electronic_invoice_obliged_subject', 'codice_destinatario',
                                        'company_type', 'lastname', 'firstname']);

});
