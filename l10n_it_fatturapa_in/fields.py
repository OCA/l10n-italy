#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Float

orig_convert_to_cache = Float.convert_to_cache
orig_get_digits = Float.get_digits

E_INVOICE_PRECISION_TO_FIELD = {
    "Discount": "discount_decimal_digits",
    "Product Price": "price_decimal_digits",
    "Product Unit of Measure": "quantity_decimal_digits",
}
# Map a `decimal.precision` to the name of the field in `fatturapa.attachment`
# that stores the value used during import


def get_digits(self, env):
    digits = orig_get_digits(self, env)
    e_invoice_precision = env.context.get("l10n_it_fatturapa_in_precision")
    if e_invoice_precision:
        digits = digits[0], e_invoice_precision
    return digits


def convert_to_cache(self, value, record, validate=True):
    if (
        record._name in ("account.move", "account.move.line")
        and "fatturapa_attachment_in_id" in record._fields
    ):
        e_invoice = record.fatturapa_attachment_in_id
        if e_invoice:
            # The invoice [line] has been created by importing an e-invoice.
            # If a different precision has been used,
            # keep using that precision to read values that have it.
            field_precision = self._digits
            if isinstance(field_precision, str):
                e_invoice_precision_field = E_INVOICE_PRECISION_TO_FIELD.get(
                    field_precision
                )
                if e_invoice_precision_field:
                    e_invoice_precision = e_invoice[e_invoice_precision_field]
                    if e_invoice_precision:
                        record = record.with_context(
                            l10n_it_fatturapa_in_precision=e_invoice_precision
                        )

    return orig_convert_to_cache(self, value, record, validate=validate)


Float.convert_to_cache = convert_to_cache
Float.get_digits = get_digits
