**Italiano**

Odoo Italia non supporta più i moduli alla versione 12.0 perciò 
non ci siamo occupati ufficialmente della migrazione dei dati da 
questa versione.

Tuttavia se non si volessero perdere i dati già presenti nella 
versione 12.0 si può provare in un ambiente di test la procedura
di migrazione a proprio rischio e non garantita togliendo la
dipendenza dal modulo `l10n_it_ddt` nel `__manifest__.py` e
lanciando gli script di migrazione commentati.
Passaggi:
- decommentare il riferimento a `hooks.py` in `__init__.py`
- decommentare `external_dependencies` e `pre_init_hook` in `__manifest__.py`
- spostare la cartella `readme/migrations` nella root del modulo
