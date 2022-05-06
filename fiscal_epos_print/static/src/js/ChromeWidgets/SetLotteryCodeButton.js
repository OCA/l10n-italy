odoo.define("fiscal_epos_print.SetLotteryCodeButton", function (require) {
    "use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const {useListener} = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");
    const {Gui} = require("point_of_sale.Gui");
    var core = require("web.core");
    var _t = core._t;

    class SetLotteryCodeButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener("click", this.onClick);
            // This is from older widget system 12.0
            // var self = this;
            // This.pos.bind('change:selectedOrder',function(){
            //     //self.renderElement();
            // },this);
        }
        mounted() {
            var color = this.lottery_get_button_color();
            this.$el.css("background", color);
        }
        // WillUnmount() {
        //     this.env.pos.get('orders').off('add remove change', null, this);
        //     this.env.pos.off('change:selectedOrder', null, this);
        // }
        async onClick() {
            var self = this;
            var current_order = self.pos.get_order();
            Gui.showPopup("lotterycode", {
                title: _t("Lottery Code"),
                lottery_code: current_order.lottery_code,
                update_lottery_info_button: function () {
                    // Self.renderElement();
                },
            });
        }

        lottery_get_button_color() {
            var order = this.pos.get_order();
            var color = "#e2e2e2";
            if (order.lottery_code) {
                color = "lightgreen";
            }
            return color;
        }
    }

    SetLotteryCodeButton.template = "SetLotteryCodeButton";

    ProductScreen.addControlButton({
        component: SetLotteryCodeButton,
        condition: function () {
            return true;
        },
    });

    Registries.Component.add(SetLotteryCodeButton);

    return SetLotteryCodeButton;
});
