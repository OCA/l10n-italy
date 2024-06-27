odoo.define("fiscal_epos_print.EpsonFP81IIComponent", function (require) {
    "use strict";

    var core = require("web.core");
    var epson_epos_print = require("fiscal_epos_print.epson_epos_print");
    var _t = core._t;
    var eposDriver = epson_epos_print.eposDriver;

    const {Gui} = require("point_of_sale.Gui");
    const PosComponent = require("point_of_sale.PosComponent");
    const Registries = require("point_of_sale.Registries");

    class EpsonFP81IIComponent extends PosComponent {
        constructor() {
            super(...arguments);
            var self = this;

            // For dragging the debug widget around
            this.dragging = false;
            this.dragpos = {
                x: 0,
                y: 0,
            };

            function eventpos(event) {
                if (event.touches && event.touches[0]) {
                    return {
                        x: event.touches[0].screenX,
                        y: event.touches[0].screenY,
                    };
                }
                return {
                    x: event.screenX,
                    y: event.screenY,
                };
            }

            this.dragend_handler = function () {
                self.dragging = false;
            };
            this.dragstart_handler = function (event) {
                self.dragging = true;
                self.dragpos = eventpos(event);
            };
            this.dragmove_handler = function (event) {
                if (self.dragging) {
                    var top = this.offsetTop;
                    var left = this.offsetLeft;
                    var pos = eventpos(event);
                    var dx = pos.x - self.dragpos.x;
                    var dy = pos.y - self.dragpos.y;

                    self.dragpos = pos;

                    this.style.right = "auto";
                    this.style.bottom = "auto";
                    this.style.left = left + dx + "px";
                    this.style.top = top + dy + "px";
                }
                event.preventDefault();
                event.stopPropagation();
            };
        }

        OnMounted() {
            // Jquery reference of the component
            this.$el = $(this.el);
            // Drag listeners
            this.el.addEventListener("mouseleave", this.dragend_handler);
            this.el.addEventListener("mouseup", this.dragend_handler);
            this.el.addEventListener("touchend", this.dragend_handler);
            this.el.addEventListener("touchcancel", this.dragend_handler);
            this.el.addEventListener("mousedown", this.dragstart_handler);
            this.el.addEventListener("touchstart", this.dragstart_handler);
            this.el.addEventListener("mousemove", this.dragmove_handler);
            this.el.addEventListener("touchmove", this.dragmove_handler);
        }

        do_show() {
            var epsonFP81IIComponent = $(".status-buttons .epson-fp81ii-widget");
            epsonFP81IIComponent.removeClass("oe_hidden");
        }

        do_hide() {
            var epsonFP81IIComponent = $(".status-buttons .epson-fp81ii-widget");
            epsonFP81IIComponent.addClass("oe_hidden");
        }

        getPrinterOptions() {
            var protocol = this.env.pos.config.use_https ? "https://" : "http://";
            var printer_url =
                protocol + this.env.pos.config.printer_ip + "/cgi-bin/fpmate.cgi";
            return {url: printer_url};
        }

        onToggleComponent() {
            this.do_hide();
        }

        async openCashDrawer() {
            this.do_hide();
            // TODO find the same Component method that show loading_*
            // this.chrome.loading_show();
            // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var printer_options = this.getPrinterOptions();
            var fp90 = new eposDriver(printer_options, this);
            fp90.printOpenCashDrawer();
            const {confirmed} = await Gui.showPopup("ConfirmPopup", {
                title: _t("CashDrawer Opened"),
                body: _t("Close"),
            });
            if (confirmed) {
                fp90.resetPrinter();
            } else {
                // TODO not exist
                // this.chrome.loading_hide();
            }
        }

        async reprintLastReceipt() {
            this.do_hide();
            //            Var self = this;
            //            this._super();

            // TODO find the same Component method that show loading_*
            // this.chrome.loading_show();
            // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var printer_options = this.getPrinterOptions();
            var fp90 = new eposDriver(printer_options, this);
            // ConfirmPopup
            const {confirmed} = await Gui.showPopup("ConfirmPopup", {
                title: _t("Reprint Last Receipt?"),
                body: _t("Please confirm to reprint the last receipt"),
            });
            if (confirmed) {
                fp90.printFiscalReprintLast(
                    this.env.pos.cashier.fiscal_operator_number || "1"
                );
            } else {
                // TODO not exist
                // this.chrome.loading_hide();
            }
        }

        showAdeStatus() {
            this.do_hide();
            // TODO find the same Component method that show loading_*
            // this.chrome.loading_show();
            // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var printer_options = this.getPrinterOptions();
            var fp90 = new eposDriver(printer_options, this);
            fp90.getStatusOfFilesForADE();
        }

        async fiscalClosing() {
            this.do_hide();
            // TODO find the same Component method that show loading_*
            // this.chrome.loading_show();
            // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var printer_options = this.getPrinterOptions();
            var fp90 = new eposDriver(printer_options, this);
            // ConfirmPopup
            const {confirmed} = await this.showPopup("ConfirmPopup", {
                title: _t("Confirm Printer Fiscal Closure (Report Z)?"),
                body: _t("Please confirm to execute the Printer Fiscal Closure"),
            });
            if (confirmed) {
                // Fp90.printFiscalReport();
                fp90.printFiscalXZReport(
                    this.env.pos.cashier.fiscal_operator_number || "1"
                );
            } else {
                // TODO not exist
                // this.chrome.loading_hide();
            }
        }

        async fiscalXreport() {
            this.do_hide();
            // TODO find the same Component method that show loading_*
            // this.chrome.loading_show();
            // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var printer_options = this.getPrinterOptions();
            var fp90 = new eposDriver(printer_options, this);
            // ConfirmPopup
            const {confirmed} = await this.showPopup("ConfirmPopup", {
                title: _t("Confirm Printer Daily Financial Report (Report X)?"),
                body: _t(
                    "Please confirm to execute the Printer Daily Financial Report"
                ),
            });
            if (confirmed) {
                fp90.printFiscalXReport(
                    this.env.pos.cashier.fiscal_operator_number || "1"
                );
            } else {
                // TODO not exist
                // this.chrome.loading_hide();
            }
        }
    }

    EpsonFP81IIComponent.template = "EpsonFP81IIComponent";

    Registries.Component.add(EpsonFP81IIComponent);

    return EpsonFP81IIComponent;
});
