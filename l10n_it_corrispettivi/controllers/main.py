# Copyright 2019 Simone Rubino
#Copyright 2021 Kevin Poli - AIR s.r.l.

from odoo.addons.portal.controllers.portal import CustomerPortal


class CorrispettiviPortal(CustomerPortal):

    def _show_report(self, model, report_type, report_ref, download=False):
        if model._name == 'account.move' and model.corrispettivo:
            report_ref = 'l10n_it_corrispettivi.account_corrispettivi'
        return super()._show_report(model, report_type, report_ref, download)
