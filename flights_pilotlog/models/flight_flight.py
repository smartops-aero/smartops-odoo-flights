# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, api


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    pilot_activity_ids = fields.One2many('flight.pilot.activity', 'flight_id')
    pilottime_ids = fields.One2many('flight.pilottime', 'flight_id')
    flight_time = fields.Integer("Flight Time", compute='_compute_flight_time')
    total_time = fields.Integer("Total Flight Time", compute='_compute_flight_time')

    @api.depends('pilottime_ids')
    def _compute_flight_time(self):
        for flight in self:
            # TODO: check computation
            flight.flight_time = sum(record.minutes for record in flight.pilottime_ids if record.time_kind_id.name in ["DUAL", "PIC"])
            flight.total_time = sum(record.minutes for record in flight.pilottime_ids if record.time_kind_id.name == "TOTAL")
