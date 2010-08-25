from osv import fields, osv

class account_account_template(osv.osv):
    _inherit = "account.account.template"
    _columns =  {
        'child_consol_ids': fields.many2many('account.account.template', 'account_account_template_consol_rel', 'child_id', 'parent_id', 'Consolidated Children'),
    }
account_account_template()

class wizard_multi_charts_accounts(osv.osv_memory):
    _inherit = 'wizard.multi.charts.accounts'
    def execute(self, cr, uid, ids, context=None):
#        import pdb;pdb.set_trace()
        super(wizard_multi_charts_accounts, self).execute(cr, uid, ids, context=None)
wizard_multi_charts_accounts()
