import hashlib, requests, json
from bs4 import BeautifulSoup

items = []; 

requestUrl = 'https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php'
requestHeaders = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest' }
requestData = { 'q': 'wf-save-srch', 'save': 'false', 'qm_min': '50', 'miete_max': '600', 'rooms_min': '2','bez[]': [ '01_00', '02_00', '03_00', '04_00','02_00' ],'wbs': 0 }
responseWebsite = requests.post(requestUrl, headers=None, data=requestData, verify=False).text
contentWebsite = BeautifulSoup(json.loads(responseWebsite)['searchresults'], 'html.parser')

# print(contentWebsite)
itemsWebsite = contentWebsite.find_all(class_='_tb_left')
if itemsWebsite is not None: 
	
	for itemWebsite in itemsWebsite: 
		
		if itemWebsite is not None: 
			
			item =  itemWebsite.get_text() if itemWebsite else None
			item = item.replace('  ', ' ')
			detail, address = item.split('|')
					
			item = "{} ({})".format(address, detail)
			items.append(item)
	
print(', '.join(map(str, items)))