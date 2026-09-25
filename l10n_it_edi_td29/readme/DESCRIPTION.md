**Italiano**

Questo modulo aggiunge il supporto al tipo documento TD29 per la fatturazione elettronica italiana.

La TD29 è la "Comunicazione per la regolarizzazione delle fatture non emesse o irregolari" prevista dall'art. 6, comma 8, del D.Lgs. 471/97.

Quando il flag **TD29** è attivato su una fattura fornitore, il documento viene esportato con:

- `<TipoDocumento>TD29</TipoDocumento>`
- `<CodiceDestinatario>0000000</CodiceDestinatario>` (indirizzato al Sistema di Interscambio)

Per questo tipo di documento è necessario configurare un sezionale dedicato (giornale con propria sequenza di numerazione), da utilizzare separatamente dal sezionale delle fatture ordinarie.
