odoo.define("fiscal_epos_print_fiscalcode.models", function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var fiscal_epos_print_models = require("fiscal_epos_print.epson_epos_print");

//    const ClientListScreen = require('point_of_sale.ClientListScreen');
//    const Registries = require('point_of_sale.Registries');
//    var { Gui } = require('point_of_sale.Gui');
//    var models = require('point_of_sale.models');
//
//    const POSSaveClientOverride1 = ClientListScreen =>
//        class extends ClientListScreen {
//            async saveChanges(event) {
//                var epos_print_fiscalcode_receipt =$('.epos_print_fiscalcode_receipt').val();
//
//                console.log(epos_print_fiscalcode_receipt);
//
//                    let partnerId = await this.rpc({
//                    model: 'res.partner',
//                    method: 'create_from_ui',
//                    args: [event.detail.processedChanges],
//                });
//                //console.log(partnerId);
//                await this.env.pos.load_new_partners();
//                this.state.selectedClient = this.env.pos.db.get_partner_by_id(partnerId);
//                this.state.detailIsShown = false;
//                this.render();
//            }
//        };
//        Registries.Component.extend(ClientListScreen, POSSaveClientOverride1);
//        return ClientListScreen;

    fiscal_epos_print_models.eposDriver.include( {
        printFiscalReceiptHeader: function (receipt) {
            var self = this;
    //            this.sender = sender;
    //            var opt = options;
            var fiscalcode_message = "";
            var current_client = this.sender.env.pos.get_client();
            var fiscalcode = current_client && current_client.fiscalcode;
            if (fiscalcode && current_client.epos_print_fiscalcode_receipt) {
                fiscalcode = fiscalcode.toUpperCase();
                fiscalcode_message = "\n" + _t("F.C.: ") + fiscalcode + "\n";
            }

            if (fiscalcode_message) {
                if (!receipt.header) {
                    receipt.header = "";
                }
                receipt.header += fiscalcode_message;
            }

            return this._super(receipt);
        },
    });

    fiscal_epos_print_models.eposDriver.include( {
        printFiscaldirectIOCodiceFiscale: function (receipt) {
            var self = this;
    //            this.sender = sender;
    //            var opt = options;
            var fiscalcode_message = "";
            var current_client = this.sender.env.pos.get_client();
            var fiscalcode = current_client && current_client.fiscalcode;
            if (fiscalcode && current_client.epos_print_fiscalcode_receipt) {
                fiscalcode = fiscalcode.toUpperCase();
                fiscalcode_message = "\n" + fiscalcode + "\n";
            }

            if (fiscalcode_message) {
                if (!receipt.header) {
                    receipt.header = "";
                }
                receipt.header += fiscalcode_message;
            }

            return this._super(receipt);
        },
    });
});
