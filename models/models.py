# -*- coding: utf-8 -*-
from odoo import models, fields, api
import qrcode
import uuid

class certificates(models.Model):
    _name = 'certificates'
    _description = 'Certificates'
    x_uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), readonly=True)
    x_client = fields.Many2one('res.partner', string="Client", default=lambda self: self.env.user.partner_id.id)
    x_emisor = fields.Many2one('res.partner', string="Emisor", default=None)
    x_client_name = fields.Char(string="Client name", related='x_client.name', store=True)
    x_description = fields.Char(string="Description")
    x_emision_date = fields.Date(string="Emision date")
    x_expiration_date = fields.Date(string="Expiration date")
    x_status = fields.Selection([
        ('Solicitado', 'Solicitado'),
        ('Activo', 'Activo'),
        ('Expirado', 'Expirado'),
        ('Revocado', 'Revocado'),
    ], string='State', default='Solicitado')
    
    @api.model
    def _check_expiration_dates(self):
        today = fields.Date.today()
        expired_certificates = self.search([('x_expiration_date', '<', today), ('x_status', '!=', 'Expirado')])
        for cert in expired_certificates:
            cert.x_status = 'Expirado'

    @api.model
    def _cron_check_expiration_dates(self):
        self._check_expiration_dates()