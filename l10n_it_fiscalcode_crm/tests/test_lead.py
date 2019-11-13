from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    def setUp(self):
        super(LeadCase, self).setUp()
        self.lead = self.env["crm.lead"].create({
            "name": __file__,
            "partner_name": u"HÎ"
        })
        self.partner = self.env["res.partner"].create({"name": __file__})
        self.test_field = "AAABBB99A11A999A"

    def test_transfered_values(self):
        """Field gets transfered when creating partner."""
        self.lead.fiscalcode = self.test_field
        partner_ids = self.lead.handle_partner_assignation()
        for lead_id in partner_ids:
            self.env["crm.lead"].browse(lead_id).partner_id = partner_ids[lead_id]
        self.assertEqual(self.lead.partner_id.fiscalcode, self.test_field)

    def test_onchange_partner_id(self):
        """Lead gets fiscalcode from partner when linked to it."""
        self.partner.fiscalcode = self.test_field
        result = self.lead._onchange_partner_id_values(self.lead.partner_id.id)
        self.assertNotIn("fiscalcode", result)
        self.lead.partner_id = self.partner
        result = self.lead._onchange_partner_id_values(self.lead.partner_id.id)
        self.assertEqual(result["fiscalcode"], self.test_field)
