/*
 * Copyright 2026 Simone Rubino
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
 */

import {ResPartner} from "@point_of_sale/app/models/res_partner";
import {patch} from "@web/core/utils/patch";

patch(ResPartner.prototype, {
    get searchString() {
        let searchString = super.searchString;
        const fiscalCode = this.l10n_it_codice_fiscale;
        if (fiscalCode) {
            searchString += " " + fiscalCode;
        }
        return searchString;
    },
});
