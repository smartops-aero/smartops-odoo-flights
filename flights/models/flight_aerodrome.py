# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models, fields


class FlightAerodrome(models.Model):
    _name = 'flight.aerodrome'
    _inherit = 'flight.base'

    partner_id = fields.Char("Address")

    icao = fields.Char("ICAO identifier", unique=True, blank=True)
    iata = fields.Char("IATA identifier", unique=True, blank=True)
    elevation = fields.Integer("Aerodrome elevation in feet")
    aerodrome_type = fields.Selection([
        ("airport", "Airport"),
        ("aerodrome", "Aerodrome"),
        ("seabase", "Seabase"),
        ("heliport", "Heliport"),
    ], "Type", required=True, default="aerodrome")
