This module extends the Odoo base email functionality to support the
PEC standard (posta elettronica certificata) and correctly
parse PEC messages (See images in docs for the message structure).

According to 'daticert.xml' file, it identifies the message type and other
message data.

'consegna', 'accettazione' and the other notification messages are linked to
the original message that originated them.

It also correctly parses the mail attachments and attaches the original 'eml'
PEC message.

The module adds a menu

Contacts -> PEC

menu where to write PEC messages.

Sent and received messages are accesible by

Technical -> Email -> Messages

menu, where you can filter by PEC type

https://it.wikipedia.org/wiki/Posta_elettronica_certificata

**l10n_it_pec Incompatibility**

l10n_it_pec introduce a new field for PEC address, following a different paradigm.

Using l10n_it_pec_messages, l10n_it_pec is not needed and PEC addresses must be added as contacts of the main partner
