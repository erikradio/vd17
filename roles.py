for nameField in marc.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="700"]'):
            # print(name.attrib)
            if nameField is not None:
                code = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="4"]')
                name = nameField.find('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
                if code and name is not None:
                    if code.text == 'aut':
                        data['author'] = name.text
                    else:
                        data['author'] = ''
        
                    if code.text == 'prt':
                        data['printer'] = name.text
                    else:
                        data['printer'] = ''
        
                    if code.text == 'dte':
                        data['dedicatee'] = name.text
                    else:
                        data['dedicatee'] = ''
        
                    if code.text == 'ctb':
                        data['contributor'] = name.text
                    else:
                        data['contributor'] = ''
        
                    if code.text == 'hnr':
                        data['honoree'] = name.text
                    else:
                        data['honoree'] = ''
