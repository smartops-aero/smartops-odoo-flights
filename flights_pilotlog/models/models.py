# Copyright 2024 Ivan Kropotkin <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models

# TODO: move the models to individual files


class FlightAircraft(models.Model):
    _inherit = 'flight.aircraft'

    make_id = fields.Many2one("flight.aircraft.make")
    model_id = fields.Many2one("flight.aircraft.model")


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    period_ids = fields.One2many("flight.period", 'flight_id')


class FlightAircraftMake(models.Model):
    _name = 'flight.aircraft.make'

    name = fields.Char()


class FlightAircraftModel(models.Model):
    _name = 'flight.aircraft.model'

    name = fields.Char()


class FlightPeriod(models.Model):
    _name = 'flight.period'

    flight_id = fields.Many2one('flight.flight')
    period_type_id = fields.Many2one('flight.period.type')
    duration = fields.Integer(help="Duration in minutes")
    # TODO: check if we need more models


class FlightPeriodType(models.Model):
    _name = 'flight.period.type'

    code = fields.Char()
