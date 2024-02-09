# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightData(models.Model):
    """Implements one way data syncronization, typically from a file.

       Key principles:
       * `source_model` is main Odoo model for the current `flight.data` record.
       * single `flight.data` may create several records in different models
       * single `flight.data` may create only a single record in a specific model.
         This allows linking record and original data via field flight_source_id = Many2one("flight.data")
    """

    _name = 'flight.data'
    _description = 'Flight Data Source'

    source_type = fields.Char(required=True)
    source_model = fields.Char(required=True)
    source_ref = fields.Char(required=True)
    raw_text = fields.Text(required=True)
    is_parsed = fields.Boolean("Parsed", default=False)

    _sql_constraints = [
        ("unique_ref",
         "unique(source_type,source_model,source_ref)",
         "Record must have unique reference"
        )
    ]

    def _data_parse(self):
        """Calls a method in corresponing Model"""
        self.ensure_one()
        model = self.env[self.source_model]
        method_name = '_parse_' + self.source_type
        if hasattr(model, method_name):
            return getattr(model, method_name)(self)
        else:
            raise NotImplementedError()

    @property
    def linked_record(self):
        """Find a record that was created from this Data"""
        self.ensure_one()
        return self.env[self.source_model].search([
            ("flight_source_id", "=", self.id)
        ], limit=1)

    def _search_by_ref(self, source_type, model, ref):
        return self.search([
            ("source_type", "=", source_type),
            ("source_model", "=", model),
            ("source_ref", "=", ref),
        ], limit=1)
