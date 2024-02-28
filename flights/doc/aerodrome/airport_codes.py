#!/usr/bin/env python3

import sys
import csv

if len(sys.argv) != 2:
    print("Usage: {} <csv_file>".format(sys.argv[0]))
    sys.exit(1)

csv_file = sys.argv[1]

# Output filenames
partner_csv_filename = 'res.partner.csv'
aerodrome_csv_filename = 'flight.aerodrome.csv'

# Open the input CSV file
with open(csv_file, newline='') as input_csvfile:
    reader = csv.reader(input_csvfile)

    # Open the output CSV files for writing
    with open(partner_csv_filename, 'w', newline='') as partner_csvfile, \
            open(aerodrome_csv_filename, 'w', newline='') as aerodrome_csvfile:

        # Create CSV writers for both files
        partner_writer = csv.writer(partner_csvfile, quoting=csv.QUOTE_ALL)
        aerodrome_writer = csv.writer(aerodrome_csvfile, quoting=csv.QUOTE_ALL)

        # Write headers to both files
        partner_writer.writerow(['id', 'name', 'city', 'country_id/id', "partner_latitude", "partner_longitude"])
        aerodrome_writer.writerow(['id', 'partner_id/id', 'icao', 'iata', 'elevation', 'aerodrome_type'])

        # Skip the header line in the input CSV file
        next(reader)

        # Iterate over each row in the input CSV file
        for row in reader:
            ident, type, name, elevation_ft, continent, iso_country, iso_region, municipality, gps_code, iata_code, local_code, coordinates = row

            partner_latitude, partner_longitude = None, None
            if coordinates:
                partner_latitude, partner_longitude = coordinates.split(", ")

            # Fix country code
            iso_country = iso_country.lower()
            if iso_country == "gb":
                iso_country = "uk"

            # TODO: compute tz (from coordinates or country + municipality)
            # Write data to res.partner.csv
            partner_writer.writerow(['partner_' + ident, name, municipality, 'base.' + iso_country, partner_latitude, partner_longitude])

            # Write data to flights.aerodrome.csv
            aerodrome_writer.writerow(['aerodrome_' + ident, 'partner_' + ident, ident, iata_code, elevation_ft, type])
