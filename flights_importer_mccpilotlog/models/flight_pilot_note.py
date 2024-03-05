# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightPilotNote(models.Model):
    _inherit = "flight.pilot.note"

    def _process_mccpilotlog_xls(self, flight, flight_data, data):
        key = "remarks"
        if not data[key]:
            return
        vals = {
            "flight_id": flight.id,
            "kind": key,
            "text": data[key]
        }
        self._sync_flight_data(flight_data, vals, key)
