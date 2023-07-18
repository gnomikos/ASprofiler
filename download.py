#!/usr/bin/env python3

import datetime
from bs4 import BeautifulSoup
import requests
import wget
import os

class Download():
    # Downloads all the necessary datasets

    def __init__(self):
        self.ixp_filename = None
        self.as_to_ixp_filename = None
        self.peeringdb_filename = None
        self.as_relations_v4_filename = None
        self.as_relations_v6_filename = None
        self.as_cust_cone_filename = None

        print('Searching for the most recent datasets...')
        self.download_caida_relationship_cone_datasets()
        self.download_peeringdb()
        self.download_caida_ixp_asn_datasets()


    def download_file(self, webpage, filename):
        if os.path.exists('./' + filename):
            print('Skipping, already exists:', filename)
        else:
            print('Downloading: ' + webpage+filename)
            wget.download(webpage + filename)
            print()
        

    def download_caida_ixp_asn_datasets(self):
        webpage = 'https://publicdata.caida.org/datasets/ixps/'
        html_page = requests.get(webpage)
        soup = BeautifulSoup(html_page.text, "lxml")

        ixs = []
        ix_asns = []
        for link in soup.findAll('a'):
            if link.has_attr('href'):

                if 'ixs_' in link['href']:
                    ixs.append(link['href'])
                elif 'ix-asns_' in link['href']:
                    ix_asns.append(link['href'])

        #To find the most recent snapshot
        ixs.sort()
        ix_asns.sort()

        self.download_file(webpage, ixs[-1])
        self.download_file(webpage, ix_asns[-1])
        self.ixp_filename = ixs[-1]
        self.as_to_ixp_filename = ix_asns[-1]


    def download_peeringdb(self):
        webpage = 'https://publicdata.caida.org/datasets/peeringdb/'

        previous_date = (datetime.datetime.today() - datetime.timedelta(days=1))
        year = str(previous_date.year)
        month = '{:02d}'.format(previous_date.month)
        day = '{:02d}'.format(previous_date.day)
        
        webpage += year+'/'+month+'/'
        file = 'peeringdb_2_dump_' +year+'_'+month+'_'+day+'.json'
        self.download_file(webpage, file)
        self.peeringdb_filename =  file
        
        
    def download_caida_relationship_cone_datasets(self):
        webpage = 'https://publicdata.caida.org/datasets/as-relationships/serial-2/'
        html_page = requests.get(webpage)
        soup = BeautifulSoup(html_page.text, "lxml")

        as_relations_v4 = []

        for link in soup.findAll('a'):
            if link.has_attr('href'):

                if 'as-rel2.txt.bz2' in link['href']:
                    as_relations_v4.append(link['href'])

        #To find the most recent snapshot
        as_relations_v4.sort()

        self.download_file(webpage, as_relations_v4[-1])
        self.as_relations_v4_filename = as_relations_v4[-1]


        webpage = 'https://publicdata.caida.org/datasets/2013-asrank-data-supplement/data/'
        html_page = requests.get(webpage)
        soup = BeautifulSoup(html_page.text, "lxml")

        as_relations_v6 = []
        as_cust_cone = []

        for link in soup.findAll('a'):
            if link.has_attr('href'):

                if 'as-rel.v6-stable.txt.bz2' in link['href']:
                    as_relations_v6.append(link['href'])
                elif 'ppdc-ases.txt.bz2' in link['href']:
                    as_cust_cone.append(link['href'])

        #To find the most recent snapshot
        as_relations_v6.sort()
        as_cust_cone.sort()

        self.download_file(webpage, as_relations_v6[-1])
        self.download_file(webpage, as_cust_cone[-1])
        self.as_relations_v6_filename = as_relations_v6[-1]
        self.as_cust_cone_filename = as_cust_cone[-1]
            

