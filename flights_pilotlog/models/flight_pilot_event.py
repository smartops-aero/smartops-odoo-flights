# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightPilotEvent(models.Model):
    _name = "flight.pilot.event"

    flight_id = fields.Many2many('flight.flight')
    kind_id = fields.Many2one('flight.pilot.event.kind')
    count = fields.Integer('Count')


class FlightPilotEventKind(models.Model):
    # e.g. landing_night, landing day, takefoff_night, takeoff_day, holding, approach
    _name = 'flight.pilot.event.kind'
    _description = 'Flight Pilot Event Kind'

    code = fields.Char()
    description = fields.Char()
