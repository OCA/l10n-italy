# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import logging
import xlrd

from collections import namedtuple
from datetime import datetime, date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


# Map every keyword to useful info
Header = namedtuple(
    'Header',
    ['name',            # Defines column name
     'col',             # Defines in which column we can find related info
     'model',           # Defines model to look up to
     'field',           # Defines in which field we'll write this info
     'apply_on',        # Defines which obj this data will apply to (may be
                        #   different from `model`)
     'required',        # Defines whether the field is required in Odoo
     'tmpl_default',    # Defines the default value when creating templates
     'type']            # Defines the type of the value we expect (and how
                        #   to manage it)
)
HEADERS = (
    Header(
        name=_('Asset Name'),
        col=0,
        model='asset.asset',
        field='name',
        apply_on='asset.asset',
        required=True,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Asset Category Import Code'),
        col=1,
        model='asset.category',
        field='import_code',
        apply_on='asset.asset',
        required=True,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Asset Code'),
        col=2,
        model='asset.asset',
        field='code',
        apply_on='asset.asset',
        required=False,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Asset Import Code'),
        col=3,
        model='asset.asset',
        field='import_code',
        apply_on='asset.asset',
        required=True,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Used'),
        col=4,
        model='asset.asset',
        field='used',
        apply_on='asset.asset',
        required=False,
        tmpl_default='',
        type='bool'
    ),
    Header(
        name=_('Currency'),
        col=5,
        model='res.currency',
        field='name',
        apply_on='asset.asset',
        required=True,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Purchase Date'),
        col=6,
        model='asset.asset',
        field='purchase_date',
        apply_on='asset.asset',
        required=False,
        tmpl_default='',
        type='date'
    ),
    Header(
        name=_('Purchase Amount'),
        col=7,
        model='asset.asset',
        field='purchase_amount',
        apply_on='asset.asset',
        required=False,
        tmpl_default=0,
        type='float'
    ),
    Header(
        name=_('Sale Date'),
        col=8,
        model='asset.asset',
        field='sale_date',
        apply_on='asset.asset',
        required=False,
        tmpl_default='',
        type='date'
    ),
    Header(
        name=_('Sale Amount'),
        col=9,
        model='asset.asset',
        field='sale_amount',
        apply_on='asset.asset',
        required=False,
        tmpl_default=0,
        type='float'
    ),
    Header(
        name=_('Depreciation Type Import Code'),
        col=10,
        model='asset.depreciation.type',
        field='import_code',
        apply_on='asset.depreciation',
        required=True,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Depreciation Mode Import Code'),
        col=11,
        model='asset.depreciation.mode',
        field='import_code',
        apply_on='asset.depreciation',
        required=True,
        tmpl_default='',
        type='str'
    ),
    Header(
        name=_('Depreciation Start Date'),
        col=12,
        model='asset.depreciation',
        field='date_start',
        apply_on='asset.depreciation',
        required=False,
        tmpl_default='',
        type='date'
    ),
    Header(
        name=_('Zero Depreciation Until'),
        col=13,
        model='asset.depreciation',
        field='zero_depreciation_until',
        apply_on='asset.depreciation',
        required=False,
        tmpl_default='',
        type='date'
    ),
    Header(
        name=_('Pro-Rata Temporis'),
        col=14,
        model='asset.depreciation',
        field='pro_rata_temporis',
        apply_on='asset.depreciation',
        required=False,
        tmpl_default='',
        type='bool'
    ),
    Header(
        name=_('Depreciation %'),
        col=15,
        model='asset.depreciation',
        field='percentage',
        apply_on='asset.depreciation',
        required=False,
        tmpl_default=0,
        type='float',
    ),
    Header(
        name=_('Depreciation Base Coeff.'),
        col=16,
        model='asset.depreciation',
        field='base_coeff',
        apply_on='asset.depreciation',
        required=False,
        tmpl_default=0,
        type='float',
    ),
    Header(
        name=_('Depreciable Amount'),
        col=17,
        model='asset.depreciation',
        field='amount_depreciable',
        apply_on='asset.depreciation',
        required=False,
        tmpl_default=0,
        type='float',
    ),
    Header(
        name=_('Line Description'),
        col=18,
        model='asset.depreciation.line',
        field='name',
        apply_on='asset.depreciation.line',
        required=True,
        tmpl_default='',
        type='str',
    ),
    Header(
        name=_('Line Date'),
        col=19,
        model='asset.depreciation.line',
        field='date',
        apply_on='asset.depreciation.line',
        required=True,
        tmpl_default='',
        type='date',
    ),
    Header(
        name=_('Line Type'),
        col=20,
        model='asset.depreciation.line',
        field='move_type',
        apply_on='asset.depreciation.line',
        required=True,
        tmpl_default='',
        type='selection',
    ),
    Header(
        name=_('Line Amount'),
        col=21,
        model='asset.depreciation.line',
        field='amount',
        apply_on='asset.depreciation.line',
        required=False,
        tmpl_default=0,
        type='float',
    ),
)


