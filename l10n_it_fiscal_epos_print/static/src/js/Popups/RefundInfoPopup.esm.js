import {Component, useRef, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {_t} from "@web/core/l10n/translation";
import {usePos} from "@point_of_sale/app/store/pos_hook";
import {registry} from "@web/core/registry";

export class RefundInfoPopup extends Component {
    static template = "RefundInfoPopup";
    static components = {Dialog};
    static props = {
        title: {type: String, optional: true},
        refund_date: {type: String, optional: true},
        refund_report: {type: String, optional: true},
        refund_doc_num: {type: String, optional: true},
        refund_cash_fiscal_serial: {type: String, optional: true},
        refund_full_refund: {type: Boolean, optional: true},
        update_refund_info_button: {type: Function, optional: true},
        close: {type: Function},
    };
    static defaultProps = {
        confirmText: _t("Ok"),
        cancelText: _t("Cancel"),
        body: "",
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.state = useState({
            inputValue: this.props.startingValue,
            showError: false,
        });
        this.inputRefundReport = useRef("inputRefundReport");
        this.inputRefundDate = useRef("inputRefundDate");
        this.inputRefundDocNum = useRef("inputRefundDocNum");
        this.inputRefundCashFiscalSerial = useRef("inputRefundCashFiscalSerial");
        this.inputRefundFullRefund = useRef("inputRefundFullRefund");
    }
    clickConfirmRefund() {
        const allValid = () => {
            return (
                this.inputRefundDate.el.value &&
                this.inputRefundReport.el.value &&
                this.inputRefundDocNum.el.value &&
                this.inputRefundCashFiscalSerial.el.value
            );
        };

        if (allValid()) {
            this.state.showError = false;
            var refund_date = this.inputRefundDate.el.value;
            var refund_report = this.inputRefundReport.el.value;
            var refund_doc_num = this.inputRefundDocNum.el.value;
            var refund_cash_fiscal_serial = this.inputRefundCashFiscalSerial.el.value;
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
            this.props.close();
        } else {
            this.state.showError = true;
        }
    }
}

// Register the component
registry.category("components").add("RefundInfoPopup", RefundInfoPopup);
