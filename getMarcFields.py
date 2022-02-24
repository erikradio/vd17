from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
from xml.etree import ElementTree as ET
import codecs
from datetime import datetime
import copy, time, datetime
from collections import defaultdict

# Personal names - author, editor, translator, and anything else that appears in the personal names fields
# Title (transcribed from the piece, and normed)
# Language
# Genre/topic
# Printers/publishers
# [Places of printing/publication]
# Dates of publication


def getData(record):
    bib = []
    data = {}
    roles = defaultdict(list)

    for marc in record.findall('{http://www.loc.gov/MARC21/slim}record'):
        # title
        title=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="245"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        data['title'] = title.text
        #  author
        for nameField in marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="100"]'):
            # print(name.attrib)
            code = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="4"]')
            name = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
            if code.text == 'aut':
                data['author'] = name.text


        # publisher
        pubName=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="b"]')
        data['publisherName'] = pubName.text
        # place of publication
        pubPlace=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        data['publisherPlace'] = pubPlace.text
        # date of publication
        pubDate=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="c"]')
        data['publicationDate'] = pubDate.text
        # language
        lang=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="041"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        data['language'] = lang.text
        # genre/form
        genre = marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="655"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        data['genre'] = genre.text
        # various roles


        for nameField in marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="700"]'):
            # print(name.attrib)
            codes = nameField.findall('{http://www.loc.gov/MARC21/slim}subfield[@code="4"]')
            for code in codes:
                names = nameField.findall('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
                for name in names:
                    roles[code.text].append(name.text)
        data.update(roles)
        bib.append(data)
        # print(data)

        # print(data)
    return bib


def write(rows):
    fieldnames = set()
    for row in rows:
        for key in row:
            fieldnames.add(key)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    if not rows:
        raise ValueError("No data provided")
    with open('vd17_'+str(st)+'.csv','w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            for field in fieldnames:
                if field not in row:
                    row[field] = None
            writer.writerow(row)

def main():

    with open(sys.argv[1],'r') as xmlFile:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        bibs = []
        for record in root.findall('{http://docs.oasis-open.org/ns/search-ws/sruResponse}records/{http://docs.oasis-open.org/ns/search-ws/sruResponse}record/{http://docs.oasis-open.org/ns/search-ws/sruResponse}recordData'):
            bibs.extend(getData(record))
        write(bibs)


# make this a safe-ish cli script
if __name__ == '__main__':
    # print(tree)

    main()
