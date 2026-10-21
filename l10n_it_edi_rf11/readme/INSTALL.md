## Fresh install (Odoo 18, no prior 74-ter data)

Install the module normally, from **Apps** or with:

```bash
odoo -c <odoo.conf> -d <DB> -i l10n_it_edi_rf11 --stop-after-init
```

It depends on `l10n_it_edi_sender_partner`, which transitively pulls in core
`l10n_it_edi` + `l10n_it_edi_extension`.

## Upgrade from Odoo 16 (DB that had `l10n_it_fatturapa_out_rf11`)

This module is the Odoo 18 successor of the Odoo 16 module
`l10n_it_fatturapa_out_rf11`. It ships a `pre_init_hook`
(`pre_absorb_old_module`) that **renames the old module into this one**,
merging its `ir.model.data` and preserving every 74-ter value. All fields keep
identical column names across versions, on core models:

- `res.partner`: `is_74ter_agent`, `agent_74ter_id`, `invoices_paid_by_agent`
- `res.company`: `payments_74ter_journal_id`
- `account.move`: `agent_74ter_id`, `to_be_paid_by_agent_74ter`

### Best way — mark it for install *in the migration run itself*

Because `l10n_it_edi_rf11` is a **new module name** in v18, Odoo treats it as a
fresh install (migration scripts under `migrations/` never run for a
first-time install — only `pre_init_hook` does). You must therefore add it with
`-i` to the **same OpenUpgrade invocation** that upgrades the rest of the DB:

```bash
odoo -c <odoo.conf> -d <DB> -u all -i l10n_it_edi_rf11 \
     --stop-after-init --no-http
```

(with your usual OpenUpgrade environment/config). Apply the `-i` **only to
customer databases where `l10n_it_fatturapa_out_rf11` was installed**;
installing it elsewhere is harmless (the hook is a no-op) but pointless.

**Why the same run matters — ordering guarantee.** In a single Odoo run,
modules being installed execute their `pre_init_hook` while the load graph is
processed; modules that no longer exist in the code (here:
`l10n_it_fatturapa_out_rf11`) are flagged *to remove* and are uninstalled only
at the **end** of that same run. So the rename fires *first* and the old
module is absorbed before the obsolete-module cleanup could drop its columns —
no data is lost.

### After the upgrade — verify

- `l10n_it_fatturapa_out_rf11` is gone from **Apps**; `l10n_it_edi_rf11` is
  installed.
- The 74-ter flags/fields listed above are preserved on partners, company and
  posted invoices.
- Company *RegimeFiscale* RF11 is set: `res.company.l10n_it_tax_system = 'RF11'`.
  This is migrated **separately** by `l10n_it_edi_extension` (from the v16
  `fatturapa_fiscal_position.code`), which runs ahead of this module via the
  dependency chain — this module does **not** touch it.
