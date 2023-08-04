import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_vat_period_end_statement>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_abicab>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_account>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_account_stamp>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_account_tax_kind>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_appointment_code>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_ateco>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_declaration_of_intent>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_delivery_note>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_delivery_note_base>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fatturapa>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fatturapa_in>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fatturapa_out>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fatturapa_out_di>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fiscal_document_type>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fiscal_payment_term>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_fiscalcode>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_ipa>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_payment_reason>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_pec>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_rea>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_sdi_channel>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_vat_payability>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_website_portal_ipa>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_withholding_tax>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_withholding_tax_reason>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
