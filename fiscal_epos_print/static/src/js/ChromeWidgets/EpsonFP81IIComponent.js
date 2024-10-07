/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { EpsonEposPrint } from "../epson_epos_print";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";

export class EpsonFP81IIComponent extends Component {
    static components = {
        EpsonEposPrint,
        ConfirmPopup,
    };

    setup() {
        super.setup();
        this.pos = useService('pos');
        this.popup = useService("popup");
    }

    do_hide() {
        const epsonFP81IIComponent = document.querySelector(".status-buttons .epson-fp81ii-widget");
        epsonFP81IIComponent.classList.add("visually-hidden");
    }

    onToggleComponent() {
        this.do_hide();
    }

    getPrinterOptions() {
        const protocol = this.pos.config.use_https ? "https://" : "http://";
        const printer_url = `${protocol}${this.pos.config.printer_ip}/cgi-bin/fpmate.cgi`;
        return { url: printer_url };
    }

    // async openCashDrawer() {
    //     this.do_hide();
    //     const printer_options = this.getPrinterOptions();
    //     const fp90 = new EpsonEposPrint(printer_options, this);
    //     fp90.printOpenCashDrawer();
    //     const { confirmed } = await this.popup.add(ConfirmPopup, {
    //         title: _t("CashDrawer Opened"),
    //         body: _t("Close"),
    //     });
    //     if (confirmed) {
    //         fp90.resetPrinter();
    //     }
    // }

    // async reprintLastReceipt() {
    //     this.do_hide();
    //     const printer_options = this.getPrinterOptions();
    //     const fp90 = new EpsonEposPrint(printer_options, this);
    //     const { confirmed } = await this.popup.add(ConfirmPopup, {
    //         title: _t("Reprint Last Receipt?"),
    //         body: _t("Please confirm to reprint the last receipt"),
    //     });
    //     var cashier = this.pos.get_cashier();
    //     if (confirmed) {
    //         fp90.printFiscalReprintLast(cashier || "1");
    //     }
    // }

    // showAdeStatus() {
    //     this.do_hide();
    //     const printer_options = this.getPrinterOptions();
        // const fp90 = new EpsonEposPrint(printer_options, this);
        // fp90.getStatusOfFilesForADE();
    // }

    // async deleteOrders() {
    //     const { confirmed } = await this.popup.add(ConfirmPopup, {
    //         title: _t("Delete Paid Orders?"),
    //         body: _t(
    //             "This operation will permanently destroy all paid orders from the local storage. You will lose all the data. This operation cannot be undone."
    //         ),
    //     });
    //     if (confirmed) {
    //         this.pos.db.remove_all_orders();
    //         this.pos.set_synch("connected", 0);
    //     }
    // }

    async zClosure() {
        this.do_hide();
        const printer_options = this.getPrinterOptions();
        const fp90 = new EpsonEposPrint(printer_options, this);
        const { confirmed } = await this.popup.add(ConfirmPopup, {
            title: _t("Confirm Printer Fiscal Closure (Report Z)?"),
            body: _t("Please confirm to execute the Printer Fiscal Closure"),
        });
        const cashier = this.pos.get_cashier();
        if (confirmed) {
            fp90.printFiscalZReport(cashier || "1");
        }
    }

    // async fiscalXreport() {
    //     this.do_hide();
    //     const printer_options = this.getPrinterOptions();
        // const fp90 = new EpsonEposPrint(printer_options, this);
        // const { confirmed } = await Gui.showPopup("ConfirmPopup", {
        //     title: this.env._t("Confirm Printer Daily Financial Report (Report X)?"),
        //     body: this.env._t("Please confirm to execute the Printer Daily Financial Report"),
        // });
        // if (confirmed) {
        //     fp90.printFiscalXReport(this.pos.cashier.fiscal_operator_number || "1");
        // }
    // }
}

EpsonFP81IIComponent.template = "fiscal_epos_print.EpsonFP81IIComponent";

// Add the EpsonFP81IIComponent to Navbar components
patch(Navbar, {
    components: { ...Navbar.components, EpsonFP81IIComponent },
});
