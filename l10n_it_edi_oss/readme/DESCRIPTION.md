Modulo tecnico per l'integrazione tra `l10n_eu_oss_oca` (regime OSS - One Stop Shop)
e `l10n_it_edi` (fatturazione elettronica italiana).

Quando viene emessa una fattura con un'imposta OSS, il modulo modifica la generazione
del file XML FatturaPA per:

- Impostare AliquotaIVA a 0,00 (invece dell'aliquota estera effettiva)
- Aggiungere il codice Natura N3.2 (non imponibile - cessioni intracomunitarie)
- Aggiungere un blocco AltriDatiGestionali con TipoDato "OSS" e l'aliquota effettiva
- Impostare Imposta a 0,00 nel riepilogo DatiRiepilogo
- Aggiungere il RiferimentoNormativo con il riferimento all'Art. 41 D.L. 331/1993

Inoltre, quando vengono create nuove imposte OSS tramite il wizard di `l10n_eu_oss_oca`,
il modulo imposta automaticamente il codice Natura e il riferimento normativo.

---

Technical module integrating `l10n_eu_oss_oca` (OSS - One Stop Shop regime) with
`l10n_it_edi` (Italian electronic invoicing).

When an invoice is issued with an OSS tax, this module modifies the FatturaPA XML
generation to:

- Set AliquotaIVA to 0.00 (instead of the actual foreign tax rate)
- Add the Natura code N3.2 (non-taxable - intra-community transfers)
- Add an AltriDatiGestionali block with TipoDato "OSS" and the actual tax rate
- Set Imposta to 0.00 in the DatiRiepilogo summary
- Add the RiferimentoNormativo with the reference to Art. 41 D.L. 331/1993

Additionally, when new OSS taxes are created through the `l10n_eu_oss_oca` wizard,
the module automatically sets the Natura code and law reference.
