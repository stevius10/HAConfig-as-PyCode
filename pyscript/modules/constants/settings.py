AUTO_MOTION_TIMEOUT = 70
AUTO_TURN_OFF_AWAY_TRANSITION = 20

AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MIN = 60
AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MAX = 600
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

SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE = 34
SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE = 10
SCRIPT_AIR_CLEANER_HELPER_PM_MINIMUM = 8
SCRIPT_AIR_CLEANER_SPEED_THRESHOLD = 30
SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY = 900
SCRIPT_AIR_CLEANER_THRESHOLD_START = 15
SCRIPT_AIR_CLEANER_THRESHOLD_STOP = 6
SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN = 600
SCRIPT_AIR_CLEANER_TIMEOUT_HELPER = 280
SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY = 1