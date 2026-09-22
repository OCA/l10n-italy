# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import collections
import re

from odoo import _, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"
    tax_registry_id = fields.Many2one(
        "account.tax.registry",
        "VAT registry",
        help="You can group several journals within 1 registry. In printing "
        "wizard, you will be able to select the registry in order to load"
        " that group of journals",
    )

    @staticmethod
    def _get_number_from_string(number_string):
        try:
            number = re.findall(r"\d+", number_string)
            if isinstance(number, list):
                number = "".join(number)
            sequence_char = re.findall(r"[^0-9]", number_string)
            if isinstance(sequence_char, list):
                sequence_char = "".join(sequence_char)
            return sequence_char, int(number)
        except ValueError:
            return False, False

    def check_holes(self, moves):
        # check the sequenciality of moves' numbers in the journal
        self.ensure_one()
        journal_errors = []
        sorted_moves = sorted(moves, key=lambda m: m.name)

        if any([not move.name for move in moves]):
            moves_without_name = str([move.id for move in moves if not move.name])
            journal_errors.append(
                _("Journal '%s' moves without name: %s")
                % (self.name, " - ".join(moves_without_name))
            )

        numbers_dict = {}
        for move in sorted_moves:
            sequence_char, number = self._get_number_from_string(move.name)
            if sequence_char not in numbers_dict:
                numbers_dict[sequence_char] = [number]
            else:
                numbers_dict[sequence_char].append(number)
        if len(numbers_dict) > 1:
            journal_errors.append(
                _("Journal '%s' has more than 1 sequence: %s")
                % (self.name, " ".join(numbers_dict.keys()))
            )
        numbers = []
        for sequence_char in numbers_dict:
            numbers.extend(numbers_dict[sequence_char])
        extra_numbers = [
            item for item, count in collections.Counter(numbers).items() if count > 1
        ]
        missing_numbers = []
        for item in range(0, len(numbers)):
            if (
                numbers[item] != numbers[0]
                and numbers[item] - numbers[item - 1] != 1
                and numbers[item - 1] not in extra_numbers
            ):
                missing_numbers.append(numbers[item - 1])
        if extra_numbers:
            journal_errors.append(
                _("Journal '%s' extra numbers: %s")
                % (self.name, " - ".join([str(x) for x in extra_numbers]))
            )
        if missing_numbers:
            journal_errors.append(
                _("Journal '%s' missing numbers after: %s")
                % (self.name, " - ".join([str(x) for x in missing_numbers]))
            )
        if journal_errors:
            return "\n".join(journal_errors)
        return ""
