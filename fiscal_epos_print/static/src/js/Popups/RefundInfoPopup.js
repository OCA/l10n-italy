odoo.define("fiscal_epos_print.RefundInfoPopup", function (require) {
    "use strict";

    const {useState, useRef} = owl.hooks;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");

    class RefundInfoPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);

            this.state = useState({inputValue: this.props.startingValue});
            this.inputRefundReport = useRef("inputRefundReport");
            this.inputRefundDate = useRef("inputRefundDate");
            this.inputRefundDocNum = useRef("inputRefundDocNum");
            this.inputRefundCashFiscalSerial = useRef("inputRefundCashFiscalSerial");
            this.inputDatePicker = null;
            // TODO to be removed;
            // this.refund_report = null;
            // this.refund_date = null;
            // this.refund_doc_num = null;
            // this.refund_cash_fiscal_serial = null;
            // this.datepicker = null;
        }

        mounted() {
            this.inputRefundReport.el.focus();
            this.initializeDatePicker();
        }

        // TODO this first migration is from method show() and it's seems to be incorrect
        // mounted(options){
        //     options = options || {};
        //     super.mounted(...arguments);
        //     this.update_refund_info_button = options.update_refund_info_button;
        //     // this.renderElement();
        //     this.datepicker = null;
        //     // this.$('refund_report').focus();
        //     this.initializeDatePicker();
        // }

        clickConfirmRefund() {
            this.$el = $(this.el);
            var self = this;
            function allValid() {
                return self.$el
                    .find("input")
                    .toArray()
                    .every(function (element) {
                        return element.value && element.value != "";
                    });
            }

            if (allValid()) {
                this.$el.find("#error-message-dialog").hide();

                var order = this.env.pos.get_order();
                order.refund_report = this.$el.find("#refund_report").val();
                order.refund_date = this.$el.find("#refund_date").val();
                order.refund_doc_num = this.$el.find("#refund_doc_num").val();
                order.refund_cash_fiscal_serial = this.$el
                    .find("#refund_cash_fiscal_serial")
                    .val();
                this.trigger("close-popup");
                if (
                    this.props.update_refund_info_button &&
                    this.props.update_refund_info_button instanceof Function
                ) {
                    this.props.update_refund_info_button();
                }
            } else {
                this.$el.find("#error-message-dialog").show();
            }
        }

        initializeDatePicker() {
            var self = this;
            this.$el = $(this.el);
            var element = this.$el.find("#refund_date").get(0);
            if (element && !this.datepicker) {
                this.datepicker = new Pikaday({
                    field: element,
                });
            }
        }
    }

    RefundInfoPopup.template = "RefundInfoPopup";

    RefundInfoPopup.defaultProps = {
        confirmText: "Ok",
        cancelText: "Cancel",
        body: "",
    };

    Registries.Component.add(RefundInfoPopup);

    return RefundInfoPopup;
});
