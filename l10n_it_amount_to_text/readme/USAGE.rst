**Italiano**

Chiamare la funzione ``amount_to_text`` nel modello valuta (``res.currency``).

Per esempio, se è necessario convertire un importo in testo aggiungere questo codice ai report::

    <t t-foreach="docs" t-as="o">
        <t t-set="currency" t-value="o.currency_id"/>
        # Language obtained from context
        <t t-esc="currency.with_context({'lang': 'it_IT'}).amount_to_text(45.75)"/>

        # Language obtained from user/partner settings.
        # If not it_IT, Odoo core amount_to_text will be used.
        <t t-esc="currency.amount_to_text(45.75)"/>
    </t>

**English**

Call function ``amount_to_text`` in currency model (``res.currency``).

For example, add this code if you need to convert amount to text in your reports::

    <t t-foreach="docs" t-as="o">
        <t t-set="currency" t-value="o.currency_id"/>
        # Language obtained from context
        <t t-esc="currency.with_context({'lang': 'it_IT'}).amount_to_text(45.75)"/>

        # Language obtained from user/partner settings.
        # If not it_IT, Odoo core amount_to_text will be used.
        <t t-esc="currency.amount_to_text(45.75)"/>
    </t>
