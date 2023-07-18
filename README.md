## Introduction

ASprofiler fetches the most recent available datasets to profile with an easy and fast way the selected ASes (Autonomous Systems) in terms of their:
 - Providers
 - Customers
 - Peers
 - Customer Cone (direct/indirect customers)
 - IXPs in which they have presence
 - Facilities in which they have presence
 - Geographic information (city/country level) 


Here is the database list from which the tool retrieves all the appropriate data:
 1. [AS Relationships](https://www.caida.org/catalog/datasets/as-relationships)
 2. [AS to Organization Mappings](https://www.caida.org/catalog/datasets/as-organizations)
 3. [AS Customer Cone](https://www.caida.org/catalog/datasets/as-relationships)
 4. [Facility Information](https://www.caida.org/catalog/datasets/peeringdb)
 5. [Internet eXchange Points (IXPs) information](https://www.caida.org/catalog/datasets/ixps)

**Why ASprofiler is important?**

The output data might be used to:
- Increase the granularity of the existing information concerning the AS portfolio
- Evaluate the networking expansion of the customer base
- Geolocate ASes based on where they exchange Internet traffic
------------

## How it works
- Collects all the necessary datasets from the publicly available databases
- Arranges downloaded datasets for easy access
- Processes the requested ASes and export their profiles

## How to run
`$ python3 asprofiler.py -if asns.csv -of export.json`

_asns.csv_: contains all the candidate ASes to build their profile (with format 1,2,3)

_export.json_: contains all the exported information

## Requirements
- Python 3.5 or greater
- UltraJSON
- requests
- wget
- beautifulsoup4

## License

This repository is licensed under the [GNU AGPLv3](LICENSE). All code in this repository belongs to [Georgios Nomikos](https://www.linkedin.com/in/georgenomikos).
