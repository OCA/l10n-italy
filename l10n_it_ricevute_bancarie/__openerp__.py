# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
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

{
    'name': "Ricevute Bancarie",
    'version': "8.0.1.3.2",
    'author': "Odoo Community Association (OCA)",
    'category': "Accounting & Finance",
    'website': "http://www.odoo-italia.org",
    'license': "AGPL-3",
    'depends': [
        'account_voucher',
        'l10n_it_fiscalcode',
        'account_due_list',
        'base_iban',
        'l10n_it_abicab'],
    'data': [
        "views/partner_view.xml",
        "views/configuration_view.xml",
        "riba_sequence.xml",
        "views/wizard_accreditation.xml",
        "views/wizard_unsolved.xml",
        "views/riba_view.xml",
        "views/account_view.xml",
        "views/wizard_riba_issue.xml",
        "views/wizard_riba_file_export.xml",
        "views/account_config_view.xml",
        "riba_workflow.xml",
        "views/distinta_report.xml",
        "views/riba_detail_view.xml",
        "report.xml",
        "security/ir.model.access.csv",
    ],
    'demo': ["demo/riba_demo.xml"],
    'test': [
        'test/riba_invoice.yml',
        'test/issue_riba.yml',
        'test/unsolved_riba.yml',
    ],
    'installable': True,
}
