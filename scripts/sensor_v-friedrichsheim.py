import hashlib, requests
from bs4 import BeautifulSoup

items = []

requestUrl = 'https://www.friedrichsheim-eg.de/category/freie-wohnungen/'
responseWebsite = requests.get(requestUrl,  verify=False)
parserWebsite = BeautifulSoup(responseWebsite.content, 'html.parser')

contentWebsite = parserWebsite.find(id='main')

if contentWebsite is not None: 
	# print(contentWebsite)
	
	itemsWebsite = contentWebsite.find_all('h2', class_='entry-title')
	# print(itemsWebsite)

	for itemWebsite in itemsWebsite: 
		
		if itemWebsite is not None: 
			
			tmp = itemWebsite; address = tmp.get_text() if tmp else None 
			
			if address is not None: 
				item = "{}".format(address)
				items.append(item)

print(', '.join(map(str, items)))
