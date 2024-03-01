# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


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
    event_time_ids = fields.One2many('flight.event.time', 'flight_id')

    param_ids = fields.One2many('flight.flight.param', 'flight_id')


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
