# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models, api

# TODO: move the models to individual files


class FlightEvent(models.Model):
    _inherit = 'flight.event'

    # Computed fields to calculate delays
    scheduled_delay = fields.Float(compute='_compute_scheduled_delay', store=True)
    estimated_delay = fields.Float(compute='_compute_estimated_delay', store=True)
    target_delay = fields.Float(compute='_compute_target_delay', store=True)
    requested_delay = fields.Float(compute='_compute_requested_delay', store=True)

    @api.depends('scheduled_date', 'actual_date')
    def _compute_scheduled_delay(self):
        for event in self:
            if event.scheduled_date and event.actual_date:
                event.scheduled_delay = (event.actual_date - event.scheduled_date).total_seconds() / 60.0

    @api.depends('estimated_date', 'actual_date')
    def _compute_estimated_delay(self):
        for event in self:
            if event.estimated_date and event.actual_date:
                event.estimated_delay = (event.actual_date - event.estimated_date).total_seconds() / 60.0

    @api.depends('target_date', 'actual_date')
    def _compute_target_delay(self):
        for event in self:
            if event.target_date and event.actual_date:
                event.target_delay = (event.actual_date - event.target_date).total_seconds() / 60.0

    @api.depends('requested_date', 'actual_date')
    def _compute_requested_delay(self):
        for event in self:
            if event.requested_date and event.actual_date:
                event.requested_delay = (event.actual_date - event.requested_date).total_seconds() / 60.0
