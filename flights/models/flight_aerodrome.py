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
        ("airport", "Airport"),
        ("aerodrome", "Aerodrome"),
        ("seabase", "Seabase"),
        ("heliport", "Heliport"),
    ], "Type", required=True, default="aerodrome")

    _sql_constraints = [
        # TODO: this doesn't work with null values
        #("icao_unique", "unique(icao)", "Aerodrome with this ICAO already exists!"),
        #("iata_unique", "unique(iata)", "Aerodrome with this IATA already exists!"),
    ]
