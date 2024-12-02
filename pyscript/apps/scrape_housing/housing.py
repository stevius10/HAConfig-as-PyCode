from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.mappings import MAP_KEY_ERROR, MAP_KEY_RESULT

from .scrape import fetch, scrape

def scrape_housing(provider):
    result = []
    structure = DATA_SCRAPE_HOUSING_PROVIDERS[provider]["structure"]

    try: 
        content = fetch(provider)
        return { MAP_KEY_RESULT: scrape(content, structure["item"], structure["address_selector"], structure["rent_selector"], structure["size_selector"], structure["rooms_selector"], structure["details_selector"]) }
    except Exception as e:
        return { MAP_KEY_ERROR: str(e) }
