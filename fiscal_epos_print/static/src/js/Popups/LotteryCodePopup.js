odoo.define("fiscal_epos_print.LotteryCodePopup", function (require) {
    "use strict";

    const {useRef, useState} = owl;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const {_lt} = require("@web/core/l10n/translation");

    class LotteryCodePopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);

            this.state = useState({inputValue: this.props.startingValue});
            this.inputLotteryCode = useRef("inputLotteryCode");
        }

        clickConfirmLotteryCode() {
            this.$el = $(this.el);
            var self = this;
            function allValid() {
                return self.$el
                    .find("input")
                    .toArray()
                    .every(function (element) {
                        return element.value && element.value !== "";
                    });
            }

            if (allValid()) {
                this.$el.find("#error-message-dialog").hide();

                var lottery_code = this.inputLotteryCode.el.value;
                this.env.pos.context = {
                    lottery_code: lottery_code,
                };
                this.env.pos.set_lottery_code_data(lottery_code);
                if (
                    this.props.update_lottery_info_button &&
                    this.props.update_lottery_info_button instanceof Function
                ) {
                    this.props.update_lottery_info_button();
                }
                this.env.posbus.trigger("close-popup", {popupId: this.props.id});
            } else {
                this.$el.find("#error-message-dialog").show();
            }
        }
    }

    LotteryCodePopup.template = "LotteryCodePopup";

    LotteryCodePopup.defaultProps = {
        confirmText: _lt("Ok"),
        cancelText: _lt("Cancel"),
        title: _lt("Confirm ?"),
        body: "",
    };

    Registries.Component.add(LotteryCodePopup);

    return LotteryCodePopup;
});
