# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
#
#    Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or (at
#    your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/lgpl-3.0.txt.
#
##############################################################################

from odoo import fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    is_pec = fields.Boolean("PEC server")

    email_from_for_fatturaPA = fields.Char("Sender Email Address for FatturaPA")

    email_exchange_system = fields.Char("Exchange System Email Address")

