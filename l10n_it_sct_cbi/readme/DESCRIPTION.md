This module adds new payment export types to use in the payment order.
For italian credit transfer, the format codes are
- CBIBdyPaymentRequest.00.04.01
- CBIBdyCrossBorderPaymentRequest.00.01.01

The created XML follows the CBI standards in https://www.cbi-org.eu/My-Menu/Servizio-CBI-Documentazione/Servizio-CBI-Documentazione-Standard.

Note (ITA):

Le specifiche CBI del bonifico XML SEPA (versione 00.04.01) si basano sul messaggio ISO20022 pain.001.001.09 e sono compliant al Rulebook SEPA.

Ad esempio la presenza obbligatoria dell’ABI della banca di addebito contenuto nel campo “MmbId” che è invece facoltativo nel tracciato ISO.
