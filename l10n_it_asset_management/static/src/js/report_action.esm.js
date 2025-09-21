import {ReportAction} from "@web/webclient/actions/reports/report_action";
import {patch} from "@web/core/utils/patch";

const MODULE_NAME = "l10n_it_asset_management";

patch(ReportAction.prototype, {
    setup() {
        super.setup(...arguments);
        this.isAssetReport = this.props.report_name.startsWith(`${MODULE_NAME}.`);
    },

    /**
     * Override of method _get_xlsx_name in account_financial_report/static/src/js/report_action.esm.js
     * to manage assets reports.
     * @param {String} str
     * @returns {String}
     */
    _get_xlsx_name(str) {
        if (!this.isAssetReport) return super._get_xlsx_name(...arguments);

        if (typeof str !== "string") {
            return str;
        }
        const parts = str.split(".");
        const qweb_report = parts[1];
        let xlsx_report = "";
        switch (qweb_report) {
            case "template_asset_previsional_qweb":
            case "template_asset_previsional_html":
                xlsx_report = "report_asset_previsional_xlsx";
                break;
            case "template_asset_journal_qweb":
            case "template_asset_journal_html":
                xlsx_report = "report_asset_journal_xlsx";
                break;
        }
        return `${MODULE_NAME}.` + xlsx_report;
    },
});
