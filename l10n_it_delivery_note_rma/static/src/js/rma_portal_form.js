/* Copyright 2021 Tecnativa - David Vidal
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("rma_ddt.animation", function (require) {
    "use strict";
    const publicWidget = require("web.public.widget");

    /**
     * Adds some machinery to the customer portal RMA form:
     *
     * - Avoid submitting the form if no qty or operation is reported.
     * - Show automatically the observations field when the operation is selected
     *   and hide it back with no operation selected.
     */
    publicWidget.registry.PortalRmaDdt = publicWidget.Widget.extend({
        selector: "#form-request-rma-ddt",
        events: {
            "change .rma-operation": "_onChangeOperationId",
            "change #delivery-rma-qty input": "_onChangeQty",
        },

        /**
         * @override
         */
        start: function () {
            const ids = this.$("[name*='-operation_id']")
                .map(function () {
                    return this.name.replace("-operation_id", "");
                })
                .get();
            this.$submit = $("#form-request-rma-ddt button[type='submit']");
            this.rows_ids = ids;
            // We'll build an object that will ease the form check. It could be further
            // extended with additional checks.
            this.rows = {};
            _.each(ids, (id) => {
                this.rows[id] = {
                    $comment: this.$(`#comment-${id}`),
                    $comment_input: this.$(`[name='${id}-description']`),
                    $operation: this.$(`[name='${id}-operation_id']`),
                    $qty: this.$(`[name='${id}-quantity']`),
                };
            });
            this._checkCanSubmit();
        },
        /**
         * @private
         * @param {Object} row: the form row structure
         */
        _show_comment: function (row) {
            if (row.$comment) {
                row.$comment.addClass("show");
                if (row.$comment_input) {
                    row.$comment_input.focus();
                }
            }
        },
        /**
         * @private
         * @param {Object} row: the form row structure
         */
        _hide_comment: function (row) {
            if (row.$comment) {
                row.$comment.removeClass("show");
            }
        },
        /**
         * We should be able to submit only when an operation is selected and a
         * quantity entered in a row at least.
         * @private
         */
        _canSubmit: function () {
            var can_submit = false;
            for (const id of this.rows_ids) {
                const row = this.rows[id];
                if (
                    row &&
                    // Qty greater than 0
                    row.$qty &&
                    row.$qty.val() &&
                    Number(row.$qty.val()) &&
                    // An operation is defined
                    row.$operation &&
                    row.$operation.val()
                ) {
                    can_submit = true;
                    break;
                }
            }
            return can_submit;
        },
        /**
         * Checked every time we change the quantity or the operation and at start
         *
         * @private
         * @param {Object} row: the form row structure
         */
        _checkCanSubmit: function () {
            this.$submit.prop("disabled", !this._canSubmit());
        },
        /**
         * @private
         * @param {InputEvent} ev
         */
        _onChangeOperationId: function (ev) {
            // Toggle comment on or off if an operation is requested
            const id = ev.currentTarget.name.replace("-operation_id", "");
            var row = this.rows[id];
            if (row && row.$operation && row.$operation.val()) {
                this._show_comment(row);
            } else {
                this._hide_comment(row);
            }
            this._checkCanSubmit();
        },
        /**
         * @private
         */
        _onChangeQty: function () {
            this._checkCanSubmit();
        },
    });
});
