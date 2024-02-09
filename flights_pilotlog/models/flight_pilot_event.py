# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightPilotEvent(models.Model):
    flight_id = fields.Many2many('flight.flight')
    # kind_id =
    count = fields.Integer()


class FlightPilotEventKind(models.Model):
    # e.g. landing_night, landing day, takefoff_night, takeoff_day, holding, approach
    _name = 'flight.pilot.event.kind_id'

