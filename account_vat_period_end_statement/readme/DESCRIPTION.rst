**Italiano**

    Per fare la liquidazione IVA, aprire Fatturazione > Contabilità > Liquidazioni IVA, il menù è visibile solo quando è abilitato il gruppo 'Mostrare funzionalità contabili complete'.
    Selezionare un registro che conterrà le registrazioni contabili della liquidazione.
    Il campo 'Conto IVA erario' contiene il conto dove verrà effettuata la registrazione della liquidazione IVA.

    L'oggetto 'Liquidazione IVA' permette di specificare ogni importo e il conto utilizzato dalla liquidazione.
    Di norma, gli importi di debito e credito delle imposte vengono caricati automaticamente dai periodi selezionati
    (vedere Configurazione per generare correttamente i periodi).
    I debiti e crediti precedenti vengono caricati dalle liquidazioni IVA precedenti, in base allo stato del loro pagamento.

    A seguito dell’introduzione della normativa OSS, per chi fa vendite online su diversi paesi, deve necessariamente escludere dalla liquidazione iva ciò che farà parte della liquidazione OSS.
    E’ stato introdotto un nuovo campo per filtrare le imposte da elaborare, quindi va indicato il conto configurato nelle imposte  “Conto utilizzato per la liquidazione IVA”.
    Quindi selezionare il conto IVA debito per elaborare liquidazione iva su tutte le imposte che hanno in configurazione il conto IVA debito.  Per la liquidazione OSS invece selezionare conto  dedicato ad esempio IVA debito OSS Francia.
    E’ necessario creare un periodo di dichiarazione IVA dedicato all’OSS .
    Per caricare invece tutte le imposte che hanno un conto per la liquidazione IVA, è sufficiente lasciare vuoto il filtro per conti.

    Per creare la registrazione contabile, fare clic sul pulsante 'Crea movimento', dentro la scheda 'Conti'.
    Se i termini di pagamento sono impostati viene scritta anche la scadenza (o le scadenze).

    La scheda 'Erario' contiene informazioni sui pagamenti,
    qui si possono visualizzare i risultati della liquidazione ('Importo IVA erario')
    e l'importo residuo da pagare ('Importo a saldo').
    La liquidazione può essere pagata come qualunque altro debito, con la riconciliazione delle registrazioni contabili.

    È inoltre possibile stampare la liquidazione IVA facendo clic su Stampa > Stampa liquidazione IVA.

**English**

    In order to create a 'VAT Statement', open Accounting > Adviser > VAT Statements, this menu is only visible when the group 'Show Full Accounting Features' is enabled.
    Select a Journal that will contain the journal entries of the statement.
    The field 'Tax authority VAT' account contains the account where the statement balance will be registered.

    The 'VAT statement' object allows to specify every amount and relative account
    used by the statement.
    By default, amounts of debit and credit taxes are automatically loaded
    from taxes of the selected periods (see Configuration to correctly generate the periods).
    Previous debit or credit is loaded from previous VAT statement, according
    to its payments status.

    Following the introduction of the OSS legislation, for those who make online sales in different countries, it must necessarily exclude from the VAT settlement what will be part of the OSS settlement.
    A new field has been introduced to filter the taxes to be processed, so the account configured in the taxes "Account used for VAT settlement" must be indicated.
    Then select the VAT debit account to process VAT settlement on all taxes that have the VAT debit account in setup.
    For OSS settlement, on the other hand, select a dedicated account, for example, OSS debit VAT France. It is necessary to create a VAT return period dedicated to the OSS.
    To load all taxes that have a VAT settlement account instead, just leave the filter by accounts blank.

    In order to generate the journal entry, click on 'Create move' button, inside the 'Accounts' tab.
    If you select a payment term, the due date(s) will be set.

    The 'tax authority' tab contains information about payment(s),
    here you can see statement's result ('authority VAT amount') and residual
    amount to pay ('Balance').
    The statement can be paid like every other debit, by journal item
    reconciliation.

    It is also possible to print the 'VAT statement' clicking on print > Print VAT period end statement.
