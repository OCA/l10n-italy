import {patch} from "@web/core/utils/patch";
import {ClosePosPopup} from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import {EpsonEposPrint} from "../epson_epos_print.esm";
import {_t} from "@web/core/l10n/translation";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";

/**
 * Patch the ClosePosPopup to execute fiscal Z closure when closing session
 */
patch(ClosePosPopup.prototype, {
    /**
     * Execute fiscal printer Z closure before closing the session
     */
    async executeFiscalZClosure() {
        // Check if fiscal printer is configured
        if (!this.pos.config.printer_ip) {
            // No fiscal printer configured, skipping Z closure
            return true;
        }

        try {
            // Get printer options
            const protocol = this.pos.config.use_https ? "https://" : "http://";
            const printerUrl = `${protocol}${this.pos.config.printer_ip}/cgi-bin/fpmate.cgi`;
            const printerOptions = {url: printerUrl};

            // Initialize fiscal printer
            const fiscalPrinter = new EpsonEposPrint(printerOptions, this);

            // Get operator number
            const cashier = this.pos.get_cashier();
            const operatorNumber = cashier?.fiscal_operator_number || "1";

            // Executing fiscal Z closure for session closing...

            // Execute Z closure
            // Note: This is synchronous in the original implementation
            fiscalPrinter.printFiscalZReport(operatorNumber);

            // Give some time for the printer to process
            // eslint-disable-next-line no-undef
            await new Promise((resolve) => setTimeout(resolve, 2000));

            return true;
        } catch {
            // Error during fiscal Z closure

            // Show error dialog but allow to continue
            this.dialog.add(AlertDialog, {
                title: _t("Fiscal Printer Warning"),
                body: _t(
                    "Failed to execute fiscal Z closure on the printer. The session will still be closed. Please perform the Z closure manually on the printer."
                ),
            });

            // Return true to allow session closing to continue
            return true;
        }
    },

    /**
     * Override closeSession to add fiscal Z closure
     */
    async closeSession() {
        // Execute fiscal Z closure before closing the session
        const zClosureSuccess = await this.executeFiscalZClosure();

        if (!zClosureSuccess) {
            // Fiscal Z closure failed, but continuing with session close
        }

        // Call the original closeSession method
        return await super.closeSession(...arguments);
    },
});
