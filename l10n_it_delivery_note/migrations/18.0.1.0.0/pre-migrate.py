from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.is_module_installed(env.cr, "l10n_it_delivery_note_base"):
        openupgrade.update_module_names(
            env.cr,
            [("l10n_it_delivery_note_base", "l10n_it_delivery_note")],
            merge_modules=True,
        )
