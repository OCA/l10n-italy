# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from http import HTTPStatus
from urllib.parse import urlparse

from odoo import http, tests

from ..controllers.main import CustomerPortal


class TestMyAccount(tests.HttpCase):
    def _prepare_form_data(self, user):
        """Form data ready for POST in /my/account.

        For simplicity, user will authenticate with login as password.
        """
        self.authenticate(user.login, user.login)

        controller = CustomerPortal()
        partner_data = user.partner_id.read(controller._get_mandatory_fields())[0]
        del partner_data["id"]

        form_data = partner_data
        form_data["csrf_token"] = http.Request.csrf_token(self)
        return form_data

    def test_wrong_fiscalcode(self):
        """An error message is displayed when fiscal code is wrong."""
        # Arrange
        demo_user = self.env.ref("base.user_demo")
        form_data = self._prepare_form_data(demo_user)
        form_data.update(
            {
                # Check fiscal code of a person
                "company_name": "",
                "l10n_it_codice_fiscale": "12345670546",
            }
        )

        # Act
        response = self.url_open("/my/account", data=form_data)

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(urlparse(response.url).path, "/my/account")
        self.assertIn(b"must have 16 characters", response.content)

    def test_correct_fiscalcode(self):
        """A correct fiscal code redirects to home."""
        # Arrange
        demo_user = self.env.ref("base.user_demo")
        form_data = self._prepare_form_data(demo_user)
        form_data.update(
            {
                # Check fiscal code of a person
                "company_name": "",
                "l10n_it_codice_fiscale": "RSSMRA84H04H501X",
            }
        )

        # Act
        response = self.url_open("/my/account", data=form_data)

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(urlparse(response.url).path, "/my/home")
