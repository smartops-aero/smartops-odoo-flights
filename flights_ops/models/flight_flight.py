# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime
from odoo import models, fields


class FlightFlight(models.Model):
    _inherit = 'flight.flight'

    status = fields.Selection([
        ("scheduled", "Scheduled"),
        ("delayed", "Delayed"),
        ("departed", "Departed"),
        ("arrived", "Arrived"),
        ("canceled", "Canceled"),
        ("done", "Done"),
    ], "Flight status", required=True, default="scheduled")
