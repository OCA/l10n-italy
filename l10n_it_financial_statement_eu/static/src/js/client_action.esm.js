/** @odoo-module **/
import {ReportAction} from "@web/webclient/actions/reports/report_action";
import {patch} from "web.utils";

const MODULE_NAME = "l10n_it_financial_statement_eu";

patch(ReportAction.prototype, "l10n_it_financial_statement_eu.ReportAction", {
    setup() {
        this._super.apply(this, arguments);
        this.isFinancialStatementEU = this.props.report_name.startsWith(
            `${MODULE_NAME}.`
        );
    },

    export_fseu_xlsx() {
        this.action.doAction({
            type: "ir.actions.report",
            report_type: "xlsx",
            report_name: "l10n_it_financial_statement_eu.fseu_xlsx_report",
            report_file: "Financial statement EU",
            data: this.props.data || {},
            context: this.props.context || {},
            display_name: this.title,
        });
    },

    export_fseu_xbrl() {
        this.action.doAction({
            type: "ir.actions.report",
            report_type: "qweb-xml",
            report_name: "l10n_it_financial_statement_eu.fseu_xbrl_report",
            report_file: "XBRL-financial-statements",
            data: this.props.data || {},
            context: this.props.context || {},
            display_name: this.title,
        });
    },
});
