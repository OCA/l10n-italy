**Italiano**

Il core di Odoo fornisce `amount_to_text`, il quale converte importi
numerici in testo ottenendo la lingua dal contesto fornito o dalle
impostazioni utente/partner, con alcune limitazioni.

Esempio: 45,75 €

  - Lingua utente "Inglese" → forty-five euro and seventy-five cents
  - Lingua utente "Italiano" → quarantacinque euro e settantacinque
    centesimi

L'unità/sottounità di valuta non viene tradotta e non viene gestita la
forma singolare. Il core di Odoo restituisce l'importo inglese in
minuscolo.

Questo modulo fornisce una base per tradurre le unità/sottounità di
valuta, adattando le parole alle regole della lingua italiana.

Vengono inoltre gestite le eccezioni per la forma singolare delle valute
EUR, USD, GBP e CNY.

Esempio: 1,01 €

  - La parte intera diventa "un euro", non "uno euro"
  - La parte decimale diventa "un centesimo", non "uno centesimi"

**English**

Odoo core provides `amount_to_text`, which converts numerical amounts to
text getting language from given context or user/partner setting, with
some limitations.

Example: 45,75 €

  - User Language 'English' -\> forty-five euro and seventy-five cents
  - User Language 'Italian' -\> quarantacinque euro e settantacinque
    centesimi

Currency unit/subunit is not translated and singular form is not
handled. Odoo core returns the English amount in lowercase.

This module provides a base for translating currency unit/subunit
adapting words to italian language rules.

Singular form expections for EUR, USD, GBP and CNY currencies are
handled as well.

Example: 1,01 €

  - Integer part becomes "un euro", not "uno euro"
  - Decimal part becomes "un centesimo", not "uno centesimi"
