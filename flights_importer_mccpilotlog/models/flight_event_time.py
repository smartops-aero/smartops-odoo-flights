# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime, timedelta
import pytz

from odoo import fields, models

FLIGHT_EVENT_MAP = {
    "time_dep":    ("flights.flight_event_kind_departure", "A", "departure_id"),
    "time_depsch": ("flights.flight_event_kind_departure", "S", "departure_id"),
    "time_to":     ("flights.flight_event_kind_takeoff",   "A", "departure_id"),
    "time_ldg":    ("flights.flight_event_kind_landing",   "A", "arrival_id"),
    "time_arr":    ("flights.flight_event_kind_arrival",   "A", "arrival_id"),
    "time_arrsch": ("flights.flight_event_kind_arrival",   "S", "arrival_id"),
}



class FlightEventTime(models.Model):
    _inherit = 'flight.event.time'

    def _process_mccpilotlog_xls(self, flight, flight_data, data):

        date_value = data["pilotlog_date"]
        date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()

        def time2dt(time_value, tz_value):
            dt_value = f"{date_value} {time_value}"
            dt = datetime.strptime(dt_value, "%Y-%m-%d %H:%M")

            tz = pytz.timezone(tz_value)
            localized_dt = tz.localize(dt)

            # Convert to UTC time
            utc_dt = localized_dt.astimezone(pytz.utc)

            # Convert to naive datetime (remove timezone information)
            naive_dt = utc_dt.replace(tzinfo=None)

            return naive_dt

        pilot = flight_data.partner_id
        result = {}
        for key, (event_kind, time_kind, aerodrome_field) in FLIGHT_EVENT_MAP.items():
            aerodrome = flight[aerodrome_field]
            tz_value = aerodrome.partner_id.tz if aerodrome else "UTC"
            result[key] = {
                "flight_id": flight.id,
                "kind_id": self.env.ref(event_kind).id,
                "time_kind": time_kind,
                "time": time2dt(data[key], tz_value),
            }

        # Add +1 day if needed
        for start, end in (("time_dep", "time_arr"), ("time_depsch", "time_arrsch"), ("time_to", "time_ldg")):
            if result[start]["time"] > result[end]["time"]:
                result[end]["time"] += timedelta(days=1)
                result[end]["overnight"] = 1

        for key, vals in result.items():
            self._sync_flight_data(flight_data, vals, key)
