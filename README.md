Flights Odoo modules

Manage flight related records (private, operator or airline) in Odoo

flights - base module
    FlightAirport
    FlightAircraft
    FlightFlight
    FlightFlightEvent
    FlightEventTime
    FlightFlightCrew

FlightFlightPrefix

FlightAircaft
   reg = charfiled(registration)


FlightFlightNumber
    #e.g.  KL 3201 | KL 3101A 
    prefix = fk(FlightFlightPrefix)
    number = string()
FlightFlight
 aircraft = fk()
 number = fk()
 dep = fK(Airport)
 arr = Airport
 crew = Many2Many(FlightFlightCrew)
 
  times = m2m(FlightFlightTime)
 
    events = m2m(FlightEvent)

FlightEvent m2m Times


FlightFlightTime
    flight =
    event_type = fk
    when | at | date | datetime | at_datetime | = 
    
FlightFlightEventType
    code = "t"
    description = "Take-off"

    code = "l"
    description = "Take-off"

FlightTimeEnum
    a = actual
    s = scheduled
    e = estimated
    t = target

        SCHEDULED = 0, "scheduled"
        TARGET = 1, "target"
        ACTUAL = 2, "actual"
        ESTIMATED = 3, "estimated"
        REQUESTED = 4, "requested"




FlightFlightCrewRole

FlightFlightCrew()
    role = FlightCrewRole() -> e.g. PIC (pilot in command), SIC (second-in-command) - OBS (observer) - INS (Instructor) - EXA

================================================================================================
flights_pilotlog - individual pilot records
    Aircraft
        model = 
    AircraftModel
        make = 
    AircraftMake   
        name = "Cessna" 
    FlightDurationKind
        "Total" = default(engine start event - engine stop event)
        "Night" = Night <= Total
        "PIC"
        "SIC"

    FlightDuration
        fk = flight
        fk = FlightDurationKind

    Endorsement
