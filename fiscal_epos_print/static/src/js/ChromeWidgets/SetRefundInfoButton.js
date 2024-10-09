/** @odoo-module */

import { Component, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { RefundInfoPopup } from "../Popups/RefundInfoPopup";

export class SetRefundInfoButton extends Component {
    static template = "SetRefundInfoButton";
    static components = {
        ErrorPopup
    }
    setup() {
        super.setup();
        this.pos = usePos();
        this.popup = useService("popup");

        onMounted(() => {
            this.bind_order_events();
            this.orderline_change();
        });
    }
    is_available() {
        const order = this.pos.get_order();
        return order;
    }
    render() {
        var color = this.refund_get_button_color();
        $('#refund_info_button').css('background-color', color);
    }
    async onClickRefund() {
        var self = this;
        var current_order = this.pos.get_order();
        var dd = null;
        var mm = null;
        var yyyy = null;
        // if (current_order) {
        //     dd = ("0" + current_order.date_order.getDate()).slice(-2);
        //     mm = ("0" + (current_order.date_order.getMonth() + 1)).slice(-2);
        //     yyyy = current_order.date_order.getFullYear();
        // }
        await this.popup.add(RefundInfoPopup, {
            title: _t("Refund Information Details"),
            // refund_date: yyyy + "-" + mm + "-" + dd,
            // refund_report: current_order.refund_report,
            // refund_doc_num: current_order.refund_doc_num,
            // refund_cash_fiscal_serial: current_order.refund_cash_fiscal_serial,
            // refund_full_refund: current_order.refund_full_refund,
        }).then(async () => {
            this.update_refund_info_button();
        });
    }
    update_refund_info_button() {
        this.render();
    }
    bind_order_events() {
        var order = this.pos.get_order();
        if (!order) {
            return;
        }
        if (this.old_order) {
            this.old_order.unbind(null, null, this);
        }
        // TODO: Servono?
        // this.pos.bind("change:selectedOrder", this.orderline_change, this);
        var lines = order.orderlines;
        // lines.unbind("add", this.orderline_change, this);
        // lines.bind("add", this.orderline_change, this);
        // lines.unbind("remove", this.orderline_change, this);
        // lines.bind("remove", this.orderline_change, this);
        // lines.unbind("change", this.orderline_change, this);
        // lines.bind("change", this.orderline_change, this);
        this.old_order = order;
    }
    refund_get_button_color() {
        var order = this.pos.get_order();
        var color = "#e2e2e2";
        if (order) {
            var lines = order.orderlines;
            var has_refund =
                lines.find(function (line) {
                    return line.quantity < 0.0;
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
    }
    orderline_change() {
        var order = this.pos.get_order();
        if (order) {
            var lines = order.orderlines;
            order.has_refund =
                lines.find(function (line) {
                    return line.quantity < 0.0;
                }) !== undefined;
        }
        this.render();
    }
}
ProductScreen.addControlButton({
    component: SetRefundInfoButton
});
registry.category("pos_screens").add("SetRefundInfoButton", SetRefundInfoButton);
return SetRefundInfoButton;
