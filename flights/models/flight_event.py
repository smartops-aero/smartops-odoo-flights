# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, api


class FlightEventTime(models.Model):
    _name = 'flight.event.time'
    _inherit = 'flight.base'
    _description = 'Flight Event Time'

    flight_id = fields.Many2one('flight.flight')
    kind_id = fields.Many2one('flight.event.kind', 'Flight Event Kind')

    time_kind = fields.Selection([
        ("S", "Scheduled"),
        ("T", "Target"),
        ("E", "Estimated"),
        ("A", "Actual"),
        ("R", "Requested"),
    ], "Time Kind", required=True, default="A")

    time = fields.Datetime()

    def _compute_time(self):
        # display time portion only HH:MM but append +/- days difference with the flight
        # e.g. 01:15+1 - landing time next day
        # self.time.date - self.flight_id.date => append after time or skip if same / 0
        pass

    def _compute_display_name(self):
        return f"{self.kind}{self.event_id.code}T {self._compute_time()}".upper()


class FlightEventKind(models.Model):
    _name = 'flight.event.kind'
    _description = 'Flight Event Kind'
    _inherit = 'flight.base'
    _rec_name = 'code'

    code = fields.Char()
    description = fields.Char()
