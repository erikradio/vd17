from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

fieldnames = ['title', 'form', 'leader', 'author', 'date', 'place_of_publication','publisher',' TOC', 'content_type', 'media_type', 'carrier_type', 'id_control_number', 'id_national_bibliographic_control_number', 'id_other_standard_identifier','id_system_control_number']
ns = {'zs':'http://www.loc.gov/zing/srw/'}
ET.register_namespace('zs', 'http://www.loc.gov/zing/srw/')

microfilms = ['a', 'b','c','f','o','q']

    # do your stuff
with open(sys.argv[1], 'r') as xmlfile:
    output_dicts = []



    tree=ET.parse(xmlfile)

    root=tree.getroot()


    records = root.find('{http://www.loc.gov/zing/srw/}records')

    for record in records.findall('{http://www.loc.gov/zing/srw/}record/{http://www.loc.gov/zing/srw/}recordData/{http://www.loc.gov/MARC21/slim}record'):
        output_dict = {}
        # print(record)
        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="245"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            title = x.text
            output_dict['title'] = title

        for x in record.findall('{http://www.loc.gov/MARC21/slim}leader'):
            leader = x.text[6]
            if leader in microfilms:
                output_dict['leader'] = 'microfilm'
            else:
                output_dict['leader'] = leader

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="300"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            form = x.text
            output_dict['form'] = form

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

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="336"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            contentType = x.text
            output_dict['content_type'] = contentType

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="337"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            mediaType = x.text
            output_dict['media_type'] = mediaType

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="338"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            carrierType = x.text
            output_dict['carrier_type'] = carrierType

        for x in record.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="505"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]'):
            TOC = x.text
            output_dict['TOC'] = TOC

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
        # print(output_dicts)


        with open("output.csv", "w") as f:
            # field_names = [k for k in output_dicts[0]]  # all our dicts have the same keys
            writer = csv.DictWriter(f, fieldnames=fieldnames)  # Create the writer instance
            writer.writeheader()  # write the header
            # Begin writing data
            for row in output_dicts:
                writer.writerow(row)
