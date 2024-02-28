# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models


class FlightPilotNote(models.Model):
    flight_id = fields.Many2many('flight.flight')
    kind = fields.Selection([
        ("remarks", "Remarks"),
        ("route", "Routing"),
        ("endorsement", "Endorsement"),
    ], "Kind", required=True, default="remarks")
    text = fields.Text()
   # signature = Image / OCA sign module
