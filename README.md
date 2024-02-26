# Flights Odoo modules

Manage flight related records (private, operator or airline) in Odoo.
=======

# Modules UI

flight (base module)

flight.flight Base List View
Flight Date | Aircraft | Departure Aerodrome | Departure Time UTC (if event exists or -) | Arrival Aerodrome | Arrival Time UTC (display +1 in the end if next day) | Total time | Flight time

Notes:
- Aircraft is aircraft registration
- Flight date is either the date of "off blocks" (departure) event or flight date if no event exits
- Departure time is '-' if no departure event exists
- Arrival time should be '-' if no arrival event exists (on blocks) and have '+1' appended in the end if the flight arrived next day
- total time should be calculated difference between on blocks and off blocks event
- flight time should be calculated difference between landing and takeoff events


flight_pilotlog (individual pilot logbook records extension)

flight.flight extended list view when a pilot is selected, some extra fields some are hidden, different order:

flight date | departure (place, time) | arrival (place, time) | aircraft (model code, registration) | single pilot time (SE, ME) | multi-pilot time | total time | name PIC | # takeoffs (day, night)  | # landings (day, night) | Operational conditions (night, ifr) | Pilot fucntion time (PIC, CO-PILOT, DUAl, instrucor)  | renarkts
