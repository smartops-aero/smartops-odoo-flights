# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, api


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    pilot_activity_ids = fields.One2many('flight.pilot.activity', 'flight_id')
    pilottime_ids = fields.One2many('flight.pilottime', 'flight_id')
    pilot_note_ids = fields.One2many('flight.pilot.note', 'flight_id')
    flight_time = fields.Integer("Flight Time", compute='_compute_flight_time')
    total_time = fields.Integer("Total Flight Time", compute='_compute_flight_time')

    @api.depends('pilottime_ids')
    def _compute_flight_time(self):
        for flight in self:
            # TODO: check computation
            flight.flight_time = sum(pt.minutes for pt in flight.pilottime_ids if pt.time_kind_id.name in ["DUAL", "PIC"])
            flight.total_time = sum(pt.minutes for pt in flight.pilottime_ids if pt.time_kind_id.name == "TOTAL")

    def _check_errors(self):
        self.ensure_one()
        result = super()._check_errors()
        # Check total time
        if self.flight_time > self.total_time:
            result.append("DUAL + PIC > TOTAL")
        # Check Pilottime
        for pt in self.pilottime_ids:
            if (pt.minutes > self.total_time):
                result.append(f"{pt.time_kind_id.name} > TOTAL!")

        return result

    def get_pilottime_by_code(self, code):
        self.ensure_one()
        return self.pilottime_ids.filtered(lambda r: r.time_kind_id.name == code).minutes or 0
    def get_pilot_activity_by_code(self, code):
        self.ensure_one()
        return self.pilot_activity_ids.filtered(lambda r: r.kind_id.code == code).count or 0

    def get_note_by_code(self, code):
        self.ensure_one()
        return self.pilot_note_ids.filtered(lambda r: r.kind == code).text
