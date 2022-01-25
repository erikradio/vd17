from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
from xml.etree.ElementTree import fromstring, ElementTree
import codecs

# https://sru.k10plus.de/vd17?version=2.0&operation=searchRetrieve&query=pica.nid=118756141&maximumRecords=500&startRecord=1&recordSchema=marcxml
# https://sru.k10plus.de/vd17?version=2.0&operation=searchRetrieve&query=pica.all=Schenk Erasmus II. von Limpurg&maximumRecords=500&startRecord=1&recordSchema=marcxml


csvfile =sys.argv[1]
# collection=sys.argv[3]
with open(sys.argv[1], 'rU', errors='ignore') as csvFile:
    reader = csv.DictReader(csvFile)
    worksCount = []
    for row in reader:
        gnd = row['GND-Nummer']
        url = 'https://sru.k10plus.de/vd17?version=2.0&operation=searchRetrieve&query=pica.nid='+ gnd + '&maximumRecords=500&startRecord=1&recordSchema=marcxml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        if r.raise_for_status():
            print(gnd)


        # print(r.text)
        tree = ElementTree(fromstring(r.content))
        root = tree.getroot()


        ns = {'zs':'http://docs.oasis-open.org/ns/search-ws/sruResponse'}

        vdResponse = r.text

        newFile=open('vd17_'+gnd+'.xml','w', encoding ='utf8')
        newFile.write(vdResponse)


        for count in root.findall('zs:numberOfRecords',ns):
            thing = int(count.text)
            worksCount.append(thing)
            if thing > 500:
                print(gnd, thing)
    # total = sum(gnd, worksCount)
    # print(total)
        # if thing < 500:
        #     print(thing)





# log = logging.getLogger(__name__)
# logging.basicConfig(level="DEBUG")


# newFile=open('cub_'+date+'.xml','w')
#

# for r in recs:
#     newFile.write(str(r))
#     print (r)
