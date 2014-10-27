# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import except_orm
import datetime


class wizard_compute_fc(models.TransientModel):

    _name = "wizard.compute.fc"
    _description = "Compute Fiscal Code"
    _rec_name = 'fiscalcode_surname'

    fiscalcode_surname = fields.Char('Surname', size=64)
    fiscalcode_firstname = fields.Char('First name', size=64)
    birth_date = fields.Date('Date of birth')
    birth_city = fields.Many2one(
        'res.city.it.code.distinct', string='City of birth')
    birth_province = fields.Many2one(
        'res.city.it.code.province', string='Province')
    sex = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female'),
        ], "Sex")

    @api.multi
    def onchange_birth_city(self, birth_city):
        res = {}
        if (birth_city):
            ct = self.env['res.city.it.code'].browse(birth_city)
            res['domain'] = {
                'birth_province': [('town_name', '=', ct.name)]
            }
        else:
            res['domain'] = {'birth_province': []}
        res['value'] = {'birth_province': ''}
        return res

    def _codicefiscale(self, cognome, nome, giornonascita, mesenascita,
                       annonascita, sesso, cittanascita):

        MESI = 'ABCDEHLMPRST'
        CONSONANTI = 'BCDFGHJKLMNPQRSTVWXYZ'
        VOCALI = 'AEIOU'
        LETTERE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        REGOLECONTROLLO = {
            'A': (0, 1), 'B': (1, 0), 'C': (2, 5),
            'D': (3, 7), 'E': (4, 9), 'F': (5, 13),
            'G': (6, 15), 'H': (7, 17), 'I': (8, 19),
            'J': (9, 21), 'K': (10, 2), 'L': (11, 4),
            'M': (12, 18), 'N': (13, 20), 'O': (14, 11),
            'P': (15, 3), 'Q': (16, 6), 'R': (17, 8),
            'S': (18, 12), 'T': (19, 14), 'U': (20, 16),
            'V': (21, 10), 'W': (22, 22), 'X': (23, 25),
            'Y': (24, 24), 'Z': (25, 23),
            '0': (0, 1), '1': (1, 0), '2': (2, 5),
            '3': (3, 7), '4': (4, 9), '5': (5, 13),
            '6': (6, 15), '7': (7, 17), '8': (8, 19),
            '9': (9, 21)
        }

        """Funzioni per il calcolo del C.F."""
        def _surname(stringa):
            """
            Ricava, da stringa, 3 lettere in base alla convenzione dei C.F.
            """
            cons = [c for c in stringa if c in CONSONANTI]
            voc = [c for c in stringa if c in VOCALI]
            chars = cons + voc
            if len(chars) < 3:
                chars += ['X', 'X']
            return chars[:3]

        def _name(stringa):
            """
            Ricava, da stringa, 3 lettere in base alla convenzione dei C.F.
            """
            cons = [c for c in stringa if c in CONSONANTI]
            voc = [c for c in stringa if c in VOCALI]
            if len(cons) > 3:
                cons = [cons[0]] + [cons[2]] + [cons[3]]
            chars = cons + voc
            if len(chars) < 3:
                chars += ['X', 'X']
            return chars[:3]

        def _datan(giorno, mese, anno, sesso):
            """
            Restituisce il campo data del CF.
            """
            chars = (list(anno[-2:]) + [MESI[int(mese)-1]])
            gn = int(giorno)
            if sesso == 'F':
                gn += 40
            chars += list("%02d" % gn)
            return chars

        def _codicecontrollo(c):
            """
            Restituisce il codice di controllo, l'ultimo carattere del C.F.
            """
            sommone = 0
            for i, car in enumerate(c):
                j = 1 - i % 2
                sommone += REGOLECONTROLLO[car][j]
            resto = sommone % 26
            return [LETTERE[resto]]

        """Restituisce il C.F costruito sulla base degli argomenti."""
        nome = nome.upper()
        cognome = cognome.upper()
        sesso = sesso.upper()
        cittanascita = cittanascita.upper()
        chars = (_surname(cognome) +
                 _name(nome) +
                 _datan(giornonascita, mesenascita, annonascita, sesso) +
                 list(cittanascita))
        chars += _codicecontrollo(chars)
        return ''.join(chars)

    def _get_national_code(self, birth_city, birth_prov, birth_date):
        cities = self.env['res.city.it.code'].search([
            ('name', '=', birth_city), ('province', '=', birth_prov)],
            order='creation_date ASC, var_date ASC, notes ASC')
        if not cities or len(cities) == 0:
            return ''
        """
        notes fields contains variation data while var_date may contain the
        eventual date of the variation. notes may be:
        - ORA: city changed name, name_var contains new name, national_code_var
               contains the repeated national code.
               There are some cities that contains two identical values, for
               example PORTO (CO), has two ORA entries for G906 and G907, this
               is rather unpredictable and the first value will be taken
        - AGG: city has been aggregated to another one and doesn't exist
               anymore. name_var and national_code_var contain recent data.
               Some cities have particular cases, for example ALME' (BG) that
               is listed as aggregate to another city since 1927 but gained
               independence (creation_date) in 1948
        - AGP: partially aggregated, city has been split and assigned to more
               than one other cities. name_var and national_code_var contain
               recent data. It's not possible to determine the correct code
               for new city so the original code is returned
        - AGT: temporarily aggregated to another city, if possible this gets
               ignored. name_var and national_code_var contain recent data
        - VED: reference to another city. This is assigned to cities that
               changed name and were then subject to other changes.
        """
        # Checks for any VED element
        newcts = None
        for ct in cities:
            if ct.notes == 'VED':
                newcts = self.env['res.city.it.code'].search([
                    ('name', '=', ct.name_var)])
                break
        if newcts:
            cities = newcts
        return self._check_national_codes(
            birth_city, birth_prov, birth_date, cities)

    def _check_national_codes(
            self, birth_city, birth_prov, birth_date, cities):
        nc = ''
        dtcostvar = None
        for ct in cities:
            if (ct.creation_date and
                    (not dtcostvar or not ct.creation_date or
                        dtcostvar < ct.creation_date)):
                dtcostvar = ct.creation_date
            if not ct.notes:
                nc = ct.national_code
            elif (ct.notes == 'ORA' and
                    (not dtcostvar or not ct.var_date or
                        dtcostvar < ct.var_date)):
                if (not ct.var_date or ct.var_date <= birth_date):
                    nc = ct.national_code_var
                elif not nc:
                    nc = ct.national_code
                if (ct.var_date):
                    dtcostvar = ct.var_date
            elif (ct.notes == 'AGG' and
                    (not dtcostvar or not ct.var_date or
                        dtcostvar < ct.var_date)):
                if (not ct.var_date or ct.var_date <= birth_date):
                    nc = ct.national_code_var
                elif not nc:
                    nc = ct.national_code
                if (ct.var_date):
                    dtcostvar = ct.var_date
            elif (ct.notes == 'AGP' and
                    (not dtcostvar or not ct.var_date or
                        dtcostvar < ct.var_date)):
                nc = ct.national_code
                if (ct.var_date):
                    dtcostvar = ct.var_date
            elif (ct.notes == 'AGP' and
                    (not dtcostvar or not ct.var_date or
                        dtcostvar < ct.var_date)):
                nc = ct.national_code

        return nc

    @api.multi
    def compute_fc(self):
        active_id = self._context.get('active_id')
        partner = self.env['res.partner'].browse(active_id)
        for f in self:
            if (not f.fiscalcode_surname or not f.fiscalcode_firstname or
                    not f.birth_date or not f.birth_city or not f.sex):
                raise except_orm(
                    _('Error'), ('One or more fields are missing'))
            nat_code = self._get_national_code(
                f.birth_city.name, f.birth_province.name, f.birth_date)
            if not nat_code:
                raise except_orm(_('Error'), _('National code is missing'))
            birth_date = datetime.datetime.strptime(f.birth_date, "%Y-%m-%d")
            CF = self._codicefiscale(
                f.fiscalcode_surname,
                f.fiscalcode_firstname,
                str(birth_date.day),
                str(birth_date.month),
                str(birth_date.year),
                f.sex,
                nat_code)
            if partner.fiscalcode and partner.fiscalcode != CF:
                raise except_orm(_('Error'), (
                    'Existing fiscal code %s is different from the computed'
                    ' one (%s). If you want to use the computed one, remove'
                    ' the existing one') % (partner.fiscalcode, CF))
            partner.fiscalcode = CF
            partner.individual = True
        return {'type': 'ir.actions.act_window_close'}
