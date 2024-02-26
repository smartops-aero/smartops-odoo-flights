# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models


class FlightAircraft(models.Model):
    _inherit = 'flight.aircraft'

    def _parse_mccpilotlog_xls(self, flight_data):
        data = json.loads(flight_data.raw_text)

        registration = data["ac_reg"]
        aircraft = self.env["flight.aircraft"].search([
            ('registration', '=', registration)
        ])
        if aircraft:
            return aircraft

        make_name = data["ac_make"]
        make = self.env["flight.aircraft.make"].search([
            ("name", "=", make_name),
        ])
        if not make:
            make = self.env["flight.aircraft.make"].create({"name": make_name})

        model_name = data["ac_model"]
        model = self.env["flight.aircraft.model"].search([
            ("make_id", "=", make.id),
            ("name", "=", model_name),
        ])
        if not model:
            model = self.env["flight.aircraft.model"].create({
                "name": model_name,
            })

        aircraft = self.env["flight.aircraft"]._sync_flight_data(flight_data, {
            "registration": registration,
            "model_id": model.id,
        })

        # TODO: Check other fields
        # flight.aircraft
        # * ac_model
        # * ac_variant
        # * ac_reg
        # * ac_fin
        # * ac_rating
        # * ac_class

        # flight.aircraft.model.tag
        # * ac_sea
        # * ac_engines
        # * ac_engtype
        # * ac_tailwheel
        # * ac_complex
        # * ac_tmg
        # * ac_heavy
        # * ac_highperf
        # * ac_aerobatic
        # * ac_seats
        return aircraft


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
        # TODO: this method should be deleted or refactored to deduplicate code
        # with _parse_mccpilotlog_xls
        data = json.loads(flight_data.raw_text)
        meta = data.get("meta", {})

        make_name = meta.get("Make")
        make = self.env["flight.aircraft.make"].search([
            ("name", "=", make_name),
        ])

        model_name = meta.get("Model")
        model = None
        if make:
            model = self.env["flight.aircraft.model"].search([
                ("make_id", "=", make.id),
                ("name", "=", model_name),
            ])
        else:
            make = self.env["flight.aircraft.make"].create({"name": make_name})

        if not model:
            # TODO: add model tags?
            model = self.env["flight.aircraft.model"].create({
                # TODO: should we use field "code" instead?
                "name": model_name,
                "mtow": 142000 if meta.get("Kg5700") else 12000,
            })

        return self._sync_flight_data(flight_data, {
            "registration": meta.get("Reference"),
            "model_id": model.id,
        })
