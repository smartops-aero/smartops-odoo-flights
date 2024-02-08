# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models, fields




class FlightAircraftMake(models.Model):
    _name = 'flight.aircraft.make'

    name = fields.Char()


class FlightAircraftModelTag(models.Model):
    _name = 'flight.aircraft.model.tag'
    name = fields.Char()

    # Examples:
    # retractable, high performance, pressurized, taa, propeller, turbine, jet, efis, aerobatic, tailwheel
    # turboprop will have turbiane and propeller
    # turbojet will have turbine and jet


class FlightAircraftModel(models.Model):
    _name = 'flight.aircraft.model'
    name = fields.Char()
    make_id = fields.Many2one("flight.aircraft.make")
    code = fields.Char("ICAO type code")
    tag_ids = fields.Many2many("flight.aircraft.model.tag")

    #  if   "Kg5700": is true - record 142000 lbs by defaukt as mtow (medium), otherwise record 12000 lbs by default (light)

    mtow = fields.Integer("Maximum take-off weight in pounds")

    def get_weight_category(self):
        if self.mtow >= 299200:
            return "H"
        elif self.mtow >= 12500:
            return "M"
        return "L"


    # TODO(ivank): add class and category models as per below
    # class_id = fields.Many2many()
    # category_id = fields.Many2many()


class FlightAircraft(models.Model):
    _name = 'flight.aircraft'
    _inherit = 'flight.base'
    _rec_name = 'registration'

    registration = fields.Char("Aircraft registration", unique=True)
    sn = fields.Char("Aircraft serial number")
    year = fields.Date("Year of manufacture")

    model_id = fields.Many2one("flight.aircraft.model")


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

    def _parse_mccpilotlog(self, flight_data):
        data = json.loads(flight_data.raw_text)
        meta = data.get("meta", {})
        return self._sync_flight_data(flight_data, {
            "registration": meta.get("Reference")
        })
