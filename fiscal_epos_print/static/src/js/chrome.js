odoo.define("fiscal_epos_print.chrome", function (require) {
    "use strict";

    var core = require("web.core");
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var chrome = require('point_of_sale.chrome');
    var epson_epos_print = require('fiscal_epos_print.epson_epos_print');
    var _t = core._t;
    var eposDriver = epson_epos_print.eposDriver;

    /* --------- Epson ePOS FP81II main Widget --------- */

    var EpsonFP81IIWidget = PosBaseWidget.extend({
        template: "EpsonFP81IIWidget",

        init: function(parent, options){
            this._super(parent, options);
            var self = this;

            // for dragging the debug widget around
            this.dragging  = false;
            this.dragpos = {x:0, y:0};

            function eventpos(event){
                if(event.touches && event.touches[0]) {
                    return {x: event.touches[0].screenX, y: event.touches[0].screenY};
                }else{
                    return {x: event.screenX, y: event.screenY};
                }
            }

            this.dragend_handler = function(event) {
                self.dragging = false;
            };
            this.dragstart_handler = function(event) {
                self.dragging = true;
                self.dragpos = eventpos(event);
            };
            this.dragmove_handler = function(event) {
                if(self.dragging){
                    var top = this.offsetTop;
                    var left = this.offsetLeft;
                    var pos  = eventpos(event);
                    var dx   = pos.x - self.dragpos.x;
                    var dy   = pos.y - self.dragpos.y;

                    self.dragpos = pos;

                    this.style.right = 'auto';
                    this.style.bottom = 'auto';
                    this.style.left = left + dx + 'px';
                    this.style.top  = top  + dy + 'px';
                }
                event.preventDefault();
                event.stopPropagation();
            };
        },

        show: function() {
            this.$el.css({opacity:0});
            this.$el.removeClass('oe_hidden');
            this.$el.animate({opacity:1},250,'swing');
        },

        hide: function() {
            var self = this;
            this.$el.animate({opacity:0,},250,'swing',function() {
                self.$el.addClass('oe_hidden');
            });
        },

        getPrinterOptions: function () {
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return {url: printer_url};
        },

        start: function() {
            var self = this;

            this.el.addEventListener('mouseleave', this.dragend_handler);
            this.el.addEventListener('mouseup',    this.dragend_handler);
            this.el.addEventListener('touchend',   this.dragend_handler);
            this.el.addEventListener('touchcancel',this.dragend_handler);
            this.el.addEventListener('mousedown',  this.dragstart_handler);
            this.el.addEventListener('touchstart', this.dragstart_handler);
            this.el.addEventListener('mousemove',  this.dragmove_handler);
            this.el.addEventListener('touchmove',  this.dragmove_handler);

            this.$('.toggle').click(function() {
                self.hide();
            });

            this.$('.button.show_ade_status').click(function() {
                self.hide();
                self.chrome.loading_show();
                self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                var printer_options = self.getPrinterOptions();
                var fp90 = new eposDriver(printer_options, self);
                fp90.getStatusOfFilesForADE();
            });

            this.$('.button.fiscal_closing').click(function() {
                self.hide();
                self.chrome.loading_show();
                self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                var printer_options = self.getPrinterOptions();
                var fp90 = new eposDriver(printer_options, self);
                self.gui.show_popup('confirm', {
                    'title': _t('Confirm Printer Fiscal Closure (Report Z)?'),
                    'body': _t('Please confirm to execute the Printer Fiscal Closure'),
                    confirm: function() {
                        fp90.printFiscalReport();
                    },
                    cancel: function() {
                        self.chrome.loading_hide();
                    },
                });
            });

            this.$('.button.fiscal_xreport').click(function() {
                self.hide();
                self.chrome.loading_show();
                self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                var printer_options = self.getPrinterOptions();
                var fp90 = new eposDriver(printer_options, self);
                self.gui.show_popup('confirm', {
                    'title': _t('Confirm Printer Daily Financial Report (Report X)?'),
                    'body': _t('Please confirm to execute the Printer Daily Financial Report'),
                    confirm: function() {
                        fp90.printFiscalXReport();
                    },
                    cancel: function() {
                        self.chrome.loading_hide();
                    },
                });
            });

            this.$('.button.open_cashdrawer').click(function() {
                self.hide();
                self.chrome.loading_show();
                self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                var printer_options = self.getPrinterOptions();
                var fp90 = new eposDriver(printer_options, self);
                fp90.printOpenCashDrawer();
            });

            this.$('.button.reprint_last_receipt').click(function() {
                self.hide();
                self.chrome.loading_show();
                self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                var printer_options = self.getPrinterOptions();
                var fp90 = new eposDriver(printer_options, self);
                self.gui.show_popup('confirm',{
                    'title': _t('Reprint Last Receipt?'),
                    'body': _t('Please confirm to reprint the last receipt'),
                    confirm: function() {
                        fp90.printFiscalReprintLast();
                    },
                    cancel: function() {
                        self.chrome.loading_hide();
                    },
                });
            });
        },

    });

    var EpsonEPOSWidget = PosBaseWidget.extend({
        template: 'EpsonEPOSWidget',

        button_click: function () {
            var widget = $('.pos-content .epson-fp81ii-widget');
            if (widget.hasClass('oe_hidden')) {
                widget.css({opacity:0});
                widget.removeClass('oe_hidden');
                widget.animate({opacity:1},250,'swing');
            } else {
                widget.animate({opacity:0,},250,'swing',function() {
                    widget.addClass('oe_hidden');
                });
            }
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
        'name':   'epson-epos-widget',
        'widget': EpsonEPOSWidget,
        'append':  '.pos-rightheader',
    });

    widgets.push({
        'name':  'epsonfp81ii',
        'widget': EpsonFP81IIWidget,
        'append': '.pos-content',
    });

    return {
        EpsonEPOSWidget: EpsonEPOSWidget,
        EpsonFP81IIWidget: EpsonFP81IIWidget,
    };
});
