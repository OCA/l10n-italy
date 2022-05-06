odoo.define("fiscal_epos_print.SetRefundInfoButton", function (require) {
    "use strict";

    var core = require("web.core");
    var _t = core._t;
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    // Const {useListener} = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");
    // Const {Gui} = require("point_of_sale.Gui");
    // const {posbus} = require("point_of_sale.utils");
    // const PaymentScreen = require("point_of_sale.PaymentScreen");

    class SetRefundInfoButton extends PosComponent {
        // Constructor() {
        // super(...arguments);
        // useListener('click', this.onClick);
        // This is from older widget system 12.0
        // this.pos.bind('change:selectedOrder',function(){
        //     this.orderline_change();
        //     this.bind_order_events();
        // },this);
        // }

        mounted() {
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

        // WillUnmount() {
        //     this.env.pos.get('orders').off('add remove change', null, this);
        //     this.env.pos.off('change:selectedOrder', null, this);
        // }
        async onClickRefund() {
            var self = this;
            var current_order = this.env.pos.get_order();
            this.showPopup("RefundInfoPopup", {
                title: _t("Refund Information Details"),
                refund_date: current_order.refund_date,
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
            //            Return true;
            return this.env.pos;
        },
    });

    Registries.Component.add(SetRefundInfoButton);

    return SetRefundInfoButton;
});
