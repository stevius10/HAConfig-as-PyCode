from typing import List

from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING, MAP_RESULT_STATUS

from scrape_housing.apartment import Apartment
from scrape_housing.scrape import scrape, fetch

def scrape_housing(provider):
        apartments = List[Apartment]
        apartments_string = List[str]

        structure = DATA_SCRAPE_HOUSING_PROVIDERS[provider]["structure"]
        try:
            apartments = scrape(fetch(provider), structure["item"], structure["address_selector"], structure["rent_selector"], structure["size_selector"], structure["rooms_selector"], structure["details_selector"])
            for apartment in apartments:
                apartments_string.append(str(apartment))

            return { provider: apartments_string }

        except Exception as e:
            return { provider: str(e) }
