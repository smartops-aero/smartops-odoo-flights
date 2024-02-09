# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models


class FlightAerodrome(models.Model):
    _inherit = 'flight.aerodrome'

    # TODO(ivank): please ensure the importer saves all these fields in the partner_id
    # NotesUser will be extender by flights_pilotlog module with FlightsAerodromePilotNotes
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
    #    "TZCode": 333, # TODO
    #    "Latitude": 37218,
    #    "ShowList": false,
    #    "AFCountry": 223,
    #    "Longitude": -42036,
    #    "NotesUser": "ATIS 128.400",  # TODO
    #    "RegionUser": 0,
    #    "ElevationFT": 0,
    #    "Record_Modified": 1616320991
    #  },
    #  "platform": 9,
    #  "_modified": 1616317613
    # },

    def _parse_mccpilotlog(self, flight_data):
        data = json.loads(flight_data.raw_text)
        meta = data.get("meta", {})
        partner = self.env["res.partner"]._sync_flight_data(flight_data, {
            # TODO: check mapping
            "name": meta.get("AFName"),
            # TODO: fix geo modules installation
            #"geo_point": "POINT(%s %s)" % (meta.get("Latitude", 0) / 1000, meta.get("Longitude", 0) / 1000),
        })
        return self._sync_flight_data(flight_data, {
            "iata": meta.get("AFIATA"),
            "icao": meta.get("AFICAO"),
            "elevation": meta.get("ElevationFT"),
            "partner_id": partner.id,
        })
