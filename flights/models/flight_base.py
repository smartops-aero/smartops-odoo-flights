# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightBase(models.AbstractModel):
    _name = 'flight.base'
    _description = 'Flight Base'

    flight_source_id = fields.Many2one("flight.data", required=False, readonly=True)
    flight_source_key = fields.Char()

    def _sync_flight_data(self, flight_data, vals, key=None):
        """Update record or create a new one"""
        if "flight_source_id" not in vals:
            vals["flight_source_id"] = flight_data.id
        record = flight_data._get_linked_record(self, key)
        if record:
            record.write(vals)
        else:
            record = self.create(vals)
        flight_data.is_parsed = True
        return record

    _sql_constraints = [
        ("flight_source_id_key_unique", "unique(flight_source_id, flight_source_key)", "Record with the same flight_source_id and flight_source_key already exists!")
    ]
