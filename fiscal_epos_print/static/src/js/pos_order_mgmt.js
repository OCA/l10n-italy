odoo.define("fiscal_epos_print.pos_order_mgmt", function (require) {
    "use strict";

    var core = require("web.core");
    var pos_order_mgmt = require('pos_order_mgmt.widgets');
    var epson_epos_print = require('fiscal_epos_print.epson_epos_print');
    var _t = core._t;
    var OrderListScreenWidget = pos_order_mgmt.OrderListScreenWidget;
    var eposDriver = epson_epos_print.eposDriver;

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

});