HEADERS_BY_COL = {h.col: h for h in HEADERS}


def get_header_by_model_and_field(model, field):
    for h in HEADERS:
        if h.model == model and h.field == field:
            return h
    raise ValueError(
        _("No file column for model `{}` and field `{}`")
        .format(model, field)
    )


def get_import_code_column(model):
    return get_header_by_model_and_field(model, 'import_code').col


def to_bool(v, w, s):
    return bool(v)


def to_date(v, w, s):
    try:
        if not v:
            return fields.Date.to_date(v)
        if isinstance(v, (int, float)):
            return date(*xlrd.xldate_as_tuple(v, w.datemode)[:3])
        return datetime.strptime(v, '%d/%m/%Y').date()
    except:
        raise ValidationError(_(f"Invalid date {v}"))


def to_float(v, w, s):
    try:
        if not v:
            return 0
        return float(v)
    except:
        raise ValidationError(_(f"Invalid float number {v}"))


def to_selection(v, w, s):
    if not v:
        return ''
    return trim(str(v)).lower()


def to_str(v, w, s):
    if not v:
        return ''
    return trim(str(v), True)


def trim(s, internal_spaces=False):
    return (' ' if internal_spaces else '').join(s.split())


CONVERTERS = {
    'bool': to_bool,
    'date': to_date,
    'float': to_float,
    'selection': to_selection,
    'str': to_str,
}


def convert_via_headers(vals, model, workbook, sheet):
    new_vals = {}
    for num, val in vals.items():
        header = HEADERS_BY_COL[num]
        if header.model == model:
            new_vals.update({
                header.field: CONVERTERS[header.type](val, workbook, sheet)
            })
    return new_vals


