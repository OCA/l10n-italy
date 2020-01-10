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
        },

        export_as_JSON: function() {
            var result = OrderSuper.prototype.export_as_JSON.call(this);
            result.refund_report = this.refund_report;
            result.refund_date = this.refund_date;
            result.refund_doc_num = this.refund_doc_num;
            result.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;
            result.fiscal_receipt_number = this.fiscal_receipt_number;
            result.fiscal_receipt_amount = this.fiscal_receipt_amount;
            result.fiscal_receipt_date = this.fiscal_receipt_date; // parsed by backend
            result.fiscal_z_rep_number = this.fiscal_z_rep_number;
            result.fiscal_printer_serial = this.fiscal_printer_serial || null;
            return result;
        },

        export_for_printing: function(){
            var receipt = OrderSuper.prototype.export_for_printing.call(this);

            receipt.refund_date = this.refund_date;
            receipt.refund_report = this.refund_report;
            receipt.refund_doc_num = this.refund_doc_num;
            receipt.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;
            receipt.fiscal_receipt_number = this.fiscal_receipt_number;
            receipt.fiscal_receipt_amount = this.fiscal_receipt_amount;
            receipt.fiscal_receipt_date = this.fiscal_receipt_date;
            receipt.fiscal_z_rep_number = this.fiscal_z_rep_number;
            receipt.fiscal_printer_serial = this.fiscal_printer_serial;

            return receipt
        },

        getPrinterOptions: function (){
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return {url: printer_url};
        },

        get_total_with_tax: function() {
            if (this.pos.config.iface_tax_included) {
                if (this.pos.company.tax_calculation_rounding_method === "round_globally") {
                    return this.get_subtotal();
                }
                else {
                    return this.get_total_without_tax() + this.get_total_tax();
                }
            } else {
                return this._super();
            }
        },

        // TODO: Do we need to call the super?
        // The problem here is that the v10 has wrong calculation when rounding globally
        get_total_tax: function() {
            if (this.pos.company.tax_calculation_rounding_method === "round_globally") {
                // As always, we need:
                // 1. For each tax, sum their amount across all order lines
                // 2. Round that result
                // 3. Sum all those rounded amounts
                var groupTaxes = {};
                this.orderlines.each(function (line) {
                    var taxDetails = line.get_tax_details();
                    var taxIds = Object.keys(taxDetails);
                    for (var t = 0; t<taxIds.length; t++) {
                        var taxId = taxIds[t];
                        if (!(taxId in groupTaxes)) {
                            groupTaxes[taxId] = 0;
                        }
                        groupTaxes[taxId] += taxDetails[taxId];
                    }
                });

                var sum = 0;
                var taxIds = Object.keys(groupTaxes);
                for (var j = 0; j<taxIds.length; j++) {
                    var taxAmount = groupTaxes[taxIds[j]];
                    sum += round_pr(taxAmount, this.pos.currency.rounding);
                }
                return sum;
            } else {
                return round_pr(this.orderlines.reduce((function(sum, orderLine) {
                    return sum + orderLine.get_tax();
                }), 0), this.pos.currency.rounding);
            }
        },
    });

    var _orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var res = _orderline_super.export_for_printing.call(this, arguments);
            res['tax_department'] = this.get_tax_details_r();
            return res;
        },
        get_tax_details_r: function(){
            var details =  this.get_all_prices();
            for (var i in details.taxDetails){
                return {
                    code: this.pos.taxes_by_id[i].fpdeptax,
                    taxname: this.pos.taxes_by_id[i].name,
                }
            }
            this.pos.gui.show_popup('error', {
                'title': _t('Error'),
                'body': _t('No taxes found'),
            });
        },
        // stolen from v12
        _compute_all: function(tax, base_amount, quantity) {
            if (tax.amount_type === 'fixed') {
                var sign_base_amount = Math.sign(base_amount) || 1;
                // Since base amount has been computed with quantity
                // we take the abs of quantity
                // Same logic as bb72dea98de4dae8f59e397f232a0636411d37ce
                return tax.amount * sign_base_amount * Math.abs(quantity);
            }
            if ((tax.amount_type === 'percent' && !tax.price_include) || (tax.amount_type === 'division' && tax.price_include)){
                return base_amount * tax.amount / 100;
            }
            if (tax.amount_type === 'percent' && tax.price_include){
                return base_amount - (base_amount / (1 + tax.amount / 100));
            }
            if (tax.amount_type === 'division' && !tax.price_include) {
                return base_amount / (1 - tax.amount / 100) - base_amount;
            }
            return false;
        },
        compute_all: function(taxes, price_unit, quantity, currency_rounding, no_map_tax) {
            var res = _orderline_super.compute_all.call(this, taxes, price_unit, quantity, currency_rounding, no_map_tax);
            var self = this;

            if (this.pos.company.tax_calculation_rounding_method == "round_globally"){
               currency_rounding = currency_rounding * 0.00001;
            }

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
