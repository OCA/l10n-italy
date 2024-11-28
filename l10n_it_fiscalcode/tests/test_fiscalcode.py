# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from codicefiscale import isvalid

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestFiscalCode(TransactionCase):
    def setUp(self):
        super().setUp()

        self.partner = self.env.ref("base.res_partner_2")
        self.rome_province = self.env.ref("base.state_it_rm")

    def test_fiscalcode_compute(self):
        wizard = (
            self.env["wizard.compute.fc"]
            .with_context(active_id=self.partner.id)
            .create(
                {
                    "fiscalcode_surname": "ROSSI",
                    "fiscalcode_firstname": "MARIO",
                    "birth_date": "1984-06-04",
                    "sex": "M",
                    "birth_city": 10048,
                    "birth_province": self.rome_province.id,
                }
            )
        )
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, "RSSMRA84H04H501X")

    def test_fiscalcode_check(self):
        # Wrong FC length
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Person",
                    "is_company": False,
                    "fiscalcode": "123",
                }
            )
        # Correct FC
        self.env["res.partner"].create(
            {
                "name": "Person",
                "is_company": False,
                "fiscalcode": "RSSMRA84H04H501X",
            }
        )
        # Empty FC
        self.env["res.partner"].create(
            {
                "name": "Person",
            }
        )
        # FC is VAT number
        self.env["res.partner"].create(
            {
                "name": "Person",
                "company_name": "Company",
                "is_company": False,
                "fiscalcode": "123456789",
            }
        )
        # Invalid FC
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Person",
                    "is_company": False,
                    "fiscalcode": "AAAMRA00H04H5010",
                }
            )

    def test_fiscal_code_check_change_to_person(self):
        """
        When a partner changes type from company to person,
        the fiscal code is checked.
        """
        # Arrange
        wrong_person_fiscalcode = "AAAMRA00H04H5010"
        partner = self.env["res.partner"].create(
            {
                "name": "Test partner",
                "company_type": "company",
            }
        )
        partner.fiscalcode = wrong_person_fiscalcode
        # pre-condition
        self.assertFalse(isvalid(partner.fiscalcode))

        # Act
        with self.assertRaises(ValidationError) as ve:
            partner.company_type = "person"
        exc_message = ve.exception.args[0]

        # Assert
        self.assertIn("fiscal code", exc_message)
        self.assertIn("isn't valid", exc_message)

    def test_fiscal_code_check_company_VAT_change_to_person(self):
        """
        When a partner changes type from company to person
        and has a company VAT as fiscalcode,
        the fiscal code is checked.
        """
        # Arrange
        company_vat = "06363391001"
        partner = self.env["res.partner"].create(
            {
                "name": "Test partner",
                "company_type": "company",
            }
        )
        partner.fiscalcode = company_vat
        # pre-condition
        self.assertFalse(isvalid(partner.fiscalcode))

        # Act
        with self.assertRaises(ValidationError) as ve:
            partner.company_type = "person"
        exc_message = ve.exception.args[0]

        # Assert
        self.assertIn("fiscal code", exc_message)
        self.assertIn("16 characters", exc_message)

    def test_uniqueness_disabled(self):
        """If a company has no "Fiscal code is unique",
        partners with the same fiscal code are allowed."""
        # Arrange
        fiscal_code = "RSSMRA84H04H501X"
        company = self.env.company
        # pre-condition
        self.assertFalse(company.l10n_it_fiscalcode_check_uniqueness)

        # Act
        partners = self.env["res.partner"].create(
            [
                {
                    "name": "Test fiscal code uniqueness",
                    "fiscalcode": fiscal_code,
                },
                {
                    "name": "Test duplicated fiscal code",
                    "fiscalcode": fiscal_code,
                },
            ]
        )

        # Assert
        self.assertEqual(
            partners[0].fiscalcode,
            partners[1].fiscalcode,
        )

    def test_uniqueness_constraint(self):
        """If a company has "Fiscal code is unique",
        partners with the same fiscal code are not allowed."""
        # Arrange
        partner_names = [
            "Test same fiscal code",
            "Test duplicated fiscal code",
        ]
        fiscal_code = "RSSMRA84H04H501X"
        company = self.env.company
        company.l10n_it_fiscalcode_check_uniqueness = True
        # pre-condition
        self.assertTrue(company.l10n_it_fiscalcode_check_uniqueness)

        # Act
        with self.assertRaises(ValidationError) as ve:
            self.env["res.partner"].create(
                [
                    {
                        "name": partner_name,
                        "fiscalcode": fiscal_code,
                    }
                    for partner_name in partner_names
                ]
            )
        exc_message = ve.exception.args[0]

        # Assert
        self.assertIn("same fiscal code", exc_message)
        self.assertIn(fiscal_code, exc_message)
        for partner_name in partner_names:
            self.assertIn(partner_name, exc_message)

    def test_company_uniqueness_constraint(self):
        """Uniqueness constraint can be checked for the whole company."""
        # Arrange
        partner_names = [
            "Test same fiscal code",
            "Test duplicated fiscal code",
        ]
        fiscal_code = "RSSMRA84H04H501X"
        company = self.env["res.company"].create(
            {
                "name": "Test company",
                "l10n_it_fiscalcode_check_uniqueness": False,
            }
        )
        self.env["res.partner"].create(
            [
                {
                    "name": partner_name,
                    "fiscalcode": fiscal_code,
                    "company_id": company.id,
                }
                for partner_name in partner_names
            ]
        )
        company.l10n_it_fiscalcode_check_uniqueness = True
        # pre-condition
        self.assertTrue(company.l10n_it_fiscalcode_check_uniqueness)

        # Act
        with self.assertRaises(ValidationError) as ve:
            company.l10n_it_fiscalcode_check_uniqueness_constraint()
        exc_message = ve.exception.args[0]

        # Assert
        self.assertIn("same fiscal code", exc_message)
        self.assertIn(fiscal_code, exc_message)
        for partner_name in partner_names:
            self.assertIn(partner_name, exc_message)