class AssetHistoryImport(models.TransientModel):
    _name = 'wizard.asset.history.import'
    _description = "Assets History Import"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        'res.company',
        default=get_default_company_id,
        required=True,
        string="Company",
    )

    file = fields.Binary(
        string="File"
    )

    filename = fields.Char(
        string="File Name"
    )

    template_file = fields.Binary(
        string="Template File"
    )

    @api.multi
    def download_template_file(self):
        """
        Retrieve an asset with any depreciation line to create a template
        file with its data.
        If no asset is found, simply return an empty template file with
        sheet headers only (as by `template_file` default).
        """
        assets = self.env['asset.depreciation.line'].search(
            [('asset_id.import_code', 'not in', (False, '')),
             ('asset_id.category_id.import_code', 'not in', (False, '')),
             ('company_id', '=', self.company_id.id),
             ('depreciation_id.mode_id.import_code', 'not in', (False, '')),
             ('depreciation_id.type_id.import_code', 'not in', (False, ''))],
            limit=10
        ).mapped('asset_id')
        self.template_file = assets.make_template_file_data(HEADERS)
        return {
            'name': 'Download Template File',
            'type': 'ir.actions.act_url',
            'url': '/web/content/{res_model}/{res_id}/template_file/'
                   'Import%20File%20Template.xlsx?download=true'
                   .format(res_model=self._name, res_id=self.id)
        }

    @api.multi
    def import_file(self):
        """ Imports the `file` content """
        self.check_before_import()
        file_data, workbook, sheet = self.parse_file()
        assets = self.import_assets_from_data(file_data, workbook, sheet)
        if not assets:
            raise ValidationError(
                _("Nothing could be imported.")
            )

        return self.launch_view(assets.ids)

    @api.multi
    def launch_view(self, asset_ids):
        """ Opens tree view upon assets """
        act = self.env.ref('assets_management.action_asset').read(load='')[0]
        act.update({'domain': [('id', 'in', asset_ids)]})
        return act

    def check_before_import(self):
        if not self.file:
            raise ValidationError(
                _("No file to import!")
            )
        # Checks correct file extension
        filename = trim(self.filename, internal_spaces=False)
        if filename.split('.')[-1].lower() not in ('xls', 'xlsx'):
            raise ValidationError(
                _("Cannot determine file extension. Please check its"
                  " extension (only .xls and .xlsx are allowed).")
            )

    def convert_to_asset_vals(self, asset_dict, workbook, sheet):
        """
        Takes `asset_dict` as read from imported file, returns vals to be
        written into the DB (via a `create()` or `write()`
        """
        vals = convert_via_headers(asset_dict, 'asset.asset', workbook, sheet)

        categ_code = asset_dict[get_import_code_column('asset.category')]
        categ = self.get_obj_by_import_code('asset.category', categ_code)
        if not categ:
            raise ValidationError(
                _("Could not find category for import code ") + categ_code
            )

        curr_col = get_header_by_model_and_field('res.currency', 'name').col
        curr = self.env['res.currency'].search([
            ('name', '=', asset_dict[curr_col])
        ])
        if not curr:
            raise ValidationError(
                _("Could not find currency for name '{}'.\n"
                  "Is it in its ISO 4217 format?")
            )

        vals.update({
            'category_id': categ.id,
            'company_id': self.company_id.id,
            'currency_id': curr.id,
        })

        return vals

    def convert_to_dep_vals(self, dep_dict, workbook, sheet):
        """
        Takes `dep_dict` as read from imported file, returns vals to be
        written into the DB (via a `create()` or `write()`
        """
        vals = convert_via_headers(
            dep_dict, 'asset.depreciation', workbook, sheet
        )

        mode_code = dep_dict[get_import_code_column('asset.depreciation.mode')]
        type_code = dep_dict[get_import_code_column('asset.depreciation.type')]
        dep_mode = self.get_obj_by_import_code(
            'asset.depreciation.mode', mode_code
        )
        dep_type = self.get_obj_by_import_code(
            'asset.depreciation.type', type_code
        )
        if not dep_mode and dep_type:
            raise ValidationError(
                _("Could not retrieve depreciation mode and type by codes"
                  " '{}' and '{}'.")
                .format(mode_code, type_code)
            )

        vals.update({
            'mode_id': dep_mode.id,
            'type_id': dep_type.id,
        })

        return vals

    def convert_to_lines_vals(self, line_dicts, workbook, sheet):
        """
        Takes `line_dicts` as read from imported file, returns list of vals
        to be written into the DB (via a `create()` or `write()`
        """
        vals = []
        for line_dict in line_dicts:
            vals.append(
                convert_via_headers(
                    line_dict, 'asset.depreciation.line', workbook, sheet
                )
            )
        return vals

    def get_obj_by_import_code(self, model, code):
        """
        This method returns an asset, a category, a depreciation type or
        mode according to given `model` and `code`.
        """
        return self.env[model].get_by_import_code(code)

    def import_assets_from_data(self, file_data, workbook, sheet):
        grouped_data = {}
        required_headers = tuple(filter(lambda h: h.required, HEADERS))
        for n, row in enumerate(file_data, start=2):
            missing_h = [h.name for h in required_headers if not row.get(h.col)]
            if missing_h:
                raise ValidationError(
                    _("Line {} misses required info on column(s) {}."
                      " Aborting import.").format(str(n), ', '.join(missing_h))
                )

            key = tuple(
                row[h.col] for h in HEADERS if h.field == 'import_code'
            )
            if key not in grouped_data:
                grouped_data[key] = {
                    'asset_data': {
                        n: v for n, v in row.items()
                        if HEADERS_BY_COL[n].apply_on == 'asset.asset'
                    },
                    'dep_data': {
                        n: v for n, v in row.items()
                        if HEADERS_BY_COL[n].apply_on == 'asset.depreciation'
                    },
                    'lines_data': []
                }

            grouped_data[key]['lines_data'].append({
                n: v for n, v in row.items()
                if HEADERS_BY_COL[n].apply_on == 'asset.depreciation.line'
            })

        ctx = dict(self._context or [], skip_depreciation_creation=True)
        asset_obj = self.env['asset.asset'].with_context(ctx)
        dep_obj = self.env['asset.depreciation']
        dep_line_obj = self.env['asset.depreciation.line']
        asset_ids = set()
        asset_code_cache = dict()
        for data in grouped_data.values():
            asset_data = data['asset_data']
            asset_code = asset_data[get_import_code_column('asset.asset')]
            asset_vals = self.convert_to_asset_vals(
                asset_data, workbook, sheet
            )

            if asset_code in asset_code_cache:
                asset = asset_code_cache[asset_code]
            else:
                asset = self.get_obj_by_import_code('asset.asset', asset_code)
                if not asset:
                    asset_vals.pop('import_code', None)
                    asset = asset_obj.create(asset_vals)
                elif len(asset) == 1:
                    asset_vals.pop('import_code', None)
                    asset.write(asset_vals)
                else:
                    raise ValidationError(
                        _("Cannot determine the assets to update, found"
                          " multiple assets with same code `{}`.")
                        .format(asset_code)
                    )
                asset_code_cache[asset_code] = asset

            dep_vals = self.convert_to_dep_vals(
                data['dep_data'], workbook, sheet
            )
            dep = dep_obj.search(
                [('asset_id', '=', asset.id),
                 ('mode_id', '=', dep_vals['mode_id']),
                 ('type_id', '=', dep_vals['type_id'])]
            )
            if dep:
                dep.write(dep_vals)
            else:
                dep_vals.update({'asset_id': asset.id})
                dep = dep_obj.create(dep_vals)

            lines_vals = self.convert_to_lines_vals(
                data['lines_data'], workbook, sheet
            )
            for line_vals in lines_vals:
                line_vals.update({'depreciation_id': dep.id})
                dep_line_obj.create(line_vals)

            asset_ids.add(asset.id)

        return self.env['asset.asset'].browse(asset_ids)

    def parse_file(self):
        try:
            workbook = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.file)
            )
            sheet = workbook.sheet_by_index(0)
        except xlrd.XLRDError:
            raise ValidationError(
                _("Attention! Invalid xls(x) file. Aborting import.")
            )

        file_headers = sheet.row_values(0)
        if not file_headers:
            raise ValidationError(
                _("File headers must be set in the first row.")
            )
        if len(HEADERS) != len(file_headers):
            raise ValidationError(
                _("Headers number mismatch: aborting import."
                  " Please download the template file and use it to create"
                  " your own file to import.")
            )

        data = [
            {num: val for num, val in enumerate(sheet.row_values(x))}
            for x in range(1, sheet.nrows)
        ]
        return data, workbook, sheet
