# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
import logging
import re
import urllib
from datetime import datetime
from io import BytesIO

import requests
from lxml import etree

from odoo import _, exceptions, fields, models

_logger = logging.getLogger(__name__)

DOWNLOAD_BATCH_LIMIT = 10
SENT_FROM_FATTURHELLO_NOTIFICATION_TYPE = "FHSDI"
TIMEOUT = 20


class FatturhelloConnector(models.AbstractModel):
    _name = "l10n_it_fatturapa_fatturhello.connector"
    _description = "Manage communication with Fatturhello API."

    def _get_relative_paths(self):
        """Dictionary mapping all relative paths of managed API endpoints."""
        return {
            ("login", "POST"): "b2beasy/login",
            ("upload", "POST"): "b2beasy/Upload",
            ("sdi_files", "GET"): "b2beasy/Interscambio/%(idazienda)s",
            ("sdi_years", "GET"): "b2beasy/Interscambioanni/%(idazienda)s",
            ("download", "GET"): "b2beasy/Allegati/%(idfile)s",
            ("sdi_status", "GET"): "fatture/StatoSdi",
        }

    def _get_url(self, base_url, path_key, path_values=None):
        """Get the full URL of an API endpoint.

        :param path_key: Identifier of the endpoint
            to be searched in the result of `_get_relative_paths`
        :param path_values: Dictionary of values to be substituted in the path
        """
        if not base_url:
            raise exceptions.UserError(_("Base URL is mandatory."))

        relative_paths = self._get_relative_paths()
        relative_path = relative_paths.get(path_key)
        if relative_path is None:
            raise exceptions.UserError(_("Path %s not found.", path_key))
        elif path_values:
            relative_path = relative_path % path_values

        # Otherwise the last path part
        # is substituted by the relative path.
        # See urllib.parse.urljoin docs.
        if relative_path.startswith("/"):
            relative_path = relative_path[1:]
        if not base_url.endswith("/"):
            base_url += "/"

        return urllib.parse.urljoin(base_url, relative_path)

    def _request(self, *args, **kwargs):
        """Wrapper around `requests.request` to raise proper Odoo exceptions."""
        kwargs = kwargs or dict()
        kwargs.setdefault("timeout", TIMEOUT)
        try:
            # Disable because timeout is actually in kwargs
            # pylint: disable=external-request-timeout
            response = requests.request(*args, **kwargs)
        except requests.exceptions.RequestException as exc:
            _logger.exception("Response creation failed.")
            raise exceptions.UserError(
                _("Response creation failed, see the logs for more details.")
            ) from exc
        else:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as exc:
                _logger.exception("Request failed.")
                raise exceptions.UserError(
                    _("Request failed, see the logs for more details.")
                ) from exc

        response.encoding = "utf-8-sig"

        return response

    def _get_company_data(self, company, companies_data):
        """Extract the data of `company` from `companies_data`.

        :param company: Odoo's `res.company` record
        :param companies_data: Fatturhello's list of dictionaries,
            each representing the data of one company.
        ."""
        company.ensure_one()
        company_vat, company_fc = company.vat, company.fiscalcode
        for company_data in companies_data:
            if company_data["pi"] == company_vat and company_data["cf"] == company_fc:
                break
        else:
            raise exceptions.UserError(
                _(
                    "The company '%(company)s' does not match "
                    "any company in this Fatturhello account.\n"
                    "Please check that VAT '%(vat)s' and FC '%(fc)s' correspond.",
                    company=company.name,
                    vat=company_vat or "",
                    fc=company_fc or "",
                )
            )
        return company_data

    def _login_user_pass(self, base_url, username, password):
        """Call the API to login with user and password."""
        url = self._get_url(base_url, ("login", "POST"))

        if not username:
            raise exceptions.UserError(_("Username is mandatory."))
        if not password:
            raise exceptions.UserError(_("Password is mandatory."))

        response = self._request(
            "POST",
            url,
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "createtoken": True,
                }
            ),
        )

        result = response.json()
        if not result.get("success"):
            raise exceptions.UserError(
                _(
                    "Login with user and password failed.\nResponse is:\n%s",
                    json.dumps(result, indent=4),
                )
            )

        return result

    def get_secrets(self, url, company, username, password):
        """Get secrets used to authenticate API calls."""
        login_result = self._login_user_pass(url, username, password)
        company_data = self._get_company_data(company, login_result["aziende"])
        return {
            "authtoken": login_result["authtoken"],
            "company_identifier": company_data["codice"],
        }

    def _login_token(self, base_url, authtoken):
        """Call the API to login with authtoken."""
        url = self._get_url(base_url, ("login", "POST"))

        if not authtoken:
            raise exceptions.UserError(_("Token is mandatory."))

        response = self._request(
            "POST",
            url,
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "token": authtoken,
                }
            ),
        )

        result = response.json()
        if not result.get("success"):
            raise exceptions.UserError(
                _(
                    "Login with token failed.\nResponse is:\n%s",
                    json.dumps(result, indent=4),
                )
            )

        return result

    def get_session_token(self, url, authtoken):
        """Get session token for single API call authentication."""
        login_result = self._login_token(url, authtoken)
        return login_result["token"]

    def _upload_post(
        self,
        base_url,
        session_token,
        company_identifier,
        file_name,
        file_content,
    ):
        """Upload a file for a company.

        :param company_identifier: The identifier of the Company
            where the file will be uploaded.
        """
        url = self._get_url(base_url, ("upload", "POST"))

        response = self._request(
            "POST",
            url,
            headers={
                "Authorization": f"Bearer {session_token}",
            },
            data={
                "idupload": company_identifier,
            },
            files={
                "file": (file_name, BytesIO(file_content)),
            },
        )

        result = response.json()
        if not result.get("success"):
            raise exceptions.UserError(
                _(
                    "Upload failed.\nResponse is:\n%s",
                    json.dumps(result, indent=4),
                )
            )

        return result

    def _prepare_e_invoice_upload_values(self, upload_result):
        """Values to be updated on an Odoo `ir.attachment` after a successful upload."""
        return {
            "fatturhello_protocol": upload_result["files"][0]["protocollo"],
            "state": "sent_to_fatturhello",
        }

    def upload_e_invoice(self, base_url, session_token, company_identifier, e_invoice):
        """Upload an e-invoice for a company.

        :param company_identifier: The identifier of the Company
            where the file will be uploaded.
        """
        e_invoice.ensure_one()
        upload_result = self._upload_post(
            base_url,
            session_token,
            company_identifier,
            e_invoice.name,
            e_invoice.raw,
        )
        e_invoice.update(self._prepare_e_invoice_upload_values(upload_result))
        return True

    def _get_sdi_files_list(
        self,
        base_url,
        session_token,
        company_identifier,
        offset=None,
        limit=None,
        order=None,
        year=None,
    ):
        """Get the list of SdI files for a company.

        :param company_identifier: The identifier of the Company in Fatturhello
            owning the SdI files.
        """
        url = self._get_url(
            base_url,
            ("sdi_files", "GET"),
            path_values=dict(idazienda=company_identifier),
        )

        response = self._request(
            "GET",
            url,
            headers={
                "Authorization": f"Bearer {session_token}",
            },
            params={
                "offset": offset,
                "limit": limit,
                "order": order,
                "anno": year,
            },
        )

        result = response.json()
        if not result.get("success"):
            raise exceptions.UserError(
                _(
                    "List Download failed.\nResponse is:\n%s",
                    json.dumps(result, indent=4),
                )
            )

        return result

    def _filter_e_bills(self, files_data):
        """Extract from `files_data` only the E-Bills to be imported."""
        return [
            row
            for row in files_data
            if row["statotesto"] == "ricevuta" and row["statopa"] == "3"
        ]

    def _get_sdi_years(
        self,
        base_url,
        session_token,
        company_identifier,
    ):
        """Get the list of years that SdI has been used for a company.

        :param company_identifier: The identifier of the Company in Fatturhello.
        """
        url = self._get_url(
            base_url,
            ("sdi_years", "GET"),
            path_values=dict(idazienda=company_identifier),
        )

        response = self._request(
            "GET",
            url,
            headers={
                "Authorization": f"Bearer {session_token}",
            },
        )

        return response.json()

    def get_e_bills_list(
        self,
        base_url,
        session_token,
        company_identifier,
        last_downloaded_e_bill_identifer=None,
    ):
        """Get the list of identifiers of E-Bills to be downloaded.

        E-Bills are ordered from the oldest to the latest one.

        :param company_identifier: The identifier of the Company in Fatturhello
            owning the E-Bills.
        :param last_downloaded_e_bill_identifer: Identifier of the downloaded E-Bill.
            If provided, only the identifiers of the E-Bills
            more recent than the specified one will be dowloaded.
        """
        e_bills_years = self._get_sdi_years(
            base_url,
            session_token,
            company_identifier,
        )
        # Order years from most recent
        e_bills_years = sorted(e_bills_years, reverse=True)

        e_bills_identifiers = []
        found_last_downloaded_e_bill = False
        for e_bills_year in e_bills_years:
            # Download all the E-Bills of the year
            # in batches, from the latest one,
            # until we find the last we already downloaded (if any)
            if found_last_downloaded_e_bill:
                break

            offset = 0
            while files_data := self._get_sdi_files_list(
                base_url,
                session_token,
                company_identifier,
                offset=offset,
                limit=DOWNLOAD_BATCH_LIMIT,
                order="desc",
                year=e_bills_year,
            ).get("rows"):
                if found_last_downloaded_e_bill:
                    break
                offset += len(files_data) + 1

                year_e_bills_data = self._filter_e_bills(files_data)
                year_e_bills_identifiers = [
                    e_bill_data["idallegatoxml"] for e_bill_data in year_e_bills_data
                ]

                for e_bill_identifier in year_e_bills_identifiers:
                    if e_bill_identifier == last_downloaded_e_bill_identifer:
                        found_last_downloaded_e_bill = True
                        break
                    e_bills_identifiers.append(e_bill_identifier)

        # We have downloaded the E-Bills from the latest to the oldest
        # so that we can stop when the `last_downloaded` is found,
        # but we should process them from the oldest to the latest.
        e_bills_identifiers.reverse()
        return e_bills_identifiers

    def download_file(
        self,
        base_url,
        session_token,
        company_identifier,
        file_identifier,
    ):
        """Download a file from a company.

        :param company_identifier: The identifier of the Company in Fatturhello
            owning the file.
        :param file_identifier: The identifier of the file to be downloaded.
        """
        url = self._get_url(
            base_url,
            ("download", "GET"),
            path_values=dict(idfile=file_identifier),
        )

        response = self._request(
            "GET",
            url,
            headers={
                "Authorization": f"Bearer {session_token}",
            },
        )

        content = response.content
        if not content:
            raise exceptions.UserError(
                _(
                    "Download failed.\nResponse is:\n%s",
                    content.decode(),
                )
            )
        name = re.findall("filename=(.+)", response.headers["content-disposition"])[0]
        return name, content

    def _get_sdi_file_status(
        self,
        base_url,
        session_token,
        company_identifier,
        file_identifier,
    ):
        """Get the SdI status of a SdI file.

        :param company_identifier: The identifier of the Company in Fatturhello
            owning the SdI file.
        """
        url = self._get_url(base_url, ("sdi_status", "GET"))

        response = self._request(
            "GET",
            url,
            headers={
                "Authorization": f"Bearer {session_token}",
            },
            params={
                "identificativo": file_identifier,
            },
        )

        result = response.json()
        if not result.get("success"):
            raise exceptions.UserError(
                _(
                    "Status check failed.\nResponse is:\n%s",
                    json.dumps(result, indent=4),
                )
            )

        return result

    def _prepare_sdi_notification_type(self, fatturhello_status):
        # Determine the notification type
        status_str = fatturhello_status["Esito"]
        if status_str == "Inoltrata al Sdi":
            # This is Fatturhello confirming
            # that the invoice has been sent to SdI:
            # it is not a notification from SdI
            notification_type = SENT_FROM_FATTURHELLO_NOTIFICATION_TYPE
        elif status_str.startswith("Fattura ricevuta"):
            notification_type = "RC"
        else:
            # Consider anything else as a "Notifica di Scarto".
            # This will be refined
            # when we will know all possible Fatturhello statuses.
            notification_type = "NS"
            _logger.info(
                f"Fatturhello status considered as a 'Notifica di Scarto': {status_str}"
            )
        return notification_type

    def _prepare_sdi_notification(
        self,
        file_name,
        fatturhello_status_index,
        fatturhello_status,
    ):
        """Transform a status from Fatturhello in SdI Messaggi format."""
        notification_type = self._prepare_sdi_notification_type(fatturhello_status)

        # Build the notification
        sdi_notification_name = (
            "_".join(
                (
                    file_name.split(".")[0],
                    notification_type,
                    str(fatturhello_status_index),
                )
            )
            + ".xml"
        )

        status_date = fields.Datetime.to_string(fatturhello_status["Data"])
        status_str = fatturhello_status["Esito"]
        if notification_type == SENT_FROM_FATTURHELLO_NOTIFICATION_TYPE:
            # Build a dummy XML to follow the usual flow
            response_content_root = etree.Element("ReceivedFromFatturhello")
            etree.SubElement(response_content_root, "Descrizione").text = status_str
        elif notification_type == "RC":
            response_content_root = etree.Element("RicevutaConsegna")
            etree.SubElement(
                response_content_root, "DataOraConsegna"
            ).text = status_date
        elif notification_type == "NS":
            response_content_root = etree.Element("NotificaScarto")
            errors_list = etree.SubElement(response_content_root, "ListaErrori")
            etree.SubElement(errors_list, "Descrizione").text = status_str
        else:
            raise exceptions.UserError(
                _(
                    "Notification type %(notification_type)s not managed",
                    notification_type=notification_type,
                )
            )

        etree.SubElement(response_content_root, "NomeFile").text = file_name
        etree.SubElement(response_content_root, "IdentificativoSdI")
        etree.SubElement(response_content_root, "DataOraRicezione").text = status_date
        etree.SubElement(response_content_root, "MessageId")
        return sdi_notification_name, etree.tostring(response_content_root)

    def get_e_invoice_status_list(
        self,
        base_url,
        session_token,
        company_identifier,
        file_identifier,
    ):
        """Get all the status updates of `file_identifier`.

        The statuses are ordered from oldest to latest.
        """
        e_bill_status_list = self._get_sdi_file_status(
            base_url,
            session_token,
            company_identifier,
            file_identifier,
        ).get("rows")

        for e_bill_status in e_bill_status_list:
            e_bill_status["Data"] = datetime.strptime(
                e_bill_status["Data"],
                "%d/%m/%Y %H:%M:%S",
            )

        e_bill_status_list.sort(
            key=lambda status: status["Data"],
        )
        return e_bill_status_list
