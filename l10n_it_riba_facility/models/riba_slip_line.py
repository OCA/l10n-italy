# Copyright 2026 Nextev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import models


class RibaSlipLine(models.Model):
    _inherit = "riba.slip.line"

    def _riba_facility_start_date(self):
        """Date from which the RiBa uses the bank receipts facility.

        Returns the credit entry date, falling back to the acceptance date
        for slips credited without a journal entry (e.g. imported data or
        slips confirmed via the old 'skip-to-credited' button).
        """
        self.ensure_one()
        return (
            self.slip_id.date_credited
            or self.credit_move_id.date
            or self.slip_id.date_accepted
            or False
        )

    def _riba_facility_release_date(self):
        """Date from which the RiBa no longer uses the bank receipts facility.

        The RiBa uses the facility up to and including the due date; it is
        free from the next day. If the slip went past due, it is released on
        the past due date (same day); if no past due date is recorded it is
        considered immediately free (the bank has reversed the advance).
        """
        self.ensure_one()
        release = self.due_date + timedelta(days=1)
        if self.state == "past_due":
            past_due_date = self.past_due_move_id.date or self.slip_id.date_past_due
            if past_due_date:
                release = min(release, past_due_date)
            else:
                # Past due registered without a date: treat as immediately free.
                start = self._riba_facility_start_date()
                if start:
                    release = start
        return release

    def _riba_facility_is_used_at(self, date):
        """True if on the given date the RiBa is using the bank receipts facility.

        Uses the bank receipts facility from start_date up to and
        including the due date; free from the next day (or from the
        past due date if earlier).
        """
        self.ensure_one()
        start = self._riba_facility_start_date()
        if not start or not self.due_date:
            return False
        return start <= date < self._riba_facility_release_date()
