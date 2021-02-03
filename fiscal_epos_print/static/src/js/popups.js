odoo.define("fiscal_epos_print.popups", function (require) {
    "use strict";

    var core = require("web.core");
    var popups = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var _t = core._t;

    function addPadding(str, padding=4) {
        var pad = new Array(padding).fill(0).join('') + str;
        return pad.substr(pad.length - padding, padding);
    }

    var RefundInfoPopupWidget = popups.extend({
        template: 'RefundInfoPopupWidget',
        init: function(parent) {
            this.refund_report = null;
            this.refund_date = null;
            this.refund_doc_num = null;
            this.refund_cash_fiscal_serial = null;
            this.datepicker = null;
            return this._super(parent);
        },
        show: function(options){
            options = options || {};
            this._super(options);
            this.update_refund_info_button = options.update_refund_info_button;
            this.renderElement();
            this.datepicker = null;
            this.$('refund_report').focus();
            this.initializeDatePicker();
        },
        click_confirm: function(){
            var self = this;
            function allValid() {
                return self.$('input').toArray().every(function(element) {
                    return element.value && element.value != ''
                })
            }

            if (allValid()) {
                this.$('#error-message-dialog').hide()

                var order = this.pos.get_order();
                order.refund_report = this.$('#refund_report').val();
                order.refund_date = this.$('#refund_date').val();
                order.refund_doc_num = this.$('#refund_doc_num').val();
                order.refund_cash_fiscal_serial = this.$('#refund_cash_fiscal_serial').val();
                this.gui.close_popup();
                if (this.update_refund_info_button && this.update_refund_info_button instanceof Function) {
                    this.update_refund_info_button();
                }
            } else {
                this.$('#error-message-dialog').show()
            }
        },
        initializeDatePicker: function() {
            var self = this,
                element = this.$('#refund_date').get(0);

            if (element && !this.datepicker) {
                this.datepicker = new Pikaday({
                    field: element,
                });
            }
        },
    });

    var LotteryCodePopupWidget = popups.extend({
        template: 'LotteryCodePopupWidget',
        init: function(parent) {
            this.lottery_code = null;
            return this._super(parent);
        },
        show: function(options){
            options = options || {};
            this._super(options);
            this.update_lottery_info_button = options.update_lottery_info_button;
            this.renderElement();
            this.$('lottery_code').focus();
        },
        // TODO automatically close popup on barcode scanned
        click_confirm: function(){
            var self = this;
            function allValid() {
                return self.$('input').toArray().every(function(element) {
                    return element.value && element.value != ''
                })
            }

            if (allValid()) {
                this.$('#lottery-error-message-dialog').hide()

                var order = this.pos.get_order();
                order.lottery_code = this.$('#lottery_code').val();
                this.gui.close_popup();
                if (this.update_lottery_info_button && this.update_lottery_info_button instanceof Function) {
                    this.update_lottery_info_button();
                }
            } else {
                this.$('#lottery-error-message-dialog').show()
            }
        },
    });

    gui.define_popup({name:'refundinfo', widget: RefundInfoPopupWidget});
    gui.define_popup({name:'lotterycode', widget: LotteryCodePopupWidget});

});
