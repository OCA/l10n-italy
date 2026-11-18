import {Component, useRef, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {usePos} from "@point_of_sale/app/store/pos_hook";

export class LotteryCodePopup extends Component {
    static template = "l10n_it_fiscal_epos_print.LotteryCodePopup";
    static components = {Dialog};
    static props = {
        title: {type: String, optional: true},
        lottery_code: {type: String, optional: true},
        onConfirm: {type: Function, optional: true},
        close: Function,
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.state = useState({
            lotteryCode: this.props.lottery_code || "",
            showError: false,
        });
        this.inputRef = useRef("lotteryCodeInput");
    }

    onInputChange(ev) {
        this.state.lotteryCode = ev.target.value;
        this.state.showError = false; // Hide error when typing
    }

    confirm() {
        const lotteryCode = this.state.lotteryCode.trim();

        if (!lotteryCode) {
            this.state.showError = true;
            return;
        }

        // Save lottery code to current order
        const currentOrder = this.pos.get_order();
        if (currentOrder) {
            currentOrder.lottery_code = lotteryCode;
        }

        // Call the onConfirm callback if provided
        if (this.props.onConfirm) {
            this.props.onConfirm(lotteryCode);
        }

        this.props.close();
    }

    cancel() {
        this.props.close();
    }
}
