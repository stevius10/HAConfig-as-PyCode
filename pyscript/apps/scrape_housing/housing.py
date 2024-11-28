from typing import List

from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS

from .scrape import *

def scrape_housing(provider):
    apartments_string = List[str]
    structure = DATA_SCRAPE_HOUSING_PROVIDERS[provider]["structure"]
    apartments = scrape(fetch(provider), structure["item"], structure["address_selector"], structure["rent_selector"], structure["size_selector"], structure["rooms_selector"], structure["details_selector"])
    for apartment in apartments:
        apartments_string.append(apartment_string(apartment))

    return { provider: str(apartments) }
