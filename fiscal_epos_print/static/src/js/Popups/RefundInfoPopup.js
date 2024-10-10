/** @odoo-module */

import { useState, useRef } from "@odoo/owl";
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class RefundInfoPopup extends AbstractAwaitablePopup {
    static template = "RefundInfoPopup";
    static defaultProps = {
        confirmText: _t("Ok"),
        cancelText: _t("Cancel"),
        body: "",
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.state = useState({inputValue: this.props.startingValue});
        this.inputRefundReport = useRef("inputRefundReport");
        this.inputRefundDate = useRef("inputRefundDate");
        this.inputRefundDocNum = useRef("inputRefundDocNum");
        this.inputRefundCashFiscalSerial = useRef("inputRefundCashFiscalSerial");
        this.inputRefundFullRefund = useRef("inputRefundFullRefund");
    }
    clickConfirmRefund() {
        this.$el = $(this.el);
        var self = this;
        function allValid() {
            return self.$el
                .find("input")
                .not("#refund_full_refund")
                .toArray()
                .every(function (element) {
                    return element.value && element.value != "";
                });
        }
        if (allValid()) {
            this.$el.find("#error-message-dialog").hide();
            var refund_date = this.inputRefundDate.el.value;
            var refund_report = this.inputRefundReport.el.value;
            var refund_doc_num = this.inputRefundDocNum.el.value;
            var refund_cash_fiscal_serial =
                this.inputRefundCashFiscalSerial.el.value;
            var refund_full_refund = this.inputRefundFullRefund.el.checked;
            this.pos.context = {
                refund_details: true,
                refund_date: refund_date,
                refund_report: refund_report,
                refund_doc_num: refund_doc_num,
                refund_cash_fiscal_serial: refund_cash_fiscal_serial,
                refund_full_refund: refund_full_refund,
            };
            this.pos.set_refund_data(
                refund_date,
                refund_report,
                refund_doc_num,
                refund_cash_fiscal_serial,
                refund_full_refund
            );
            if (
                this.props.update_refund_info_button &&
                this.props.update_refund_info_button instanceof Function
            ) {
                this.props.update_refund_info_button();
            }
            this.confirm();
        } else {
            this.$el.find("#error-message-dialog").show();
        }
    }
}