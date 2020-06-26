# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AssetAccountingInfo(models.Model):
    """
    This model is necessary to manage info about the relationships between
    assets and accounting records. We could have used `Many2many` fields to
    create tables between assets, depreciation lines, invoices, invoice
    lines, account moves and account move lines; but we need a custom
    management, a bit more complex than the one provided by the standard
    `Many2many` field.

    NB: a few methods could have been decorated with @api.constrains or
    @api.depends, but that would have limited them by being triggered only
    upon some fields' changes, and would have made it very hard to be
    customizable by third party modules.
    Therefore, it has been chosen to define them as simple Python methods which
    are called right after ``create`` and ``write`` methods if some fields
    (which can be retrieved by method ``get_main_fields``) are found within
    ``vals`` dictionary.
    """

    _name = 'asset.accounting.info'
    _description = "Asset Accounting Relations"
    _table = 'asset_accounting_info'

    asset_id = fields.Many2one(
        'asset.asset',
        ondelete='set null',
        string="Asset"
    )

    company_id = fields.Many2one(
        'res.company',
        readonly=True,
        string="Company",
    )

    dep_line_id = fields.Many2one(
        'asset.depreciation.line',
        ondelete='set null',
        string="Depreciation Line"
    )

    invoice_id = fields.Many2one(
        'account.invoice',
        ondelete='set null',
        string="Invoice"
    )

    invoice_line_id = fields.Many2one(
        'account.invoice.line',
        ondelete='set null',
        string="Invoice Line"
    )

    move_id = fields.Many2one(
        'account.move',
        ondelete='set null',
        string="Move"
    )

    move_line_id = fields.Many2one(
        'account.move.line',
        ondelete='set null',
        string="Move Line"
    )

    relation_type = fields.Selection(
        [('create', "Asset Creation"),
         ('update', "Asset Update"),
         ('partial_dismiss', "Asset Partial Dismissal"),
         ('dismiss', "Asset Dismissal")],
        required=True,
        string="Relation Type"
    )

    @api.model
    def create(self, vals):
        info = super().create(vals)
        info.check_and_normalize()
        return info

    @api.multi
    def write(self, vals):
        fnames = self.get_main_fields()

        # ``load=''`` avoids returning tuple ``(rec.id, rec.name)`` for M2o
        # fields and simply returns ``rec.id``
        old_info_vals = {d['id']: d for d in self.read(fnames, load='')}
        res = super().write(vals)
        new_info_vals = {d['id']: d for d in self.read(fnames, load='')}

        # old/new_info_vals dicts both have the same keys
        to_check_ids = []
        for aa_info_id, old_vals in old_info_vals.items():
            new_vals = new_info_vals[aa_info_id]
            common_fs = set(new_vals).intersection(old_vals)
            extra_fs = set(new_vals).union(old_vals) - common_fs
            if extra_fs or any(new_vals[k] != old_vals[k] for k in common_fs):
                to_check_ids.append(aa_info_id)

        if to_check_ids:
            self.browse(to_check_ids).check_and_normalize()

        return res

    @api.multi
    def name_get(self):
        return [(aa_info.id, aa_info.make_name()) for aa_info in self]

    @api.model
    def cron_vacuum_table(self):
        """ A cron that deletes obsolete records """
        aa_info = self.get_records_to_delete_by_cron()
        aa_info.unlink()

    @api.model
    def get_main_fields(self):
        return [
            'asset_id', 'dep_line_id',
            'invoice_id', 'invoice_line_id',
            'move_id', 'move_line_id'
        ]

    @api.multi
    def button_unlink(self):
        """ Button action: deletes a.a.info """
        self.unlink()

    def check_and_normalize(self):
        for info in self:
            info.check_coherence()
            info.normalize_info()

    def check_coherence(self):
        """ Checks info coherence """
        self.check_company_coherence()
        self.check_data_coherence()

    def check_company_coherence(self):
        """ Checks companies """
        self.ensure_one()
        companies = self.get_all_companies()
        if len(companies) > 1:
            raise ValidationError(
                _("Incoherent company data.")
            )

    def check_data_coherence(self):
        self.ensure_one()

        # If dep_line_id and asset_id are set, check whether the depreciation
        # line belongs to the given asset
        if self.asset_id and self.dep_line_id \
                and self.asset_id != self.dep_line_id.depreciation_id.asset_id:
            raise ValidationError(
                _("Incoherent asset data.")
            )

        # If invoice_line_id and invoice_id are set, check whether the invoice
        # line belongs to the given invoice
        if self.invoice_id and self.invoice_line_id \
                and self.invoice_id != self.invoice_line_id.invoice_id:
            raise ValidationError(
                _("Incoherent invoice data.")
            )

        # If move_line_id and move_id are set, check whether the move line
        # belongs to the given move
        if self.move_id and self.move_line_id \
                and self.move_id != self.move_line_id.move_id:
            raise ValidationError(
                _("Incoherent move data.")
            )

    def get_all_companies(self):
        company_ids = []

        fnames = self.get_main_fields()
        for aa_info in self:
            for fname in fnames:
                # Using sudo() to avoid security problems during this check
                rec = aa_info.sudo()[fname]
                if rec and rec.company_id.id not in company_ids:
                    company_ids.append(rec.company_id.id)

        return self.env['res.company'].browse(company_ids)

    def get_normalized_info_vals(self):
        self.ensure_one()
        vals = {}

        # Set asset as dep line's asset if dep line is set
        if not self.asset_id and self.dep_line_id:
            vals['asset_id'] = self.dep_line_id.asset_id.id

        # Set invoice_id as invoice line's invoice if invoice line is set
        if not self.invoice_id and self.invoice_line_id:
            vals['invoice_id'] = self.invoice_line_id.invoice_id.id

        # Set move_id as move line's move if move line is set
        if not self.move_id and self.move_line_id:
            vals['move_id'] = self.move_line_id.move_id.id

        # Set company
        companies = self.get_all_companies()
        if len(companies) == 1:
            vals['company_id'] = companies.id
        else:
            vals['company_id'] = False

        return vals

    def get_records_to_delete_by_cron(self):
        """
        Returns every a.a.info that fits the condition:
            (no asset AND no depreciation line)
            OR
            (no invoice AND no invoice line AND no move AND no move line)
        """
        return self.search([
            '|',
            '&',
            ('asset_id', '=', False),
            ('dep_line_id', '=', False),
            '&',
            '&',
            '&',
            ('invoice_id', '=', False),
            ('invoice_line_id', '=', False),
            ('move_id', '=', False),
            ('move_line_id', '=', False),
        ])

    def make_name(self):
        self.ensure_one()
        if self.asset_id:
            name = self.asset_id.make_name()
        else:
            name = _("Unknown Asset")
        relation_name = dict(self._fields['relation_type'].selection) \
            .get(self.relation_type)
        if relation_name:
            name += " - " + relation_name
        return name.strip()

    def normalize_info(self):
        """ Normalize asset accounting info if needed """
        self.ensure_one()
        vals = self.get_normalized_info_vals()
        if vals:
            self.write(vals)
