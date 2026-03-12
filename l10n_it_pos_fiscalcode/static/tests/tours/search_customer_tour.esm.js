/*
 * Copyright 2026 Simone Rubino
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
 */

import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import * as PartnerList from "@point_of_sale/../tests/tours/utils/partner_list_util";
import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";
import {registry} from "@web/core/registry";

const customerName = "Test Customer with fiscal code";
const customerFiscalCode = "RSSMRA84H04H501X";

registry.category("web_tour.tours").add("SearchByFiscalCode", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ProductScreen.clickPartnerButton(),
            PartnerList.searchCustomerValue(customerFiscalCode),
            PartnerList.clickPartner(customerName),
            ProductScreen.customerIsSelected(customerName),
            Chrome.endTour(),
        ].flat(),
});
