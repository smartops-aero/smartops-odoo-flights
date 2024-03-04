# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields, api


class FlightFlight(models.Model):
    _name = 'flight.flight'
    _inherit = 'flight.base'
    _description = 'Flight'

    _rec_name = 'flight_number_id'

    aircraft_id = fields.Many2one('flight.aircraft')
    date = fields.Date()

    flight_number_id = fields.Many2one('flight.number')
    operator_id = fields.Many2one("res.partner", "Operator Company")

    crew_ids = fields.One2many('flight.crew', 'flight_id', "Crew")
    pax_ids = fields.Many2many("res.partner", string="Passengers")

    departure_id = fields.Many2one('flight.aerodrome')
    arrival_id = fields.Many2one('flight.aerodrome')
    event_time_ids = fields.One2many('flight.event.time', 'flight_id', string="Flight Timing")

    param_ids = fields.One2many('flight.flight.param', 'flight_id')

    @api.depends("aircraft_id", "date")
    def _compute_display_name(self):
        for record in self:
            # TODO check timezone for date
            record.display_name = f"{record.aircraft_id.registration}: {record.date}"


class FlightFlightParam(models.Model):
    _name = 'flight.flight.param'
    _inherit = 'flight.base'
    _description = 'Flight Parameter'

    flight_id = fields.Many2one('flight.flight')
    param_type_id = fields.Many2one('flight.flight.param.type')
    value = fields.Float()


class FlightFlightParamType(models.Model):
    _name = 'flight.flight.param.type'
    _description = 'Flight Parameter Type'

    name = fields.Char()
    code = fields.Char()


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
