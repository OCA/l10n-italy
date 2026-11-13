# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestQuadroVpInterests(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.env.company
        journal = cls.env["account.journal"].search(
            [("type", "=", "general"), ("company_id", "=", company.id)], limit=1
        )
        account = cls.env["account.account"].search(
            [("company_id", "=", company.id)], limit=1
        )
        cls.statement = cls.env["account.vat.period.end.statement"].create(
            {
                "journal_id": journal.id,
                "date": "2022-09-30",
                "interests_debit_vat_account_id": account.id,
                "interests_debit_vat_amount": 2.44,
            }
        )
        cls.comunicazione = cls.env["comunicazione.liquidazione"].create(
            {
                "year": 2022,
                "taxpayer_vat": "11876260784",
                "taxpayer_fiscalcode": "FNCPLC19D01I168X",
                "declarant_fiscalcode": "FNCPLC19D01I168X",
                "codice_carica_id": cls.env.ref("l10n_it_appointment_code.1").id,
            }
        )

    def _compute_quadro(self, quarter):
        quadro = self.env["comunicazione.liquidazione.vp"].create(
            {
                "comunicazione_id": self.comunicazione.id,
                "period_type": "quarter",
                "quarter": quarter,
                "liquidazioni_ids": [(6, 0, self.statement.ids)],
            }
        )
        quadro.compute_from_liquidazioni()
        return quadro

    def test_quarter_interests(self):
        """Interests of a quarterly statement go in VP12."""
        self.assertEqual(self._compute_quadro(3).interessi_dovuti, 2.44)

    def test_fifth_quarter_no_interests(self):
        """VP12 is left empty in the 5th quarter (annual adjustment)."""
        self.assertEqual(self._compute_quadro(5).interessi_dovuti, 0.0)
