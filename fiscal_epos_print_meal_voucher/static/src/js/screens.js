odoo.define("fiscal_epos_print_meal_voucher.screens", function (require) {
    "use strict";

    var core = require("web.core");
    var utils = require('web.utils');
    var screens = require('point_of_sale.screens');
    var PaymentScreenWidget = screens.PaymentScreenWidget;
    var float_is_zero = utils.float_is_zero;
    var _t = core._t;

    PaymentScreenWidget.include({
        order_is_valid: function(force_validation) {
            var receipt = this.pos.get_order();
            var res = this._super(force_validation);
            var order_total = receipt.get_total_with_tax();
            var tickets_total = 0;
            for (var i = 0; i < receipt.paymentlines.models.length; i++ ) {
                var line = receipt.paymentlines.models[i];
                if (line.cashregister.journal.fiscalprinter_payment_type == '4') {
                    tickets_total += line.amount;
                }
            }
            if (tickets_total > order_total) {
                if (! float_is_zero(tickets_total - order_total, this.pos.currency.decimals)) {
                    // avoid rounding errors
                    this.gui.show_popup('error',{
                            'title': _t('Wrong tickets total'),
                            'body':  _t("Impossible to pay with tickets more then the amount due"),
                        });
                    return false;
                }
            }
            return res;
        },

        render_paymentlines: function() {
            var self  = this;
            var res = this._super();
            var paymentlines = this.$('.paymentlines');
            paymentlines.on('click','.tickets_number_minus',function(){
                self.click_tickets_number_minus($(this).data('cid'));
            });
            paymentlines.on('click','.tickets_number_plus',function(){
                self.click_tickets_number_plus($(this).data('cid'));
            });
            return res;
        },

        click_tickets_number_minus: function(cid) {
            var lines = this.pos.get_order().get_paymentlines();
            for ( var i = 0; i < lines.length; i++ ) {
                if (lines[i].cid === cid) {
                    lines[i].tickets_number -= 1;
                    if (lines[i].tickets_number < 1) {
                        lines[i].tickets_number = 1;
                    }
                    this.reset_input();
                    this.render_paymentlines();
                }
            }
        },

        click_tickets_number_plus: function(cid) {
            var lines = this.pos.get_order().get_paymentlines();
            for ( var i = 0; i < lines.length; i++ ) {
                if (lines[i].cid === cid) {
                    lines[i].tickets_number += 1;
                    this.reset_input();
                    this.render_paymentlines();
                }
            }
        },

    });

});
