from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

ns = {'zs':'http://www.loc.gov/zing/srw/'}
ET.register_namespace('zs', 'http://www.loc.gov/zing/srw/')

    # do your stuff
with open(sys.argv[1], 'r') as xmlfile:



    tree=ET.parse(xmlfile)

    root=tree.getroot()


    records = root.find('{http://www.loc.gov/zing/srw/}records')

    for record in records.findall('{http://www.loc.gov/zing/srw/}record/{http://www.loc.gov/zing/srw/}recordData/{http://www.loc.gov/MARC21/slim}record'):
        # print(record)
        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="245"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            title = x.text

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="024"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            identifier = x.text

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="c"]'):
            date = x.text

        for x in record.findall('{http://www.loc.gov/MARC21/slim}controlfield[@tag="001"]'):
            id_001 = x.text

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="016"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            id_016 = x.text

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="024"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            id_024 = x.text

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="035"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            id_035 = x.text

        # for title in record.findall('title'):
        #     print(title.text)
