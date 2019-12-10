odoo.define("fiscal_epos_print.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var core = require("web.core");
    var screens = require('point_of_sale.screens');
    var utils = require('web.utils');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var chrome = require('point_of_sale.chrome');
    var round_pr = utils.round_precision;
    var pos_order_mgmt = require('pos_order_mgmt.widgets');
    var pos_popup = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var _t = core._t;
    var OrderListScreenWidget = pos_order_mgmt.OrderListScreenWidget;
    var OrderSuper = models.Order;
    var RefundInfoPopupWidgetSuper = pos_popup;
    var PaymentScreenWidget = screens.PaymentScreenWidget;
    var ReceiptScreenWidget = screens.ReceiptScreenWidget;

    function addPadding(str, padding=4) {
        var pad = new Array(padding).fill(0).join('') + str;
        return pad.substr(pad.length - padding, padding);
    }

    ReceiptScreenWidget.include({
        show: function(){
            if (!this.pos.config.printer_ip || (this.pos.config.printer_ip && this.pos.config.show_receipt_when_printing) ){
                this._super();
            }
            else
            {
                this.click_next();
            }
        }
    });

    PaymentScreenWidget.include({
        order_is_valid: function(force_validation) {
            var self = this;
            var receipt = this.pos.get_order();
            if (receipt.has_refund && (receipt.refund_date == null || receipt.refund_date === '' ||
                                       receipt.refund_doc_num == null || receipt.refund_doc_num == '' ||
                                       receipt.refund_cash_fiscal_serial == null || receipt.refund_cash_fiscal_serial == '' ||
                                       receipt.refund_report == null || receipt.refund_report == '')) {
                this.gui.show_popup('error',{
                    'title': _t('Refund Information Not Present'),
                    'body':  _t("The refund information aren't present. Please insert them before printing the receipt"),
                });
                return false;
            }
            return this._super(force_validation);
        }
    });

    models.Order = models.Order.extend({
        initialize: function(attributes, options){
            OrderSuper.prototype.initialize.call(this, attributes,options);
            this.refund_report = null;
            this.refund_date = null;
            this.refund_doc_num = null;
            this.refund_cash_fiscal_serial = null;
            this.has_refund = false;
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
        },

        export_as_JSON: function() {
            var result = OrderSuper.prototype.export_as_JSON.call(this);
            result.refund_report = this.refund_report;
            result.refund_date = this.refund_date ? this.refund_date.substr(4, 4) + '-' + // year
                                                    this.refund_date.substr(2, 2) + '-' + // month
                                                    this.refund_date.substr(0, 2) : null; // day
            result.refund_doc_num = this.refund_doc_num;
            result.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;
            return result;
        },

        export_for_printing: function(){
            var receipt = OrderSuper.prototype.export_for_printing.call(this);

            receipt.refund_date = this.refund_date;
            receipt.refund_report = this.refund_report;
            receipt.refund_doc_num = this.refund_doc_num;
            receipt.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;

            return receipt
        },
    });

    var set_refund_info_button = screens.ActionButtonWidget.extend({
        template: 'SetRefundInfoButton',
        init: function(parent, options) {
            var self = this;
            this._super(parent, options);
            this.pos.bind('change:selectedOrder',function(){
                this.orderline_change();
                this.bind_order_events();
            },this);
            this.bind_order_events();
            this.orderline_change();
        },
        renderElement: function() {
            this._super();
            var color = this.refund_get_button_color();
            this.$el.css('background', color);
        },
        button_click: function () {
            var self = this;
            var current_order = self.pos.get_order();
            self.gui.show_popup('refundinfo', {
                title: _t('Refund Information Details'),
                refund_date: current_order.refund_date,
                refund_report: current_order.refund_report,
                refund_doc_num: current_order.refund_doc_num,
                refund_cash_fiscal_serial: current_order.refund_cash_fiscal_serial,
                update_refund_info_button: function(){
                    self.renderElement();
                },
            });
        },
        bind_order_events: function() {
            var self = this;
            var order = this.pos.get_order();

            if (!order) {
                return;
            }

            if(this.old_order) {
                this.old_order.unbind(null,null,this);
            }

            this.pos.bind('change:selectedOrder', this.orderline_change, this);

            var lines = order.orderlines;
                lines.unbind('add',     this.orderline_change, this);
                lines.bind('add',       this.orderline_change, this);
                lines.unbind('remove',  this.orderline_change, this);
                lines.bind('remove',    this.orderline_change, this);
                lines.unbind('change',  this.orderline_change, this);
                lines.bind('change',    this.orderline_change, this);

            this.old_order = order;
        },
        refund_get_button_color: function() {
            var order = this.pos.get_order();
            var lines = order.orderlines;
            var has_refund = lines.find(function(line){ return line.quantity < 0.0;}) != undefined;
            var color = '#e2e2e2';
            if (has_refund == true)
            {
                if (order.refund_date && order.refund_date != '' && order.refund_doc_num && order.refund_doc_num != '' &&
                    order.refund_cash_fiscal_serial && order.refund_cash_fiscal_serial != '' && order.refund_report && order.refund_report != '') {
                        color = 'lightgreen';
                }
                else
                {
                    color = 'red';
                }
            }
            return color;
        },
        orderline_change: function(){
            var order = this.pos.get_order();
            var lines = order.orderlines;
            order.has_refund = lines.find(function(line){ return line.quantity < 0.0;}) != undefined;
            this.renderElement();
        },
    });

    screens.define_action_button({
        'name': 'set_refund_info',
        'widget': set_refund_info_button,
    });

    var RefundInfoPopupWidget = pos_popup.extend({
        template: 'RefundInfoPopupWidget',
        init: function(parent) {
            this.refund_report = null;
            this.refund_date = null;
            this.refund_doc_num = null;
            this.refund_cash_fiscal_serial = null;
            this.datepicker = null;
            return this._super(parent);
        },
        show: function(options){
            options = options || {};
            this._super(options);
            this.update_refund_info_button = options.update_refund_info_button;
            this.renderElement();
            this.datepicker = null;
            this.$('refund_report').focus();
            this.initializeDatePicker();
        },
        click_confirm: function(){
            var self = this;
            function allValid() {
                return self.$('input').toArray().every(function(element) {
                    return element.value && element.value != ''
                })
            }

            if (allValid()) {
                this.$('#error-message-dialog').hide()

                var order = this.pos.get_order();
                order.refund_report = this.$('#refund_report').val();
                order.refund_date = this.$('#refund_date').val();
                order.refund_doc_num = this.$('#refund_doc_num').val();
                order.refund_cash_fiscal_serial = this.$('#refund_cash_fiscal_serial').val();
                this.gui.close_popup();
                if (this.update_refund_info_button && this.update_refund_info_button instanceof Function) {
                    this.update_refund_info_button();
                }
            } else {
                this.$('#error-message-dialog').show()
            }
        },
        initializeDatePicker: function() {
            var self = this,
                element = this.$('#refund_date').get(0);

            if (element && !this.datepicker) {
                this.datepicker = new Pikaday({
                    field: element,
                    parse: function(str) {
                        return new Date(str.slice(4, 8),
                                        str.slice(2, 4),
                                        str.slice(0, 2))
                    },
                    toString: function(date) {
                        var str = date.toLocaleDateString().split('/');
                        return addPadding(str[1], 2) +
                            addPadding(str[0], 2) +
                            addPadding(str[2]);
                    }
                });
            }
        },
    });
    gui.define_popup({name:'refundinfo', widget: RefundInfoPopupWidget});

    var eposDriver = core.Class.extend({
        init: function(options, sender) {
            options = options || {};
            this.url = options.url || 'http://192.168.1.1/cgi-bin/fpmate.cgi';
            this.fiscalPrinter = new epson.fiscalPrint();
            this.fpreponse = false;
            this.sender = sender;
            this.fiscalPrinter.onreceive = function(res, tag_list_names, add_info) {
                this.fpreponse = tag_list_names
                if (res['code'] == "EPTR_REC_EMPTY"){
                    sender.chrome.loading_hide();
                    alert(_t("Error missing paper."));
                }
                if (add_info.responseCommand == "1138") {
                    // coming from FiscalPrinterADEFilesButtonWidget
                    sender.chrome.loading_hide();
                    var to_be_sent = add_info.responseData[9] + add_info.responseData[10] + add_info.responseData[11] + add_info.responseData[12];
                    var old = add_info.responseData[13] + add_info.responseData[14] + add_info.responseData[15] + add_info.responseData[16];
                    var rejected = add_info.responseData[17] + add_info.responseData[18] + add_info.responseData[19] + add_info.responseData[20];
                    var msg = _t("Files waiting to be sent: ") + to_be_sent + _t("\nOld files: ") + old + _t("\nRejected files: ") + rejected
                    alert(msg);
                }
            }
            this.fiscalPrinter.onerror = function() {
                sender.chrome.loading_hide();
                alert(
                _t('Network error. Printer can not be reached')
                );
            }
        },

        /*
          Prints a sale item line.
        */
        printRecItem: function(args) {
            var tag = '<printRecItem'
                + ' description="' + (args.description || '') + '"'
                + ' quantity="' + (args.quantity || '1') + '"'
                + ' unitPrice="' + (args.unitPrice || '') + '"'
                + ' department="' + (args.department || '1') + '"'
                + ' justification="' + (args.justification || '1') + '"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />';
            return tag;
        },

        /*
          Prints a sale refund item line.
        */
        printRecRefund: function(args) {
            var message = 'REFUND ' +
                addPadding(args.refund_report) + ' ' +
                addPadding(args.refund_doc_num) + ' ' +
                args.refund_date + ' ' +
                args.refund_cash_fiscal_serial;

            var tag = '<printRecMessage'
                + ' messageType="4" message="' + message + '" font="1" index="1"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />\n'
                + '<printRecRefund'
                + ' description="' + (args.description || '') + '"'
                + ' quantity="' + (args.quantity || '1') + '"'
                + ' unitPrice="' + (args.unitPrice || '') + '"'
                + ' department="' + (args.department || '1') + '"'
                + ' justification="' + (args.justification || '1') + '"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />';
            return tag;
        },

        /*
          Adds a discount to the last line.
        */
        printRecItemAdjustment: function(args) {
            var tag = '<printRecItemAdjustment'
                + ' operator="' + (args.operator || '1') + '"'
                + ' adjustmentType="' + (args.adjustmentType || 0) + '"'
                + ' description="' + (args.description || '' ) + '"'
                + ' amount="' + (args.amount || '') + '"'
                + ' department="' + (args.department || '') + '"'
                + ' justification="' + (args.justification || '2') + '"'
                + ' />';
            return tag;
        },

        /*
          Prints a payment.
        */
        printRecTotal: function(args) {
            var tag = '<printRecTotal'
                + ' operator="' + (args.operator || '1') + '"'
                + ' description="' + (args.description || _t('Payment')) + '"'
                + ' payment="' + (args.payment || '') + '"'
                + ' paymentType="' + (args.paymentType || '0') + '"'
                + ' index="' + (args.paymentIndex || '0') + '"'
                + ' />';
            return tag;
        },

        // Remember that the header goes after <printerFiscalReceipt>
        // but before <beginFiscalReceipt /> otherwise it will not be printed
        // as additional header messageType=1
        printFiscalReceiptHeader: function(receipt){
            var msg = '';
            if (receipt.header != '' && receipt.header.length > 0) {
                var hdr = receipt.header.split(/\r\n|\r|\n/);
                _.each(hdr, function(m, i) {
                    msg += '<printRecMessage' + ' messageType="1" message="' + m
                         + '" font="1" index="' + (i+1) + '"'
                         + ' operator="' + (receipt.operator || '1') + '" />'
                    });
            }
            return msg;
        },

        // Remember that the footer goes within <printerFiscalReceipt><beginFiscalReceipt />
        // as PROMO code messageType=3
        printFiscalReceiptFooter: function(receipt){
            var msg = '';
            if (receipt.footer != '' && receipt.footer.length > 0) {
                var hdr = receipt.footer.split(/\r\n|\r|\n/);
                _.each(hdr, function(m, i) {
                    msg += '<printRecMessage' + ' messageType="3" message="' + m
                         + '" font="1" index="' + (i+1) + '"'
                         + ' operator="' + (receipt.operator || '1') + '" />'
                    });
            }
            return msg;
        },

        /*
          Prints a receipt
        */
        printFiscalReceipt: function(receipt) {
            var self = this;
            var xml = '<printerFiscalReceipt>';
            // header must be printed before beginning a fiscal receipt
            xml += this.printFiscalReceiptHeader(receipt);
            xml += '<beginFiscalReceipt />';
            // footer can go only as promo code so within a fiscal receipt body
            xml += this.printFiscalReceiptFooter(receipt);
            _.each(receipt.orderlines, function(l, i, list) {
                if (l.price >= 0) {
                    if(l.quantity>=0) {
                        xml += self.printRecItem({
                            description: l.product_name,
                            quantity: l.quantity,
                            unitPrice: l.price,
                            department: l.tax_department.code
                        });
                        if (l.discount) {
                            xml += self.printRecItemAdjustment({
                                adjustmentType: 0,
                                description: _t('Discount') + ' ' + l.discount + '%',
                                amount: round_pr(l.quantity * l.price - l.price_display, self.sender.pos.currency.rounding),
                            });
                        }
                    }
                    else
                    {
                        xml += self.printRecRefund({
                            refund_date: receipt.refund_date,
                            refund_report: receipt.refund_report,
                            refund_doc_num: receipt.refund_doc_num,
                            refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
                            description: _t('Refund >>> ') + l.product_name,
                            quantity: l.quantity * -1.0,
                            unitPrice: l.price,
                            department: l.tax_department.code
                        });
                    }
                }
                else {
                    xml += self.printRecItemAdjustment({
                        adjustmentType: 3,
                        description: l.product_name,
                        department: l.tax_department.code,
                        amount: -l.price,
                    });
                }
            });
            _.each(receipt.paymentlines, function(l, i, list) {
                xml += self.printRecTotal({
                    payment: l.amount,
                    paymentType: l.type,
                    paymentIndex: l.type_index,
                    description: l.journal,
                });
            });
            xml += '<endFiscalReceipt /></printerFiscalReceipt>';
            this.fiscalPrinter.send(this.url, xml);
            console.log(xml);
        },

        printFiscalReport: function() {
            var xml = '<printerFiscalReport>';
            xml += '<displayText operator="1" data="' + _t('Fiscal Closing') + '" />';
            xml += '<printZReport operator="1" />';
            xml += '</printerFiscalReport>';
            this.fiscalPrinter.send(this.url, xml);
        },

        getStatusOfFilesForADE: function() {
            var xml = '<printerCommand>';
            xml += '<directIO command="1138" data="01" />';
            xml += '</printerCommand>';
            this.fiscalPrinter.send(this.url, xml);
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
            alert(_t("No taxes found"));
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

    // when print order i validate call print receipt
    screens.PaymentScreenWidget.include({
        getPrinterOptions: function (){
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return {url: printer_url};
        },
        sendToFP90Printer: function(receipt, printer_options) {
            var fp90 = new eposDriver(printer_options, this);
            fp90.printFiscalReceipt(receipt);
        },
        finalize_validation: function() {
            // we need to get currentOrder before calling the _super()
            // otherwise we will likely get a empty order when we want to skip
            // the receipt preview
            var currentOrder = this.pos.get_order();
            this._super.apply(this, arguments);
            if (this.pos.config.printer_ip && !currentOrder.is_to_invoice()) {
                var printer_options = this.getPrinterOptions();
                var receipt = currentOrder.export_for_printing();
                this.sendToFP90Printer(receipt, printer_options);
                currentOrder._printed = true;
            }
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

    OrderListScreenWidget.include({
        _prepare_order_from_order_data: function (order_data, action) {
            var order = this._super(order_data, action);
            order.refund_report = order_data.refund_report;
            order.refund_date = order_data.refund_date ? order_data.refund_date.substr(8, 2) +  // day
                                                         order_data.refund_date.substr(5, 2) +  // month
                                                         order_data.refund_date.substr(0, 4)    // year
                                                       : null;
            order.refund_doc_num = order_data.refund_doc_num;
            order.refund_cash_fiscal_serial = order_data.refund_cash_fiscal_serial;

            return order;
        },
        // copiato da screens.PaymentScreenWidget
        getPrinterOptions: function (){
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return [{url: printer_url}];
        },
        // copiato da screens.PaymentScreenWidget
        sendToFP90Printer: function(receipt, printer_options) {
            for (var i = 0; i < printer_options.length; i++){
                var printer_option = printer_options[i];
                var fp90 = new eposDriver(printer_option, this);
                fp90.printFiscalReceipt(receipt);
            }
        },
        action_print: function (order_data, order) {
            if (this.pos.config.printer_ip) {
                var receipt = order.export_for_printing();
                var printer_options = this.getPrinterOptions();
                this.sendToFP90Printer(receipt, printer_options);
            }
            return this._super(order_data, order);
        },
    });

    var FiscalPrinterADEFilesButtonWidget = PosBaseWidget.extend({
        template: 'FiscalPrinterADEFilesButtonWidget',

        button_click: function () {
            this.chrome.loading_show();
            this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            var printer_options = {url: printer_url};
            var fp90 = new eposDriver(printer_options, this);
            fp90.getStatusOfFilesForADE();
        },

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.button_click();
            });
        },

    });

    var widgets = chrome.Chrome.prototype.widgets;
    widgets.push({
        'name': 'ADE files status',
        'widget': FiscalPrinterADEFilesButtonWidget,
        'append': '.pos-rightheader',
        'args': {
            'label': _t('ADE files status'),
        },
    });

    return {
        eposDriver: eposDriver,
        FiscalPrinterADEFilesButtonWidget: FiscalPrinterADEFilesButtonWidget,
        RefundInfoButtonActionWidget: set_refund_info_button
    };

});
