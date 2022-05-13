odoo.define("fiscal_epos_print.EpsonEPOSButton", function (require) {
    "use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class EpsonEPOSButton extends PosComponent {

        /**
         * Method that manage EpsonFP81IIComponent visibility through onClick
         *  Handler
         */
        onClick() {
            var epsonFP81IIComponent = $('.status-buttons .epson-fp81ii-widget');
            if (epsonFP81IIComponent.hasClass('oe_hidden')) {
                epsonFP81IIComponent.css({opacity:0});
                epsonFP81IIComponent.removeClass('oe_hidden');
                epsonFP81IIComponent.animate({opacity:1},250,'swing');
            } else {
                epsonFP81IIComponent.animate({opacity:0,},250,'swing',function() {
                    epsonFP81IIComponent.addClass('oe_hidden');
                });
            }
        }

    }

    EpsonEPOSButton.template = 'EpsonEPOSButton';

    Registries.Component.add(EpsonEPOSButton);

    return EpsonEPOSButton;
});
