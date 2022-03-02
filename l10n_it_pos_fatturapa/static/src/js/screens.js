odoo.define("l10n_it_pos_fatturapa.screens", function (require) {
    "use strict";

    const {parse} = require("web.field_utils");
    const PosComponent = require("point_of_sale.PosComponent");
    const Registries = require("point_of_sale.Registries");
    const ClientDetailsEdit = require("point_of_sale.ClientDetailsEdit");

    const ClientDetailsEditFatturapa = (ClientDetailsEdit) =>
        class extends ClientDetailsEdit {
            constructor() {
                super(...arguments);
            }

            mounted() {
                this.electronic_invoice_subjected();
                super.mounted(...arguments);
            }
            willUnmount() {
                this.electronic_invoice_subjected();
                super.willUnmount(...arguments);
            }

            electronic_invoice_subjected() {
                var self = this;
                $(".electronic_invoice_subjected")
                    .off("change")
                    .on("change", function (event) {
                        this.value = this.checked;
                        $("#electronic_invoice_subjected").css(
                            "display",
                            this.checked ? "block" : "none"
                        );
                    });
            }
        };

    Registries.Component.extend(ClientDetailsEdit, ClientDetailsEditFatturapa);

    return ClientDetailsEdit;
});
