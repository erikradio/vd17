def get_results_from_response():
    with open(sys.argv[1], 'rU', errors='ignore') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            gnd = row['GND-Nummer']
            url = 'https://sru.gbv.de/gvk?version=1.1&operation=searchRetrieve&query=pica.gnd=' + gnd +'&maximumRecords=500&startRecord=%s&recordSchema=mods'
            r = requests.get(url)
            r.encoding = 'utf-8'
            r.raise_for_status()

            # print(r.text)
            tree = ElementTree(fromstring(r.content))
            root = tree.getroot()


            ns = {'zs':'http://www.loc.gov/zing/srw/'}

            vdResponse = r.text

def main():
    aggregated_results = []
    offset = 0
    while True:
        
        response = requests.get(url % offset + 1)
        results_from_response = get_results_from_response(response)
        offset += len(results_from_response)
        aggregated_results = aggregated_results.extend(results_from_response)
        # Break condition
        if not results_from_response:  # If they send back an empty array
            break
