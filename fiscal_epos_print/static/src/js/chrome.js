odoo.define("fiscal_epos_print.chrome", function (require) {
    "use strict";

    var core = require("web.core");
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var chrome = require('point_of_sale.chrome');
    var epson_epos_print = require('fiscal_epos_print.epson_epos_print');
    var _t = core._t;
    var eposDriver = epson_epos_print.eposDriver;


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
        FiscalPrinterADEFilesButtonWidget: FiscalPrinterADEFilesButtonWidget,
    };

});
