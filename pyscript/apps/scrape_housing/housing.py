from typing import List

from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.mappings import MAP_KEY_RESULT

from .scrape import fetch, scrape

from utils import *

def scrape_housing(provider):
    result = []

    structure = DATA_SCRAPE_HOUSING_PROVIDERS[provider]["structure"]

    content = fetch(provider)
    result = scrape(content, structure["item"], structure["address_selector"], structure["rent_selector"], structure["size_selector"], structure["rooms_selector"], structure["details_selector"])

    return { MAP_KEY_RESULT: result or "" }
