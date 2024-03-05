import hashlib, requests
from bs4 import BeautifulSoup 

items = []; 

requestUrl = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=700&gesamtflaeche_von=50&gesamtflaeche_bis=&zimmer_von=2&zimmer_bis=&keinwbs=1&sort-by=recent'

responseWebsite = requests.get(requestUrl,  verify=False)
parserWebsite = BeautifulSoup(responseWebsite.content, 'html.parser')
[s.extract() for s in parserWebsite(['script'])]

contentWebsite = parserWebsite.find(class_ = 'filtered-mietangebote')
# print(contentWebsite)

if contentWebsite is not None: 
	
	itemsWebsite = contentWebsite.find_all(class_='angebot-content')
	print(itemsWebsite)
	
	'''
	<tr class="angebot-address">
	<th class="screen-reader-text">Adresse</th>
	<td>
	<a href="https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/0100-01032-1402-0388/"><address>Daumstr. 203, 13599 Berlin/Haselhorst</address><h3 class="angebot-title">Schicke Neubauwohnung mit Fußbodenheizung im Erstbezug</h3></a> </td>
	</tr>
	<tr class="angebot-area">
	<th>Fläche</th>
	<td>1 Zimmer | 46,25 m2</td>
	</tr>
	<tr class="availability">
	<th>Frei ab</th>
	<td>01.03.2023</td>
	</tr>
	<tr class="angebot-kosten">
	<th>Gesamtmiete</th>
	<td>ab 686,35 €</td>
	</tr>
	<tr class="angebot-characteristics">
	<th class="screen-reader-text">besondere Eigenschaften</th>
	<td>
'''
	
	for itemWebsite in itemsWebsite: 
		
		if itemWebsite is not None: 
			print(itemsWebsite)
			tmp = itemWebsite.find('address', class_=None); address = tmp.get_text().replace('\t', '').replace('Berlin/', '') if tmp else None 
			tmp = itemWebsite.find(class_='angebot-area').find('td'); area =  tmp.get_text() if tmp else None
			tmp = itemWebsite.find(class_='angebot-kosten').find('td'); rent =  tmp.get_text() if tmp else None
			
			if address is not None:
				item = "{} ({}, {})".format(address, area, rent).replace('\n', '')
				items.append(item)

else:
  if not parserWebsite: 
    print("Error parse")
    
print(', '.join(map(str, items)))