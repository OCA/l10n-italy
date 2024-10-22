from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "partner_name": u"HÎ"
        })
        self.partner = self.env["res.partner"].create({"name": __file__})

    def test_transfered_values(self):
        """Field gets transfered when creating partner."""
        company_fiscal_code = "12345670017"
        self.lead.fiscalcode = company_fiscal_code
        partner_ids = self.lead.handle_partner_assignation()
        for lead_id in partner_ids:
            self.env["crm.lead"].browse(lead_id).partner_id = partner_ids[lead_id]
        partner = self.lead.partner_id
        self.assertEqual(partner.fiscalcode, company_fiscal_code)
        self.assertTrue(partner.is_company)

    def test_onchange_partner_id(self):
        """Lead gets fiscalcode from partner when linked to it."""
        person_fiscal_code = "AAABBB99A11A999A"
        self.partner.fiscalcode = person_fiscal_code
        result = self.lead._onchange_partner_id_values(self.lead.partner_id.id)
        self.assertNotIn("fiscalcode", result)
        self.lead.partner_id = self.partner
        result = self.lead._onchange_partner_id_values(self.lead.partner_id.id)
        self.assertEqual(result["fiscalcode"], person_fiscal_code)
        partner = self.lead.partner_id
        self.assertFalse(partner.is_company)
