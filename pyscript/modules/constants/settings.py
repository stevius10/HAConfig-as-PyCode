AUTO_MOTION_TIMEOUT = 70
AUTO_TURN_OFF_AWAY_TRANSITION = 20

SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE = 50
SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE = 10
SCRIPT_AIR_CLEANER_HELPER_PM_MINIMUM = 8
SCRIPT_AIR_CLEANER_SPEED_THRESHOLD = 30
SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY = 900
SCRIPT_AIR_CLEANER_THRESHOLD_START = 15
SCRIPT_AIR_CLEANER_THRESHOLD_STOP = 6
SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN = 600
SCRIPT_AIR_CLEANER_TIMEOUT_HELPER = 280
SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY = 2

SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MIN = 1 # 60
SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MAX = 10 # 600
SERVICE_SCRAPE_HOUSING_FILTER_AREA = 50
SERVICE_SCRAPE_HOUSING_FILTER_RENT = 705
SERVICE_SCRAPE_HOUSING_FILTER_ROOMS = 2
SERVICE_SCRAPE_HOUSING_SENSOR_LENGTH = 254
SERVICE_SCRAPE_HOUSING_PROVIDERS = {
  "degewo": { "url": f"https://immosuche.degewo.de/de/search?size=10&page=1&property_type_id=1&categories%5B%5D=1&lat=&lon=&area=&address%5Bstreet%5D=&address%5Bcity%5D=&address%5Bzipcode%5D=&address%5Bdistrict%5D=&district=33%2C+46%2C+28%2C+29%2C+60&property_number=&price_switch=true&price_radio={SERVICE_SCRAPE_HOUSING_FILTER_RENT}-warm&price_from=&price_to=&qm_radio=SERVICE_SCRAPE_HOUSING_FILTER_AREA&qm_from={SERVICE_SCRAPE_HOUSING_FILTER_ROOMS}&qm_to=&rooms_radio=custom&rooms_from=&rooms_to=&wbs_required=&order=rent_total_without_vat_asc",
    "structure": { "item": ".properties-container .property-container", "address_selector": ".property-subtitle", "rent_selector": ".property-rent", "size_selector": ".property-size", "rooms_selector": ".property-rooms", "details_selector": ".property-actions a"  } },
  "friedrichsheim": { "url": "https://www.friedrichsheim-eg.de/category/freie-wohnungen/",
    "structure": { "item": "#main h2.entry-title", "address_selector": "*", "rent_selector": None, "size_selector": None, "rooms_selector": None, "details_selector": None } },
 "howoge": { "url": "https://www.howoge.de/immobiliensuche/wohnungssuche.html?tx_howrealestate_json_list%5Bpage%5D=1&tx_howrealestate_json_list%5Blimit%5D=12&tx_howrealestate_json_list%5Blang%5D=&tx_howrealestate_json_list%5Brooms%5D=&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Charlottenburg-Wilmersdorf&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Neukoelln&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Tempelhof-Schöneberg&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Mitte&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Friedrichshain-Kreuzberg",
    "structure": { "item": ".tx-howsite-flats .list-entry", "address_selector": ".address", "rent_selector": ".price", "size_selector": None, "rooms_selector": ".rooms", "details_selector": ".wbs" } },
 "ibw": { "url": "https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php",
    "structure": {"item": "_tb_left", "address_selector": "*", "rent_selector": None, "size_selector": None, "rooms_selector": None, "details_selector": None }, 
    "request_headers": { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest' },
    "request_data": { 'q': 'wf-save-srch', 'save': 'false', 'qm_min': SERVICE_SCRAPE_HOUSING_FILTER_AREA, 'miete_max': SERVICE_SCRAPE_HOUSING_FILTER_RENT, 'rooms_min': SERVICE_SCRAPE_HOUSING_FILTER_ROOMS, 'bez[]': ['01_00', '02_00', '03_00', '04_00', '02_00'], 'wbs': 1 } },

 "gewobag": { # approved 210624
    "url": f"https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=neukoelln-rudow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis={SERVICE_SCRAPE_HOUSING_FILTER_RENT}&gesamtflaeche_von={SERVICE_SCRAPE_HOUSING_FILTER_AREA}&gesamtflaeche_bis=&zimmer_von={SERVICE_SCRAPE_HOUSING_FILTER_ROOMS}&zimmer_bis=&keinwbs=0&sort-by=recent",
    "structure": { "item": ".filtered-mietangebote .angebot-content", "address_selector": "address", "rent_selector": ".angebot-kosten td", "size_selector": ".angebot-area td", "rooms_selector": "", "details_selector": "" } },

  "wbm": { # approved 190624
    "url": "https://www.wbm.de/wohnungen-berlin/angebote/",
    "structure": { "item": "#content .immo-element", "address_selector": ".address", "rent_selector": ".main-property-rent", "size_selector": ".main-property-size", "rooms_selector": ".main-property-rooms", "details_selector": ".check-property-list" } }
}