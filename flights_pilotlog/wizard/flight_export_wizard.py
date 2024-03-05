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

        # Flights
        headers = ["Date", "AircraftID", "From", "To", "Route", "TimeOut",
                   "TimeOff", "TimeOn", "TimeIn", "OnDuty", "OffDuty", "TotalTime", "PIC",
                   "SIC", "Night", "Solo", "CrossCountry", "NVG", "NVGOps", "Distance",
                   "DayTakeoffs", "DayLandingsFullStop", "NightTakeoffs",
                   "NightLandingsFullStop", "AllLandings", "ActualInstrument",
                   "SimulatedInstrument", "HobbsStart", "HobbsEnd", "TachStart",
                   "TachEnd", "Holds", "Approach1", "Approach2", "Approach3", "Approach4",
                   "Approach5", "Approach6", "DualGiven", "DualReceived",
                   "SimulatedFlight", "GroundTraining", "InstructorName",
                   "InstructorComments", "Person1", "Person2", "Person3", "Person4",
                   "Person5", "Person6", "FlightReview", "Checkride", "IPC",
                   "NVGProficiency", "FAA6158", "PilotComments"]

        def record2row(flight):
            # Be sure to keep the same order for the fields
            return [
                # "Date",
                # TODO: check tz
                flight.date.strftime("%Y-%m-%d"),

                # "AircraftID",
                flight.aircraft_id.registration,

                # "From",
                flight.departure_id.icao,

                # "To",
                flight.departure_id.icao,

                # "Route",
                # TODO: we don't have route example at the moment
                "",

                # "TimeOut",
                flight.get_time_by_code("OB") or "",

                # "TimeOff",
                flight.get_time_by_code("TO") or "",

                # "TimeOn",
                flight.get_time_by_code("LD") or "",

                # "TimeIn",
                flight.get_time_by_code("IB") or "",

                # "OnDuty",
                # TODO: check
                flight.get_time_by_code("OB") or "",

                # "OffDuty",
                # TODO: check
                flight.get_time_by_code("IB") or "",

                # "TotalTime",
                flight.get_pilottime_by_code("TOTAL"),

                # "PIC",
                flight.get_pilottime_by_code("PIC"),

                # "SIC",
                flight.get_pilottime_by_code("SIC"),

                # "Night",
                flight.get_pilottime_by_code("NIGHT"),

                # "Solo",
                # TODO
                0,

                # "CrossCountry",
                flight.get_pilottime_by_code("XS"),

                # "NVG",
                # TODO
                0,

                # "NVGOps",
                # TODO
                0,

                # "Distance",
                # TODO
                0,

                # "DayTakeoffs",
                flight.get_pilot_activity_by_code("TODAY"),

                # "DayLandingsFullStop",
                flight.get_pilot_activity_by_code("LDDAY"),

                # "NightTakeoffs",
                flight.get_pilot_activity_by_code("TONIGHT"),

                # "NightLandingsFullStop",
                flight.get_pilot_activity_by_code("LDNIGHT"),

                # "AllLandings",
                # TODO: just a sum?
                0,

                # "ActualInstrument",
                flight.get_pilottime_by_code("IMC"),

                # "SimulatedInstrument",
                flight.get_pilottime_by_code("HOOD"),

                # "HobbsStart",
                flight.get_param_by_code("hobbs_in"),

                # "HobbsEnd",
                flight.get_param_by_code("hobbs_out"),

                # "TachStart",
                # TODO
                0,

                # "TachEnd",
                # TODO
                0,

                # "Holds",
                # TODO
                0,

                # "Approach1",
                # TODO
                0,

                # "Approach2",
                # TODO
                0,

                # "Approach3",
                # TODO
                0,

                # "Approach4",
                # TODO
                0,

                # "Approach5",
                # TODO
                0,

                # "Approach6",
                # TODO
                0,

                # "DualGiven",
                # TODO
                0,

                # "DualReceived",
                # TODO
                0,

                # "SimulatedFlight",
                # TODO
                0,

                # "GroundTraining",
                # TODO
                0,

                # "InstructorName",
                # TODO
                "",

                # "InstructorComments",
                # TODO
                "",
                # "Person1",
                # TODO
                "",
                # "Person2",
                # TODO
                "",
                # "Person3",
                # TODO
                "",
                # "Person4",
                # TODO
                "",
                # "Person5",
                # TODO
                "",
                # "Person6",
                # TODO
                "",
                # "FlightReview",
                # TODO
                "",
                # "Checkride",
                # TODO
                "",
                # "IPC",
                # TODO
                "",
                # "NVGProficiency",
                # TODO
                "",
                # "FAA6158",
                # TODO
                "",

                # "PilotComments"
                flight.get_note_by_code("remarks"),
            ]

        records = self.env['flight.flight'].search([])
        files_data["Flights.csv"] = self.generate_csv(headers, records, record2row)

        return self.zip_files(files_data)
