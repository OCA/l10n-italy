La configurazione del regime OSS è gestita interamente dal modulo standard
Odoo `l10n_eu_oss`. Questo modulo (`l10n_it_edi_oss`) aggiunge solo l'adattamento
per la fatturazione elettronica italiana e non richiede configurazioni proprie.

## Prerequisiti

- La società deve avere come *Paese fiscale* l'Italia e la *Partita IVA* valorizzata.
- Il modulo `l10n_it_edi` deve essere già configurato e funzionante.
- Devono esistere le normali imposte di vendita italiane (percentuali).

## Passi

1. **Abilitare l'OSS.** In *Contabilità → Configurazione → Impostazioni*, sezione
   *Imposte*, attivare **"Vendita a distanza intracomunitaria (UE)"**
   (`module_l10n_eu_oss`) e salvare: viene installato `l10n_eu_oss`.

2. **Installare `l10n_it_edi_oss`.** Dipende da `l10n_it_edi` e `l10n_eu_oss`.
   All'installazione, un *post-init hook* allinea automaticamente eventuali imposte
   OSS italiane già presenti impostando Natura **N3.2** e Riferimento Normativo
   **Art. 41 D.L. 331/1993**.

3. **Generare imposte e posizioni fiscali OSS.** Tornare in *Contabilità →
   Configurazione → Impostazioni*, sezione *Imposte*, e premere
   **"Aggiorna mappatura imposte"** (*Refresh tax mapping*). Vengono create:
   - una posizione fiscale `OSS B2C <Paese>` (ad applicazione automatica) per
     ogni Paese UE di destinazione, escluso il Paese della società e i Paesi per
     cui esiste già una posizione fiscale con partita IVA estera;
   - le imposte OSS con l'aliquota del Paese di destinazione (aliquote dalla mappa
     interna di `l10n_eu_oss`), collocate in un gruppo imposte e in un conto
     dedicati e marcate con il tag OSS.

4. **Verificare la mappatura proposta.**
   - *Contabilità → Configurazione → Posizioni fiscali*: controllare le posizioni
     *"OSS B2C ..."* e la relativa corrispondenza tra imposta interna e imposta OSS.
   - *Contabilità → Configurazione → Imposte*: controllare le imposte OSS create.
     Ogni imposta OSS italiana deve riportare Natura **N3.2** (`l10n_it_exempt_reason`)
     e Riferimento Normativo **Art. 41 D.L. 331/1993** (`l10n_it_law_reference`).
     Se si creano imposte OSS manualmente, impostare anche questi campi.

## Funzionamento in fattura

Quando si fattura un cliente B2C di un altro Paese UE, la posizione fiscale OSS si
applica automaticamente e sostituisce l'imposta interna con l'imposta OSS di
destinazione. In fase di generazione dell'XML FatturaPA, `l10n_it_edi_oss` imposta
AliquotaIVA 0,00, Natura N3.2, un blocco AltriDatiGestionali con l'aliquota
effettiva, Imposta 0,00 nel riepilogo e il relativo RiferimentoNormativo.

## Note

- La soglia OSS è di **10.000 € annui** di vendite B2C intracomunitarie: al di sotto
  si può continuare ad applicare l'IVA nazionale, al di sopra l'adesione all'OSS è
  obbligatoria. Odoo non calcola automaticamente questa soglia.
- Premere nuovamente **"Aggiorna mappatura imposte"** ogni volta che si aggiungono
  nuove imposte di vendita nazionali o dopo aggiornamenti del modulo.

---

OSS regime configuration is handled entirely by the standard Odoo module
`l10n_eu_oss`. This module (`l10n_it_edi_oss`) only adds the adaptation for Italian
electronic invoicing and requires no configuration of its own.

## Prerequisites

- The company *Fiscal Country* must be Italy and its *VAT* number must be set.
- The `l10n_it_edi` module must already be configured and working.
- The regular Italian (percentage) sale taxes must exist.

## Steps

1. **Enable OSS.** In *Accounting → Configuration → Settings*, *Taxes* section,
   enable **"EU Intra-community Distance Selling"** (`module_l10n_eu_oss`) and save:
   this installs `l10n_eu_oss`.

2. **Install `l10n_it_edi_oss`.** It depends on `l10n_it_edi` and `l10n_eu_oss`.
   On installation, a *post-init hook* automatically aligns any existing Italian OSS
   taxes, setting Natura **N3.2** and Law Reference **Art. 41 D.L. 331/1993**.

3. **Generate OSS taxes and fiscal positions.** Back in *Accounting → Configuration
   → Settings*, *Taxes* section, click **"Refresh tax mapping"**. This creates:
   - an `OSS B2C <Country>` fiscal position (auto-applied) for each EU
     destination country, excluding the company's own country and any country for
     which a foreign-VAT fiscal position already exists;
   - the OSS taxes with the destination country rate (rates from the `l10n_eu_oss`
     built-in map), placed in a dedicated tax group and account and flagged with the
     OSS tag.

4. **Verify the proposed mapping.**
   - *Accounting → Configuration → Fiscal Positions*: review the *"OSS B2C ..."*
     positions and their domestic-tax → OSS-tax mapping.
   - *Accounting → Configuration → Taxes*: review the created OSS taxes. Each Italian
     OSS tax must carry Natura **N3.2** (`l10n_it_exempt_reason`) and Law Reference
     **Art. 41 D.L. 331/1993** (`l10n_it_law_reference`). If you create OSS taxes
     manually, set these fields too.

## Behaviour on invoices

When you invoice a B2C customer in another EU country, the OSS fiscal position is
applied automatically and replaces the domestic tax with the destination OSS tax.
While generating the FatturaPA XML, `l10n_it_edi_oss` sets AliquotaIVA to 0.00,
Natura N3.2, an AltriDatiGestionali block with the actual rate, Imposta 0.00 in the
summary and the related RiferimentoNormativo.

## Notes

- The OSS threshold is **EUR 10,000 per year** of intra-community B2C sales: below it
  you may keep applying domestic VAT, above it OSS registration is mandatory. Odoo
  does not compute this threshold automatically.
- Click **"Refresh tax mapping"** again whenever you add new domestic sale taxes or
  after module updates.
