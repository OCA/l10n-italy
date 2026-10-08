## Migration from 16.0 (l10n_it_fatturapa_pec) to 18.0 (l10n_it_edi_pec)

This module replaces `l10n_it_fatturapa_pec` (Odoo 16) with a complete rewrite
based on Odoo 18's native `l10n_it_edi` architecture.

### Name change and dependencies

The module was renamed from `l10n_it_fatturapa_pec` to `l10n_it_edi_pec`.

Dependencies were drastically simplified:

- **v16**: `l10n_it_fatturapa_out`, `l10n_it_fatturapa_in`, `l10n_it_sdi_channel`, `mail`
- **v18**: `l10n_it_edi`, `mail`

The modules `l10n_it_fatturapa_out`, `l10n_it_fatturapa_in` and
`l10n_it_sdi_channel` are no longer needed.

### Integration with l10n_it_edi core

The module now extends Odoo 18's `l10n_it_edi` core methods instead of
implementing a standalone flow:

- `_l10n_it_edi_upload()` on `account.move`: intercepts sending for PEC-enabled
  companies and sends directly via SMTP, with fallback to `super()` for the
  proxy channel
- `_l10n_it_edi_update_send_state()`: excludes PEC invoices from proxy polling
- `_l10n_it_edi_export_check()`: validates PEC configuration and removes the
  proxy user requirement
- `action_check_l10n_it_edi()`: triggers PEC fetchmail for manual status check

### Removed sdi.channel model

The `sdi.channel` model has been completely removed. PEC configuration is now
managed directly on `res.company` through the fields:

- `l10n_it_edi_use_pec` (Boolean)
- `l10n_it_edi_pec_server_id` (Many2one -> ir.mail_server)
- `l10n_it_edi_pec_fetch_server_id` (Many2one -> fetchmail.server)
- `l10n_it_edi_pec_email_exchange_system` (Char)

These fields are exposed in Settings via `res.config.settings`. The views
`sdi_view.xml` and `company_view.xml` are replaced by
`res_config_settings_views.xml`.

### Removed fatturapa.attachment.out model

In v16, `fatturapa.attachment.out` managed the lifecycle of sent invoices and SdI
notification parsing (`_message_type_ns`, `_message_type_rc`, etc.). In v18,
the entire flow is handled directly on `account.move` through the core
notification chain:

`_l10n_it_edi_parse_notification()` -> `_l10n_it_edi_transform_notification()` ->
`_l10n_it_edi_get_message()` -> `_l10n_it_edi_write_send_state()`

### Removed fatturapa.attachment.in model

Incoming vendor bill reception no longer uses `fatturapa.attachment.in`. The
module now directly creates an empty `account.move`, attaches the XML file and
calls `move._extend_with_attachments()` to populate fields from the electronic
invoice.

### SdI state mapping

State mapping has changed to align with the `l10n_it_edi` core:

| SdI Code | v16 (fatturapa.attachment.out) | v18 (account.move) |
|---|---|---|
| NS (Notifica di Scarto) | `sender_error` | `rejected` |
| RC (Ricevuta di Consegna) | `validated` | `forwarded` |
| MC (Mancata Consegna) | `recipient_error` | `forward_failed` |
| NE (Notifica Esito) | `accepted` / `rejected` | `accepted` / `rejected` |
| DT (Decorrenza Termini) | `validated` | `accepted` |

### Removed first_invoice_sent flow

The first PEC sending management mechanism (`first_invoice_sent` field on
`sdi.channel`, initial address `sdi01@pec.fatturapa.it` and automatic address
change after first sending) has been removed. The SdI PEC address must now be
configured directly in the `l10n_it_edi_pec_email_exchange_system` field.

### Simplified sending mechanism

- **v16**: `sdi.channel.send_via_pec()` created `mail.message` and `mail.mail`
  records, then delegated sending to Odoo's mail system
- **v18**: `_l10n_it_edi_upload()` directly builds a Python `EmailMessage` and
  sends it via `ir.mail_server.send_email()`, without creating intermediate
  database records

### Field renames

| v16 | v18 |
|---|---|
| `is_fatturapa_pec` | `is_l10n_it_edi_pec` |
| `email_from_for_fatturaPA` | `l10n_it_edi_pec_email_from` |

### Tests

The test base class changed from `FatturaPACommon`
(`l10n_it_fatturapa_out.tests`) to `TestItEdi` (`l10n_it_edi.tests.common`),
consistent with the new core extension pattern.
