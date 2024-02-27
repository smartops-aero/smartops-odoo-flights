#!/usr/bin/env python3
import sys
import csv
from xml.sax.saxutils import escape

def escape_xml(text):
    return escape(text, {"'": "&apos;", '"': "&quot;", "&": "&amp;", "<": "&lt;", ">": "&gt;"})

if len(sys.argv) != 2:
    print("Usage: {} <csv_file>".format(sys.argv[0]))
    sys.exit(1)

csv_file = sys.argv[1]

print('<?xml version="1.0" encoding="utf-8"?>')
print('<odoo noupdate="1">')

with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header line
    for row in reader:
        ident, type, name, elevation_ft, continent, iso_country, iso_region, municipality, gps_code, iata_code, local_code, coordinates = row

        iso_country = iso_country.lower()
        if iso_country == "gb":
            iso_country = "uk"

        # Output res.partner record with id attribute
        print('    <record model="res.partner" id="partner_{}">'.format(ident))
        print('        <field name="name">{}</field>'.format(escape_xml(name)))
        print('        <field name="city">{}</field>'.format(escape_xml(municipality)))
        print('        <field name="country_id" ref="base.{}"/>'.format(iso_country))
        print('    </record>')

        # Output flight.aerodrome record with id attribute
        print('    <record model="flight.aerodrome" id="aerodrome_{}">'.format(ident))
        print('        <field name="partner_id" ref="partner_{}"/>'.format(ident))
        print('        <field name="icao">{}</field>'.format(ident))
        print('        <field name="iata">{}</field>'.format(iata_code))
        if elevation_ft:
            print('        <field name="elevation">{}</field>'.format(elevation_ft))
        print('        <field name="aerodrome_type">{}</field>'.format(type))
        print('    </record>')
        print('')

print('</odoo>')
