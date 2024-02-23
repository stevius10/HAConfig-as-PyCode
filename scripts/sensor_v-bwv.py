import hashlib, requests

response = requests.get('https://www.bwv-berlin.de/wohnungsangebote.html', verify=False)

if "Derzeit können wir Ihnen leider keine Wohnungen zur Vermietung anbieten" not in response.text:
	print(hashlib.sha256(response.content).hexdigest())
else: 
	print()