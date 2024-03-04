# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightCrew(models.Model):
    _inherit = 'flight.crew'

    def _process_mccpilotlog_xls(self, flight, flight_data, data):
        default_pilot = flight_data.partner_id
        for key in ("pilot1_name", "pilot2_name", "pilot3_name", "pilot4_name"):
            name = data[key]
            if not name:
                continue
            pilot = default_pilot if name == "SELF" else None
            if not pilot:
                # We assume, that every pilot has unique name
                pilot = self.env['res.partner'].search([
                    ("name", "=", name)
                ], limit=1)
            if not pilot:
                pilot = self.env['res.partner'].create({
                    "name": name,
                })

            # Always use PIC, because the file doesn't have information about role
            role = self.env.ref("flights.flight_crew_role_pic")
            vals = {
                "flight_id": flight.id,
                "partner_id": pilot.id,
                "role_id": role.id,
            }
            self._sync_flight_data(flight_data, vals, key)
