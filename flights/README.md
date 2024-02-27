# Flights

Base module


# Installation

## Aerodromes


1. Install [base_import_async](https://github.com/OCA/queue/tree/16.0/base_import_async) (optional)

2. Import csv files from `doc/aerodrome/` in the following order:

    * `res.partner.csv`
    * `flight.aerodrome.csv`


## OCA/geospatial

The module uses OCA/geospatial module, which require extra packages to be installed:

```
sudo apt-get install postgis postgresql-postgis-scripts
```

See https://github.com/OCA/geospatial/tree/16.0/base_geoengine



# Configuration

In case of 413 Error during file uploading you many need to check configuration of your webserver. For example, for nginx you may need to add following instruction:

```
client_max_body_size 22M;

```

# Roadmap

* Add User/Manager groups
