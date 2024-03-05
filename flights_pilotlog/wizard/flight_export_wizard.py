# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightExportWizard(models.TransientModel):
    _inherit = 'flight.export.wizard'
    _description = 'Flight Data Exporting'

    action = fields.Selection(selection_add=[
        ("foreflight", "ForeFlight")
    ])
    def action_export(self):
        if self.action == "foreflight":
            return self.do_foreflight()
        else:
            return super().action_export()

    def do_foreflight(self):
        files_data = {}

        # Aircraft
        headers = [
            "AircraftID",
            "EquipmentType",
            "TypeCode",
            "Year",
            "Make",
            "Model",
            "Category",
            "Class",
            "GearType",
            "EngineType",
            "Complex",
            "TAA",
            "HighPerformance",
            "Pressurized"
        ]
        def record2row(aircraft):
            return [
                # "AircraftID",
                aircraft.registration,

                # "EquipmentType",
                "aircraft",

                # "TypeCode",
                "", # TODO

                # "Year",
                aircraft.year,

                # "Make",
                aircraft.model_id.make_id.name,

                # "Model",
                aircraft.model_id.name,

                # "Category",
                aircraft.model_id.class_id.aircraft_category,

                # "Class",
                aircraft.model_id.class_id.name,

                # "GearType",
                aircraft.model_id.gear_type,

                # "EngineType",
                aircraft.model_id.engine_type,

                # "Complex",
                False,  # TODO

                # "TAA",
                False,  # TODO

                # "HighPerformance",
                False,  # TODO

                # "Pressurized"
                False,  # TODO
            ]

        records = self.env['flight.aircraft'].search([])
        files_data["Aircraft.csv"] = self.generate_csv(headers, records, record2row)

        return self.zip_files(files_data)
