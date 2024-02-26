# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import base64
import logging
import json
import xlrd
from io import BytesIO


from odoo import fields, models


_logger = logging.getLogger(__name__)
SOURCE_TYPE = 'mccpilotlog'


class MagicWizard(models.TransientModel):

    _inherit = 'flight.wizard'

    action = fields.Selection(selection_add=[
        ("mccpilotlog", "mccPILOTLOG (json)"),
        ("mccpilotlog_xls", "mccPILOTLOG (xls)"),
    ], default="mccpilotlog")

    def do_action(self):
        if self.action == "mccpilotlog":
            return self.do_mccpilotlog()
        elif self.action == "mccpilotlog_xls":
            return self.do_mccpilotlog_xls()
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

    def do_mccpilotlog_xls(self):
        workbook = xlrd.open_workbook(file_contents=base64.decodebytes(self.payload))
        sheet = workbook.sheet_by_index(0)
        column_names = [sheet.cell_value(0, col_index) for col_index in range(sheet.ncols)]
        for row_index in range(1, sheet.nrows):
            # Create a dictionary for the current row
            row_dict = {}
            for col_index, col_name in enumerate(column_names):
                # Populate the dictionary with column name: cell value pairs
                row_dict[col_name] = sheet.cell_value(row_index, col_index)
            import wdb; wdb.set_trace()

    def do_mccpilotlog(self):
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
