from odoo import models, api


class TrialBalanceReportCompute(models.TransientModel):
    _inherit = 'report_trial_balance_qweb'

    def _inject_account_group_values(self):
        query_inject_account_group = """
            INSERT INTO
                report_trial_balance_qweb_account
                (
                report_id,
                create_uid,
                create_date,
                account_group_id,
                parent_id,
                code,
                name,
                sequence,
                level
                )
            SELECT
                %s AS report_id,
                %s AS create_uid,
                NOW() AS create_date,
                accgroup.id,
                accgroup.parent_id,
                coalesce(accgroup.code_prefix, accgroup.name),
                accgroup.name,
                accgroup.parent_left * 100000,
                accgroup.level
            FROM
                account_group accgroup
            WHERE
                accgroup.cee_group = %s"""
        query_inject_account_params = (
            self.id,
            self.env.uid,
            'true' if self.env.context.get('cee_balance') else 'false'
        )
        self.env.cr.execute(query_inject_account_group,
                            query_inject_account_params)

    @api.multi
    def compute_data_for_report(self):
        res = super(TrialBalanceReportCompute, self).compute_data_for_report()
        return res
