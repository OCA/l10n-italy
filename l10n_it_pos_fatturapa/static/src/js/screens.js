odoo.define("l10n_it_pos_fatturapa.ClientDetailsEdit", function (require) {
    "use strict";

    var ClientDetailsEdit = require("point_of_sale.ClientDetailsEdit");
    const Registries = require("point_of_sale.Registries");

    const PosClientDetailsEdit = (ClientDetailsEdit) =>
        class extends ClientDetailsEdit {
            constructor() {
                super(...arguments);
                const partner = this.props.partner;
                this.changes.electronic_invoice_obliged_subject =
                    partner.electronic_invoice_obliged_subject;
            }
            captureChange(event) {
                super.captureChange(event);
                if (event.target.name === "electronic_invoice_obliged_subject") {
                    $("#electronic_invoice_obliged_subject").css(
                        "display",
                        event.target.checked ? "block" : "none"
                    );
                    this.changes[event.target.name] = event.target.checked;
                }
            }
        };

    Registries.Component.extend(ClientDetailsEdit, PosClientDetailsEdit);

    return ClientDetailsEdit;
});
