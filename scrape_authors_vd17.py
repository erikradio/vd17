from bs4 import BeautifulSoup
import pandas as pd
import csv, sys

html = open(sys.argv[1]).read()
htmlDoc = open(sys.argv[1], 'r')
soup = BeautifulSoup(html, features = 'lxml')
tables = soup.find_all("table")



#using pandas
# df = pd.read_html(htmlDoc)
# for i, table in enumerate(df):
#     table.to_csv('test.csv')

#with dynamic header generation
# output_dicts = []
# headers = set()
# for table in tables:
#     output_dict = {}
#     table_rows = table.find_all('tr')
#     for tr in table_rows:
#         tds = tr.find_all('td')
#         row = [i.text for i in tds]
#         # We expect first td to be header,
#         # second td to be data
#         if len(row) != 2:
#             continue  
#         key, value = row[0], row[1]
#         output_dict[key] = value
#         headers.add(key)
#     output_dicts.append(output_dict)
# with open('test.csv', 'w') as f:
#     w = csv.DictWriter(f, headers)
#     w.writeheader()
#     for output_dict in output_dicts:
#         w.writerow(output_dict)

#without dynamic header generation
fieldnames = ['GND-Nummer:', 'Bekenntnis:', 'Gesellschaftspflanze und -wort:','Aufnahme:','Aufenthaltsort des Mitglieds:',
                'Wirkung:','Bildungsweg:','Werdegang:','Wappen/Portrait:','name']

output_dicts = []

for table in tables:
    output_dict = {}
    table_rows = table.find_all('tr')
    for tr in table_rows:
        tds = tr.find_all('td')
        row = [i.text for i in tds]
        # We expect first td to be header,
        # second td to be data
        if row[0] not in fieldnames:
            output_dict['name'] = row[0]

        if len(row) != 2:
            continue  # Doesn't look like we expect
        key, value = row[0], row[1]
        output_dict[key] = value

    output_dicts.append(output_dict)

with open('test.csv', 'w', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames)
    w.writeheader()
    for output_dict in output_dicts:
        w.writerow(output_dict)
#using dicts
# outputDict = {}
# for table in tables:
#     table_rows = table.find_all('tr')
#     for tr in table_rows:
#         td = tr.find_all('td')
#         # print(td)
#
#         row = [i.text for i in td]
#         if len(row) > 1:
#             key, value = row[0], row[1]
#             outputDict[key] = value
#
#         if row[0] not in fieldnames:
#             name = row[0]
#             outputDict['name'] = name
#
#     with open('test.csv', 'w') as outcsv:
#         writer = csv.DictWriter(outcsv, fieldnames = fieldnames)
#         writer.writeheader()
#
#         for row in outputDict:
#             print(row)
#             writer.writerow(row)


#using lists
# output_rows = []
# for table in tables:
#     for table_row in table.findAll('tr'):
#         columns = table_row.findAll('td')
#         output_row = []
#         for column in columns:
#             output_row.append(column.text)
#         output_rows.append(output_row)

#

# with open('output.csv', 'w') as csvfile:
#      writer = csv.writer(csvfile)
#      writer.writerow(headers)
#      writer.writerows(output_rows)
