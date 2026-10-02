# Leonardo Donelli - Creativi Quadrati
# © 2016 Alessio Gerace - Agile Business Group
# © 2018-2020 Lorenzo Battistini
# © 2019-2020 Roberto Fichera - Level Prime Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Driver per stampanti fiscali compatibili ePOS-Print XML",
    "version": "18.0.1.0.0",
    "category": "Point Of Sale",
    "summary": "ePOS-Print XML Fiscal Printer Driver - Stampanti Epson compatibili: "
    "FP81II, FP90III",
    "author": (
        "Odoo Community Association (OCA), Agile Business Group, "
        "Leonardo Donelli, TAKOBI, Level Prime Srl"
    ),
    "license": "AGPL-3",
    "website": "https://github.com/OCA/l10n-italy",
    "maintainers": ["eLBati"],
    "depends": [
        "point_of_sale",
        "hr",
        "pos_hr",
        "pos_full_refund",
    ],
    "data": [
        "views/account.xml",
        "views/point_of_sale.xml",
        "views/employee_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "l10n_it_fiscal_epos_print/static/src/css/pos.css",
            "l10n_it_fiscal_epos_print/static/lib/fiscalprint/fiscalprint.js",
            "l10n_it_fiscal_epos_print/static/src/js/epson_epos_print.esm.js",
            "l10n_it_fiscal_epos_print/static/src/js/models.esm.js",
            "l10n_it_fiscal_epos_print/static/src/js/utils/refundUtils.esm.js",
            # Navbar patches
            "l10n_it_fiscal_epos_print/static/src/js/navbar/closing_popup_patch.esm.js",
            # # ChromeWidgets
            "l10n_it_fiscal_epos_print/static/src/js/ChromeWidgets/EpsonEPOSButton.esm.js",
            "l10n_it_fiscal_epos_print/static/src/js/ChromeWidgets/EpsonFP81IIComponent.esm.js",
            "l10n_it_fiscal_epos_print/static/src/js/ChromeWidgets/SetLotteryCodeButton.esm.js",
            "l10n_it_fiscal_epos_print/static/src/js/ChromeWidgets/SetRefundInfoButton.esm.js",
            # # Popups
            "l10n_it_fiscal_epos_print/static/src/js/Popups/LotteryCodePopup.esm.js",
            "l10n_it_fiscal_epos_print/static/src/js/Popups/RefundInfoPopup.esm.js",
            # # Screens
            "l10n_it_fiscal_epos_print/static/src/js/Screens/PaymentScreen/PaymentScreen.esm.js",
            # # Popups
            "l10n_it_fiscal_epos_print/static/src/xml/Popups/LotteryCodePopup.xml",
            "l10n_it_fiscal_epos_print/static/src/xml/Popups/RefundInfoPopup.xml",
            # # Others
            "l10n_it_fiscal_epos_print/static/src/xml/ChromeWidgets/EpsonEPOSButton.xml",
            "l10n_it_fiscal_epos_print/static/src/xml/ChromeWidgets/EpsonFP81IIComponent.xml",
            "l10n_it_fiscal_epos_print/static/src/xml/ChromeWidgets/NavbarExtension.xml",
            "l10n_it_fiscal_epos_print/static/src/xml/ChromeWidgets/SetLotteryCodeButton.xml",
            "l10n_it_fiscal_epos_print/static/src/xml/ChromeWidgets/SetRefundInfoButton.xml",
            "l10n_it_fiscal_epos_print/static/src/xml/ChromeWidgets/ControlButtons.xml",
            "l10n_it_fiscal_epos_print/static/src/js/Screens/TicketScreen/TicketScreen.esm.js",
        ],
    },
    "installable": True,
    "auto_install": False,
}
