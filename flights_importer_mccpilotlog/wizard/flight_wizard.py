# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import base64
import logging
import json

from odoo import fields, models


_logger = logging.getLogger(__name__)


class MagicWizard(models.TransientModel):

    _inherit = 'flight.wizard'

    action = fields.Selection(selection_add=[
        ("mccpilotlog", "mccPILOTLOG")
    ], default="mccpilotlog")

    def do_action(self):
        if self.action == "mccpilotlog":
            return self.do_mccpilotlog()
        else:
            return super().do_action()

    def _update_flight_data(self, vals):
        existing = self.env['flight.data'].search([
            ('source_type', '=', vals['source_type']),
            ('source_model', '=', vals['source_model']),
            ('source_ref', '=', vals['source_ref']),
        ])
        if existing:
            if self.override:
                existing.write({
                    "raw_text": vals["raw_text"],
                    "is_parsed": False,
                })
            return existing
        else:
            return self.env['flight.data'].create(vals)

    def do_mccpilotlog(self):
        SOURCE_TYPE = 'mccpilotlog'
        TABLE_MAP = {
            "aircraft": "flight.aircraft",
            "airfield": "flight.aerodrome",
            "flight": "flight.flight",
            "pilot": "res.partner",
        }

        # Load data into `flight.data` table first
        for data in json.loads(base64.decodebytes(self.payload)):
            table = data.get("table").lower()
            if table not in TABLE_MAP:
                _logger.debug("Unsupported record: %s", table)
                continue
            model = TABLE_MAP[table]
            self._update_flight_data({
                'source_type': SOURCE_TYPE,
                'source_model': model,
                'source_ref': data.get("guid"),
                'raw_text': json.dumps(data)
            })

        # Parse data
        # TODO: use queue_job for async work?
        # TODO: In case if we don't use queue_job, but have performance issue,
        # we may add a counter and make cr.commit() every 1000 records
        for flight_data in self.env['flight.data'].search([
                ("source_type", "=", SOURCE_TYPE),
                ("source_model", "in", ["flight.aerodrome", "flight.aircraft", "res.partner"]),
                ("is_parsed", "=", False)
        ]):
            flight_data._data_parse()

        # parse flights last because they have references to other models
        for flight_data in self.env['flight.data'].search([
                ("source_type", "=", SOURCE_TYPE),
                ("source_model", "in", ["flight.flight"]),
                ("is_parsed", "=", False)
        ]):
            flight_data._data_parse()

        return {'type': 'ir.actions.act_window_close'}
