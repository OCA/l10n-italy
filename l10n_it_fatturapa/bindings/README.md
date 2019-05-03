# Informazioni riguardanti la fatturazione elettronica

## Incongruenze rispetto alle specifiche del file xsd

* StringNNType: nelle specifiche da 1 a NN, lo SDI accetta da 0 a N
* Amount8DecimalType, Amount2DecimalType, RateType, QuantitaType sono xs:decimal
  ma la specifica vieta gli zeri finali, quindi li modifichiamo in xs:string

## Istruzioni per generazione nuovi bindings

* Scaricare il relativo xsd in locale o copiare il file che si trova nella cartella xsd
* Applicare la patch allegata, adattarla se necessario, nota il file in xsd include già le patch
* Generare i bindings utilizzando: `pyxbgen schema.xsd`
* Rimuovere i riferimenti locali dai file py con il comando (adattando l'url se differente):

  `sed -i -e "s,$(pwd),https://www\.fatturapa\.gov\.it/export/fatturazione/sdi/fatturapa/v1\.2\.1,g" *.py`

* in cima ai files generati sostiture il commento con il nome del file con la seguente riga:
  `# flake8: noqa`
* sostituire i files precedenti

La patch del file xsd trasforma in stringhe in decimali che hanno bisogno di zeri finali
e aggiunge il tipo documento TD20 (Autofattura).

Per la 1.2.1 inoltre corregge un errore di namespace.
