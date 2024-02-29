# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime
import json
from odoo import models


FLIGHT_TIME_MAP = {
    "minU1": "flights_pilotlog.flight_time_kind_u1",
    "minU2": "flights_pilotlog.flight_time_kind_u2",
    "minU3": "flights_pilotlog.flight_time_kind_u3",
    "minU4": "flights_pilotlog.flight_time_kind_u4",
    "minXC": "flights_pilotlog.flight_time_kind_xc",
    "minAIR": "flights_pilotlog.flight_time_kind_air",
    "minCOP": "flights_pilotlog.flight_time_kind_cop",
    "minIFR": "flights_pilotlog.flight_time_kind_ifr",
    "minIMT": "flights_pilotlog.flight_time_kind_imt",
    "minPIC": "flights_pilotlog.flight_time_kind_pic",
    "minREL": "flights_pilotlog.flight_time_kind_rel",
    "minSFR": "flights_pilotlog.flight_time_kind_sfr",
    "minDUAL": "flights_pilotlog.flight_time_kind_dual",
    "minEXAM": "flights_pilotlog.flight_time_kind_exam",
    "minINSTR": "flights_pilotlog.flight_time_kind_instr",
    "minNIGHT": "flights_pilotlog.flight_time_kind_night",
    "minPICUS": "flights_pilotlog.flight_time_kind_picus",
    "minTOTAL": "flights_pilotlog.flight_time_kind_total",
}


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    def _parse_mccpilotlog_xls(self, flight_data):
        data = json.loads(flight_data.raw_text)

        aircraft = self.env["flight.aircraft"]._parse_mccpilotlog_xls(flight_data)

        flight = self._sync_flight_data(flight_data, {
            "date": datetime.strptime(data['pilotlog_date'], "%Y-%m-%d"),
            "departure_id": self.env['flight.aerodrome'].search_by_code(data['af_dep']).id,
            "arrival_id": self.env['flight.aerodrome'].search_by_code(data['af_arr']).id,
            "aircraft_id": aircraft.id,
        })

        self.env["flight.pilottime"]._process_mccpilotlog_xls(flight, data)
        self.env["flight.pilot.activity"]._process_mccpilotlog_xls(flight, data)
        self.env["flight.event.time"]._process_mccpilotlog_xls(flight, data)

        # flight_event_time
        # * time_dep
        # * time_depsch
        # * time_arr
        # * time_arrsch
        # * time_to
        # * time_ldg

        # flight_pilottime
        # * time_air
        # * time_total
        # * time_pic
        # * time_sic
        # * time_dual
        # * time_picus
        # * time_instructor
        # * time_examiner
        # * time_night
        # * time_xc
        # * time_ifr
        # * time_hood
        # * time_actual
        # * time_relief
        # * time_user1
        # * time_user2
        # * time_user3
        # * time_user4

        # flight_pilot_activity
        # * to_day
        # * to_night
        # * ldg_day
        # * ldg_night
        # * lift
        # * holding

        # TODO

        # pliotlog_notes
        # * route

        return flight

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

        for key, time_kind in FLIGHT_TIME_MAP.items():
            self.env['flight.time']._sync_flight_data(flight_data, {
                'flight_id': flight.id,
                'partner_id': pilot.id,
                'time_kind_id': self.env.ref(time_kind).id,
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
