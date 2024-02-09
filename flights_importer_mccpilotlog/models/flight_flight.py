# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models


FLIGHT_TIME_MAP = {
    "minU1": "flights_pilotlog.flight_time_type_u1",
    "minU2": "flights_pilotlog.flight_time_type_u2",
    "minU3": "flights_pilotlog.flight_time_type_u3",
    "minU4": "flights_pilotlog.flight_time_type_u4",
    "minXC": "flights_pilotlog.flight_time_type_xc",
    "minAIR": "flights_pilotlog.flight_time_type_air",
    "minCOP": "flights_pilotlog.flight_time_type_cop",
    "minIFR": "flights_pilotlog.flight_time_type_ifr",
    "minIMT": "flights_pilotlog.flight_time_type_imt",
    "minPIC": "flights_pilotlog.flight_time_type_pic",
    "minREL": "flights_pilotlog.flight_time_type_rel",
    "minSFR": "flights_pilotlog.flight_time_type_sfr",
    "minDUAL": "flights_pilotlog.flight_time_type_dual",
    "minEXAM": "flights_pilotlog.flight_time_type_exam",
    "minINSTR": "flights_pilotlog.flight_time_type_instr",
    "minNIGHT": "flights_pilotlog.flight_time_type_night",
    "minPICUS": "flights_pilotlog.flight_time_type_picus",
    "minTOTAL": "flights_pilotlog.flight_time_type_total",
}


class FlightFlight(models.Model):
    _inherit = 'flight.flight'
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

    def _parse_mccpilotlog(self, flight_data):
        data = json.loads(flight_data.raw_text)
        meta = data.get("meta", {})

        pilot = self.env['res.partner']._search_mccpilotlog(meta['P1Code'])

        flight = self._sync_flight_data(flight_data, {
            "departure_id": self.env["flight.aerodrome"]._search_mccpilotlog(meta["DepCode"]).id,
            "arrival_id": self.env["flight.aerodrome"]._search_mccpilotlog(meta["ArrCode"]).id,
        })

        self.env['flight.flight.param']._sync_flight_data(flight_data, {
            "flight_id": flight.id,
            "param_type_id": self.env.ref("flights.flight_param_type_hobbs_in").id,
            "value": meta.get("HobbsIn"),
        }, "hobbs_in")

        self.env['flight.flight.param']._sync_flight_data(flight_data, {
            "flight_id": flight.id,
            "param_type_id": self.env.ref("flights.flight_param_type_hobbs_out").id,
            "value": meta.get("HobbsOut"),
        }, "hobbs_out")

        for key, time_type in FLIGHT_TIME_MAP.items():
            self.env['flight.time']._sync_flight_data(flight_data, {
                'flight_id': flight.id,
                'partner_id': pilot.id,
                'time_type_id': self.env.ref(time_type).id,
                'minutes': meta.get(key, 0),
            }, key)

        crew = [self.env['res.partner']._search_mccpilotlog(meta[key]) for key in ("P2Code", "P3Code", "P4Code")]
        crew = [pilot] + [another_pilot for another_pilot in crew if another_pilot]
        role_pilot = self.env.ref("flights.flight_crew_role_pilot")
        for partner in crew:
            self.env['flight.crew']._sync_flight_data(flight_data, {
                'flight_id': flight.id,
                'partner_id': partner.id,
                'role_id': role_pilot.id,
            })
