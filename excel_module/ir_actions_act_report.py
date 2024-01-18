from odoo import api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class Report(models.Model):
    _inherit = 'ir.actions.report'

    report_type = fields.Selection(selection_add=[('excel', 'Excel')])

    def render_excel(self, ids, data=None):
        model = self.model
        records = self.env[model].browse(ids)
        report_object = self.env['report.' + self.report_name]
        if getattr(report_object, 'excel_as_binary', False):
            content = report_object.excel_as_binary(records)
        else:
            RES = report_object.excel(records)
            if isinstance(RES, dict):
                RES = (RES, {})
            if len(RES) != 2:
                raise Exception("Please return (data, options) as tuple.")
            data, options = RES
            assert isinstance(data, dict), "Returned Data must be of type dict!"
            content = self.env['excel.maker'].create_excel(self.env, data, **options)
        return content, 'xlsx'