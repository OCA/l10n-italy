odoo.define("fiscal_epos_print.SetRefundInfoButton", function (require) {
    "use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const core = require("web.core");
    const _t = core._t;

    class SetRefundInfoButton extends PosComponent {
        onMounted() {
            this.bind_order_events();
            this.orderline_change();
        }

        is_available() {
            const order = this.env.pos.get_order();
            return order;
        }

        render() {
            var color = this.refund_get_button_color();
            $(this.el).css("background", color);
        }

        async onClickRefund() {
            var self = this;
            var current_order = this.env.pos.get_order();
            if (
                current_order.refund_date === null ||
                current_order.refund_date === ""
            ) {
                this.showPopup("ErrorPopup", {
                    title: _t("Error"),
                    body: _t(
                        "Must select a refund order before clicking on this button!"
                    ),
                });
            }
            var dd = ("0" + current_order.refund_date.getDate()).slice(-2);
            var mm = ("0" + (current_order.refund_date.getMonth() + 1)).slice(-2);
            var yyyy = current_order.refund_date.getFullYear();
            this.showPopup("RefundInfoPopup", {
                title: _t("Refund Information Details"),
                refund_date: yyyy + "-" + mm + "-" + dd,
                refund_report: current_order.refund_report,
                refund_doc_num: current_order.refund_doc_num,
                refund_cash_fiscal_serial: current_order.refund_cash_fiscal_serial,
                update_refund_info_button: function () {
                    self.render();
                },
            });
        }

        bind_order_events() {
            var order = this.env.pos.get_order();

            if (!order) {
                return;
            }

            if (this.old_order) {
                this.old_order.unbind(null, null, this);
            }

            this.env.pos.bind("change:selectedOrder", this.orderline_change, this);

            var lines = order.orderlines;
            lines.unbind("add", this.orderline_change, this);
            lines.bind("add", this.orderline_change, this);
            lines.unbind("remove", this.orderline_change, this);
            lines.bind("remove", this.orderline_change, this);
            lines.unbind("change", this.orderline_change, this);
            lines.bind("change", this.orderline_change, this);

            this.old_order = order;
        }

        refund_get_button_color() {
            var order = this.env.pos.get_order();
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
            var order = this.env.pos.get_order();
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

    SetRefundInfoButton.template = "SetRefundInfoButton";

    ProductScreen.addControlButton({
        component: SetRefundInfoButton,
        condition: function () {
            return this.env.pos;
        },
    });

    Registries.Component.add(SetRefundInfoButton);

    return SetRefundInfoButton;
});
