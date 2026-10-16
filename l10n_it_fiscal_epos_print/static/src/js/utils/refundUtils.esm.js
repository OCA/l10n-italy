import {_t} from "@web/core/l10n/translation";
import {RefundInfoPopup} from "../Popups/RefundInfoPopup.esm";

export const refundUtils = {
    getButtonColor(order) {
        let color = "#e2e2e2";
        if (order) {
            const lines = order.lines;
            const has_refund =
                lines.find(function (line) {
                    return line.qty < 0.0;
                }) !== undefined;
            if (has_refund === true) {
                if (
                    order.refund_date &&
                    order.refund_date !== "" &&
                    order.refund_doc_num &&
                    order.refund_doc_num !== "" &&
                    order.refund_cash_fiscal_serial &&
                    order.refund_cash_fiscal_serial !== "" &&
                    order.refund_report &&
                    order.refund_report !== ""
                ) {
                    color = "lightgreen";
                } else {
                    color = "red";
                }
            }
        }
        return color;
    },

    async showRefundPopup(dialog, pos, updateCallback = null) {
        const current_order = pos.get_order();
        const popupOptions = {
            title: _t("Refund Information Details"),
            refund_date: String(current_order.refund_date || ""),
            refund_report: String(current_order.refund_report || ""),
            refund_doc_num: String(current_order.refund_doc_num || ""),
            refund_cash_fiscal_serial: String(
                current_order.refund_cash_fiscal_serial || ""
            ),
            refund_full_refund: Boolean(current_order.refund_full_refund),
        };

        if (updateCallback) {
            popupOptions.update_refund_info_button = updateCallback;
        }

        dialog.add(RefundInfoPopup, popupOptions);
    },
};
