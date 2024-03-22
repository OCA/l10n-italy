odoo.define("fiscal_epos_print.RefundInfoPopup", function (require) {
    "use strict";

    const {useRef, useState} = owl;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const {_lt} = require("@web/core/l10n/translation");

    class RefundInfoPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);

            this.state = useState({inputValue: this.props.startingValue});
            this.inputRefundReport = useRef("inputRefundReport");
            this.inputRefundDate = useRef("inputRefundDate");
            this.inputRefundDocNum = useRef("inputRefundDocNum");
            this.inputRefundCashFiscalSerial = useRef("inputRefundCashFiscalSerial");
            this.inputRefundFullRefund = useRef("inputRefundFullRefund");
            this.inputDatePicker = this.initializeDatePicker();
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

                var refund_date = this.$el.find("#refund_date").val();
                var refund_report = this.$el.find("#refund_report").val();
                var refund_doc_num = this.$el.find("#refund_doc_num").val();
                var refund_cash_fiscal_serial = this.$el
                    .find("#refund_cash_fiscal_serial")
                    .val();
                var refund_full_refund = this.$el.find("#refund_full_refund").val();
                this.env.pos.context = {
                    refund_details: true,
                    refund_date: refund_date,
                    refund_report: refund_report,
                    refund_doc_num: refund_doc_num,
                    refund_cash_fiscal_serial: refund_cash_fiscal_serial,
                    refund_full_refund: refund_full_refund,
                };
                this.env.pos.set_refund_data(
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
                this.env.posbus.trigger("close-popup", {popupId: this.props.id});
            } else {
                this.$el.find("#error-message-dialog").show();
            }
        }

        initializeDatePicker() {
            this.$el = $(this.el);
            var element = this.$el.find("#refund_date").get(0);
            if (element && !this.datepicker) {
                // eslint-disable-next-line
                this.datepicker = new Pikaday({
                    field: element,
                });
            }
        }
    }

    RefundInfoPopup.template = "RefundInfoPopup";

    RefundInfoPopup.defaultProps = {
        confirmText: _lt("Ok"),
        cancelText: _lt("Cancel"),
        body: "",
    };

    Registries.Component.add(RefundInfoPopup);

    return RefundInfoPopup;
});
