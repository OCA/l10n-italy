# -*- coding: utf-8 -*-
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://www.linkgroup.it/>)
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.tools.misc import formatLang
from odoo.tools.translate import _
from odoo.exceptions import Warning as UserError

from datetime import datetime
import time


class ReportRegistroIva(models.AbstractModel):
    _inherit = 'report.l10n_it_vat_registries.report_registro_iva'

    def _get_move_line(self, move, data):
        move_lines = []
        cash_move_ids = data['cash_move_ids'].get(str(move.id))

        if cash_move_ids:
            # movimenti di cassa
            for movec in self._get_move(cash_move_ids):
                move_lines.extend([move_line for move_line in movec.line_ids])
        else:
            move_lines.extend([move_line for move_line in move.line_ids])

        return move_lines

