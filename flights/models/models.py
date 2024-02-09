# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, api


class FlightNumber(models.Model):
    _name = 'flight.number'
    _inherit = 'flight.base'

    prefix_id = fields.Many2one('flight.prefix')
    numbers = fields.Char()

    @api.depends("prefix_id.name", "numbers")
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"{r.operator_id.name} {r.numbers}"


class FlightPrefix(models.Model):
    _name = 'flight.prefix'
    _inherit = 'flight.base'

    name = fields.Char("Prefix")
    description = fields.Char()


class FlightEvent(models.Model):
    _name = 'flight.event'
    _inherit = 'flight.base'

    flight_id = fields.Many2one('flight.flight')
    event_type = fields.Many2one('flight.event.type')

    # This is fine as this has a distinct meaning in air operations
    st = fields.Datetime()  # scheduled time
    et = fields.Datetime()  # estimated time
    tt = fields.Datetime()  # target time
    rt = fields.Datetime()  # requested time
    at = fields.Datetime()  # actual time


class FlightEventType(models.Model):
    _name = 'flight.event.type'
    _inherit = 'flight.base'

    code = fields.Char()
    description = fields.Char()
