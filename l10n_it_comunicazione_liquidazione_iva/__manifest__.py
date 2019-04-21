# -*- coding: utf-8 -*-
# © 2017 Alessandro Camilli - Openforce
# © 2017 Lorenzo Battistini - Agile Business Group
#
# Odoo Proprietary License v1.0
#
# This software and associated files (the "Software") may only be used
# (executed, modified, executed after modifications) if you have purchased a
# valid license from the authors, typically via Odoo Apps, or if you have
# received a written agreement from the authors of the Software
#
# You may develop Odoo modules that use the Software as a library (typically by
# depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

{
    'name': 'Comunicazione liquidazione IVA',
    'summary': 'Gestione Comunicazione liquidazione IVA ed export file xml'
            'conforme alle specifiche dell''Agenzia delle Entrate',
    'version': '10.0.0.1.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'https://www.odoo-italia.net',
    'license': 'Other proprietary',
    'depends': [
        'account_accountant', 'l10n_it_codici_carica', 'l10n_it_fiscalcode'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/comunicazione_liquidazione.xml',
        'wizard/export_file_view.xml',
        'security/security.xml',
    ],
    'installable': True,
}
