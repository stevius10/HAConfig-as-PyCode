import json
import regex as re
import requests
from typing import Optional, List, Dict
from bs4 import BeautifulSoup

from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS

from scrape_housing.apartment import Apartment
from scrape_housing.utils import get_or_default

from utils import *

providers = DATA_SCRAPE_HOUSING_PROVIDERS

@pyscript_executor
def scrape(content, item, address_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None) -> List[Apartment]:
    apartments = []

    elements = content.select(item)
    for element in elements:
        element_text = element.get_text(strip=True)

        address = get_or_default(element, address_selector)
        if not address:
            address_match = re.search(r'([A-Za-zäöüß\s.-]+\s\d+(?:,\s*[A-Za-zäöüß\s-]+)?)', element_text)
            address = address_match.group(1) if address_match else None

        rent = get_or_default(element, rent_selector)
        if not rent:
            rent_match = re.search(r'(\d+(?:,\d+)?)\s*€', element_text)
            rent = rent_match.group(1) + ' €' if rent_match else None

        size = get_or_default(element, size_selector)
        if not size:
            size_match = re.search(r'(\d+(?:,\d+)?)\s*m²', element_text)
            size = size_match.group(1) + ' m²' if size_match else None

        rooms = get_or_default(element, rooms_selector)
        if not rooms:
            rooms_match = re.search(r'(\d+(?:,\d+)?)\s*Zimmer', element_text)
            rooms = rooms_match.group(1) + ' Zimmer' if rooms_match else None

        text = get_or_default(element, details_selector) or element_text
        plz = re.search(r'\b1\d{4}\b', address)

        apartment = Apartment(address=address, rent=rent, size=size, rooms=rooms, text=text)
        if apartment.filter():
          apartments.append(apartment)

    return apartments

@pyscript_executor
def fetch(provider):
    if providers[provider].get("request_headers") and providers[provider].get("request_data"):
        response = requests.post(providers[provider]["url"], headers=providers[provider]["request_headers"], data=providers[provider]["request_data"], verify=False).text
        content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
    else:
        response = requests.get(providers[provider]["url"], verify=False)
        content = BeautifulSoup(response.content, 'html.parser')
    return content
