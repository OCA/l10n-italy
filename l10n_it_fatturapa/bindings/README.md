# Informazioni riguardanti la fatturazione elettronica

## Istruzioni per generazione nuovi bindings

* Scaricare il relativo xsd in locale o copiare il file che si trova nella cartella xsd
* Generare i bindings utilizzando: `pyxbgen <link>`
* sostituire nei file diff il _GenerationUID con quello creato da pyxbgen
* in cima ai files generati sostiture le righe:
  ```
  # ./_ds.py
  # -*- coding: utf-8 -*-
  ```
  con la sequente riga:
  `# flake8: noqa`
* sostituire i files precedentemente creati `_ds.py` e `binding.py`
* applicare le seguenti modifiche che si trovano nei files `bindings.diff` e `_ds.diff`
