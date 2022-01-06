#  Copyright 2022 Simone Rubino - Takobi
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import odoo.tests


@odoo.tests.common.tagged('post_install', '-at_install')
class TestEPOS(odoo.tests.HttpCase):

    def test_close_and_report(self):
        """Execute close_and_report tour."""
        user_admin = self.env.ref('base.user_admin')
        env = self.env(user=user_admin)
        main_pos_config = env.ref('point_of_sale.pos_config_main')
        main_pos_config.open_session_cb()

        tour_service = "odoo.__DEBUG__.services['web_tour.tour']"
        self.browser_js(
            "/pos/web",
            "%s.run('close_and_report')" % tour_service,
            "%s.tours.close_and_report.ready" % tour_service,
            login="admin",
        )
