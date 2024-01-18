import base64
from odoo import http
from odoo.http import request
from odoo.http import content_disposition
from odoo.tools.safe_eval import safe_eval as eval
from datetime import time

class ExcelReportController(http.Controller):

    @http.route('/excel_report/<report_name>', auth='user', type="http")
    def get_excel_report(self, report_name, model=None, res_id=None, **post):
        try:
            res_id = int(res_id)
        except Exception:
            if ',' in (res_id or ""):
                res_id = res_id.split(',')
                res_id = [int(x) for x in res_id]
            else:
                res_id = None

        report = request.env['ir.actions.report'].sudo().search([
            ('report_name', '=', report_name),
        ])
        if report.report_type != 'excel':
            return

        content = report.render_excel(res_id)[0]

        object = request.env[report.model].browse(res_id)

        name = report_name + '.xlsx'
        if report.print_report_name:
            name = eval(report.print_report_name, {'object': object, 'time': time})

        return http.request.make_response(content, [
            ('Content-Type', 'application/octet-stream; charset=binary'),
            ('Content-Disposition', content_disposition(name))
        ])
