import requests
from bs4 import BeautifulSoup

ANBIETER = {
  "sensor.v_charlottenburg": {
    "name": "Charlottenburger Baugenossenschaft eG",
    "url": "https://charlotte1907.de/wohnungsangebote/woechentliche-angebote"
  },
  "sensor.v_lichtenberg": {
    "name": "Wohnungsbaugenossenschaft Lichtenberg eG",
    "url": "https://www.wgli.de/wohnungssuche/"
  },
  "sensor.v_gruenemitte": {
    "name": "Wohnungsgenossenschaft Grüne Mitte Hellersdorf eG",
    "url": "https://wohnungsgenossenschaft.de/wohnungsbestand/"
  },
  "sensor.v_zentrum": {
    "name": "Wohnungsbaugenossenschaft Zentrum eG",
    "url": "https://www.wbg-zentrum.de/wohnen/wohnungsbestaende/"
  },
  "sensor.v_1892": {
    "name": "Berliner Bau- und Wohnungsgenossenschaft von 1892 eG",
    "url": "https://www.1892.de/wohnen/wohnungsangebote/"
  },
  "sensor.v_altglienicke": {
    "name": "Wohnungsgenossenschaft Altglienicke eG",
    "url": "https://www.wg-altglienicke.de/wohnungen"
  },
  "sensor.v_koepenick_nord": {
    "name": "Wohnungsbaugenossenschaft Köpenick Nord eG",
    "url": "https://www.koepenick-nord.de/unsere-wohnungen.html"
  },
  "sensor.v_reinickendorf": {
    "name": "Wohnungsbaugenossenschaft Reinickendorf eG", 
    "url": "https://charlotte1907.de/genossenschaft/wohnanlagenansprechpartner/bezirk/reinickendorf"
  },
  "sensor.v_solidaritaet": {
    "name": "Wohnungsbaugenossenschaft solidarity E.G.",
    "url": "https://wg-solidaritaet.de/wohnen/mietangebote/"
  },
  "sensor.v_neues_berlin": {
    "name": "Wohnungsbaugenossenschaft NEUES BERLIN eG",
    "url": "https://www.neues-berlin.de/wohnen/wohnungsangebote/"
  },
  "sensor.v_treptow_park": {
    "name": "Wohnungsgenossenschaft Treptow Park eG",
    "url": "https://www.berliner-genossenschaft.de/angebote/aktuelle-angebote/"
  },
  "sensor.v_bwv_berlin": {
    "name": "Beamten-Wohnungs-Verein zu Berlin eG",
    "url": "https://www.bwv-berlin.de/wohnungsangebote.html"
  },
  "sensor.v_merkur": {
    "name": "Wohnungsbaugenossenschaft MERKUR eG",
    "url": "https://www.wbg-merkur.de/wohnen/wohnungsangebote/"
  },
  "sensor.v_berlin_nord": {
    "name": "Wohnungsgenossenschaft BERLIN-NORD eG",
    "url": "https://wohnungsgenossenschaft-berlin-nord.de/wohnungsangebote/"
  },
  "sensor.v_wilhelmsruh": {
    "name": "Wohnungsbaugenossenschaft Wilhelmsruh eG",
    "url": "https://www.wbg-wilhelmsruh.de/unsere-wohnungen/freie-wohnungen/"
  },
  "sensor.v_prenzlauer_berg": {
    "name": "Wohnungsbaugenossenschaft Prenzlauer Berg eG",
    "url": "https://www.wbg-pb.de/wohnungsangebote/"
  },
  "sensor.v_weissensee": {
    "name": "Wohnungsbaugenossenschaft Weißensee eG",
    "url": "https://www.wg-weissensee.de/page83/"
  },
  "sensor.v_koepenick": {
    "name": "Wohnungsbaugenossenschaft Köpenick eG",
    "url": "https://www.wg-koepenick.de/wohnungsangebote/"
  },
  "sensor.v_treptow": {
    "name": "Wohnungsbaugenossenschaft Treptow eG",
    "url": "https://www.wbg-treptow.de/wohnungsangebote/"
  },
  "sensor.v_berliner_genossenschaft": {
    "name": "Berliner Genossenschaft",
    "url": "https://www.berliner-genossenschaft.de/angebote/aktuelle-angebote/"
  },
  "sensor.v_degewo": {
    "name": "Degewo",
    "url": "https://immosuche.degewo.de/de/search"
  }
}

def scrape_website(request_url, content_id=None, content_class=None, item_tag=None, item_class=None, address_tag=None, address_class=None, additional_processing=None):
  print(f"Starting scrape for {request_url}")
  items = []
  try:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(request_url, headers=headers, verify=True)
    response.raise_for_status()
    parser = BeautifulSoup(response.content, 'html.parser')

    if content_id:
      content = parser.find(id=content_id)
    elif content_class:
      content = parser.find(class_=content_class)
    else:
      content = parser
    
    if content:
      print(f"Parsed content for {request_url}:\n{str(content)[:254]}")
      items_website = content.find_all(item_tag, class_=item_class)
      for item in items_website:
        address = item.find(address_tag, class_=address_class).get_text().strip() if item.find(address_tag, class_=address_class) else None
        if address:
          if additional_processing:
            address = additional_processing(item, address)
          items.append(address)
    else:
      print(f"No content found for {request_url}")
  except Exception as e:
    pass
  
  return items

