# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightBase(models.AbstractModel):
    _name = 'flight.base'

    flight_source_id = fields.Many2one("flight.data", unique=True, required=False, readonly=True)

    def _sync_flight_data(self, flight_data, vals):
        """Update record or create a new one"""
        self.ensure_one()
        if "flight_source_id" not in vals:
            vals["flight_source_id"] = flight_data.id
        record = flight_data._search_linked_record(self)
        if record:
            record.write(vals)
        else:
            record = self.create(vals)
        flight_data.is_parsed = True
        return record
