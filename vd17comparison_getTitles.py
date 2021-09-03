from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

fieldnames = ['title', 'author', 'date', 'place_of_publication','publisher', 'id_control_number', 'id_national_bibliographic_control_number', 'id_other_standard_identifier','id_system_control_number']
ns = {'zs':'http://www.loc.gov/zing/srw/'}
ET.register_namespace('zs', 'http://www.loc.gov/zing/srw/')

    # do your stuff
with open(sys.argv[1], 'r') as xmlfile:
    output_dicts = []



    tree=ET.parse(xmlfile)

    root=tree.getroot()


    records = root.find('{http://docs.oasis-open.org/ns/search-ws/sruResponse}records')

    for record in records.findall('{http://docs.oasis-open.org/ns/search-ws/sruResponse}record/{http://docs.oasis-open.org/ns/search-ws/sruResponse}recordData/{http://www.loc.gov/MARC21/slim}record'):
        output_dict = {}
        # print(record)
        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="245"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            title = x.text
            output_dict['title'] = title

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="100"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            author = x.text
            output_dict['author'] = author


        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="c"]'):
            date = x.text
            output_dict['date'] = date

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            place_of_publication = x.text
            output_dict['place_of_publication'] = place_of_publication

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="b"]'):
            publisher = x.text
            output_dict['publisher'] = publisher

        for x in record.findall('{http://www.loc.gov/MARC21/slim}controlfield[@tag="001"]'):
            id_control_number = x.text
            output_dict['id_control_number'] = id_control_number

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="016"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            if len(x.text) > 0:
                id_national_bibliographic_control_number = x.text
                output_dict['id_national_bibliographic_control_number'] = id_national_bibliographic_control_number

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="024"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            id_other_standard_identifier = x.text
            output_dict['id_other_standard_identifier'] = id_other_standard_identifier

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="035"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            id_system_control_number = x.text
            output_dict['id_system_control_number'] = id_system_control_number



        output_dicts.append(output_dict)
        print(output_dicts)


        with open("output.csv", "w") as f:
            # field_names = [k for k in output_dicts[0]]  # all our dicts have the same keys
            writer = csv.DictWriter(f, fieldnames=fieldnames)  # Create the writer instance
            writer.writeheader()  # write the header
            # Begin writing data
            for row in output_dicts:
                writer.writerow(row)
