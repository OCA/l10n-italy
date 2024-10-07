/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";


export class EpsonEPOSButton extends Component {
    setup() {
        super.setup();
        this.state = useState({
            isVisible: false,
        });
    }

    onClick() {
        this.state.isVisible = !this.state.isVisible;
        const epsonFP81IIComponent = document.querySelector(".status-buttons .epson-fp81ii-widget");
        if (this.state.isVisible) {
            epsonFP81IIComponent.classList.remove("visually-hidden");
        } else {
            epsonFP81IIComponent.classList.add("visually-hidden");
        }
    }
}

EpsonEPOSButton.template = 'fiscal_epos_print.EpsonEPOSButton';

// Add the EpsonEPOSButton to Navbar components
patch(Navbar, {
    components: { ...Navbar.components, EpsonEPOSButton },
});
