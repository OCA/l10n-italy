odoo.define("fiscal_epos_print.screens", function (require) {
    "use strict";

    var core = require("web.core");
    var screens = require('point_of_sale.screens');
    var epson_epos_print = require('fiscal_epos_print.epson_epos_print');
    var _t = core._t;
    var PaymentScreenWidget = screens.PaymentScreenWidget;
    var ReceiptScreenWidget = screens.ReceiptScreenWidget;
    var eposDriver = epson_epos_print.eposDriver;

    // While the printer is still closing the dialogue with the terminal, a new
    // authorizeSales sent too soon gets its connection reset (NS_ERROR_NET_RESET).
    // Before sending, we "knock" with a read-only queryPrinterStatus until the
    // printer answers: re-knock every INTERVAL, give up after MAX.
    var EFTPOS_KNOCK_INTERVAL_MS = 1000;
    var EFTPOS_KNOCK_MAX_MS = 15000;

    ReceiptScreenWidget.include({

        lock_screen: function(locked) {
            this._super.apply(this, arguments);
            if (locked) {
                this.$('.receipt-sent').hide();
                this.$('.printing-error').show();
                this.$('.printing-retry').show();
            } else {
                this.$('.receipt-sent').show();
                this.$('.printing-error').hide();
                this.$('.printing-retry').hide();
            }
        },

        sendToFP90Printer: function(receipt, printer_options) {
            var fp90 = new eposDriver(printer_options, this);
            fp90.printFiscalReceipt(receipt);
        },

        render_receipt: function() {
            var self = this;
            this._super();
            this.$('.printing-retry').click(function(){
                if (self._locked) {
                    var currentOrder = self.pos.get_order();
                    self.chrome.loading_show();
                    self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                    var printer_options = currentOrder.getPrinterOptions();
                    printer_options.order = currentOrder;
                    var receipt = currentOrder.export_for_printing();
                    self.sendToFP90Printer(receipt, printer_options);
                }
            });
        }
    });

    PaymentScreenWidget.include({
        show: function() {
            this._super.apply(this, arguments);
            if (this.pos.config.printer_ip) {
                var currentOrder = this.pos.get_order();
                var printer_options = currentOrder.getPrinterOptions();
                var fp90 = new eposDriver(printer_options, this);
                var amount = this.format_currency(currentOrder.get_total_with_tax());
                fp90.printDisplayText(_t("SubTotal") + " " + amount);
            }
        },
        sendToFP90Printer: function(receipt, printer_options) {
            var fp90 = new eposDriver(printer_options, this);
            fp90.printFiscalReceipt(receipt);
        },
        finalize_validation: function() {
            // we need to get currentOrder before calling the _super()
            // otherwise we will likely get a empty order when we want to skip
            // the receipt preview
            var currentOrder = this.pos.get('selectedOrder');
            this._super.apply(this, arguments);
            if (this.pos.config.printer_ip && !currentOrder.is_to_invoice()) {
                if (currentOrder._eftpos_timing) {
                    currentOrder._eftpos_timing.print_start_ts = Date.now();
                }
                this.chrome.loading_show();
                this.chrome.loading_message(_t('Connecting to the fiscal printer'));
                var printer_options = currentOrder.getPrinterOptions();
                printer_options.order = currentOrder;
                var receipt = currentOrder.export_for_printing();
                this.sendToFP90Printer(receipt, printer_options);
            }
        },
        _get_eftpos_payment_line: function(order) {
            return _.find(order.get_paymentlines(), function(line) {
                var journal = line.cashregister && line.cashregister.journal;
                return journal && journal.fiscalprinter_eftpos;
            }) || null;
        },

        /*
          When the order is paid through a journal flagged "Activate EFT-POS",
          authorize the amount on the terminal BEFORE creating the order and
          printing. authorizeEftpos() is asynchronous, so we show an animated
          loading overlay while the customer taps the card / enters the PIN and
          branch on the outcome in the callback:
            - approved -> mark the order authorized and re-enter validate_order,
              which now falls through to the standard validation (_super) and
              creates the order and prints the receipt exactly as before;
            - declined -> show an error and abort - no order, no receipt.
        */
        validate_order: function(force_validation) {
            var self = this;
            var order = this.pos.get_order();
            var eftposLine = order && this._get_eftpos_payment_line(order);
            if (this.pos.config.printer_ip && eftposLine && !order.is_to_invoice()
                    && !order._eftpos_authorized) {
                // Only contact the terminal once the order is otherwise valid.
                if (!this.order_is_valid(force_validation)) {
                    return;
                }
                // Concurrency guard: never run two exchanges at once (the loading
                // overlay also blocks the UI during one).
                if (this.pos._eftpos_busy) {
                    this.gui.show_popup('error', {
                        'title': _t('Payment terminal busy'),
                        'body': _t('The payment terminal is still busy with the previous transaction. Please wait a few seconds and try again.'),
                    });
                    return;
                }
                this.pos._eftpos_busy = true;
                this.chrome.loading_show();
                this.chrome.loading_message(_t('Waiting for the payment terminal'));
                var printer_options = order.getPrinterOptions();
                printer_options.order = order;
                var fp90 = new eposDriver(printer_options, this);
                var releaseEftpos = function() {
                    self.pos._eftpos_busy = false;
                    self.chrome.loading_hide();
                };
                // Send the actual (non-idempotent) amount exchange.
                var sendExchange = function() {
                    self.chrome.loading_message(_t('Waiting for the payment terminal'));
                    try {
                        fp90.authorizeEftpos({
                            amount: eftposLine.get_amount(),
                            timeout: eftposLine.cashregister.journal.fiscalprinter_eftpos_timeout,
                        }, function(outcome) {
                            releaseEftpos();
                            if (!outcome.approved) {
                                console.log('EFT-POS not approved:', outcome);
                                var details = 'code: ' + (outcome.code || 'n/d') +
                                    (outcome.status != null ? ', status: ' + outcome.status : '') +
                                    (outcome.elapsed_ms != null ? ', ' + Math.round(outcome.elapsed_ms / 1000) + 's' : '');
                                var body;
                                if (outcome.declined) {
                                    body = _t('The payment terminal declined the transaction (electronic payment error).') +
                                        ' (' + details + '). ' +
                                        _t('No receipt or order was created.');
                                } else if (outcome.code === 'FP_NO_ANSWER_NETWORK') {
                                    body = _t('The payment terminal is busy (network error): the request was reset while the printer was still handling the previous transaction. Please wait a few seconds and try again.') +
                                        ' (' + details + ').';
                                } else {
                                    body = _t('No answer from the payment terminal') +
                                        ' (' + details + '). ' +
                                        _t('The transaction was not completed; no receipt or order was created.');
                                    if (outcome.code === 'FP_NO_ANSWER') {
                                        body += ' ' + _t('This usually means a time-out: increase the EFT-POS timeout on the payment method and on the printer (SET 31).');
                                    }
                                }
                                self.gui.show_popup('error', {
                                    'title': _t('EFT-POS payment not completed'),
                                    'body': body,
                                });
                                return;
                            }
                            order._eftpos_authorized = true;
                            order._eftpos_timing = {
                                authorize_ms: outcome.elapsed_ms,
                                auth_done_ts: Date.now(),
                            };
                            self.validate_order(force_validation);
                        });
                    } catch (err) {
                        // Never leave the busy flag stuck if the request fails to start.
                        releaseEftpos();
                        console.log('EFT-POS request failed to start:', err);
                        self.gui.show_popup('error', {
                            'title': _t('EFT-POS payment not completed'),
                            'body': _t('Could not start the EFT-POS request. Please try again.'),
                        });
                    }
                };
                // "Knock" first: a read-only queryPrinterStatus tells us when the
                // printer is reachable/free (it resets the connection while still
                // busy with the terminal). A status query cannot start a payment,
                // so it is safe to repeat. Only once it answers do we send the real
                // exchange; otherwise re-knock until EFTPOS_KNOCK_MAX_MS, then give
                // up with a clear message.
                var knockDeadline = Date.now() + EFTPOS_KNOCK_MAX_MS;
                var knock = function() {
                    fp90.probePrinterReady(function(ready) {
                        if (ready) {
                            sendExchange();
                        } else if (Date.now() < knockDeadline) {
                            self.chrome.loading_message(_t('Payment terminal busy, waiting...'));
                            setTimeout(knock, EFTPOS_KNOCK_INTERVAL_MS);
                        } else {
                            releaseEftpos();
                            self.gui.show_popup('error', {
                                'title': _t('Payment terminal busy'),
                                'body': _t('The payment terminal is still busy with the previous transaction. Please wait a few seconds and try again.'),
                            });
                        }
                    });
                };
                knock();
                return;
            }
            return this._super(force_validation);
        },

        order_is_valid: function(force_validation) {
            if (this.pos.config.iface_tax_included == 'subtotal') {
                this.gui.show_popup('error',{
                    'title': _t('Wrong tax configuration'),
                    'body':  _t("Product prices on receipts must be set to 'Tax-Included Price' in POS configuration"),
                });
                return false;
            }
            var self = this;
            var receipt = this.pos.get_order();
            if (receipt.has_refund && (receipt.refund_date == null || receipt.refund_date === '' ||
                                       receipt.refund_doc_num == null || receipt.refund_doc_num == '' ||
                                       receipt.refund_cash_fiscal_serial == null || receipt.refund_cash_fiscal_serial == '' ||
                                       receipt.refund_report == null || receipt.refund_report == '')) {
                    this.gui.show_popup('error',{
                        'title': _t('Refund Information Not Present'),
                        'body':  _t("The refund information aren't present. Please insert them before printing the receipt"),
                    });
                    return false;
            }
            return this._super(force_validation);
        }
    });

    var set_refund_info_button = screens.ActionButtonWidget.extend({
        template: 'SetRefundInfoButton',
        init: function(parent, options) {
            var self = this;
            this._super(parent, options);
            this.pos.bind('change:selectedOrder',function(){
                this.orderline_change();
                this.bind_order_events();
            },this);
            this.bind_order_events();
            this.orderline_change();
        },
        renderElement: function() {
            this._super();
            var color = this.refund_get_button_color();
            this.$el.css('background', color);
        },
        button_click: function () {
            var self = this;
            var current_order = self.pos.get_order();
            self.gui.show_popup('refundinfo', {
                title: _t('Refund Information Details'),
                refund_date: current_order.refund_date,
                refund_report: current_order.refund_report,
                refund_doc_num: current_order.refund_doc_num,
                refund_cash_fiscal_serial: current_order.refund_cash_fiscal_serial,
                update_refund_info_button: function(){
                    self.renderElement();
                },
            });
        },
        bind_order_events: function() {
            var self = this;
            var order = this.pos.get_order();

            if (!order) {
                return;
            }

            if(this.old_order) {
                this.old_order.unbind(null,null,this);
            }

            this.pos.bind('change:selectedOrder', this.orderline_change, this);

            var lines = order.orderlines;
                lines.unbind('add',     this.orderline_change, this);
                lines.bind('add',       this.orderline_change, this);
                lines.unbind('remove',  this.orderline_change, this);
                lines.bind('remove',    this.orderline_change, this);
                lines.unbind('change',  this.orderline_change, this);
                lines.bind('change',    this.orderline_change, this);

            this.old_order = order;
        },
        refund_get_button_color: function() {
            var order = this.pos.get_order();
            var color = '#e2e2e2';
            if(order) {
                var lines = order.orderlines;
                var has_refund = lines.find(function(line){ return line.quantity < 0.0;}) != undefined;
                if (has_refund == true)
                {
                    if (order.refund_date && order.refund_date != '' && order.refund_doc_num && order.refund_doc_num != '' &&
                        order.refund_cash_fiscal_serial && order.refund_cash_fiscal_serial != '' && order.refund_report && order.refund_report != '') {
                            color = 'lightgreen';
                    }
                    else
                    {
                        color = 'red';
                    }
                }
            }
            return color;
        },
        orderline_change: function(){
            var order = this.pos.get_order();
            if (order) {
                var lines = order.orderlines;
                order.has_refund = lines.find(function(line){ return line.quantity < 0.0;}) != undefined;
            }
            this.renderElement();
        },
    });

    screens.define_action_button({
        'name': 'set_refund_info',
        'widget': set_refund_info_button,
    });

    // TODO Evaluate how to set lottery code without popup, automatically on barcode scanned
    var set_lottery_code_button = screens.ActionButtonWidget.extend({
        template: 'SetLotteryCodeButton',
        init: function(parent, options) {
            this._super(parent, options);
            var self = this;
            this.pos.bind('change:selectedOrder',function(){
                self.renderElement();
            },this);
        },
        renderElement: function() {
            this._super();
            var color = this.lottery_get_button_color();
            this.$el.css('background', color);
        },
        button_click: function () {
            var self = this;
            var current_order = self.pos.get_order();
            self.gui.show_popup('lotterycode', {
                title: _t('Lottery Code'),
                lottery_code: current_order.lottery_code,
                update_lottery_info_button: function(){
                    self.renderElement();
                },
            });
        },
        lottery_get_button_color: function() {
            var order = this.pos.get_order();
            var color = '#e2e2e2';
            if (order && order.lottery_code) {
                color = 'lightgreen';
            }
            return color;
        },
    });

    screens.define_action_button({
        'name': 'set_lottery_code',
        'widget': set_lottery_code_button,
    });

    return {
        RefundInfoButtonActionWidget: set_refund_info_button,
        LotteryCodeButtonActionWidget: set_lottery_code_button
    };

});
