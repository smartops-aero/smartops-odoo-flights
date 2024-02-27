#!/bin/bash

# Check if a CSV file name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <csv_file>"
    exit 1
fi

# Get the CSV file name from input
csv_file="$1"

# Function to escape XML special characters
escape_xml() {
    echo "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' -e 's/"/\&quot;/g' -e "s/'/\&apos;/g"
}

# Output XML header
echo '<?xml version="1.0" encoding="utf-8"?>'
echo '<odoo>'

# Read CSV file line by line, skipping the header
tail -n +2 "$csv_file" | while IFS= read -r line; do
    # Split the line into fields using a comma as the delimiter
    IFS=',' read -r -a fields <<< "$line"

    # Extract individual fields
    ident="${fields[0]}"
    type="${fields[1]}"
    name="${fields[2]}"
    elevation_ft="${fields[3]}"
    continent="${fields[4]}"
    iso_country="${fields[5]}"
    iso_region="${fields[6]}"
    municipality="${fields[7]}"
    gps_code="${fields[8]}"
    iata_code="${fields[9]}"
    local_code="${fields[10]}"
    coordinates="${fields[11]}"

    # Convert ISO country code to lowercase
    iso_country_lower=$(echo "$iso_country" | tr '[:upper:]' '[:lower:]')

    # Output res.partner record with id attribute
    echo "    <record model=\"res.partner\" id=\"partner_$ident\">"
    echo "        <field name=\"name\">$(escape_xml "$name")</field>"
    echo "        <field name=\"city\">$(escape_xml "$municipality")</field>"
    echo "        <field name=\"country_id\" ref=\"base.${iso_country_lower}\"/>"
    echo '    </record>'

    # Output flight.aerodrome record with id attribute
    echo "    <record model=\"flight.aerodrome\" id=\"aerodrome_$ident\">"
    echo "        <field name=\"partner_id\" ref=\"partner_$ident\"/>"
    echo "        <field name=\"icao\">$ident</field>"
    echo "        <field name=\"iata\">$iata_code</field>"
    echo "        <field name=\"elevation\">$elevation_ft</field>"
    echo "        <field name=\"aerodrome_type\">$type</field>"
    echo '    </record>'
    echo
done

# Close XML
echo '</odoo>'
