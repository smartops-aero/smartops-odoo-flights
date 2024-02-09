# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightPilotTime(models.Model):
    _name = 'flight.pilot_time'

    partner_id = fields.Many2many('res.partner',) # Different pilots on the same flight will log different times

    flight_id = fields.Many2one('flight.flight')
    kind_id = fields.Many2one('flight.pilot_time.kind')
    minutes = fields.Integer("Number of minutes")


class FlightPilotTimeKind(models.Model):
    _name = 'flight.pilot_time.kind'

    code = fields.Char()
