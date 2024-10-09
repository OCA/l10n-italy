#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase

from .fatturapa_common import FatturapaCommon


class TestPreview(FatturapaCommon, HttpCase):
    def _get_preview(self, e_invoice):
        preview_action = e_invoice.ftpa_preview()
        preview_url = preview_action["url"]
        response = self.url_open(preview_url)
        return response.content.decode()

    def test_selected_company(self):
        """
        The preview set in the current company
        is different from the preview set in the user's default company;
        the preview in the current company is used."""
        # Arrange
        user = self.env.user
        other_company = self.other_company
        user.company_ids += other_company
        default_user_company = user.company_id
        env = self.env(
            context=dict(
                **self.env.context,
                allowed_company_ids=[
                    other_company.id,
                    default_user_company.id,
                ],
            ),
        )
        current_company = env.company
        current_company.fatturapa_preview_style = "FoglioStileAssoSoftware.xsl"
        default_user_company.fatturapa_preview_style = (
            "Foglio_di_stile_fatturaordinaria_v1.2.2.xsl"
        )
        # pre-condition
        self.assertNotEqual(current_company, default_user_company)
        self.assertNotEqual(
            current_company.fatturapa_preview_style,
            default_user_company.fatturapa_preview_style,
        )

        # Act
        e_invoice = self.create_attachment(
            "preview_selected_company", "IT01234567890_FPR03.xml"
        )
        self.authenticate(user.login, user.login)
        self.opener.cookies["cids"] = ",".join(
            map(str, env.context["allowed_company_ids"])
        )
        preview = self._get_preview(e_invoice)

        # Assert
        expected_preview = env["fatturapa.attachment"].get_fattura_elettronica_preview(
            e_invoice
        )
        self.assertIn(expected_preview, preview)
