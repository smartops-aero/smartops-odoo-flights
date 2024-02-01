# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models, api

# TODO: move the models to individual files


class FlightOperator(models.Model):
    _name = 'flight.operator'

    code = fields.Char()
    partner_id = fields.Char("Address")
    # TODO: check if want to add more fields
    # {
    #  "user_id": 125880,
    #  "table": "Operator",
    #  "guid": "00000000-0000-0000-0000-000000040048",
    #  "meta": {
    #    "AFCat": 8,
    #    "AFCode": "00000000-0000-0000-0000-000000040048",
    #    "AFIATA": "NKT",
    #    "AFICAO": "LTCV",
    #    "AFName": "Sirnak Serafettin Elci",
    #    "TZCode": 333,
    #    "Latitude": 37218,
    #    "ShowList": false,
    #    "AFCountry": 223,
    #    "Longitude": -42036,
    #    "NotesUser": "ATIS 128.400",
    #    "RegionUser": 0,
    #    "ElevationFT": 0,
    #    "Record_Modified": 1616320991
    #  },
    #  "platform": 9,
    #  "_modified": 1616317613
    # },


class FlightAircraft(models.Model):

    _name = 'flight.aircraft'

    registration = fields.Char("Registration number")
    # TODO: check if want to add more fields
    # {
    #   "user_id": 125880,
    #   "table": "Aircraft",
    #   "guid": "00000000-0000-0000-0000-000000000367",
    #   "meta": {
    #     "Fin": "",
    #     "Sea": false,
    #     "TMG": false,
    #     "Efis": false,
    #     "FNPT": 0,
    #     "Make": "Cessna",
    #     "Run2": false,
    #     "Class": 5,
    #     "Model": "C150",
    #     "Power": 1,
    #     "Seats": 0,
    #     "Active": true,
    #     "Kg5700": false,
    #     "Rating": "",
    #     "Company": "Other",
    #     "Complex": false,
    #     "CondLog": 69,
    #     "FavList": false,
    #     "Category": 1,
    #     "HighPerf": false,
    #     "SubModel": "",
    #     "Aerobatic": false,
    #     "RefSearch": "PHALI",
    #     "Reference": "PH-ALI",
    #     "Tailwheel": false,
    #     "DefaultApp": 0,
    #     "DefaultLog": 2,
    #     "DefaultOps": 0,
    #     "DeviceCode": 1,
    #     "AircraftCode": "00000000-0000-0000-0000-000000000367",
    #     "DefaultLaunch": 0,
    #     "Record_Modified": 1616320991
    #   },
    #   "platform": 9,
    #   "_modified": 1616317613
    # },


class FlightNumber(models.Model):
    _name = 'flight.number'

    airline_id = fields.Many2one('flight.airline')
    numbers = fields.Char()


class FlightAirline(models.Model):
    _name = 'flight.airline'

    name = fields.Char("Prefix")
    description = fields.Char()


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

    departure_id = fields.Many2one('flight.operator')
    event_ids = fields.One2many('flight.event', 'flight_id')
    arrival_id = fields.Many2one('flight.operator')


class FlightEvent(models.Model):
    _name = 'flight.event'

    event_type = fields.Many2one('flight.event.type')

    scheduled_date = fields.Datetime()
    estimated_date = fields.Datetime()
    target_date = fields.Datetime()
    requested_date = fields.Datetime()
    actual_date = fields.Datetime()



class FlightEventType(models.Model):
    _name = 'flight.event.type'

    code = fields.Char()
    description = fields.Char()
