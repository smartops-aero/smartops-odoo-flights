# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightFlight(models.Model):
    _name = 'flight.flight'
    _inherit = 'flight.base'
    _rec_name = 'flight_number_id'

    aircraft_id = fields.Many2one('flight.aircraft')

    flight_number_id = fields.Many2one('flight.number')
    operator = fields.Many2many("res.partner")

    crew_ids = fields.One2many('flight.crew', 'flight_id')
    pax_ids = fields.Many2many("res.partner", "flight_id")

    departure_id = fields.Many2one('flight.aerodrome')
    arrival_id = fields.Many2one('flight.aerodrome')
    event_ids = fields.One2many('flight.event', 'flight_id')

    parameter_ids = fields.One2Many()




FlightParameterType():

hobbs_in
hobbs_out
oil_before
oil_after
fuel_before
fiel_after
