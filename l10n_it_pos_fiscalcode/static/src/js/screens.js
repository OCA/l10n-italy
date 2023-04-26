odoo.define("l10n_it_pos_fiscalcode.ClientDetailsEdit", function (require) {
    "use strict";

    const ClientDetailsEdit = require("point_of_sale.ClientDetailsEdit");
    const Registries = require("point_of_sale.Registries");
    const {_t} = require("web.core");

    const PosClientDetailsEdit = (ClientDetailsEdit) =>
        class extends ClientDetailsEdit {
            _validFiscalCode(fcins) {
                const fc = fcins.toUpperCase();
                const fcReg = /^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$/;
                if (!fcReg.test(fc)) {
                    return false;
                }

                const set1 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const set2 = "ABCDEFGHIJABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const seteven = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const setodd = "BAKPLCQDREVOSFTGUHMINJWZYX";
                let s = 0;

                for (let i = 1; i <= 13; i += 2)
                    s += seteven.indexOf(set2.charAt(set1.indexOf(fc.charAt(i))));
                for (let i = 0; i <= 14; i += 2)
                    s += setodd.indexOf(set2.charAt(set1.indexOf(fc.charAt(i))));
                if (s % 26 !== fc.charCodeAt(15) - "A".charCodeAt(0)) return false;
                return true;
            }
            saveChanges() {
                const processedChanges = {};
                for (const [key, value] of Object.entries(this.changes)) {
                    if (this.intFields.includes(key)) {
                        processedChanges[key] = parseInt(value) || false;
                    } else {
                        processedChanges[key] = value;
                    }
                }
                if (processedChanges.fiscalcode && processedChanges.fiscalcode !== "") {
                    if (!this._validFiscalCode(processedChanges.fiscalcode)) {
                        return this.showPopup("ErrorPopup", {
                            title: _t("The Fiscal code doesn't seem to be correct"),
                        });
                    }
                }
                super.saveChanges();
            }
        };

    Registries.Component.extend(ClientDetailsEdit, PosClientDetailsEdit);

    return ClientDetailsEdit;
});
