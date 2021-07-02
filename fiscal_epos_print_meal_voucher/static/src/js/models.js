odoo.define('fiscal_epos_print_meal_voucher.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.Order = models.Order.extend({

        has_payments_with_tickets: function () {
            var paymentlines = this.get_paymentlines();
            for (var i = 0; i < paymentlines.length; i++) {
                var line = paymentlines[i];
                if (line.cashregister.journal.fiscalprinter_payment_type == '4') {
                    // Payment type: 4 = Ticket with number
                    return true;
                }
            }
            return false;
        },
    });

    var original_export_for_printing = models.Paymentline.prototype.export_for_printing;
    var original_initialize = models.Paymentline.prototype.initialize;
    var original_export_as_JSON = models.Paymentline.prototype.export_as_JSON;

    models.Paymentline = models.Paymentline.extend({
        export_for_printing: function() {
            var res = original_export_for_printing.apply(this, arguments);
            if (res.type == '4') {
                res.type_index = this.tickets_number;
                // la stampante come importo si aspetta il valore unitario del ticket
                res.amount = res.amount / this.tickets_number;
            }
            return res;
        },

        initialize: function(attributes, options) {
            var res = original_initialize.apply(this, arguments);
            this.tickets_number = 0;
            if (this.cashregister.journal.fiscalprinter_payment_type == '4') {
                // when adding a payment line of type "tickets", set 1 ticket by default
                this.tickets_number = 1
            }
            return res;
        },

        export_as_JSON: function() {
            var res = original_export_as_JSON.apply(this, arguments);
            res.tickets_number = this.tickets_number;
            return res;
        },
    });

});
