import {_t} from "@web/core/l10n/translation";
import {Component} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {Navbar} from "@point_of_sale/app/navbar/navbar";
import {patch} from "@web/core/utils/patch";
import {EpsonEposPrint} from "../epson_epos_print.esm";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {ask} from "@point_of_sale/app/store/make_awaitable_dialog";

export class EpsonFP81IIComponent extends Component {
    static components = {
        EpsonEposPrint,
        ConfirmationDialog,
    };

    setup() {
        super.setup();
        this.pos = useService("pos");
        this.dialog = useService("dialog");
    }

    do_hide() {
        // eslint-disable-next-line no-undef
        const epsonFP81IIComponent = document.querySelector(
            ".status-buttons .epson-fp81ii-widget"
        );
        epsonFP81IIComponent.classList.add("visually-hidden");
    }

    onToggleComponent() {
        this.do_hide();
    }

    getPrinterOptions() {
        const protocol = this.pos.config.use_https ? "https://" : "http://";
        const printer_url = `${protocol}${this.pos.config.printer_ip}/cgi-bin/fpmate.cgi`;
        return {url: printer_url};
    }

    async zClosure() {
        this.do_hide();
        const printer_options = this.getPrinterOptions();
        const fp90 = new EpsonEposPrint(printer_options, this);
        const confirmed = await ask(this.dialog, {
            title: _t("Confirm Printer Fiscal Closure (Report Z)?"),
            body: _t("Please confirm to execute the Printer Fiscal Closure"),
        });
        const cashier = this.pos.get_cashier();
        if (confirmed) {
            fp90.printFiscalZReport(cashier || "1");
        }
    }

    async fiscalXreport() {
        this.do_hide();
        const printer_options = this.getPrinterOptions();
        const fp90 = new EpsonEposPrint(printer_options, this);
        const confirmed = await ask(this.dialog, {
            title: _t("Confirm Printer Daily Financial Report (Report X)?"),
            body: _t("Please confirm to execute the Printer Daily Financial Report"),
        });
        const cashier = this.pos.get_cashier();
        const operatorNumber = cashier?.fiscal_operator_number || "1";
        if (confirmed) {
            fp90.printFiscalXReport(operatorNumber);
        }
    }
}

EpsonFP81IIComponent.template = "l10n_it_fiscal_epos_print.EpsonFP81IIComponent";

// Add the EpsonFP81IIComponent to Navbar components
patch(Navbar, {
    components: {...Navbar.components, EpsonFP81IIComponent},
});
