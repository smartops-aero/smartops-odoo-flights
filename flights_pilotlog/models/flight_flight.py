# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, api


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    pilot_activity_ids = fields.One2many('flight.pilot.activity', 'flight_id')
    pilottime_ids = fields.One2many('flight.pilottime', 'flight_id')
    pilot_note_ids = fields.One2many('flight.pilot.note', 'flight_id')

    def _check_errors(self):
        self.ensure_one()
        result = super()._check_errors()
        # Check Pilottime
        for pt in self.pilottime_ids:
            if (pt.minutes > self.total_duration):
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
