odoo.define("l10n_it_pos_fatturapa.ClientDetailsEdit", function (require) {
    "use strict";

    const {_t} = require("web.core");
    const ClientDetailsEdit = require("point_of_sale.ClientDetailsEdit");
    const Registries = require("point_of_sale.Registries");

    const PosClientDetailsEditCode = (ClientDetailsEdit) =>
        class extends ClientDetailsEdit {
            constructor() {
                super(...arguments);
            }
            captureChange(event) {
                super.captureChange(event);
                if (event.target.name === "electronic_invoice_subjected") {
                    const checked = event.currentTarget.checked;
                    this.changes[event.target.name] = checked ? true: false;
                    $(".electronic_invoice_subjected")
                        .toArray()
                        .forEach(function (el) {
                            $(el).css("display", checked ? "block" : "none");
                        });
                }
            }
        };

    Registries.Component.extend(ClientDetailsEdit, PosClientDetailsEditCode);

    return ClientDetailsEdit;
});
