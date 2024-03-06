# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import pytz

from odoo import fields, models, api
from odoo.addons.base.models.res_partner import _tz_get

TIME_KIND2VALUE = {
    "S": 0,
    "T": 100,
    "E": 200,
    "A": 300,
    "R": 400,
}


class FlightEventTime(models.Model):
    """
    All events times are in UTC
    """
    _name = 'flight.event.time'
    _inherit = 'flight.base'
    _description = 'Flight Event Time'
    _order = "sequence"

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
    # overnight = fields.Integer()
    # tz = fields.Selection(_tz_get, compute="_compute_display_time", store=True)
    display_time = fields.Char(compute="_compute_display_time", store=True)
    sequence = fields.Integer(compute="_compute_sequence", store=True)

    @api.depends("kind_id.sequence", "time_kind")
    def _compute_sequence(self):
        for record in self:
            record.sequence = TIME_KIND2VALUE[record.time_kind] + record.kind_id.sequence

    @api.depends("time", "overnight", "kind_id.is_arrival")
    def _compute_display_time(self):
        # display time portion only HH:MM but append +/- days difference with the flight
        # e.g. 01:15+1 - landing time next day
        # self.time.date - self.flight_id.date => append after time or skip if same / 0
        for record in self:
            overnight = 0
            if record.kind_id.is_arrival:
                overnight = record.overnight
                aerodrome = record.flight_id.arrival_id
            else:
                aerodrome = record.flight_id.departure_id
            record.tz = aerodrome.partner_id.tz or "UTC"
            time = pytz.utc.localize(record.time).astimezone(pytz.timezone(record.tz))
            time_str = time.strftime('%H:%M')
            if overnight:
                time_str += f' (+{overnight})'
            record.display_time = time_str

    @api.depends("time_kind", "kind_id.code", "display_time")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.time_kind}{record.kind_id.code}T {record.display_time}".upper()


class FlightEventKind(models.Model):
    _name = 'flight.event.kind'
    _description = 'Flight Event Kind'
    _inherit = 'flight.base'
    _rec_name = 'code'

    code = fields.Char()
    description = fields.Char()
    # is_arrival = fields.Boolean()
    sequence = fields.Integer()


class FlightDurationKind(models.Model):
    start_event = fields.One2many("event")
    end_event = fields.One2many("event")
    name = fields.Char()

