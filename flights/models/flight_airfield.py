# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models, fields


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
        data = json.loads(flight_data.raw_text)
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
