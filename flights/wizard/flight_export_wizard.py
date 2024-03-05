# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import base64
import csv
import tempfile
import zipfile
from odoo import models, fields, api


class FlightExportWizard(models.TransientModel):
    _name = 'flight.export.wizard'
    _description = 'Flight Data Exporting'

    action = fields.Selection([], string='Export Format')

    def action_export(self):
        if not self.action:
            raise UserError(_("Please select Export format. Install additional modules if needed"))
        else:
            raise NotImplementedError()

    def generate_csv(self, headers, records, record2row):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp_file:
            csv_writer = csv.writer(temp_file)

            csv_writer.writerow(headers)

            for r in records:
                csv_writer.writerow(record2row(r))

        with open(temp_file.name, 'r') as temp_file_read:
            csv_content = temp_file_read.read()

        return csv_content

    def zip_files(self, files_data):
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_path = tempfile.mktemp(suffix='.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                # Write each file to the temporary directory and add it to the zip archive
                for filename, content in files_data.items():
                    file_path = temp_dir + '/' + filename
                    with open(file_path, 'w') as file:
                        file.write(content)
                    zip_file.write(file_path, arcname=filename)

            # Read the zip file content and encode it
            with open(zip_file_path, 'rb') as zip_file:
                zip_content = zip_file.read()
                encoded_content = base64.b64encode(zip_content)

        # Create attachment for the zip file
        zip_file_name = f'{self.action}.zip'
        attachment = self.env['ir.attachment'].create({
            'name': zip_file_name,
            'datas': encoded_content,
            'store_fname': zip_file_name,
            'res_model': self._name,
        })

        # Return action to download the attachment
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s/%s' % (attachment.id, zip_file_name),
            'target': 'self',
        }
