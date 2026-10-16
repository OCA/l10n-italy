import {_t} from "@web/core/l10n/translation";
import {Component} from "@odoo/owl";
import {usePos} from "@point_of_sale/app/store/pos_hook";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";
import {LotteryCodePopup} from "../Popups/LotteryCodePopup.esm";

export class SetLotteryCodeButton extends Component {
    static template = "l10n_it_fiscal_epos_print.SetLotteryCodeButton";

    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
    }

    get currentOrder() {
        return this.pos.get_order();
    }

    get buttonColor() {
        const order = this.currentOrder;
        return order?.lottery_code ? "lightgreen" : "#e2e2e2";
    }

    onClickLotteryCode() {
        this.dialog.add(LotteryCodePopup, {
            title: _t("Lottery Code"),
            lottery_code: this.currentOrder?.lottery_code || "",
            onConfirm: (lotteryCode) => {
                if (this.currentOrder) {
                    this.currentOrder.lottery_code = lotteryCode;
                }
            },
        });
    }
}

// Register the component
registry.category("components").add("SetLotteryCodeButton", SetLotteryCodeButton);

// Add the button to ControlButtons
patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SetLotteryCodeButton,
    },
});
