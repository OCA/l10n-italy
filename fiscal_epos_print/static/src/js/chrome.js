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

    var PrinterFiscalClosure = PosBaseWidget.extend({
        template: 'PrinterFiscalClosure',

        button_click: function () {
            var self = this;
            this.chrome.loading_show();
            this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            var printer_options = {url: printer_url, requested_z_report: true};
            var fp90 = new eposDriver(printer_options, this);
            this.gui.show_popup('confirm', {
                'title': _t('Confirm Printer Fiscal Closure (Report Z)?'),
                'body': _t('Please confirm to execute the Printer Fiscal Closure'),
                confirm: function() {
                    fp90.printFiscalReport();
                },
                cancel: function() {
                    self.chrome.loading_hide();
                },
            });
        },

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.button_click();
            });
        },
    });

    var PrinterFiscalXReport = PosBaseWidget.extend({
        template: 'PrinterFiscalXReport',

        button_click: function () {
            var self = this;
            this.chrome.loading_show();
            this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            var printer_options = {url: printer_url, requested_z_report: true};
            var fp90 = new eposDriver(printer_options, this);
            this.gui.show_popup('confirm', {
                'title': _t('Confirm Printer Daily Financial Report (Report X)?'),
                'body': _t('Please confirm to execute the Printer Daily Financial Report'),
                confirm: function() {
                    fp90.printFiscalXReport();
                },
                cancel: function() {
                    self.chrome.loading_hide();
                },
            });
        },

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.button_click();
            });
        },
    });

    var PrinterFiscalOpenCashDrawer = PosBaseWidget.extend({
        template: 'PrinterFiscalOpenCashDrawer',

        button_click: function () {
            this.chrome.loading_show();
            this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            var printer_options = {url: printer_url, requested_z_report: true};
            var fp90 = new eposDriver(printer_options, this);
            fp90.printOpenCashDrawer();
        },

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.button_click();
            });
        },
    });

    var PrinterFiscalReprintLast = PosBaseWidget.extend({
        template: 'PrinterFiscalReprintLast',

        button_click: function () {
            var self = this;
            this.chrome.loading_show();
            this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            var printer_options = {url: printer_url, requested_z_report: true};
            var fp90 = new eposDriver(printer_options, this);

            this.gui.show_popup('confirm',{
                'title': _t('Confirm Print Last Receipt?'),
                'body': _t('Please confirm to print the last receipt'),
                confirm: function(){
                    fp90.printFiscalReprintLast();
                },
                cancel: function(){
                    self.chrome.loading_hide();
                },
            });
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

    widgets.push({
        'name': _t('Open CashDrawer'),
        'widget': PrinterFiscalOpenCashDrawer,
        'append': '.pos-rightheader',
        'args': {
            'label': 'Open CashDrawer',
        },
    });

    widgets.push({
        'name': _t('Printer Fiscal Closure'),
        'widget': PrinterFiscalClosure,
        'append': '.pos-rightheader',
        'args': {
            'label': 'Printer Fiscal Closure',
        },
    });

    widgets.push({
        'name': _t('Printer Fiscal X Report'),
        'widget': PrinterFiscalXReport,
        'append': '.pos-rightheader',
        'args': {
            'label': 'Printer Fiscal X Report',
        },
    });

    widgets.push({
        'name': _t('Reprinter Last Receipt'),
        'widget': PrinterFiscalReprintLast,
        'append': '.pos-rightheader',
        'args': {
            'label': 'Reprinter Last Receipt',
        },
    });

    return {
        FiscalPrinterADEFilesButtonWidget: FiscalPrinterADEFilesButtonWidget,
        PrinterFiscalClosure: PrinterFiscalClosure,
        PrinterFiscalXReport: PrinterFiscalXReport,
        PrinterFiscalOpenCashDrawer: PrinterFiscalOpenCashDrawer,
        PrinterFiscalReprintLast: PrinterFiscalReprintLast,
    };

});
