# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models, fields


class FlightAerodrome(models.Model):
    _name = 'flight.aerodrome'
    _inherit = 'flight.base'
    _description = 'Aerodrome'

    partner_id = fields.Char("Address")

    icao = fields.Char("ICAO identifier")
    iata = fields.Char("IATA identifier")
    elevation = fields.Integer("Aerodrome elevation in feet")
    aerodrome_type = fields.Selection([
        ("small_airport", "Small Airport"),
        ("medium_airport", "Medium Airport"),
        ("large_airport", "Large Airport"),
        ("heliport", "Heliport"),
        ("seaplane_base", "Seabase"),
        ("balloonport", "Balloonport"),
        ("closed", "Closed"),
    ], "Type", required=True, default="small_airport")

    _sql_constraints = [
        ("icao_unique", "unique(icao)", "Aerodrome with this ICAO already exists!"),
        ("iata_unique", "unique(iata) WHERE iata IS NOT NULL", "Aerodrome with this IATA already exists!"),
    ]

    def search_by_code(self, code):
        return self.search([
            "|",
            ("icao", "=", code),
            ("iata", "=", code),
        ], limit=1)

