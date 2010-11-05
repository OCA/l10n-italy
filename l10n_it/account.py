from osv import fields, osv

class account_account_template(osv.osv):
    _inherit = "account.account.template"
    _columns =  {
        'child_consol_ids': fields.many2many('account.account.template', 'account_account_template_consol_rel', 'child_id', 'parent_id', 'Consolidated Children'),
    }
account_account_template()

class wizard_multi_charts_accounts(osv.osv_memory):
    _inherit = 'wizard.multi.charts.accounts'
    _columns = {
        'chart_template_id': fields.many2one('account.chart.template', 'Chart Template', required=True, readonly=True),
        }
    _defaults = {
        'code_digits': lambda *a:0,
    }
    def execute(self, cr, uid, ids, context=None):
        super(wizard_multi_charts_accounts, self).execute(cr, uid, ids, context=None)

        obj_multi = self.browse(cr, uid, ids[0])
        obj_acc = self.pool.get('account.account')
        obj_acc_template = self.pool.get('account.account.template')
        obj_acc_chart = self.pool.get('account.chart.template')
        company_id = obj_multi.company_id.id
        acc_template_ref = {}
        #cerco tutti gli account.chart.template diversi da quello creato dal wizard di default
        chart_template_ids = obj_acc_chart.search(cr, uid, [('id', '!=', obj_multi.chart_template_id.id)])
        for chart_template_id in chart_template_ids:
            #genero il pdc consolidato
            chart_template = obj_acc_chart.browse(cr, uid, chart_template_id)
            children_acc_template = obj_acc_template.search(cr, uid, [('parent_id','child_of',[chart_template.account_root_id.id]),('nocreate','!=',True)])
            children_acc_template.sort()
            for account_template in obj_acc_template.browse(cr, uid, children_acc_template):
                tax_ids = []
                for tax in account_template.tax_ids:
                    tax_ids.append(tax_template_ref[tax.id])
                dig = 0
                code_main = account_template.code and len(account_template.code) or 0
                code_acc = account_template.code or ''
                if code_main>0 and code_main<=dig and account_template.type != 'view':
                    code_acc=str(code_acc) + (str('0'*(dig-code_main)))
                vals={
                    'name': (chart_template.account_root_id.id == account_template.id) and chart_template.name or account_template.name,
                    'currency_id': account_template.currency_id and account_template.currency_id.id or False,
                    'code': code_acc,
                    'type': account_template.type,
                    'user_type': account_template.user_type and account_template.user_type.id or False,
                    'reconcile': account_template.reconcile,
                    'shortcut': account_template.shortcut,
                    'note': account_template.note,
                    'parent_id': account_template.parent_id and ((account_template.parent_id.id in acc_template_ref) and acc_template_ref[account_template.parent_id.id]) or False,
                    'tax_ids': [(6,0,tax_ids)],
                    'company_id': company_id,
                }
                
                if(account_template.child_consol_ids):
                    #scrivo i consolidati in account.account prendendoli da account.template
                    account_id = obj_acc.search(cr, uid, [('code','=',code_acc)])
                    child_consol_ids = []
                    for child in account_template.child_consol_ids:
                        child_consol_ids.append(child.id)
                    vals['child_consol_ids'] = [(6, 0, child_consol_ids)]

                new_account = obj_acc.create(cr, uid, vals)
                acc_template_ref[account_template.id] = new_account

wizard_multi_charts_accounts()
