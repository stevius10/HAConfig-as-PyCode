import json
import requests
from bs4 import BeautifulSoup

# TODO: sys.path to constants/settings.py
AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_AREA = 50
AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_RENT = 700
AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_ROOMS = 2
AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS = {
  "sensor.scrape_friedrichsheim": "https://www.friedrichsheim-eg.de/category/freie-wohnungen/",
  "sensor.scrape_gewobag": f"https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=neukoelln-rudow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_RENT}&gesamtflaeche_von={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_AREA}&gesamtflaeche_bis=&zimmer_von={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_ROOMS}&zimmer_bis=&keinwbs=1&sort-by=recent",
  "sensor.scrape_ibw": "https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php",
  "sensor.scrape_wbm": "https://www.wbm.de/wohnungen-berlin/angebote/",
  "sensor.scrape_degewo": f"https://immosuche.degewo.de/de/search?size=10&page=1&property_type_id=1&categories%5B%5D=1&lat=&lon=&area=&address%5Bstreet%5D=&address%5Bcity%5D=&address%5Bzipcode%5D=&address%5Bdistrict%5D=&district=33%2C+46%2C+28%2C+29%2C+60&property_number=&price_switch=true&price_radio={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_RENT}-warm&price_from=&price_to=&qm_radio=AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_AREA&qm_from={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_ROOMS}&qm_to=&rooms_radio=custom&rooms_from=&rooms_to=&wbs_required=&order=rent_total_without_vat_asc",
  "sensor.scrape_howoge": "https://www.howoge.de/immobiliensuche/wohnungssuche.html?tx_howrealestate_json_list%5Bpage%5D=1&tx_howrealestate_json_list%5Blimit%5D=12&tx_howrealestate_json_list%5Blang%5D=&tx_howrealestate_json_list%5Brooms%5D=&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Charlottenburg-Wilmersdorf&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Neukoelln&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Tempelhof-Schöneberg&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Mitte&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Friedrichshain-Kreuzberg",
  "sensor.scrape_stadtundland": f"https://www.stadtundland.de/immobiliensuche.php?form=stadtundland-expose-search-1.form&sp%3Acategories%5B3946%5D%5B%5D=-&sp%3Acategories%5B3952%5D%5B%5D=__last__&sp%3AroomsFrom%5B%5D={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_ROOMS}&sp%3AroomsTo%5B%5D=&sp%3ArentPriceFrom%5B%5D=&sp%3ArentPriceTo%5B%5D={AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_RENT}&sp%3AareaFrom%5B%5D=AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_AREA&sp%3AareaTo%5B%5D=&sp%3Afeature%5B%5D=__last__&action=submit"
}

def fetch(url, method="GET", headers=None, data=None, verify=False):
  response = requests.request(method, url, headers=headers, data=data, verify=verify)
  return BeautifulSoup(response.content, 'html.parser')

def extract(content, item, address_selector, area_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
  apartments = []
  apartment = content.select(item)

  for element in apartments:
    address = element.select_one(address_selector).get_text().strip() if element.select_one(address_selector) else None
    area = element.select_one(area_selector).get_text().strip() if element.select_one(area_selector) else None
    rent = element.select_one(rent_selector).get_text().strip() if element.select_one(rent_selector) else None
    size = element.select_one(size_selector).get_text().strip() if size_selector and element.select_one(size_selector) else None
    rooms = element.select_one(rooms_selector).get_text().strip() if rooms_selector and element.select_one(rooms_selector) else None
    details = element.select_one(details_selector).get_text() if details_selector and element.select_one(details_selector) else None

  return apartments

def scrape_friedrichsheim():
  content = fetch(AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS['friedrichsheim'])
  item = '#main h2.entry-title'
  return extract(content, item, 'self::h2', None, None)

def scrape_gewobag():
  content = fetch(AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS['gewobag'])
  item = '.filtered-mietangebote .angebot-content'
  return extract(content, item, 'address', '.angebot-area td', '.angebot-kosten td')

def scrape_ibw():
  header = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest' }
  data = { 'q': 'wf-save-srch', 'save': 'false', 'bez[]': ['01_00', '02_00', '03_00', '04_00', '02_00'], 'qm_min': AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_AREA, 'miete_max': AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_RENT, 'rooms_min': AUTO_NOTIFY_SCRAPE_HOUSING_FILTER_ROOMS, 'wbs': 0 }
  response = requests.post(AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS['ibw'], headers=HEADERS, data=data, verify=False).text
  content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
  item = '._tb_left'
  return extract(content, item, 'self::div', None, None)

def scrape_wbm():
  content = fetch(AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS['wbm'])
  item = '#content .immo-element'
  return extract(content, item, '.address', '.area', '.main-property-rent', '.main-property-size', '.main-property-rooms', '.check-property-list')

def scrape_degewo():
  content = fetch(AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS['degewo'])
  item = '.properties-container .row'
  return extract(content, item, '.property-title', '.property-city', '.property-rent', '.property-area', '.property-rooms', '.property-info')

def scrape_howoge():
  content = fetch(AUTO_NOTIFY_SCRAPE_HOUSING_SENSORS['howoge'])
  item = '.tx-howsite-flats .list-entry'
  return extract(content, item, '.address', '.address', '.price', '.rooms', '.rooms', '.wbs')

if __name__ == "__main__":
  if len(sys.argv) > 1:
    globals()[sys.argv[1]]()