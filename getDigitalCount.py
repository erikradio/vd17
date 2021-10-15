from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
from xml.etree.ElementTree import fromstring, ElementTree
import codecs



csvfile =sys.argv[1]
# collection=sys.argv[3]
with open(sys.argv[1], 'rU', errors='ignore') as csvFile:
    reader = csv.DictReader(csvFile)

    urns = []
    records = []
    for row in reader:
        gnd = row['GND-Nummer']
        url = 'https://sru.k10plus.de/vd17?version=2.0&operation=searchRetrieve&query=pica.nid=' + gnd + '&maximumRecords=500&startRecord=1&recordSchema=marcxml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        r.raise_for_status()

        # print(r.text)
        tree = ElementTree(fromstring(r.content))
        root = tree.getroot()


        ns = {'zs':'http://docs.oasis-open.org/ns/search-ws/sruResponse'}




        for count in root.findall('zs:numberOfRecords',ns):
            thing = int(count.text)

            if thing > 500:
                print(thing,gnd)
            records.append(thing)
        for x in root.findall('{http://docs.oasis-open.org/ns/search-ws/sruResponse}records/{http://docs.oasis-open.org/ns/search-ws/sruResponse}record/{http://docs.oasis-open.org/ns/search-ws/sruResponse}recordData/{http://www.loc.gov/MARC21/slim}record/{http://www.loc.gov/MARC21/slim}datafield[@tag="856"]/{http://www.loc.gov/MARC21/slim}subfield[@code="u"]'):
            print(x.text)

            urns.append(x.text)



# 9176 urns 
# 14205 records
