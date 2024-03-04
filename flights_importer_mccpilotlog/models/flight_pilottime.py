# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


def duration2minutes(value):
    if not value or value == "00:00":
        return 0

    hours, minutes = value.split(":")
    return 60 * int(hours) + int(minutes)


PILOTTIME_MAP = {
    "time_air": "flights_pilotlog.flight_pilottime_kind_air",
    "time_total": "flights_pilotlog.flight_pilottime_kind_total",
    "time_pic": "flights_pilotlog.flight_pilottime_kind_pic",
    "time_sic": "flights_pilotlog.flight_pilottime_kind_sic",
    "time_dual": "flights_pilotlog.flight_pilottime_kind_dual",
    "time_picus": "flights_pilotlog.flight_pilottime_kind_picus",
    "time_instructor": "flights_pilotlog.flight_pilottime_kind_instructor",
    "time_examiner": "flights_pilotlog.flight_pilottime_kind_examiner",
    "time_night": "flights_pilotlog.flight_pilottime_kind_night",
    "time_xc": "flights_pilotlog.flight_pilottime_kind_xc",
    "time_ifr": "flights_pilotlog.flight_pilottime_kind_ifr",
    "time_hood": "flights_pilotlog.flight_pilottime_kind_hood",
    "time_actual": "flights_pilotlog.flight_pilottime_kind_actual",
    "time_relief": "flights_pilotlog.flight_pilottime_kind_relief",
}



class FlightPilotTime(models.Model):

    _inherit = "flight.pilottime"

    def _process_mccpilotlog_xls(self, flight, flight_data, data):
        pilot = flight_data.partner_id
        for key, pilottime_kind in PILOTTIME_MAP.items():
            vals = {
                "flight_id": flight.id,
                "partner_id": pilot.id,
                "time_kind_id": self.env.ref(pilottime_kind).id,
                "minutes": duration2minutes(data[key]),
            }
            self._sync_flight_data(flight_data, vals, key)
