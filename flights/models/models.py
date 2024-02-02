# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, api


class FlightNumber(models.Model):
    _name = 'flight.number'
    _inherit = 'flight.base'

    operator_id = fields.Many2one('flight.operator')
    numbers = fields.Char()

    @api.depends("operator_id.name", "numbers")
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"{r.operator_id.name} {r.numbers}"


class FlightOperator(models.Model):
    _name = 'flight.operator'
    _inherit = 'flight.base'

    name = fields.Char("Prefix")
    description = fields.Char()


class FlightCrew(models.Model):
    _name = 'flight.crew'
    _inherit = 'flight.base'

    partner_id = fields.Many2one('res.partner')
    role_id = fields.Many2one('flight.crew.role')
    flight_id = fields.Many2one('flight.flight')


class FlightCrewRole(models.Model):
    _name = 'flight.crew.role'
    _inherit = 'flight.base'

    code = fields.Char()
    description = fields.Char()


class FlightEvent(models.Model):
    _name = 'flight.event'
    _inherit = 'flight.base'

    flight_id = fields.Many2one('flight.flight')
    event_type = fields.Many2one('flight.event.type')

    scheduled_date = fields.Datetime()
    estimated_date = fields.Datetime()
    target_date = fields.Datetime()
    requested_date = fields.Datetime()
    actual_date = fields.Datetime()


class FlightEventType(models.Model):
    _name = 'flight.event.type'
    _inherit = 'flight.base'

    code = fields.Char()
    description = fields.Char()
