# Informazioni riguardanti la fatturazione elettronica

## Istruzioni per generazione nuovi bindings

* Scaricare il relativo xsd in locale o copiare il file che si trova nella cartella xsd
* Generare i bindings utilizzando: `pyxbgen schema.xsd`
* Rimuovere i riferimenti locali dai file py con il comando (adattando l'url se differente):

  `sed -i -e "s,$(pwd),https://www\.fatturapa\.gov\.it/export/fatturazione/sdi/fatturapa/v1\.2\.1,g" *.py`

* in cima ai files generati sostiture il commento con il nome del file con la seguente riga:
  `# flake8: noqa`
* sostituire i files precedenti
