# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# from io import BytesIO
# from reportlab.pdfgen import canvas

class MyModule(http.Controller):

    @http.route(['/my/mis_certificados'], type='http', auth="user", website=True)
    def my_portalCertificatesListView(self, **kw):
        certificates = request.env['certificates'].search([('x_client', '=', request.env.user.partner_id.id)])
        return request.render('my_portal.certificates', {'certificates': certificates})

    @http.route(['/my/request_certificate'], type='http', auth="user", website=True)
    def my_portalCertificatesForm(self, **kw):
        return request.render('my_portal.request_certificate')

    @http.route(['/my/certificates/create'], type='http', auth="user", methods=['POST'], website=True)
    def create_certificate(self, **post):
        request.env['certificates'].sudo().create({
            'x_client': request.env.user.partner_id.id,
            'x_description': post.get('x_description'),
            'x_status': 'Solicitado',
        })
        return '<script>window.location = "/my/mis_certificados";</script>'

    @http.route(['/my/check_certificate'], type='http', auth="public", website=True)
    def my_portalCheckCertificates(self, **kw):
        certificate = request.env['certificates'].search([('x_uuid', '=', kw.get('UUID')), ('x_status', '=', 'Activo')])
        return request.render('my_portal.check_certificates', {'certificate': certificate})

    @http.route(['/my/certificate'], type='http', auth="public", website=True)
    def my_portalCertificate(self, **kw):
        certificate = request.env['certificates'].search([('x_uuid', '=', kw.get('UUID')), ('x_status', '=', 'Activo')])
        return request.render('my_portal.see_certificate', {'certificate': certificate})

    @http.route(['/my/printCertificate'], type='http', auth="user", website=True)
    def pruebas(self, **kw):
        certificate = request.env['certificates'].sudo().search([('x_uuid', '=', kw['UUID']), ('x_status', '=', 'Activo')])
        if not certificate.exists():
            return request.not_found()

        report_ref = request.env.ref('my_portal.my_pdf_report')
        if not report_ref:
            return request.not_found()

        pdf_content, _ = report_ref.sudo()._render_qweb_pdf(report_ref, certificate.id)
        pdf_http_headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content))
        ]
        return request.make_response(pdf_content, headers=pdf_http_headers)