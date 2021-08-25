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
            var order = this.pos.get_order();
            var paymentlines = this.$('.paymentlines');
            paymentlines.on('click','.tickets_number_minus',function(){
                self.click_tickets_number_minus($(this).data('cid'));
            });
            paymentlines.on('click','.tickets_number_plus',function(){
                self.click_tickets_number_plus($(this).data('cid'));
            });

            var total_eligible = order.get_total_meal_voucher_eligible();
            var total_received = order.get_total_meal_voucher_received();
            var change = order.get_change();
            if (total_received > total_eligible && change) {
                this.$("#meal-voucher-issue-credit").removeClass("oe_hidden");
            } else {
                this.$("#meal-voucher-issue-credit").addClass("oe_hidden");
            }
            return res;
        },

        renderElement: function() {
            var self = this;
            var res = this._super();
            this.$('.js_issue_ticket_credit').click(function(){
                self.issue_ticket_credit();
            });
            return res;
        },

        issue_ticket_credit: function() {
            var order = this.pos.get_order();
            if (! this.pos.config.ticket_credit_product_id) {
                this.gui.show_popup('error',{
                        'title': _t('Missing ticket credit product'),
                        'body':  _t("Please configure Ticket credit product in Point of sale configuration"),
                    });
                return false;
            }
            var product = this.pos.db.get_product_by_id(this.pos.config.ticket_credit_product_id[0]);
            var change = order.get_change();
            var existing_credit_line;
            for (var i = 0; i < (order.orderlines.length); i++) {
                if(order.orderlines.at(i).get_product().id == product.id){
                    existing_credit_line = order.orderlines.at(i);
                    break
                }
            }
            if (existing_credit_line) {
                change = existing_credit_line.price + change;
                existing_credit_line.set_quantity('remove');
            }
            order.add_product(product, {price: change});
            this.render_paymentlines();
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
