English
~~~~~~~~~~~~~~~~~

**Configuration**

You need to configure a bank account for the company that makes the payment, having at least the following data:

- IBAN
- BIC
- CUC

In addition, it is necessary to create a payment *mode* dedicated to the SEPA Credit Transfer, selecting SEPA CBI Credit Transfer to Suppliers as a *method*, automatically created upon module installation.

This method is already configured to use the correct PAIN version (Pain.00.04.00).


**Operation**

When creating a supplier invoice, you must select the created SCT payment mode as a way of payment of the same.

The invoice field *Payment reference* contains information that will be reported in the payment order field *Communication*, which is a mandatory field for the payment to be issued.

Once the invoice is confirmed, it is necessary to add it to a payment order.

Confirming the payment order, you can create and export the XML file for the bank.



Italiano
~~~~~~~~~~~~~~~~~

**Configurazione**

È necessario configurare un conto bancario per l'azienda che esegue il pagamento, che abbia almeno le seguenti informazioni:

- IBAN
- BIC
- CUC

Inoltre è necessario creare una *modalità* di pagamento dedicata al bonifico SEPA, selezionando come *metodo* "Bonifico SEPA CBI a fornitori", creato automaticamente all'installazione del modulo.

Questo metodo è già configurato per utilizzare la corretta versione PAIN (pain.00.04.00).


**Operatività**

Quando si crea una fattura fornitore bisogna selezionare come modo di pagamento della stessa la modalità di pagamento SEPA SCT creata.

Il campo della fattura *Riferimento di pagamento* contiene informazioni che verranno riportate nel campo *Comunicazione* dell'ordine di pagamento, che è un campo obbligatorio perché il pagamento venga emesso.

Quindi, una volta confermata, è necessario aggiungere la fattura a un ordine di pagamento.

Una volta confermato l'ordine di pagamento, è possibile creare ed esportare il file XML da passare alla banca.
