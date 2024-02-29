# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightPilotActivity(models.Model):
    _name = "flight.pilot.activity"
    _description = 'Flight Pilot Activity'

    flight_id = fields.Many2many('flight.flight')
    kind_id = fields.Many2one('flight.pilot.activity.kind')
    count = fields.Integer('Count')


class FlightPilotActivityKind(models.Model):
    # e.g. landing_night, landing day, takefoff_night, takeoff_day, holding, approach
    _name = 'flight.pilot.activity.kind'
    _description = 'Flight Pilot Activity Kind'

    code = fields.Char()
    description = fields.Char()
