# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).

import json

from odoo import fields, models, api

# TODO: move the models to individual files


class FlightBase(models.AbstractModel):
    _name = 'flight.base'

    flight_source_id = fields.Many2one("flight.data", unique=True, required=False)


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'flight.base']

    # {
    #   "user_id": 125880,
    #   "table": "Pilot",
    #   "guid": "00000000-0000-0000-0000-000000000756",
    #   "meta": {
    #     "Notes": "",
    #     "Active": true,
    #     "Company": "Wizz Air",
    #     "FavList": false,
    #     "UserAPI": "",
    #     "Facebook": "",
    #     "LinkedIn": "",
    #     "PilotRef": "",
    #     "PilotCode": "00000000-0000-0000-0000-000000000756",
    #     "PilotName": "SERAFIN G.",
    #     "PilotEMail": "",
    #     "PilotPhone": "",
    #     "Certificate": "",
    #     "PhoneSearch": "",
    #     "PilotSearch": "SERAFING",
    #     "RosterAlias": "",
    #     "Record_Modified": 1616320991
    #   },
    #   "platform": 9,
    #   "_modified": 1616317613
    # },

    def _parse_pilot_log_mcc(self, flight_data):
        data = json.loads(self.raw_text)
        meta = data.get("meta", {})
        return flight_data._data_write(self, {
            # TODO check mapping
            "name": meta.get("PilotName")
        })


class FlightData(models.Model):
    """Implements one way data syncronization, typically from a file.

       Key principles:
       * `source_model` is main Odoo model for current `flight.data` record.
       * single `flight.data` may create several records in different models
       * single `flight.data` may create only a single record in a specific model, because every model has a single field Many2one("flight.data")
    """

    _name = 'flight.data'
    _description = 'Flight Data Source'

    source_type = fields.Char(required=True)
    source_model = fields.Char(required=True)
    source_ref = fields.Char(required=True)
    raw_text = fields.Text(required=True)
    is_parsed = fields.Boolean("Parsed", default=False)

    _sql_constraints = [
        ("unique_ref",
         "unique(source_type,source_model,source_ref)",
         "Record mush unique reference"
        )
    ]

    def _data_parse(self):
        """Calls a method in corresponing Model"""
        self.ensure_one()
        model = self.env[self.source_model]
        method_name = '_parse_' + self.source_type
        if hasattr(model, method_name):
            return getattr(model, method_name)(self)
        else:
            raise NotImplementedError()

    def _search_linked_record(self, model):
        """Find a record that was created from this Data"""
        self.ensure_one()
        return model.search([
            ("flight_source_id", "=", self.id)
        ], limit=1)

    def _search_by_ref(self, source_type, model, ref):
        return self.search([
            ("source_type", "=", source_type),
            ("source_model", "=", model),
            ("source_ref", "=", ref),
        ], limit=1)

    def _data_write(self, model, vals):
        """Update record or create a new one"""
        self.ensure_one()
        record = self._search_linked_record(model)
        if record:
            record.write(vals)
        else:
            record = model.create(vals)
        return record


class FlightAirfield(models.Model):
    _name = 'flight.airfield'
    _inherit = 'flight.base'

    code = fields.Char()
    partner_id = fields.Char("Address")
    # TODO: check if want to add more fields
    # {
    #  "user_id": 125880,
    #  "table": "Airfield",
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

    def _parse_pilot_log_mcc(self, flight_data):
        data = json.loads(self.raw_text)
        meta = data.get("meta", {})
        partner = flight_data._data_write(self.env["res.partner"], {
            # TODO: check mapping
            "name": meta.get("AFName"),
        })
        return flight_data._data_write(self, {
            # TODO: check mapping
            "code": meta.get("AFIATA"),
            "partner_id": partner.id,
        })


class FlightAircraft(models.Model):

    _name = 'flight.aircraft'
    _inherit = 'flight.base'
    _rec_name = 'registration'

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
    def _parse_pilot_log_mcc(self, flight_data):
        data = json.loads(self.raw_text)
        meta = data.get("meta", {})
        return flight_data._data_write(self, {
            "registration": meta.get("Reference")
        })


class FlightNumber(models.Model):
    _name = 'flight.number'
    _inherit = 'flight.base'

    operator_id = fields.Many2one('flight.operator')
    numbers = fields.Char()


class FlightOperator(models.Model):
    _name = 'flight.operator'
    _inherit = 'flight.base'

    name = fields.Char("Prefix")
    description = fields.Char()


class FlightCrew(models.Model):
    _name = 'flight.crew'
    _inherit = 'flight.base'

    partner_id = fields.Many2one('res.partner')
    role_id = fields.Many2one('flight.crew.role')
    flight_id = fields.Many2one('flight.flight')


