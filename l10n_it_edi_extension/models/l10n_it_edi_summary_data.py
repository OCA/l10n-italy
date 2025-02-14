# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EInvoiceSummaryData(models.Model):
    _name = "l10n_it_edi.summary_data"
    _description = "E-invoice summary data"

    tax_rate = fields.Float()
    non_taxable_nature = fields.Selection(
        selection=[
            ("N1", "[N1] Escluse ex art. 15"),
            ("N2", "[N2] Non soggette"),
            (
                "N2.1",
                "[N2.1] Non soggette ad IVA ai sensi degli artt. Da 7 a 7-septies del DPR 633/72",  # noqa: E501
            ),
            ("N2.2", "[N2.2] Non soggette - altri casi"),
            ("N3", "[N3] Non imponibili"),
            ("N3.1", "[N3.1] Non imponibili - esportazioni"),
            ("N3.2", "[N3.2] Non imponibili - cessioni intracomunitarie"),
            ("N3.3", "[N3.3] Non imponibili - cessioni verso San Marino"),
            (
                "N3.4",
                "[N3.4] Non imponibili - operazioni assimilate alle cessioni all'esportazione",  # noqa: E501
            ),
            ("N3.5", "[N3.5] Non imponibili - a seguito di dichiarazioni d'intento"),
            (
                "N3.6",
                "[N3.6] Non imponibili - altre operazioni che non concorrono alla formazione del plafond",  # noqa: E501
            ),
            ("N4", "[N4] Esenti"),
            ("N5", "[N5] Regime del margine / IVA non esposta in fattura"),
            (
                "N6",
                "[N6] Inversione contabile (per le operazioni in reverse charge ovvero nei casi di autofatturazione per acquisti extra UE di servizi ovvero per importazioni di beni nei soli casi previsti)",  # noqa: E501
            ),
            (
                "N6.1",
                "[N6.1] Inversione contabile - cessione di rottami e altri materiali di recupero",  # noqa: E501
            ),
            ("N6.2", "[N6.2] Inversione contabile - cessione di oro e argento puro"),
            ("N6.3", "[N6.3] Inversione contabile - subappalto nel settore edile"),
            ("N6.4", "[N6.4] Inversione contabile - cessione di fabbricati"),
            ("N6.5", "[N6.5] Inversione contabile - cessione di telefoni cellulari"),
            ("N6.6", "[N6.6] Inversione contabile - cessione di prodotti elettronici"),
            (
                "N6.7",
                "[N6.7] Inversione contabile - prestazioni comparto edile esettori connessi",  # noqa: E501
            ),
            ("N6.8", "[N6.8] Inversione contabile - operazioni settore energetico"),
            ("N6.9", "[N6.9] Inversione contabile - altri casi"),
            (
                "N7",
                "[N7] IVA assolta in altro stato UE (prestazione di servizi di telecomunicazioni, tele-radiodiffusione ed elettronici ex art. 7-octies, comma 1 lett. a, b, art. 74-sexies DPR 633/72)",  # noqa: E501
            ),
        ],
        string="Non taxable nature",
    )
    incidental_charges = fields.Float()
    rounding = fields.Float()
    amount_untaxed = fields.Float()
    amount_tax = fields.Float()
    payability = fields.Selection(
        [
            ("I", "Immediate payability"),
            ("D", "Deferred payability"),
            ("S", "Split payment"),
        ],
        string="VAT payability",
    )
    law_reference = fields.Char(string="Law reference", size=128)
    invoice_id = fields.Many2one(
        "account.move", string="Related Invoice", ondelete="cascade", index=True
    )
