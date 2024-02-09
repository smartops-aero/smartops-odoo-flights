# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields
from ..wizard.flight_wizard import SOURCE_TYPE


class FlightBase(models.AbstractModel):
    _inherit = 'flight.base'

    def _search_mccpilotlog(self, ref):
        if ref == "00000000-0000-0000-0000-000000000000":
            return self.browse()
        return self.env['flight.data']._search_by_ref(SOURCE_TYPE, self._name, ref)
