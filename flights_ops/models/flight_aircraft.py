# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightAircraft(models.Model):
    _name = 'flight.aircraft'
    _inherit = ['flight.aircraft', 'resource.mixin']
