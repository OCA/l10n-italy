# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, tools


class ResCityItCode(models.Model):
    """
    To create res.city.it.code.csv:
    http://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Strumenti/
Codici+attivita+e+tributo/Codici+territorio/Comuni+italia+esteri/
    - download the file named: Codici Comuni d’Italia - xls
    - open it in LibreOffice and save it as .ods
    - some date cells contain a "'" to be removed using Calc's menu
      Data / Text to columns
    - rows 216,1122 contain wrong written dates
    - dates format must be yyyy-mm-dd
    - add first column with numeric ids
    - change first row with column names from res.city.it.code model
      id,national_code,cadastre_code,province,name,notes,national_code_var,
cadastre_code_var,province_var,name_var,creation_date,var_date
    - save as csv in data/res.city.it.code.csv
    """
    _name = "res.city.it.code"

    national_code = fields.Char('National code', size=4)
    cadastre_code = fields.Char(
        'Belfiore cadastre code (not used anymore)',
        size=4)
    province = fields.Char('Province', size=5)
    name = fields.Char('Name')
    notes = fields.Char('Notes', size=4)
    national_code_var = fields.Char('National code variation', size=4)
    cadastre_code_var = fields.Char('Cadastre code variation', size=4)
    province_var = fields.Char('Province variation', size=5)
    name_var = fields.Char('Name variation', size=100)
    creation_date = fields.Date('Creation date')
    var_date = fields.Date('Variation date')


class ResCityItCodeDistinct(models.Model):
    _name = 'res.city.it.code.distinct'
    _auto = False

    name = fields.Char('Name', size=100)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW res_city_it_code_distinct AS (
            SELECT name, MAX(id) AS id FROM res_city_it_code
            GROUP BY name)
            """)


class ResCityItCodeProvince(models.Model):
    _name = 'res.city.it.code.province'
    _auto = False

    name = fields.Char('Name', size=100)
    town_name = fields.Char('Name', size=100)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW res_city_it_code_province AS (
            SELECT province AS name, name as town_name, MAX(id) AS id
            FROM res_city_it_code
            GROUP BY province, name)
            """)
