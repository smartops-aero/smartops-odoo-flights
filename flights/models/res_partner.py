# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'flight.base']

    # {
    #   "user_id": 125880,
    #   "table": "Pilot",
    #   "guid": "00000000-0000-0000-0000-000000000756",
    #   "meta": {
    #     "Notes": "",
    #     "Active": true,
    #     "Company": "Wizz Air",
    #     "FavList": false,
    #     "UserAPI": "",
    #     "Facebook": "",
    #     "LinkedIn": "",
    #     "PilotRef": "",
    #     "PilotCode": "00000000-0000-0000-0000-000000000756",
    #     "PilotName": "SERAFIN G.",
    #     "PilotEMail": "",
    #     "PilotPhone": "",
    #     "Certificate": "",
    #     "PhoneSearch": "",
    #     "PilotSearch": "SERAFING",
    #     "RosterAlias": "",
    #     "Record_Modified": 1616320991
    #   },
    #   "platform": 9,
    #   "_modified": 1616317613
    # },

    def _parse_pilot_log_mcc(self, flight_data):
        data = json.loads(flight_data.raw_text)
        meta = data.get("meta", {})
        return self._sync_flight_data(flight_data, {
            # TODO check mapping
            "name": meta.get("PilotName")
        })
