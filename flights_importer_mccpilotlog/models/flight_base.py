# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models
from ..wizard.flight_wizard import SOURCE_TYPE


class FlightBase(models.AbstractModel):
    _inherit = 'flight.base'

    def _search_mccpilotlog(self, ref, key=None):
        if ref == "00000000-0000-0000-0000-000000000000":
            return self.browse()
        flight_data = self.env['flight.data']._search_by_ref(SOURCE_TYPE, self._name, ref)
        return flight_data._get_linked_record(self, key) if flight_data else self.browse()
