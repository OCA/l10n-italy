# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from os.path import join
from unittest import mock

from requests import Response, codes

from odoo.tools import file_open, file_path

from odoo.addons.l10n_it_edi.tests.common import TestItEdi

MODULE = "l10n_it_edi_fatturhello"
REQUEST_PATH = f"odoo.addons.{MODULE}.models.connector.requests.request"


class Common(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company.update(
            {
                "fatturhello_is_used": True,
                "l10n_it_codice_fiscale": "06363391001",
                "vat": "06363391001",
            }
        )
        cls.cron = cls.env.ref("l10n_it_edi.ir_cron_l10n_it_edi_download_and_update")
        cls.cron.user_id.company_ids |= cls.company
        cls.module = MODULE

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
        path = file_path(join(MODULE, "tests", "responses", name))
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

    def _get_login_wizard(self, company, values=None):
        """Return the login wizard for `company`, populated with `values`.

        If `values` is omitted, default values will be used.
        """
        if values is None:
            values = {
                "username": "username",
                "password": "password",
            }
        action = (
            self.env["res.config.settings"]
            .with_company(company)
            .fatturhello_action_login()
        )
        login_wizard = self._get_records_from_action(action, values=values)
        return login_wizard

    def _login(self, company, values=None):
        wizard = self._get_login_wizard(company)
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.return_value = self._get_response("login_success")
            return wizard.confirm()
