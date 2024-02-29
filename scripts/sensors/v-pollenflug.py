import hashlib, requests
from bs4 import BeautifulSoup 

items = []; 

requestUrl = 'https://www.gesundheit.de/biowetter/berlin-id213016/#:~:text=Biowetter%20Berlin%20(Region),-Gestern&text=Die%20derzeitige%20Wetterlage%20beeinflusst%20Arbeitsleistung,und%20Stoffwechsel%20laufen%20beschleunigt%20ab.'

responseWebsite = requests.get(requestUrl,  verify=False)
parserWebsite = BeautifulSoup(responseWebsite.content, 'html.parser')
[s.extract() for s in parserWebsite(['script'])]

contentWebsite = parserWebsite.find(class_ = 'article')
#print(contentWebsite)

if contentWebsite is not None: 
	
	itemsWebsite = contentWebsite.find_all(class_='table-ps')
	itemsBiowetter = itemsWebsite[2].find_all('tr')
	
	items = []
	for itemBiowetter in itemsBiowetter: 
		
		itemBiowetterName = itemBiowetter.select('td[data-title*=":"]')
		if itemBiowetterName is not None: 
			name = itemBiowetterName[0].get_text(strip=True) if itemBiowetterName else None 
			
		itemBiowetterValue = itemBiowetter.select('td[data-title*="Heute"]')
		if itemBiowetterValue is not None: 
			value = itemBiowetterValue[0].get_text(strip=True) if itemBiowetterValue else None 
			
			if (value not in [ None, 'None', 'keine'] and value != 'kein Pollenflug' ):
				if 'starker' in value: # Prüfen
					value='+++'
				elif 'ß' in value: # Encoding 'mäßig'
					value='++'
				elif value == 'schwacher Pollenflug': 
					value='+'
				elif value == 'kein bis schwacher Pollenflug' in value: 
					value=''
			
				items.append("{}{}".format(name, value))
				
		
print(', '.join(map(str, items)))