odoo.define('l10n_it_pos_fatturapa.screens', function (require) {
    "use strict";

    var Screens = require('point_of_sale.screens');
    var Model = require('web.Model');

    Screens.ClientListScreenWidget.include({

        display_client_details: function(visibility,partner,clickpos){
            var self = this;
            this._super.apply(self, arguments);
            if (visibility === 'edit') {
                this.$('.electronic_invoice_subjected').off('change').on('change', function(event) {
                    this.value = this.checked;
                    $('#electronic_invoice_subjected').css('display', this.checked ? 'block' : 'none');
                });
            }
        },
     });
});
