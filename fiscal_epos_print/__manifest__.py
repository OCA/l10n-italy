# Leonardo Donelli - Creativi Quadrati
# © 2016 Alessio Gerace - Agile Business Group
# © 2018-2020 Lorenzo Battistini
# © 2019-2020 Roberto Fichera - Level Prime Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Driver per stampanti fiscali compatibili ePOS-Print XML",
    "version": "14.0.1.0.1",
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
        # TODO is this necessary?
        # 'pos_order_mgmt'
    ],
    "data": [
        "views/account.xml",
        "views/point_of_sale.xml",
        "views/assets.xml",
    ],
    "qweb": [
        # Popups
        "static/src/xml/Popups/RefundInfoPopup.xml",
        # Others
        "static/src/xml/Chrome.xml",
        "static/src/xml/ChromeWidgets/EpsonEPOSButton.xml",
        "static/src/xml/ChromeWidgets/EpsonFP81IIComponent.xml",
        "static/src/xml/ChromeWidgets/SetLotteryCodeButton.xml",
        "static/src/xml/ChromeWidgets/SetRefundInfoButton.xml",
        # TODO To be converted with new components system
        # 'static/src/xml/pos.xml',
        # 'static/src/xml/lottery.xml',
    ],
    "installable": True,
    "auto_install": False,
}
