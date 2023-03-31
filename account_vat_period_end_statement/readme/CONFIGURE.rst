**Italiano**

    Per generare i periodi della dichiarazione IVA,
    aprire Fatturazione > Configurazione > Contabilità > Intervalli date > Generazione intervalli data (visibile solo in modalità debug):

    * prefisso nome intervallo: prefisso identificativo per i periodi da generare (tipicamente l'anno)
    * durata: 1 mese
    * numero di intervalli da generare: 12
    * tipo: creare un tipo o utilizzarne uno esistente, non è richiesta una configurazione particolare
    * data iniziale: primo giorno del primo periodo che sarà generato (tipicamente il primo giorno dell'anno i.e. 01/01/2018)

    Per caricare l'importo corretto, un'imposta deve essere associata al conto utilizzato nella liquidazione:

    #. aprire l'imposta da Fatturazione > Configurazione > Contabilità > Imposte,
    #. nella scheda 'Opzioni avanzate' selezionare il conto corretto (ad esempio IVA debito)
       per il campo 'Conto utilizzato per la liquidazione IVA'.

    Per calcolare gli interessi, è possibile aggiungere le informazioni da utilizzare (conto e percentuale)
    nei dati aziendali, nella scheda 'Liquidazione IVA'.

**English**

    In order to generate VAT statement's periods,
    open Accounting > Configuration > Accounting > Date ranges > Generate Date Ranges (visible only in debug mode):

    * range name prefix: prefix identifying the periods to be generated (usually the year)
    * duration: 1 month
    * number of ranges to generate: 12
    * type: create a type or use an existing one, no specific configuration is required
    * date start: first day of the first period to be generated (usually the first day of the year e.g. 01/01/2018)

    In order to load the correct amount from tax, the tax has to be
    associated to the account involved in the statement:

    #. open a tax in Accounting > Configuration > Accounting > Taxes,
    #. in the tab 'Advanced Options' select the correct account (for instance the account debit VAT)
       for the field 'Account used for VAT statement'.

    If you need to calculate interest, you can add default information in your
    company data (percentage and account), in the 'VAT statement' tab.