class FlightCrewRole(models.Model):
    _name = 'flight.crew.role'
    _inherit = 'flight.base'

    code = fields.Char()
    description = fields.Char()


class FlightFlight(models.Model):
    _name = 'flight.flight'
    _inherit = 'flight.base'

    aircraft_id = fields.Many2one('flight.aircraft')
    flight_number_id = fields.Many2one('flight.number')
    crew_ids = fields.One2many('flight.crew', 'flight_id')

    departure_id = fields.Many2one('flight.airfield')
    event_ids = fields.One2many('flight.event', 'flight_id')
    arrival_id = fields.Many2one('flight.airfield')

    # {
    #   "user_id": 125880,
    #   "table": "Flight",
    #   "guid": "00000000-0000-0000-0000-000000009218",
    #   "meta": {
    #     "PF": true,
    #     "Pax": 0,
    #     "Fuel": 0,
    #     "DeIce": false,
    #     "Route": "",
    #     "ToDay": 1,
    #     "minU1": 0,
    #     "minU2": 0,
    #     "minU3": 0,
    #     "minU4": 0,
    #     "minXC": 0,
    #     "ArrRwy": "",
    #     "DepRwy": "",
    #     "LdgDay": 1,
    #     "LiftSW": 0,
    #     "P1Code": "00000000-0000-0000-0000-000000000001",
    #     "P2Code": "00000000-0000-0000-0000-000000000000",
    #     "P3Code": "00000000-0000-0000-0000-000000000000",
    #     "P4Code": "00000000-0000-0000-0000-000000000000",
    #     "Report": "",
    #     "TagOps": "",
    #     "ToEdit": false,
    #     "minAIR": 0,
    #     "minCOP": 0,
    #     "minIFR": 0,
    #     "minIMT": 0,
    #     "minPIC": 0,
    #     "minREL": 0,
    #     "minSFR": 0,
    #     "ArrCode": "00000000-0000-0000-0000-000000009693",
    #     "DateUTC": "1998-03-16",
    #     "DepCode": "00000000-0000-0000-0000-000000009693",
    #     "HobbsIn": 0,
    #     "Holding": 0,
    #     "Pairing": "",
    #     "Remarks": "intro C150 keurig",
    #     "SignBox": 0,
    #     "ToNight": 0,
    #     "UserNum": 0,
    #     "minDUAL": 60,
    #     "minEXAM": 0,
    #     "CrewList": "",
    #     "DateBASE": "1998-03-15",
    #     "FuelUsed": 0,
    #     "HobbsOut": 0,
    #     "LdgNight": 0,
    #     "NextPage": false,
    #     "TagDelay": "",
    #     "Training": "",
    #     "UserBool": false,
    #     "UserText": "",
    #     "minINSTR": 0,
    #     "minNIGHT": 0,
    #     "minPICUS": 0,
    #     "minTOTAL": 60,
    #     "ArrOffset": 60,
    #     "DateLOCAL": "1998-03-16",
    #     "DepOffset": 60,
    #     "TagLaunch": "",
    #     "TagLesson": "",
    #     "ToTimeUTC": 0,
    #     "ArrTimeUTC": 0,
    #     "BaseOffset": -99,
    #     "DepTimeUTC": 0,
    #     "FlightCode": "00000000-0000-0000-0000-000000009218",
    #     "LdgTimeUTC": 0,
    #     "FuelPlanned": 0,
    #     "NextSummary": false,
    #     "TagApproach": "",
    #     "AircraftCode": "00000000-0000-0000-0000-000000000367",
    #     "ArrTimeSCHED": 0,
    #     "DepTimeSCHED": 0,
    #     "FlightNumber": "",
    #     "FlightSearch": "19980316:LEYLEY",
    #     "Record_Modified": 1616320991
    #   },
    #   "platform": 9,
    #   "_modified": 1616317613
    # },

    def _parse_pilot_log_mcc(self, flight_data):
        data = json.loads(self.raw_text)
        meta = data.get("meta", {})
        # TODO
        return flight_data._data_write(self, {
        })


class FlightEvent(models.Model):
    _name = 'flight.event'
    _inherit = 'flight.base'

    flight_id = fields.Many2one('flight.flight')
    event_type = fields.Many2one('flight.event.type')

    scheduled_date = fields.Datetime()
    estimated_date = fields.Datetime()
    target_date = fields.Datetime()
    requested_date = fields.Datetime()
    actual_date = fields.Datetime()


class FlightEventType(models.Model):
    _name = 'flight.event.type'
    _inherit = 'flight.base'

    code = fields.Char()
    description = fields.Char()
