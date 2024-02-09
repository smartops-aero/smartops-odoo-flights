# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models


class FlightAircraft(models.Model):
    _inherit = 'flight.aircraft'
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
