# Informazioni riguardanti la fatturazione elettronica

## Istruzioni per generazione nuovi bindings

* Scaricare il relativo xsd in locale o copiare il file che si trova nella cartella xsd
* Generare i bindings utilizzando: `pyxbgen schema.xsd`
* Rimuovere i riferimenti locali dai file py con il comando (adattando l'url se differente):

  `sed -i -e "s,$(pwd)/Schema_del_file_xml_FatturaPA_versione_1\.2\.1\.xsd,https://www\.agenziaentrate\.gov\.it/wps/file/Nsilib/Nsi/Schede/Comunicazioni/Fatture+e+corrispettivi/Fatture+e+corrispettivi+ST/ST+invio+di+fatturazione+elettronica/ST+Fatturazione+elettronica+-+Schema+VFPR12\./Schema_VFPR12\.xsd,g" *.py`

* in cima ai files generati sostiture il commento con il nome del file con la seguente riga:
  `# flake8: noqa`
* sostituire i files precedenti
* applicare le seguenti modifiche che si trovano nel file `bindings.diff`
