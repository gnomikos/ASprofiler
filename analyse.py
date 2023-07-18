#!/usr/bin/env python3

import lib
import ujson
import bz2
from collections import defaultdict
import requests

class Analyse():
    
    def __init__(self, ixp_filename, as_to_ixp_filename, as_to_facility_filename, as_to_relationship_v4_filename, as_to_relationship_v6_filename, customer_cone_filename, asns):

        self.asns = asns
        self.ixp_info = {}
        self.as_to_ixp_info = defaultdict(set)
        self.as_to_facility_info = defaultdict(set)
        self.p2c = {'v4': defaultdict(set), 'v6': defaultdict(set)}
        self.c2p = {'v4': defaultdict(set), 'v6': defaultdict(set)}
        self.p2p = {'v4': defaultdict(set), 'v6': defaultdict(set)}
        self.customer_cone = {}
        self.as2org = {}
        
        self.ixp_filename = ixp_filename
        self.as_to_ixp_filename = as_to_ixp_filename
        self.as_to_facility_filename = as_to_facility_filename

        self.as_to_relationship_v4_filename = as_to_relationship_v4_filename
        self.as_to_relationship_v6_filename = as_to_relationship_v6_filename
        self.customer_cone_filename = customer_cone_filename

        self.import_ixps_info()
        self.import_as_to_ixps_info()
        self.import_as_faciiity_info()
        self.import_as_to_customer_cone()
        self.import_as_relationship(self.as_to_relationship_v4_filename, 'v4')
        self.import_as_relationship(self.as_to_relationship_v6_filename, 'v6')
        self.get_as_to_organisations()
        

    def export_data(self, output_filename):
        
        print('Exporting data to: '+output_filename)

        data_to_export = defaultdict(dict)
        for asn in self.asns: 
            asn = int(asn)
            data_to_export[asn]['asn'] = asn
            data_to_export[asn]['orgname'] = self.as2org.get(asn)
            data_to_export[asn]['ixps'] = self.as_to_ixp_info.get(asn, None)
            data_to_export[asn]['facilities'] = self.as_to_facility_info.get(asn)
            data_to_export[asn]['providers_v4'] = [(asn, self.as2org.get(asn)) for asn in self.c2p['v4'].get(asn, [])]
            data_to_export[asn]['providers_v6'] = [(asn, self.as2org.get(asn)) for asn in self.c2p['v6'].get(asn, [])]
            data_to_export[asn]['customers_v4'] = [(asn, self.as2org.get(asn)) for asn in self.p2c['v4'].get(asn, [])]
            data_to_export[asn]['customers_v6'] = [(asn, self.as2org.get(asn)) for asn in self.p2c['v6'].get(asn, [])]
            data_to_export[asn]['peers_v4'] = [(asn, self.as2org.get(asn)) for asn in self.p2p['v4'].get(asn, [])]
            data_to_export[asn]['peers_v6'] = [(asn, self.as2org.get(asn)) for asn in self.p2p['v6'].get(asn, [])]
            data_to_export[asn]['customer_cone'] = self.customer_cone.get(asn, None)
        
        lib.export_json(data_to_export, output_filename)
        print('Finished')
            
    def get_as_to_organisations(self):
        # Fetch for each candidate ASN its corresponding organisation name.

        print('Fetching organisation names for each ASN...')        

        extra_asns=set([])
        for asn in self.asns:
            extra_asns = extra_asns.union(self.c2p['v4'].get(asn, set()))
            extra_asns = extra_asns.union(self.c2p['v6'].get(asn, set()))
            extra_asns = extra_asns.union(self.p2c['v4'].get(asn, set()))
            extra_asns = extra_asns.union(self.p2c['v6'].get(asn, set()))
            extra_asns = extra_asns.union(self.p2p['v4'].get(asn, set()))
            extra_asns = extra_asns.union(self.p2p['v6'].get(asn, set()))

        extra_asns = [str(asn) for asn in extra_asns.union(self.asns)]

        chunk = 400
        caida_api_url= 'https://api.data.caida.org/as2org/v1/asns/'
        for i in range(0, len(extra_asns), chunk):
                    
            caida_api_url+= '_'.join(extra_asns[i:i+chunk])
            request_response = requests.get(url=caida_api_url).json()

            for entry in request_response['data']:
                asn = int(entry['asn'])
                orgname = entry['orgName']
                self.as2org[asn] = orgname

            #reset query url
            caida_api_url = 'https://api.data.caida.org/as2org/v1/asns/'


    def import_ixps_info(self):

        with open(self.ixp_filename) as f:
            next(f)
            for line in f:
                data = ujson.loads(line)
                country =  data.get('country') if not isinstance(data.get('country'), list) else data.get('country')[0]
                city =  data.get('city') if not isinstance(data.get('city'), list) else data.get('city')[0]
                self.ixp_info[ int(data['ix_id'])] = (data['name'], country, city)


    def import_as_to_ixps_info(self):
        with open(self.as_to_ixp_filename) as f:
            next(f)
            for line in f:
                data = ujson.loads(line)
                self.as_to_ixp_info[int(data['asn'])].add( self.ixp_info[int(data['ix_id'])] )


    def import_as_faciiity_info(self):
        data = lib.import_json(self.as_to_facility_filename)
        for entry in data['netfac']['data']:
            
            self.as_to_facility_info[int(entry['local_asn'])].add((entry['name'], entry.get('country'), entry.get('city')))


    def import_as_relationship(self, filename, version):
        with bz2.open(filename, 'rt') as file:
            for line in file:
                if not line.startswith('#'):
                    line = line.strip().split('|')
                    provider = int(line[0])
                    customer = int(line[1])
                    relationship = line[2]
                        
                    # provider-to-customer relations
                    if relationship == '-1': 
                        self.p2c[version][provider].add(customer)
                        self.c2p[version][customer].add(provider)
                    # peer-to-peer relations
                    elif relationship == '0':
                        self.p2p[version][provider].add(customer)
                        self.p2p[version][customer].add(provider)
                    
    
    def import_as_to_customer_cone(self):
        with bz2.open(self.customer_cone_filename, 'rt') as file:
            for line in file:
                if not line.startswith('#'):
                    line = line.strip().split()
                    self.customer_cone[int(line[0])] = [int(asn) for asn in line[1:]]
                    self.customer_cone[int(line[0])].remove(int(line[0]))

