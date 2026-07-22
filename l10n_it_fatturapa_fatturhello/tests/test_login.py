# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo import exceptions

from odoo.addons.l10n_it_fatturapa_fatturhello.tests.common import REQUEST_PATH, Common


class TestLogin(Common):
    def test_success(self):
        """A successful login populates the authtoken and the identifier."""
        # Arrange
        channel = self.channel
        wizard = self._get_login_wizard(channel)
        # pre-condition
        self.assertFalse(channel.fatturhello_login_authtoken)

        # Act
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.return_value = self._get_response("login_success")
            wizard.confirm()

        # Assert
        self.assertTrue(channel.fatturhello_login_authtoken)
        self.assertEqual(
            channel.company_id.fatturhello_identifier,
            "IKZFSKX6645VVG595QG7",
        )

    def test_fail(self):
        """A failed login raises an exception."""
        # Arrange
        channel = self.channel
        wizard = self._get_login_wizard(channel)
        # pre-condition
        self.assertFalse(channel.fatturhello_login_authtoken)

        # Act
        with (
            mock.patch(REQUEST_PATH) as mock_request,
            self.assertRaises(exceptions.UserError) as exc,
        ):
            mock_request.return_value = self._get_response("login_fail")
            wizard.confirm()
        exc_message = exc.exception.args[0]

        # Assert
        self.assertIn("Login with user and password failed", exc_message)
        self.assertFalse(channel.fatturhello_login_authtoken)
