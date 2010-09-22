
from osv import osv
from osv import fields

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    _columns = {
        'fiscalcode': fields.char('Fiscal Code', size=16, help="Italian Fiscal Code"),
        }
hr_employee()
