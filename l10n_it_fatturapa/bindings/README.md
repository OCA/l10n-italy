# Informazioni riguardanti la fatturazione elettronica

## Incongruenze rispetto alle specifiche del file xsd

* StringNNType: nelle specifiche da 1 a NN, lo SDI accetta da 0 a N
* Amount8DecimalType, Amount2DecimalType, RateType, QuantitaType sono xs:decimal
  ma la specifica vieta gli zeri finali, quindi li modifichiamo in xs:string

## Istruzioni per generazione nuovi bindings

* Scaricare il relativo xsd in locale
* Applicare la patch allegata, adattarla se necessario
* Generare i bindings utilizzando: `pyxbgen schema.xsd`
* Rimuovere i riferimenti locali dai file py con il comando (adattando l'url se differente):

  `sed -i -e "s,$(pwd),https://www\.fatturapa\.gov\.it/export/fatturazione/sdi/fatturapa/v1\.2\.1,g" *.py`

* rinominare `binding.py` in `fatturapa_v_1_2.py`
* in cima ai files generati sostiture il commento con il nome del file con la seguente riga:
  `# flake8: noqa`
* nel file `fatturapa_v_1_2` individuare la classe `DataFatturaType` ed aggiungere il seguente metodo:
* sostituire i files precedenti

```python
    # remove tzinfo from parsed dates or pyxb will fail the comparison
    def __new__(cls, *args, **kwargs):
        result = super(DataFatturaType, cls).__new__(cls, *args, **kwargs)
        return result.replace(tzinfo=None)
```

La patch dell'xsd modifica il range di caratteri delle stringhe portandolo da 1-N a 0-N,
trasforma in stringhe i decimali che hanno bisogno di zeri finali,
inoltre aggiungere il tipo documento TD20 (Autofattura).

Per la 1.2.1 inoltre corregge un errore di namespace.
