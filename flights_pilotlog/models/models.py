# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models

# TODO: move the models to individual files


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


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    pilot_time_ids = fields.One2many("flight.pilot_time", 'flight_id')


class FlightPilotTime(models.Model):
    _name = 'flight.pilot_time'
    partner_id = fields.Many2many('res.partner',) # Different pilots on the same flight will log different times

    flight_id = fields.Many2one('flight.flight')
    kind_id = fields.Many2one('flight.pilot_time.kind')
    minutes = fields.Integer("Number of minutes")
    # TODO: check if we need more models

class FlightPilotEvent(models.Model):
    flight_id = fields.Many2many('flight.flight')
    kind_id =
    count = fields.Integer()

class FlightPilotEventKind(models.Model):
    # e.g. landing_night, landing day, takefoff_night, takeoff_day, holding, approach


class FlightPilotNote(models.Model):
    flight_id = fields.Many2many('flight.flight')
   # note = text()
   hobbs_in = fields.Float()
   hobbs_out = fields.Float()
   # signature = Image / OCA sign module

class FlightPilotTimeKind(models.Model):
    _name = 'flight.pilot_time.kind'

    code = fields.Char()
