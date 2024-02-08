# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
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
    code = fields.Char("ICAO type code")  # TODO: can we just use name field for that ?
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
    # class_id = fields.Many2many()  # TODO: why not Selection / Integer ?
    # category_id = fields.Many2many() # TODO: why not Selection ?


class FlightAircraft(models.Model):
    _name = 'flight.aircraft'
    _inherit = 'flight.base'
    _rec_name = 'registration'

    registration = fields.Char("Aircraft registration", unique=True)
    sn = fields.Char("Aircraft serial number")
    year = fields.Date("Year of manufacture")

    model_id = fields.Many2one("flight.aircraft.model")
