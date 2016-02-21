# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2010-2012 Associazione OpenERP Italia
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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from osv import fields, osv
from tools.translate import _

import datetime


class wizard_compute_fc(osv.osv_memory):

    _name = "wizard.compute.fc"
    _description = "Compute Fiscal Code"
    _columns = {
        'fiscalcode_surname': fields.char('Surname', size=64),
        'fiscalcode_firstname': fields.char('First name', size=64),
        'birth_date': fields.date('Date of birth'),
        'birth_city': fields.many2one('res.city', 'City of birth'),
        'sex': fields.selection([('M', 'Male'),
                                 ('F', 'Female'),
                                 ], "Sex"),
    }

    def _codicefiscale(
        self, cognome, nome, giornonascita, mesenascita, annonascita, sesso,
        cittanascita
    ):

        MESI = 'ABCDEHLMPRST'
        CONSONANTI = 'BCDFGHJKLMNPQRSTVWXYZ'
        VOCALI = 'AEIOU'
        LETTERE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        REGOLECONTROLLO = {
            'A': (0, 1), 'B': (1, 0), 'C': (2, 5), 'D': (3, 7),
            'E': (4, 9),
            'F': (5, 13), 'G': (6, 15), 'H': (7, 17), 'I': (8, 19),
            'J': (9, 21),
            'K': (10, 2), 'L': (11, 4), 'M': (12, 18), 'N': (13, 20),
            'O': (14, 11),
            'P': (15, 3), 'Q': (16, 6), 'R': (17, 8), 'S': (18, 12),
            'T': (19, 14),
            'U': (20, 16), 'V': (21, 10), 'W': (22, 22), 'X': (23, 25),
            'Y': (24, 24),
            'Z': (25, 23),
            '0': (0, 1), '1': (1, 0), '2': (2, 5), '3': (3, 7),
            '4': (4, 9),
            '5': (5, 13), '6': (6, 15), '7': (7, 17), '8': (8, 19),
            '9': (9, 21)
        }

        # Funzioni per il calcolo del C.F.
        def _surname(stringa):
            """Ricava, da stringa, 3 lettere in base alla convenzione dei C.F.
            """
            cons = [c for c in stringa if c in CONSONANTI]
            voc = [c for c in stringa if c in VOCALI]
            chars = cons + voc
            if len(chars) < 3:
                chars += ['X', 'X']
            return chars[:3]

        def _name(stringa):
            """Ricava, da stringa, 3 lettere in base alla convenzione dei C.F.
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
            """Restituisce il campo data del CF."""
            chars = (list(anno[-2:]) + [MESI[int(mese) - 1]])
            gn = int(giorno)
            if sesso == 'F':
                gn += 40
            chars += list("%02d" % gn)
            return chars

        def _codicecontrollo(c):
            """Restituisce il codice di controllo, l'ultimo carattere del
            C.F."""
            sommone = 0
            for i, car in enumerate(c):
                j = 1 - i % 2
                sommone += REGOLECONTROLLO[car][j]
            resto = sommone % 26
            return [LETTERE[resto]]

        # Restituisce il C.F costruito sulla base degli argomenti.
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

    def compute_fc(self, cr, uid, ids, context):
        active_id = context.get('active_id', [])
        partner = self.pool.get('res.partner').browse(
            cr, uid, active_id, context)
        form_obj = self.browse(cr, uid, ids, context)
        for wizard in form_obj:
            if (
                not wizard.fiscalcode_surname or
                not wizard.fiscalcode_firstname or not wizard.birth_date or
                not wizard.birth_city or not wizard.sex
            ):
                raise osv.except_osv(
                    _('Error'), _('One or more fields are missing'))
            if not wizard.birth_city.cadaster_code:
                raise osv.except_osv(_('Error'), _('Cataster code is missing'))
            birth_date = datetime.datetime.strptime(
                wizard.birth_date, "%Y-%m-%d")
            CF = self._codicefiscale(
                wizard.fiscalcode_surname, wizard.fiscalcode_firstname, str(
                    birth_date.day),
                str(birth_date.month), str(birth_date.year), wizard.sex,
                wizard.birth_city.cadaster_code)
            if partner.fiscalcode and partner.fiscalcode != CF:
                raise osv.except_osv(
                    _('Error'),
                    _('Existing fiscal code %s is different from the computed '
                      'one (%s). If you want to use the computed one, remove '
                      'the existing one') % (partner.fiscalcode, CF))
            self.pool.get('res.partner').write(
                cr, uid, active_id, {'fiscalcode': CF, 'individual': True})
        return {}
