## Fresh install (Odoo 18, no prior 74-ter data)

Install the module normally, from **Apps** or with:

```bash
odoo -c <odoo.conf> -d <DB> -i l10n_it_account_vat_period_end_settlement_rf11 \
     --stop-after-init
```

It depends on `l10n_it_account_vat_period_end_settlement` (the Odoo 18 VAT
settlement module) and `account_tax_balance`.

## Upgrade from Odoo 16 (DB that had `account_vat_period_end_statement_rf11`)

This module is the Odoo 18 successor of the Odoo 16 module
`account_vat_period_end_statement_rf11`. It ships a `pre_init_hook`
(`pre_absorb_old_module`) that **renames the old module into this one**,
merging its `ir.model.data` and preserving every 74-ter value. All fields keep
identical column names across versions:

- `account.tax`: `is_tax_74ter`, `tax_74ter_amount`, `tax_74_ter_income_account_id`
- `account.vat.period.end.statement`: `tax_74_ter_move_id`, `net_tax_74_ter`,
  `tax_74_ter_amount`, `tax_74_ter_amount_previous`, `tax_74_ter_amount_total`

### Best way — mark it for install *in the migration run itself*

Because `l10n_it_account_vat_period_end_settlement_rf11` is a **new module
name** in v18, Odoo treats it as a fresh install (migration scripts under
`migrations/` never run for a first-time install — only `pre_init_hook` does).
Add it with `-i` to the **same OpenUpgrade invocation** that upgrades the rest
of the DB, so the rename happens before the obsolete v16 module is purged:

```bash
odoo -c <odoo.conf> -d <DB> -u all \
     -i l10n_it_account_vat_period_end_settlement_rf11 \
     --stop-after-init --no-http
```

Apply the `-i` **only to customer databases where
`account_vat_period_end_statement_rf11` was installed**; installing it
elsewhere is harmless (the hook is a no-op) but pointless.

**Ordering guarantee.** In a single Odoo run, modules being installed execute
their `pre_init_hook` while the load graph is processed; modules that no longer
exist in the code are flagged *to remove* and are uninstalled only at the
**end** of that same run. The base module
`l10n_it_account_vat_period_end_settlement` (our dependency) absorbs the v16
`account_vat_period_end_statement` the same way and, being a dependency, loads
first — so the base rename precedes ours, and no data is lost.

### After the upgrade — verify

- `account_vat_period_end_statement_rf11` is gone from **Apps**;
  `l10n_it_account_vat_period_end_settlement_rf11` is installed.
- The 74-ter fields listed above are preserved on taxes and settlements.

> Note (behaviour change vs v16): `account.tax.vat_statement_account_id` was
> removed in Odoo 18, so the 74-ter settlement entry now sources its VAT
> account from the sale tax's repartition lines (`_get_debit_accounts()`),
> the same source the VAT settlement uses for its debit lines.
