odoo.define("fiscal_epos_print.SetReprintButton", function (require) {
    "use strict";

    var core = require("web.core");
    var _t = core._t;
    var epson_epos_print = require('fiscal_epos_print.epson_epos_print');
    var eposDriver = epson_epos_print.eposDriver;
    const Registries = require('point_of_sale.Registries');
    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const { useErrorHandlers, onChangeOrder } = require('point_of_sale.custom_hooks');
    const { Gui } = require('point_of_sale.Gui');

    const SetReprintButton = (ReceiptScreen) =>
        class SetReprintButton extends ReceiptScreen {
            constructor() {
                super(...arguments);
                if (this.currentOrder._printed === false)
                {
                    this.$('.printing-retry').show();
                }
            }

            async rePrintReceipt() {
                var currentOrder = this.env.pos.get_order();


                const { confirmed } = await Gui.showPopup('ConfirmPopup', {
                    title:_t('Ristampa ultimo scontrino?'),
                    confirmText: 'Conferma',
                    cancelText: 'Annulla',
                    body: 'Usare la ristampa ultimo scontrino solo in caso di errori di comunicazione con la' +
                    'stampante e lo scontrino NON è stato stampato. Viene ristampanto uno scontrino FISCALE' +
                     'con gli stessi articoli del precedente',
                });
                if (confirmed) {
                    var printer_options = this.currentOrder.getPrinterOptions();
                    printer_options.order = currentOrder;
                    var receipt = currentOrder.export_for_printing();
                    this.sendToFP90Printer(receipt, printer_options);
                }
                else {
                    // TODO not exist
                }
            }

            async sendToFP90Printer (receipt, printer_options) {
                var fp90 = new eposDriver(printer_options, this);
//                fp90.printFiscalReceipt(receipt);
                const isPrinted = await fp90.printFiscalReceipt(receipt);
                if (isPrinted) {
                    this.currentOrder._printed = true;
                }
                else
                {
                    this.currentOrder._printed = false;
                }
            }

            //            get currentOrder() {
//                return this.env.pos.get_order();
//            }

//            confirm() {
//                this.props.resolve({ confirmed: true, payload: null });
//                this.trigger('close-temp-screen');
//            }
        };

    Registries.Component.extend(ReceiptScreen, SetReprintButton);
    return ReceiptScreen;
});
