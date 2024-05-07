import hashlib, requests

response = requests.get('https://www.gwneukoelln.de/wohnungen/wohnungsangebote/', verify=False)

if "keine passenden Wohnungen" not in response.text:
	print(hashlib.sha256(response.content).hexdigest())
else: 
	print()