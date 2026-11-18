Supporto alla liquidazione IVA per le agenzie di viaggio e turismo secondo
l'art. 74-ter, DPR 633/72 (regime speciale del margine). Vedi anche il modulo
`l10n_it_edi_rf11` per la parte di fatturazione elettronica.

L'IVA 74-ter non si calcola "imposta da imposta" (IVA sulle vendite − IVA sugli
acquisti) come nella liquidazione ordinaria, ma **sul margine**, con il metodo
detto **"base su base"**: si sottrae la *base imponibile* degli acquisti dalla
*base imponibile* delle vendite e sul margine così ottenuto si scorpora l'IVA.
Il calcolo viene effettuato mensilmente. Se il risultato è a credito viene
memorizzato e riportato alla liquidazione successiva; se a debito viene
generata la scrittura contabile (esempio più sotto) e l'IVA a debito concorre
alla liquidazione IVA ordinaria. La stampa del resoconto di liquidazione IVA
viene integrata con una sezione dedicata "74 Ter".

**Calcolo "base su base"**

1. **Le imposte 74-ter sono aliquote allo 0%.** Non devono esporre IVA in
   fattura (l'operazione è a margine): servono solo a *identificare e
   accumulare la base imponibile* delle vendite e degli acquisti 74-ter
   (imposta contrassegnata da `is_tax_74ter`). L'aliquota effettiva (es. 22%)
   è memorizzata a parte nel campo `tax_74ter_amount` e usata solo in
   liquidazione.

2. **Margine = base vendite − base acquisti.** In `compute_amounts` si somma la
   base imponibile (`base_balance`) del periodo: le vendite hanno segno
   positivo, gli acquisti negativo, quindi la somma è il margine lordo
   (IVA inclusa).

3. **Scorporo dell'IVA dal margine:**

   ```
   net_tax_74_ter    = margine / (1 + aliquota/100)   # margine netto
   tax_74_ter_amount = margine − net_tax_74_ter        # IVA 74-ter sul margine
   ```

4. **Segno del risultato:**
   - a **debito** (margine > 0): viene registrata la scrittura
     `tax_74_ter_move_id` e l'importo confluisce nella liquidazione ordinaria;
   - a **credito** (margine < 0): non si registra nulla e il valore viene
     riportato al periodo successivo (`tax_74_ter_amount_previous`).

**Esempio numerico**

Vendite 74-ter (base) € 3.660, acquisti 74-ter (base) € 1.220, aliquota 22%:

| Voce                          | Importo |
|-------------------------------|--------:|
| Base vendite                  |  3.660  |
| Base acquisti                 | −1.220  |
| **Margine (lordo)**           | **2.440** |
| Margine netto (2.440 / 1,22)  |  2.000  |
| **IVA 74-ter (2.440 − 2.000)**| **440** |

**Scritture contabili**

1) All’atto della liquidazione IVA 74 ter mensile **a debito**

Con i dati dell'esempio sopra, IVA 74 ter scorporata dal margine = € 440,00.
Il modulo genera automaticamente la scrittura (`tax_74_ter_move_id`):

                       Dare     Avere
0301009 Iva 74 Ter     440,00
0115001 IVA C/Vendite            440,00

Il conto 0301009 Iva 74 Ter è un conto di ricavo, in quanto va a rettificare il
valore dei ricavi delle vendite dei viaggi UE. Accreditando IVA C/Vendite, i
€ 440,00 si sommano all'IVA a debito e concorrono alla liquidazione IVA
ordinaria del periodo.

In caso di 74 ter **a credito** (margine negativo) non viene registrata alcuna
scrittura: il credito viene riportato alla liquidazione successiva.

2) Come i € 440,00 confluiscono nella liquidazione IVA ordinaria

Nella liquidazione mensile ordinaria l'IVA C/Vendite comprende ora anche i
€ 440,00 della scrittura 74 ter e viene chiusa contro l'IVA C/Acquisti; la
differenza costituisce l'IVA a debito (erario) o a credito del periodo.
