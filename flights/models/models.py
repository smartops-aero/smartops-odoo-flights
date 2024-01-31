# Copyright 2024 Ivan Kropotkin <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models

# TODO: move the models to individual files


class FlightAirport(models.Model):
    _name = 'flight.airport'

    code = fields.Char()
    partner_id = fields.Char("Address")


class FlightAircraft(models.Model):
    _name = 'flight.aircraft'

    registration = fields.Char("Registration number")


class FlightNumber(models.Model):
    _name = 'flight.number'

    airline_id = fields.Many2one('flight.airline')
    prefix = fields.Char()
    numbers = fields.Char()


class FlightAirline(models.Model):
    _name = 'flight.airline'

    name = fields.Char()
    default_prefix = fields.Char(help="Default prefix assigned on creating a new flight.number for this airline")


class FlightCrew(models.Model):
    _name = 'flight.crew'

    partner_id = fields.Many2one('res.partner')
    role_id = fields.Many2one('flight.crew.role')


class FlightCrewRole(models.Model):
    _name = 'flight.crew.role'

    code = fields.Char()
    description = fields.Char()


class FlightFlight(models.Model):
    _name = 'flight.flight'

    aircraft_id = fields.Many2one('flight.aircraft')
    flight_number_id = fields.Many2one('flight.number')
    crew_ids = fields.One2many('flight.crew', 'flight_id')

    departure_id = fields.Many2one('flight.airport')
    event_ids = fields.One2many('flight.event', 'flight_id')
    arrival_id = fields.Many2one('flight.airport')


class FlightEvent(models.Model):
    _name = 'flight.event'

    event_type = fields.Many2one('flight.event.type')
    actual_date = fields.Datetime()
    estimated_date = fields.Datetime()
    scheduled_date = fields.Datetime()
    target_date = fields.Datetime()


class FlightEventType(models.Model):
    _name = 'flight.event.type'

    code = fields.Char()
    description = fields.Char()
