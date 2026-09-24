**English**

Support for the VAT scheme of article 74-ter, DPR 633/72 (travel agencies and
tour operators) in the Italian electronic invoice (FatturaPA).

Operators that organise travel through the sale of "travel packages" (travel
agencies and tour operators) are subject to the special VAT scheme of art.
74-ter, DPR 633/72.

The tour operator issues the ordinary electronic invoice on behalf of the
intermediary travel agency. That invoice represents the commission the tour
operator owes the agency and replaces the vendor bill the agency would
otherwise issue to the tour operator.

The invoice is emitted as `TipoDocumento` TD01 with `RegimeFiscale` RF11,
showing that it is issued on behalf of the agency (the *Terzo Intermediario o
Soggetto Emittente* and *Soggetto Emittente* blocks), and carrying the VAT
nature code N3.6 for non-taxable operations, or N6.9 for travel within the EU,
in place of the VAT rate.

The module also lets the tour operator flag that a customer invoice is paid by
the agency, transferring the customer receivable to the agency.

**Italiano**

Supporto al regime IVA dell'art. 74-ter, DPR 633/72 (agenzie viaggi e turismo)
nella fattura elettronica (FatturaPA).

Gli operatori economici che effettuano attività di organizzazione di viaggi
attraverso la vendita di "pacchetti turistici" (agenzie di viaggio e tour
operator) devono adempiere ad uno speciale regime di applicazione dell'IVA. Si
tratta del regime disciplinato dall'art. 74-ter del DPR n. 633/72 legato
all'organizzazione in proprio di pacchetti turistici o di commercio in proprio
di pacchetti turistici acquistati da altri soggetti.

https://def.finanze.it/DocTribFrontend/decodeurn?urn=urn:doctrib::DPR:1972-10-26;633_art74ter

Il tour operator compila la fattura elettronica ordinaria, evidenziando che la
stessa è emessa per conto dell'agenzia viaggi intermediaria. Tale fattura
rappresenta le provvigioni che il tour operator deve corrispondere all'agenzia
viaggi e sostituisce la fattura passiva che l'agenzia viaggi presenterebbe al
tour operator.

Nel dettaglio il tour operator compila la fattura elettronica ordinaria
("TipoDocumento" TD01 e "RegimeFiscale" RF11 "Agenzie viaggi e turismo
(art.74-ter, DPR 633/72)") evidenziando che la stessa è emessa per conto
dell'agenzia viaggi intermediaria (valorizzando i blocchi "Terzo Intermediario
o Soggetto emittente" e "Soggetto emittente") ed inserendo, in luogo
dell'aliquota IVA, il codice natura N3.6 se la fattura riguarda operazioni non
imponibili o il codice N6.9 se il viaggio è nell'UE.

Il modulo consente inoltre di indicare che una fattura cliente è pagata
dall'agenzia, trasferendo il credito dal cliente all'agenzia.
