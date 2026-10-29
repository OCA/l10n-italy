import {Component, useState} from "@odoo/owl";
import {Navbar} from "@point_of_sale/app/navbar/navbar";
import {patch} from "@web/core/utils/patch";

export class EpsonEPOSButton extends Component {
    setup() {
        super.setup();
        this.state = useState({
            isVisible: false,
        });
    }

    onClick() {
        // eslint-disable-next-line no-undef
        const epsonFP81IIComponent = document.querySelector(
            ".status-buttons .epson-fp81ii-widget"
        );

        // Check actual visibility state from DOM instead of relying on internal state
        const isCurrentlyHidden =
            epsonFP81IIComponent?.classList.contains("visually-hidden");

        if (isCurrentlyHidden) {
            epsonFP81IIComponent.classList.remove("visually-hidden");
            this.state.isVisible = true;
        } else {
            epsonFP81IIComponent.classList.add("visually-hidden");
            this.state.isVisible = false;
        }
    }
}

EpsonEPOSButton.template = "l10n_it_fiscal_epos_print.EpsonEPOSButton";

// Add the EpsonEPOSButton to Navbar components
patch(Navbar, {
    components: {...Navbar.components, EpsonEPOSButton},
});
