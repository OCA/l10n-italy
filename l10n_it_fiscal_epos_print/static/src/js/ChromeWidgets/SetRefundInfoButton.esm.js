import {Component, useEffect, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {usePos} from "@point_of_sale/app/store/pos_hook";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {patch} from "@web/core/utils/patch";
import {refundUtils} from "../utils/refundUtils.esm";

export class SetRefundInfoButton extends Component {
    static template = "SetRefundInfoButton";
    static components = {
        AlertDialog,
    };
    static props = {};
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.state = useState({
            buttonColor: "#e2e2e2",
        });

        // Use useEffect to track order and order lines changes - simplified
        useEffect(
            () => {
                this.orderline_change();
            },
            () => {
                const order = this.pos.get_order();
                return order
                    ? [order, order.lines.length, ...order.lines.map((l) => l.qty)]
                    : [];
            }
        );
    }
    is_available() {
        const order = this.pos.get_order();
        return order;
    }
    get buttonColor() {
        return refundUtils.getButtonColor(this.pos.get_order());
    }
    async onClickRefund() {
        await refundUtils.showRefundPopup(this.dialog, this.pos, () =>
            this.update_refund_info_button()
        );
    }
    update_refund_info_button() {
        // Trigger re-render by updating state
        this.state.buttonColor = this.buttonColor;
    }
    orderline_change() {
        const order = this.pos.get_order();
        if (order) {
            // Update has_refund flag
            order.check_order_has_refund();
        }
        // Update button color state
        this.state.buttonColor = this.buttonColor;
    }
}

// Register the component
registry.category("components").add("SetRefundInfoButton", SetRefundInfoButton);

// Patch ControlButtons to add the refund button logic
patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SetRefundInfoButton,
    },
});

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
        // Ensure check_order_has_refund is called to update has_refund property
        const order = this.pos.get_order();
        if (order) {
            order.check_order_has_refund();
        }
    },
    async onClickRefund() {
        await refundUtils.showRefundPopup(this.dialog, this.pos);
    },
    refund_get_button_color() {
        return refundUtils.getButtonColor(this.pos.get_order());
    },
});
