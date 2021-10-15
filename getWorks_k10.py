from sickle import Sickle
import sys, json, csv
from argparse import ArgumentParser
import logging
import requests
from xml.etree.ElementTree import fromstring, ElementTree
import codecs

#https://verbundwiki.gbv.de/display/VZG/SRU
#*******http://sru.gbv.de/gvk?version=1.1&operation=searchRetrieve&query=pica.pne=100014704&maximumRecords=10&recordSchema=PicaXML

# Kunowitz, Freiherr Johann Dietrich von - 104133309  k10:27, vd:9

# Neumark, Georg - 118587404  k10:233, vd: 62

# Stubenberg, Johann Wilhelm Herr von - 118756141

csvfile =sys.argv[1]
# collection=sys.argv[3]
with open(sys.argv[1], 'rU', errors='ignore') as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        gnd = row['GND-Nummer']
        # url = 'https://sru.gbv.de/gvk?version=1.1&operation=searchRetrieve&query=pica.gnd='+ gnd + '&maximumRecords=500&startRecord=1&recordSchema=mods'
        url = 'https://sru.gbv.de/gvk?version=1.1&operation=searchRetrieve&query=pica.gnd=118756141&maximumRecords=500&startRecord=1&recordSchema=marcxml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        r.raise_for_status()

        # print(r.text)
        tree = ElementTree(fromstring(r.content))
        root = tree.getroot()


        ns = {'zs':'http://www.loc.gov/zing/srw/'}

        vdResponse = r.text



        newFile=open('k10_'+gnd+'.xml','w', encoding ='utf8')
        newFile.write(vdResponse)

        for count in root.findall('zs:numberOfRecords',ns):
            thing = int(count.text)
            # print(thing)
            if thing > 500:
                print(thing,gnd)





# log = logging.getLogger(__name__)
# logging.basicConfig(level="DEBUG")


# newFile=open('cub_'+date+'.xml','w')
#

# for r in recs:
#     newFile.write(str(r))
#     print (r)
