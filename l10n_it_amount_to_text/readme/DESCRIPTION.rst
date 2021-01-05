**Italiano**

Il core di Odoo fornisce ``amount_to_text``, il quale converte importi numerici in testo ottenendo la lingua dal contesto fornito o dalle impostazioni utente/partner, con alcune limitazioni.

Esempio: 45,75 €

* Lingua utente "Italiano" → Quarantacinque Euros e Settantacinque Cents
* Lingua utente "Inglese" → Forty-Five Euros and Seventy-Five Cents

L'unità/sottounità di valuta non viene tradotta e tutte le parole possiedono l'iniziale maiuscola, forma non corretta nella lingua italiana.

Questo modulo fornisce una base per tradurre le unità/sottounità di valuta, adattando le parole alle regole della lingua italiana.

**English**

Odoo core provides ``amount_to_text``, which converts numerical amounts to text getting language from given context or user/partner setting, with some limitations.

Example: 45,75 €

* User Language 'Italian' -> Quaranta Euros e Settantacinque Cents
* User Language 'English' -> Forty-Five Euros and Seventy-Five Cents

Currency unit/subunit is not translated and all words are capitalized, which is incorrect in italian language.

This module provides a base for translating currency unit/subunit adapting words to italian language rules.
