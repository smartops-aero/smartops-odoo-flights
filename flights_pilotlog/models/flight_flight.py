# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    pilot_time_ids = fields.One2many('flight.time', 'flight_id')
