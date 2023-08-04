
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/l10n-italy&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/l10n-italy/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-italy/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/l10n-italy/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/l10n-italy/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/l10n-italy/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/l10n-italy)
[![Translation Status](https://translation.odoo-community.org/widgets/l10n-italy-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/l10n-italy-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Odoo Italia Modules

Addons concerning Odoo Italian Localization.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_vat_period_end_statement](account_vat_period_end_statement/) | 16.0.1.1.0 |  | Allow to create the 'VAT Statement'.
[l10n_it_abicab](l10n_it_abicab/) | 16.0.1.0.0 | [![Borruso](https://github.com/Borruso.png?size=30px)](https://github.com/Borruso) | Base Bank ABI/CAB codes
[l10n_it_account](l10n_it_account/) | 16.0.1.0.1 |  | Modulo base usato come dipendenza di altri moduli contabili
[l10n_it_account_stamp](l10n_it_account_stamp/) | 16.0.1.0.1 |  | Gestione automatica dell'imposta di bollo
[l10n_it_account_tax_kind](l10n_it_account_tax_kind/) | 16.0.1.0.0 |  | Gestione natura delle aliquote IVA
[l10n_it_appointment_code](l10n_it_appointment_code/) | 16.0.1.0.0 |  | Aggiunge la tabella dei codici carica da usare nelle dichiarazioni fiscali italiane
[l10n_it_ateco](l10n_it_ateco/) | 16.0.1.1.0 |  | ITA - Codici Ateco
[l10n_it_declaration_of_intent](l10n_it_declaration_of_intent/) | 16.0.1.0.1 |  | Gestione dichiarazioni di intento
[l10n_it_delivery_note](l10n_it_delivery_note/) | 16.0.1.0.3 | [![As400it](https://github.com/As400it.png?size=30px)](https://github.com/As400it) | Crea, gestisce e fattura i DDT partendo dalle consegne
[l10n_it_delivery_note_base](l10n_it_delivery_note_base/) | 16.0.1.0.0 | [![As400it](https://github.com/As400it.png?size=30px)](https://github.com/As400it) [![Byloth](https://github.com/Byloth.png?size=30px)](https://github.com/Byloth) | Crea e gestisce tabelle principali per gestire i DDT
[l10n_it_fatturapa](l10n_it_fatturapa/) | 16.0.1.0.2 |  | Fatture elettroniche
[l10n_it_fatturapa_in](l10n_it_fatturapa_in/) | 16.0.1.0.0 |  | Ricezione fatture elettroniche
[l10n_it_fatturapa_out](l10n_it_fatturapa_out/) | 16.0.1.0.8 |  | Emissione fatture elettroniche
[l10n_it_fatturapa_out_di](l10n_it_fatturapa_out_di/) | 16.0.1.0.0 |  | Dichiarazioni d'intento in fatturapa
[l10n_it_fiscal_document_type](l10n_it_fiscal_document_type/) | 16.0.1.0.0 |  | ITA - Tipi di documento fiscale per dichiarativi
[l10n_it_fiscal_payment_term](l10n_it_fiscal_payment_term/) | 16.0.1.0.0 |  | Condizioni di pagamento delle fatture elettroniche
[l10n_it_fiscalcode](l10n_it_fiscalcode/) | 16.0.1.0.0 |  | ITA - Codice fiscale
[l10n_it_ipa](l10n_it_ipa/) | 16.0.1.0.1 |  | ITA - Codice IPA
[l10n_it_payment_reason](l10n_it_payment_reason/) | 16.0.1.0.0 |  | Aggiunge la tabella delle causali di pagamento da usare ad esempio nelle ritenute d'acconto
[l10n_it_pec](l10n_it_pec/) | 16.0.1.0.0 |  | Aggiunge il campo email PEC al partner
[l10n_it_rea](l10n_it_rea/) | 16.0.1.0.0 |  | Gestisce i campi del Repertorio Economico Amministrativo
[l10n_it_sdi_channel](l10n_it_sdi_channel/) | 16.0.1.0.0 | [![sergiocorato](https://github.com/sergiocorato.png?size=30px)](https://github.com/sergiocorato) | Aggiunge il canale di invio/ricezione dei file XML attraverso lo SdI
[l10n_it_vat_payability](l10n_it_vat_payability/) | 16.0.1.0.0 |  | ITA - Esigibilità IVA
[l10n_it_website_portal_ipa](l10n_it_website_portal_ipa/) | 16.0.1.0.1 |  | Aggiunge l'indice PA (IPA) tra i dettagli dell'utente nel portale.
[l10n_it_withholding_tax](l10n_it_withholding_tax/) | 16.0.1.1.2 |  | ITA - Ritenute d'acconto
[l10n_it_withholding_tax_reason](l10n_it_withholding_tax_reason/) | 16.0.1.0.0 |  | ITA - Causali pagamento per ritenute d'acconto

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
