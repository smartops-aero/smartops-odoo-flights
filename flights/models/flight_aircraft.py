# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightAircraftClass(models.Model):
    _name = 'flight.aircraft.class'
    _description = 'Aircraft Category and Class'

    aircraft_category = fields.Selection([
        ('airplane', 'Airplane'),
        ('rotorcraft', 'Rotorcraft'),
        ('glider', 'Glider'),
        ('lighter_than_air', 'Lighter than Air'),
        ('powered_lift', 'Powered Lift'),
        ('powered_parachute', 'Powered Parachute'),
        ('weight_shift_control', 'Weight Shift Control')
    ], string='Aircraft Category', help='Select the category of the aircraft')

    name = fields.Char("Aircraft class")


class FlightAircraftMake(models.Model):
    _name = 'flight.aircraft.make'
    _description = 'Aircraft Make'

    name = fields.Char()


class FlightAircraftModelTag(models.Model):
    _name = 'flight.aircraft.model.tag'
    _description = 'Aircraft Model Tag'

    name = fields.Char()

    # Examples:
    # retractable, high performance, pressurized, taa, propeller, turbine, jet, efis, aerobatic, tailwheel
    # turboprop will have turbine and propeller = turboprop
    # turbojet will have turbine and jet = turbofan


class FlightAircraftModel(models.Model):
    _name = 'flight.aircraft.model'
    _description = 'Aircraft Model'

    name = fields.Char()
    make_id = fields.Many2one("flight.aircraft.make")
    class_id = fields.Many2one("flight.aircraft.class")

    engine_type = fields.Selection([
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('non_powered', 'Non-Powered'),
        ('piston', 'Piston'),
        ('radial', 'Radial'),
        ('turbofan', 'Turbofan'),
        ('turbojet', 'Turbojet'),
        ('turboprop', 'Turboprop'),
        ('turboshaft', 'Turboshaft')
    ], string='Engine Type', help='Select the engine type of the aircraft')

    gear_type = fields.Selection([
        ('amphibian', 'Amphibian (AM)'),
        ('fixed_tailwheel', 'Fixed Tailwheel (FC)'),
        ('fixed_tricycle', 'Fixed Tricycle (FT)'),
        ('floats', 'Floats (FL)'),
        ('retractable_tailwheel', 'Retractable Tailwheel (RC)'),
        ('retractable_tricycle', 'Retractable Tricycle (RT)'),
        ('skids', 'Skids'),
        ('skis', 'Skis')
    ], string='Gear Type', help='Select the gear type of the aircraft')

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


class FlightAircraft(models.Model):
    _name = 'flight.aircraft'
    _inherit = 'flight.base'
    _description = 'Aircraft'

    _rec_name = 'registration'

    registration = fields.Char("Aircraft registration")
    sn = fields.Char("Aircraft serial number")
    year = fields.Date("Year of manufacture")

    model_id = fields.Many2one("flight.aircraft.model")

    _sql_constraints = [
        ("registration_unique", "unique(registration)", "Aircraft with this registration number already exists!")
    ]

    equipment_type = fields.Selection([
        ('aircraft', 'Aircraft'),
        ('ffs', 'Full Flight Simulator (FFS)'),
        ('ftd', 'Flight Training Device (FTD)'),
        ('batd', 'Basic Aircraft Training Device (BATD)'),
        ('aatd', 'Advanced Aircraft Training Device (AATD)'),
    ], string='Equipment Type', default='aircraft')
