# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightBase(models.AbstractModel):
    _name = 'flight.base'

    flight_source_id = fields.Many2one("flight.data", unique=True, required=False, readonly=True)
