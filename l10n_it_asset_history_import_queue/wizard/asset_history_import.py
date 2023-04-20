from odoo import _, models
from odoo.exceptions import ValidationError


class AssetHistoryImport(models.TransientModel):
    _inherit = "wizard.asset.history.import"

    def import_file(self):
        """Imports the `file` content"""
        self.with_delay().import_file_queued()
        self.env.user.notify_info(
            message="Job queued", title="Import asset history", sticky=False
        )

    def import_file_queued(self):
        """Imports the `file` content"""
        try:
            self.check_before_import()
            file_data, workbook, sheet = self.parse_file()
            assets = self.import_assets_from_data(file_data, workbook, sheet)
            if not assets:
                self.env.user.notify_warning(
                    message="Nothing could be imported.",
                    title="Import asset history",
                    sticky=True,
                )
                raise ValidationError(_("Nothing could be imported."))

            self.env.user.notify_success(
                message="Import asset done.",
                title="Import asset history",
                sticky=True,
            )

        except Exception as e:
            self.env.user.notify_danger(
                message="Error: {}".format(str(e)),
                title="Import asset history",
                sticky=True,
            )
