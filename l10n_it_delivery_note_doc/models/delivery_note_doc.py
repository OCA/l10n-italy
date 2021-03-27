# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime

from odoo import fields, models


class DeliveryNoteDoc(models.Model):
    _name = "delivery.note.doc"
    _description = "Delivery Note Document - without inventory app"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "ddt_number, name, id"

    def _default_type(self):
        return self.env["stock.delivery.note.type"].search(
            [("code", "=", "outgoing")], limit=1
        )

    def _default_company(self):
        return self.env.company

    active = fields.Boolean(default=True)
    name = fields.Char(
        string="Description",
        required=True,
        tracking=True,
    )
    ddt_number = fields.Char(
        string="DdT Number",
        copy=False,
        tracking=True,
    )
    date_ddt = fields.Date(
        string="Date", copy=False, tracking=True, default=fields.Date.context_today
    )
    date_transport_ddt = fields.Datetime(string="Transport date", tracking=True)
    packages = fields.Integer(string="Packages")
    gross_weight = fields.Float(string="Gross Weight")
    net_weight = fields.Float(string="Net Weight")
    ddt_notes = fields.Html(string="Delivery Note Notes", tracking=True)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default="draft",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Destination",
        required=True,
        index=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    line_ids = fields.One2many(
        "delivery.note.doc.line", "delivery_note_doc_id", string="Lines"
    )
    type_id = fields.Many2one(
        "stock.delivery.note.type",
        string="Type",
        default=_default_type,
        required=True,
        index=True,
    )
    transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
    )
    goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance",
        string="Appearance of goods",
    )
    transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason",
        string="Reason of transport",
    )
    transport_method_id = fields.Many2one(
        "stock.picking.transport.method",
        string="Method of transport",
    )
    company_id = fields.Many2one("res.company", required=True, default=_default_company)

    def get_dn_number(self):
        for dn in self:
            if not dn.ddt_number and dn.type_id:
                sequence = dn.type_id.sequence_id
                dn.ddt_number = sequence.next_by_id()
            return self.env.ref(
                "l10n_it_delivery_note_doc.action_report_delivery_note_doc"
            ).report_action(self)
        return True

    def update_date_transport_ddt(self):
        self.date_transport_ddt = datetime.datetime.now()

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_draft(self):
        self.write({"state": "draft"})


class DeliveryNoteDocLine(models.Model):
    _name = "delivery.note.doc.line"
    _description = "Delivery Note Document line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence asc"

    name = fields.Text(string="Description", required=True, tracking=True)
    quantity = fields.Float(
        string="Quantity",
        digits="Product Unit of Measure",
        default=1.0,
        tracking=True,
    )
    sequence = fields.Integer(string="Sequence", required=True, default=10, index=True)
    delivery_note_doc_id = fields.Many2one(
        "delivery.note.doc",
        string="Delivery Note line",
        required=True,
        ondelete="cascade",
    )
