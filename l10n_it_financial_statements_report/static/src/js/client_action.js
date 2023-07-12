odoo.define("l10n_it_financial_statements_report.client_action", function (require) {
    "use strict";

    var AFRReportAction = require("account_financial_report.client_action");
    var core = require("web.core");

    const ReportAction = AFRReportAction.include({
        on_click_export: function () {
            const MODULE_NAME = "l10n_it_financial_statements_report";

            if (this.report_name.startsWith(`${MODULE_NAME}.`)) {
                // Call our report action
                // instead of the action dynamically generated
                // from account_financial_report.
                var action = {
                    type: "ir.actions.report",
                    report_type: "xlsx",
                    report_name: "l10n_it_financial_statements_report.report_xlsx",
                    report_file: "l10n_it_financial_statements_report.report_xlsx",
                    data: this.data,
                    context: this.context,
                    display_name: this.title,
                };
                return this.do_action(action);
            }

            return this._super.apply(this, arguments);
        },
    });

    core.action_registry.add(
        "l10n_it_financial_statements_report.client_action",
        ReportAction
    );

    return ReportAction;
});
