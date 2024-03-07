# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime, timedelta
import pytz

from odoo import fields, models

MAPPING = {
    ("flights.flight_event_duration_kind_ob_ib", "A"): ("time_dep",    "time_arr"),
    ("flights.flight_event_duration_kind_ob_ib", "S"): ("time_depsch", "time_arrsch"),
    ("flights.flight_event_duration_kind_to_ld", "A"): ("time_to",     "time_ldg"),
}


class FlightEventTime(models.Model):
    _inherit = 'flight.event.time'

    def _process_mccpilotlog_xls(self, flight, flight_data, data):

        date_value = data["pilotlog_date"]
        date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()

        def time2dt(time_value):
            dt_value = f"{date_value} {time_value}"
            return datetime.strptime(dt_value, "%Y-%m-%d %H:%M")

        pilot = flight_data.partner_id
        events = {}
        durations = {}
        for (duration_kind_ref, time_kind), (start_key, end_key) in MAPPING.items():
            if data[start_key] == "00:00" and data[end_key] == "00:00":
                continue

            start_time = time2dt(data[start_key])
            end_time = time2dt(data[end_key])
            if start_time > end_time:
                end_time += timedelta(days=1)

            duration_kind = self.env.ref(duration_kind_ref)

            # start event
            vals = {
                "flight_id": flight.id,
                "kind_id": duration_kind.start_kind_id.id,
                "time_kind": time_kind,
                "time": start_time,
            }
            start = self._sync_flight_data(flight_data, vals, start_key)

            # end event
            vals = {
                "flight_id": flight.id,
                "kind_id": duration_kind.end_kind_id.id,
                "time_kind": time_kind,
                "time": end_time,
            }
            end = self._sync_flight_data(flight_data, vals, end_key)

            # duration
            vals = {
                "duration_kind_id": duration_kind.id,
                "start_id": start.id,
                "end_id": end.id,
            }
            duration = self.env['flight.event.duration']._sync_flight_data(flight_data, vals, duration_kind_ref + time_kind)
