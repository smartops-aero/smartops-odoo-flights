# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightBase(models.AbstractModel):
    _name = 'flight.base'
    _description = 'Flight Base'

    flight_source_id = fields.Many2one("flight.data", required=False, readonly=True)

    def _sync_flight_data(self, flight_data, vals):
        """Update record or create a new one"""
        if "flight_source_id" not in vals:
            vals["flight_source_id"] = flight_data.id
        record = flight_data.linked_record(self)
        if record:
            record.write(vals)
        else:
            record = self.create(vals)
        flight_data.is_parsed = True
        return record
    _sql_constraints = [
        ("flight_source_id_unique", "unique(flight_source_id)", "Record with the same flight_source_id already exists!")
    ]
