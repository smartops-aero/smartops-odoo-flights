This module allows scheduling and linking different resources to a flight.

Functionality:

- from a calendar view we want to be able to schedule (creat) a flight for a given aircraft:
  - sobt / sibt
  - crew
  - passengers

- new view for flight events grouped by flight we want to see a matrix

+-------+---------------------------------------+
| event | scheduled | actual | delay | duration |
+-------+-----------+------- +-------+--------- |
| off blocks | 10:00 | 10:15 | 0:05  |          |
| take-off   | 10:30 | 10:35 | 0:05  |          |
| landing | 11:30 | 11:25 | -0:05    | 0:50     |
| in-blocks | 11:35 | 11:35 | -     | 1:20     |

- in the flight form we want to see the links into Invoices and Bills

for bills, we want to be able to add on which flight but also where the bill took place, i.e. which airport