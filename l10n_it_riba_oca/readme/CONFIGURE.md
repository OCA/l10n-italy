**Italiano**

Nella configurazione delle RiBa è possibile specificare se si tratti di
'Salvo buon fine' o 'Al dopo incasso', che hanno un flusso completamente
diverso.

- Al dopo incasso: le fatture risulteranno pagate all'accettazione;
  l'incasso potrà essere registrato con una normale riconciliazione bancaria,
  che andrà a chiudere gli "effetti attivi" aperti all'accettazione.
- Salvo buon fine: le registrazioni generate seguiranno la struttura
  descritta nel documento <http://goo.gl/jpRhJp>

È possibile specificare diverse configurazioni (dal menù *Configurazione
→ Pagamenti → Configurazione RiBa*). Per ognuna, in caso di 'Salvo buon
fine', è necessario specificare almeno il registro e il conto da
utilizzare al momento dell'accettazione della distinta da parte della
banca. Tale conto deve essere di tipo 'Crediti' (ad esempio "RiBa
all'incasso", eventualmente da creare).
Selezionando 'Salvo buon fine' è necessario impostare il tipo di
incasso, immediato o a maturazione valuta: questo influisce sulla gestione
degli insoluti perchè solo nel caso di incasso immediato vengono stornate
le registrazioni di presentazione della RiBa.

La configurazione relativa alla fase di accredito, verrà usata nel
momento in cui la banca accredita l'importo della distinta. È possibile
utilizzare un registro creato appositamente, ad esempio "Accredito
RiBa", e un conto chiamato ad esempio "Banche c/RiBa all'incasso", che
non deve essere di tipo 'Banca e cassa'.

La configurazione relativa all'insoluto verrà utilizzata in caso di
mancato pagamento da parte del cliente. Il conto può chiamarsi ad
esempio "Crediti insoluti".

Nel caso si vogliano gestire anche le spese per ogni scadenza con
ricevuta bancaria, si deve configurare un prodotto di tipo servizio e
collegarlo in *Configurazione → Impostazioni → Contabilità → Imposte →
Spese di incasso RiBa*.

**Spese di incasso per cliente**

Sulla scheda del cliente (*Contatti*), nella sezione **RiBa**, sono
disponibili due campi che governano l'addebito delle spese di incasso al
momento della conferma della fattura:

- **Escludi spese Ri.Ba.** (`riba_exclude_expenses`): se attivo, al
  cliente non viene mai addebitata alcuna spesa di incasso, qualunque sia
  la politica impostata.
- **Politica spese Ri.Ba.** (`riba_policy_expenses`): determina quante
  righe spesa vengono aggiunte alla fattura. Le opzioni disponibili sono:

| Politica (etichetta / chiave) | Quante spese per fattura | Comportamento tra fatture diverse |
|---|---|---|
| One expense per maturity — `unlimited` | una per ogni scadenza | nessuna deduplicazione: tutte le scadenze di tutte le fatture vengono sempre addebitate |
| One expense per invoice — `one_per_invoice` | una sola, a prescindere dal numero di scadenze | nessuna deduplicazione: ogni fattura riceve la propria spesa |
| One expense per maturity month — `one_a_month` (default) | una per ciascun mese in cui cade una scadenza | salta la spesa se quel mese è già coperto da una scadenza di un'altra fattura del cliente |
| One expense per invoice month — `one_a_maturity_invoice_month` | una sola, a prescindere dal numero di scadenze | salta la spesa se nello stesso mese della data fattura esiste già un'altra fattura del cliente con spesa |
| One expense per maturity month, dedup within invoice month — `maturity_per_invoice_month` | una per ogni mese di scadenza | salta la spesa se nello stesso mese della data fattura esiste già un'altra fattura con una scadenza nello **stesso mese** |

La deduplicazione considera solo le fatture del cliente **già
confermate** che riportano una riga spesa: l'ordine di conferma delle
fatture quindi è rilevante.
