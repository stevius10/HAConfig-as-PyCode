import hashlib, requests
from bs4 import BeautifulSoup

items = []

requestUrl = 'https://www.wbm.de/wohnungen-berlin/angebote/'
responseWebsite = requests.get(requestUrl,  verify=False)
parserWebsite = BeautifulSoup(responseWebsite.content, 'html.parser')

contentWebsite = parserWebsite.find(id='content')

if contentWebsite is not None: 
	# print(contentWebsite)
	
	itemsWebsite = contentWebsite.find_all(class_='immo-element')
	# print(itemsWebsite)

	for itemWebsite in itemsWebsite: 
		
		if itemWebsite is not None: 
			
			area_list = ['friedrichshain', 'kreuzberg', 'schöneberg', 'neukölln']
			
			tmp = itemWebsite.find(class_='address'); address = tmp.get_text() if tmp else None 
			tmp = itemWebsite.find(class_='area'); area = tmp.get_text().lower() if tmp else None 
			tmp = itemWebsite.find(class_='main-property-rent'); rent =  tmp.get_text() if tmp else None
			tmp = itemWebsite.find(class_='main-property-size'); size =  tmp.get_text() if tmp else None
			tmp = itemWebsite.find(class_='main-property-rooms'); rooms =  tmp.get_text() if tmp else None
			tmp = itemWebsite.find(class_='check-property-list'); details =  tmp.get_text() if tmp else None
			
			# TODO: Falls kein WBS erf.
			if (address is not None) and ('WBS' not in details) and (any(a in area for a in area_list)): 
				item = "{} ({}/{}, {})".format(address, rooms, size, rent)
				items.append(item)

print(', '.join(map(str, items))[:254])
