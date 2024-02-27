# Airport codes

1. Get csv file here: https://datahub.io/core/airport-codes
2. Install cli tool:

        pip install csvkit

3. Check airport types:

        csvcut -c type airport-codes_csv.csv | tail -n +2 | sort | uniq

4. Convert csv to xml

        cd flights/doc/
        python airport_codes_csv2xml.py /tmp/airport-codes_csv.csv > ../data/flight_aerodrome_data.xml
