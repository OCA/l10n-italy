odoo.define('fiscal_epos_print.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var core = require("web.core");
    var utils = require('web.utils');
    var _t = core._t;
    var round_pr = utils.round_precision;
    var OrderSuper = models.Order;

    models.load_fields("account.journal",
        ["fiscalprinter_payment_type", "fiscalprinter_payment_index"]);

    models.Order = models.Order.extend({
        initialize: function(attributes, options){
            OrderSuper.prototype.initialize.call(this, attributes, options);
            this.lottery_code = null;
            this.refund_report = null;
            this.refund_date = null;
            this.refund_doc_num = null;
            this.refund_cash_fiscal_serial = null;
            this.has_refund = false;
            this.fiscal_receipt_number = null;
            this.fiscal_receipt_amount = null;
            this.fiscal_receipt_date = null;
            this.fiscal_z_rep_number = null;
            this.fiscal_printer_serial = this.pos.config.fiscal_printer_serial || null;
            this.fiscal_printer_debug_info = null;
        },

        // Manages the case in which after printing an invoice
        // you pass a barcode in the mask of the registered invoice
        add_product: function(product, options) {
            if(this._printed || this.finalized == true) {
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            OrderSuper.prototype.add_product.apply(this, arguments);
        },

        check_order_has_refund: function() {
            var order = this.pos.get_order();
            if (order) {
                var lines = order.orderlines;
                order.has_refund = lines.find(function(line){ return line.quantity < 0.0;}) != undefined;
            }
        },

        init_from_JSON: function (json) {
            OrderSuper.prototype.init_from_JSON.apply(this, arguments);
            this.lottery_code = json.lottery_code;
            this.refund_report = json.refund_report;
            this.refund_date = json.refund_date;
            this.refund_doc_num = json.refund_doc_num;
            this.refund_cash_fiscal_serial = json.refund_cash_fiscal_serial;
            this.check_order_has_refund();
            this.fiscal_receipt_number = json.fiscal_receipt_number;
            this.fiscal_receipt_amount = json.fiscal_receipt_amount;
            this.fiscal_receipt_date = json.fiscal_receipt_date;
            this.fiscal_z_rep_number = json.fiscal_z_rep_number;
            this.fiscal_printer_serial = json.fiscal_printer_serial;
            this.fiscal_printer_debug_info = json.fiscal_printer_debug_info;
        },

        export_as_JSON: function() {
            var result = OrderSuper.prototype.export_as_JSON.call(this);
            result.lottery_code = this.lottery_code;
            result.refund_report = this.refund_report;
            result.refund_date = this.refund_date;
            result.refund_doc_num = this.refund_doc_num;
            result.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;
            result.fiscal_receipt_number = this.fiscal_receipt_number;
            result.fiscal_receipt_amount = this.fiscal_receipt_amount;
            result.fiscal_receipt_date = this.fiscal_receipt_date; // parsed by backend
            result.fiscal_z_rep_number = this.fiscal_z_rep_number;
            result.fiscal_printer_serial = this.fiscal_printer_serial || null;
            result.fiscal_printer_debug_info = this.fiscal_printer_debug_info;
            return result;
        },

        export_for_printing: function(){
            var receipt = OrderSuper.prototype.export_for_printing.call(this);

            receipt.lottery_code = this.lottery_code;
            receipt.refund_date = this.refund_date;
            receipt.refund_report = this.refund_report;
            receipt.refund_doc_num = this.refund_doc_num;
            receipt.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;
            receipt.fiscal_receipt_number = this.fiscal_receipt_number;
            receipt.fiscal_receipt_amount = this.fiscal_receipt_amount;
            receipt.fiscal_receipt_date = this.fiscal_receipt_date;
            receipt.fiscal_z_rep_number = this.fiscal_z_rep_number;
            receipt.fiscal_printer_serial = this.fiscal_printer_serial;
            receipt.fiscal_printer_debug_info = this.fiscal_printer_debug_info;

            return receipt
        },

        getPrinterOptions: function (){
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return {url: printer_url};
        },
    });

    var _orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var res = _orderline_super.export_for_printing.call(this, arguments);
            res['tax_department'] = this.get_tax_details_r();
            if (res['tax_department']['included_in_price'] == true) {
                res['full_price'] = this.price
            }
            else {
                res['full_price'] = this.price * (1 + (res['tax_department']['tax_amount'] / 100))
            }
            return res;
        },
        get_tax_details_r: function(){
            var details =  this.get_all_prices();
            for (var i in details.taxDetails){
                return {
                    code: this.pos.taxes_by_id[i].fpdeptax,
                    taxname: this.pos.taxes_by_id[i].name,
                    included_in_price: this.pos.taxes_by_id[i].price_include,
                    tax_amount: this.pos.taxes_by_id[i].amount,
                }
            }
            this.pos.gui.show_popup('error', {
                'title': _t('Error'),
                'body': _t('No taxes found'),
            });
        },
        set_quantity: function(quantity, keep_price) {
            if (quantity == '0') {
                // Epson FP doesn't allow lines with quantity 0
                quantity = 'remove';
            }
            return _orderline_super.set_quantity.call(this, quantity, keep_price);
        },
        compute_all: function(taxes, price_unit, quantity, currency_rounding, no_map_tax) {
            var res = _orderline_super.compute_all.call(this, taxes, price_unit, quantity, currency_rounding, no_map_tax);
            var self = this;

            var total_excluded = round_pr(price_unit * quantity, currency_rounding);
            var total_included = total_excluded;
            var base = total_excluded;
            var list_taxes = res.taxes;
            // amount_type 'group' not handled (used only for purchases, in Italy)
            _(taxes).each(function(tax) {
                if (!no_map_tax){
                    tax = self._map_tax_fiscal_position(tax);
                }
                if (!tax){
                    return;
                }
                var tax_amount = self._compute_all(tax, base, quantity);
                tax_amount = round_pr(tax_amount, currency_rounding);
                if (!tax_amount){
                    // Intervene here: also add taxes with 0 amount
                    if (tax.price_include) {
                        total_excluded -= tax_amount;
                        base -= tax_amount;
                    }
                    else {
                        total_included += tax_amount;
                    }
                    if (tax.include_base_amount) {
                        base += tax_amount;
                    }
                    var data = {
                        id: tax.id,
                        amount: tax_amount,
                        name: tax.name,
                    };
                    list_taxes.push(data);
                }
            });
            res.taxes = list_taxes;

            return res;
        },
    });

    /*
    Overwrite Paymentline.export_for_printing() in order
    to make it export the payment type that must be passed
    to the fiscal printer.
    */
    var original = models.Paymentline.prototype.export_for_printing;
    models.Paymentline = models.Paymentline.extend({
        export_for_printing: function() {
            var res = original.apply(this, arguments);
            res.type = this.cashregister.journal.fiscalprinter_payment_type;
            res.type_index = this.cashregister.journal.fiscalprinter_payment_index;
            return res;
        }
    });

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var tax_model = _.find(this.models, function(model){ return model.model === 'account.tax'; });
            tax_model.fields.push('fpdeptax');
            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });

});
