import sys, json, csv
from argparse import ArgumentParser
from xml.etree import ElementTree as ET
from datetime import datetime
import copy, time, datetime
from collections import defaultdict
import glob
from pathlib import Path

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
    roleList = []
    langList = []

    for marc in record.findall('{http://www.loc.gov/MARC21/slim}record'):
        # title
        title=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="245"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        if title is not None:
            data['title'] = title.text
        else:
            data['title'] = ''
        subtitle=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="245"]/{http://www.loc.gov/MARC21/slim}subfield[@code="b"]')
        if subtitle is not None:
            data['subtitle'] = title.text
        else:
            data['subtitle'] = ''
        #  author
        # for nameField in marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="100"]'):
        #     # print(name.attrib)
        #     if nameField is not None:
        #         code = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="4"]')
        #         name = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        #         if code.text == 'aut':
        #             data['author'] = name.text
        #     else:
        #         data['author'] = ''
        for nameField in marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="100"]'):
            # print(name.attrib)
            codes = nameField.findall('{http://www.loc.gov/MARC21/slim}subfield[@code="4"]')
            for code in codes:
                names = nameField.findall('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
                for name in names:
                    roles[code.text].append(name.text)
        # data.update(roles)

        #marc 751 if subfield 4 is 'pup'
        for nameField in marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="751"]'):
            # print(name.attrib)
            if nameField is not None:
                code = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="4"]')
                name = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
                if code.text == 'pup':
                    data['normalizedPlace'] = name.text
            else:
                data['normalizedPlace'] = ''


        # publisher
        pubName=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="b"]')
        if pubName is not None:
            data['publisherName'] = pubName.text
        else:
            data['publisherName'] = ''
        # place of publication
        pubPlace=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        if pubPlace is not None:
            data['publisherPlace'] = pubPlace.text
        else:
            data['publisherPlace'] = ''
        # date of publication
        pubDate=marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="c"]')
        if pubDate is not None:
            data['publicationDate'] = pubDate.text
        else:
            data['publicationDate'] = ''
        # language
        wlanglist = []
        wlangs=marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="041"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        if wlangs is not None:
            for wlang in wlangs:
                wlanglist.append(wlang.text)
                data['workLanguage'] = wlanglist

        # original language
        olanglist = []
        olangs=marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="041"]/{http://www.loc.gov/MARC21/slim}subfield[@code="h"]')
        if olangs is not None:
            for olang in olangs:
                olanglist.append(olang.text)
                data['originalLanguage'] = olanglist

        #intermediate language
        ilanglist = []
        ilangs=marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="041"]/{http://www.loc.gov/MARC21/slim}subfield[@code="k"]')
        if ilangs is not None:
            for ilang in ilangs:
                ilanglist.append(ilang.text)
                data['intermediateLanguage'] = ilanglist

        # genre/form
        genreList = []
        genres = marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="655"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        if genres is not None:
            for genre in genres:
                genreList.append(genre.text)
                data['genre'] = genreList


        vd17ID = marc.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="024"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        if vd17ID is not None:
            data['id'] = vd17ID.text
        else:
            data['id'] = ''


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

    # ['aut', 'dte', 'ctb', 'prt',hnr]
        # print(bib)
    return bib


def write(rows):
    fieldnames = set()
    for row in rows:
        for key in row:
            fieldnames.add(key)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    if not rows:
        return rows
    with open('vd17_'+str(st)+'.csv','w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            for field in fieldnames:
                if field not in row:
                    row[field] = None
            # print(row)
            writer.writerow(row)

def main():
    bibs = []
    path = Path("/Users/erra1244/Desktop/vd17/marcworks")
    for file in path.glob("*.xml"):
        # print(file)
        with open(file,'r') as xmlFile:
            tree = ET.parse(xmlFile)
            root = tree.getroot()

            # print(root)
            recordCount = root.find('./{http://docs.oasis-open.org/ns/search-ws/sruResponse}numberOfRecords')
            recordCount = int(recordCount.text)
            if recordCount > 0:
                for record in root.findall('{http://docs.oasis-open.org/ns/search-ws/sruResponse}records/{http://docs.oasis-open.org/ns/search-ws/sruResponse}record/{http://docs.oasis-open.org/ns/search-ws/sruResponse}recordData'):

                    bibs.extend(getData(record))
    write(bibs)



# make this a safe-ish cli script
if __name__ == '__main__':
    # print(tree)

    main()

    
