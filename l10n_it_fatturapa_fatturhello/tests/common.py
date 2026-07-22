# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from unittest import mock

from requests import Response, codes

from odoo import tests
from odoo.modules.module import get_resource_path
from odoo.tools import file_open

MODULE = "l10n_it_fatturapa_fatturhello"
REQUEST_PATH = f"odoo.addons.{MODULE}.models.connector.requests.request"


class Common(tests.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.channel = cls.env.ref(f"{MODULE}.sdi_channel_fatturhello")
        cls.channel.sudo().company_id = cls.env.company
        cls.env.company.update(
            {
                "fiscalcode": "06363391001",
                "vat": "06363391001",
                "sdi_channel_id": cls.channel.id,
            }
        )

    def _get_records_from_action(self, action, values=None):
        """Get the records opened by `action`.

        If `action` does not return any record, one is created using `values`.
        """
        context = action.get("context", dict())
        record_model = self.env[action["res_model"]].with_context(**context)
        if record_id := action.get("res_id"):
            record = record_model.browse(record_id)
        else:
            record = record_model.create(values or dict())
        return record

    def _get_file_content(self, name):
        """Get the binary content of the file `name` in test responses."""
        path = get_resource_path(MODULE, "tests", "responses", name)
        with file_open(path, mode="rb") as f:
            return f.read()

    def _get_response(self, name, headers_name=None):
        """Get a response for the file `name` in test responses."""
        response = Response()
        response.status_code = codes.ok
        response._content = self._get_file_content(name)
        if headers_name:
            response.headers = json.loads(self._get_file_content(headers_name).decode())
        return response

    def _get_login_wizard(self, channel, values=None):
        """Return the login wizard for `channel`, populated with `values`.

        If `values` is omitted, default values will be used.
        """
        if values is None:
            values = {
                "username": "username",
                "password": "password",
            }
        action = channel.fatturhello_action_login()
        login_wizard = self._get_records_from_action(action, values=values)
        return login_wizard

    def _login(self, channel, values=None):
        wizard = self._get_login_wizard(channel)
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.return_value = self._get_response("login_success")
            return wizard.confirm()
