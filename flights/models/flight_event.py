# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
# TODO: move the models to individual files
from odoo import fields, models, api


class FlightNumber(models.Model):
    _name = 'flight.number'
    _inherit = 'flight.base'
    _description = 'Flight Number'

    prefix_id = fields.Many2one('flight.prefix')
    numbers = fields.Char()

    @api.depends("prefix_id.name", "numbers")
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"{r.prefix_id.name} {r.numbers}"


class FlightPrefix(models.Model):
    _name = 'flight.prefix'
    _inherit = 'flight.base'
    _description = 'Flight Number Prefix'

    name = fields.Char("Prefix")
    description = fields.Char()


class FlightEventTime(models.Model):
    _name = 'flight.event.time'
    _inherit = 'flight.base'
    _description = 'Flight Event Time'

    flight_id = fields.Many2one('flight.flight')
    event_id = fields.Many2one('flight.event')

    kind = fields.Selection([
        ("S", "Scheduled"),
        ("T", "Target"),
        ("E", "Estimated"),
        ("A", "Actual"),
        ("R", "Requested"),
    ], "Kind", required=True, default="A")

    time = fields.Datetime()

    def _compute_time(self):
        # display time portion only HH:MM but append +/- days difference with the flight
        # e.g. 01:15+1 - landing time next day
        # self.time.date - self.flight_id.date => append after time or skip if same / 0
        pass

    def _compute_display_name(self):
        return f"{self.kind}{self.event_id.code}T {self._compute_time()}".upper()


class FlightEvent(models.Model):
    _name = 'flight.event'
    _description = 'Flight Event'
    _inherit = 'flight.base'
    _rec_name = 'code'

    code = fields.Char()
    description = fields.Char()
