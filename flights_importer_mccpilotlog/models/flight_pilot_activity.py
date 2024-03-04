# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models

PILOT_ACTIVITY_MAP = {
    "ldg_day": "flights_pilotlog.flight_pilot_activity_kind_ld",
    "ldg_night": "flights_pilotlog.flight_pilot_activity_kind_ln",

    "to_day": "flights_pilotlog.flight_pilot_activity_kind_to",
    "to_night": "flights_pilotlog.flight_pilot_activity_kind_ton",

    "lift": "flights_pilotlog.flight_pilot_activity_kind_lift",
    "holding": "flights_pilotlog.flight_pilot_activity_kind_hld",
}



class FlightPilotActivity(models.Model):
    _inherit = "flight.pilot.activity"

    def _process_mccpilotlog_xls(self, flight, flight_data, data):
        pilot = flight_data.partner_id
        for key, activity_kind in PILOT_ACTIVITY_MAP.items():
            vals = {
                "flight_id": flight.id,
                "partner_id": pilot.id,
                "kind_id": self.env.ref(activity_kind).id,
                "count": int(data[key]),
            }
            self._sync_flight_data(flight_data, vals, key)
