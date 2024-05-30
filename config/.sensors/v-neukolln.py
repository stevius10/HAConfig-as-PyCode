import requests
from hashlib import sha256

def scrape_neukolln():
  request_url = 'https://www.gwneukoelln.de/wohnungen/wohnungsangebote/'
  response = requests.get(request_url, verify=False)
  if "keine passenden Wohnungen" not in response.text:
    return sha256(response.content).hexdigest()
  return None

if __name__ == "__main__":
  print(scrape_neukolln())