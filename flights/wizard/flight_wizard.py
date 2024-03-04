# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models, _
from odoo.exceptions import UserError


class MagicWizard(models.TransientModel):

    _name = 'flight.wizard'
    _description = 'Flight Importer'

    action = fields.Selection([
    ], "Supported formats")

    payload = fields.Binary("File", required=True, attachment=False)
    filename = fields.Char(string="Filename")
    override = fields.Boolean("Override existing records", default=True)
    partner_id = fields.Many2one("res.partner", "Pilot", default=lambda self: self.env.user.partner_id)

    def do_action(self):
        if not self.action:
            raise UserError(_("Please select File format. Install additional modules if needed"))
        else:
            raise NotImplementedError()