def scrape_1892():
  return scrape_website(
    ANBIETER["sensor.v_1892"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_altglienicke():
  return scrape_website(
    ANBIETER["sensor.v_altglienicke"]["url"],
    content_class='immo-listing__list',
    item_tag='article',
    item_class='immo-listing__list-item', 
    address_tag='div',
    address_class='immo-listing__list-item-title'
  )

def scrape_koepenick_nord():
  return scrape_website(
    ANBIETER["sensor.v_koepenick_nord"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_charlottenburg():
  return scrape_website(
    ANBIETER["sensor.v_charlottenburg"]["url"],
    content_class='immo-listing__list',
    item_tag='article',
    item_class='immo-listing__list-item',
    address_tag='div',
    address_class='immo-listing__list-item-title'
  )

def scrape_lichtenberg():
  return scrape_website(
    ANBIETER["sensor.v_lichtenberg"]["url"],
    content_class='immo-listing__list',
    item_tag='article',
    item_class='immo-listing__list-item',
    address_tag='div',
    address_class='immo-listing__list-item-title'
  )

def scrape_gruenemitte():
  return scrape_website(
    ANBIETER["sensor.v_gruenemitte"]["url"],
    content_class='siedlungshof',
    item_tag='div',
    item_class='siedlungshof',
    address_tag='h3',
    address_class=None
  )

def scrape_zentrum():
  return scrape_website(
    ANBIETER["sensor.v_zentrum"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )
  
def scrape_reinickendorf():
  return scrape_website(
    ANBIETER["sensor.v_reinickendorf"]["url"],
    content_class='immo-listing',
    item_tag='div',
    item_class='immo-listing__item',
    address_tag='div',
    address_class='immo-listing__item-title'
  )

def scrape_solidarity():
  return scrape_website(
    ANBIETER["sensor.v_solidaritaet"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_neues_berlin():
  return scrape_website(
    ANBIETER["sensor.v_neues_berlin"]["url"],
    content_class='tx-openimmo',
    item_tag='article', 
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_treptow_park():
  def process_address(item, address):
    return item.find('h3').get_text().strip()
  
  return scrape_website(
    ANBIETER["sensor.v_treptow_park"]["url"],
    content_class='tx-openimmo',
    item_tag='div',
    item_class='angebot', 
    address_tag='h3',
    address_class=None,
    additional_processing=process_address
  )

def scrape_bwv_berlin():
  return scrape_website(
    ANBIETER["sensor.v_bwv_berlin"]["url"],
    content_id='c1642',
    item_tag='p',
    item_class=None,
    address_tag='p',
    address_class=None
  )
  
def scrape_merkur():
  return scrape_website(
    ANBIETER["sensor.v_merkur"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_berlin_nord():
  return scrape_website(
    ANBIETER["sensor.v_berlin_nord"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_wilhelmsruh():
  return scrape_website(
    ANBIETER["sensor.v_wilhelmsruh"]["url"],
    content_class='tx-openimmo',
    item_tag='p',
    item_class=None,
    address_tag='p',
    address_class=None
  )
  
def scrape_prenzlauer_berg():
  return scrape_website(
    ANBIETER["sensor.v_prenzlauer_berg"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_weissensee():
  return scrape_website(
    ANBIETER["sensor.v_weissensee"]["url"],
    content_class='tx-openimmo', 
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )
  
def scrape_koepenick():
  return scrape_website(
    ANBIETER["sensor.v_koepenick"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_treptow():
  return scrape_website(
    ANBIETER["sensor.v_treptow"]["url"],
    content_class='tx-openimmo',
    item_tag='article',
    item_class='immobilie',
    address_tag='div',
    address_class='immobilie__daten__ort'
  )

def scrape_berliner_genossenschaft():
  return scrape_website(
    ANBIETER["sensor.v_berliner_genossenschaft"]["url"],
    content_class='tx-openimmo',
    item_tag='div',
    item_class='angebot',
    address_tag='h3',
    address_class=None
  )

def scrape_degewo():
  return scrape_website(
    ANBIETER["sensor.v_degewo"]["url"],
    content_class='row',
    item_tag='div',
    item_class='col-sm-6 col-lg-4',
    address_tag='div',
    address_class='address'
  )
  
results = [
    ', '.join(scrape_charlottenburg())[:254],
    ', '.join(scrape_lichtenberg())[:254],
    ', '.join(scrape_gruenemitte())[:254],
    ', '.join(scrape_zentrum())[:254],
    ', '.join(scrape_1892())[:254],
    ', '.join(scrape_altglienicke())[:254],
    ', '.join(scrape_koepenick_nord())[:254],
    ', '.join(scrape_reinickendorf())[:254],
    ', '.join(scrape_solidarity())[:254],
    ', '.join(scrape_neues_berlin())[:254],
    ', '.join(scrape_treptow_park())[:254],
    ', '.join(scrape_bwv_berlin())[:254],
    ', '.join(scrape_merkur())[:254],
    ', '.join(scrape_berlin_nord())[:254],
    ', '.join(scrape_wilhelmsruh())[:254],
    ', '.join(scrape_prenzlauer_berg())[:254],
    ', '.join(scrape_weissensee())[:254],
    ', '.join(scrape_koepenick())[:254],
    ', '.join(scrape_treptow())[:254],
    ', '.join(scrape_berliner_genossenschaft())[:254],
    ', '.join(scrape_degewo())[:254]
]

print(', '.join(results))