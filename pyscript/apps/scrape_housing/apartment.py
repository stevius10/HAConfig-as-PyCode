from typing import Optional, Dict
from datetime import datetime
import re

from constants.settings import SET_SCRAPE_HOUSING_FILTER_AREA, SET_SCRAPE_HOUSING_FILTER_ROOMS, SET_SCRAPE_HOUSING_FILTER_RENT, SET_SCRAPE_HOUSING_FILTER_PLZ

from utils import *

class Apartment:
    def __init__(self, address: str, rent: str, size: str, rooms: str, text: str):
        self.address = address
        self.rent = rent
        self.size = size
        self.rooms = rooms
        self.text = text
        self.time = {"first_time": datetime.now(), "last_time": datetime.now()}

    def update(self):
        self.time["last_time"] = datetime.now()

    def __eq__(self, apartment):
        return (self.address == apartment.address and
                self.rent == apartment.rent and
                self.size == apartment.size and
                self.rooms == apartment.rooms)

    def __hash__(self):
        return hash((self.address, self.rent, self.size, self.rooms))

    def __str__(self):
        return f"{self.address or ''}{', ' if self.rent else ''}{self.rent or ''}{', ' if self.rooms else ''}{self.rooms or ''}{', ' if self.size else ''}{self.size or ''}"[:254].strip(" ()")

    @debugged
    def filter(self) -> bool:
        if not self._has_required_fields():
            return False
        if not self._is_rent_in_range():
            return False
        if not self._is_size_in_range():
            return False
        if not self._is_rooms_in_range():
            return False
        if self._has_invalid_plz():
            return False
        if self._is_blacklisted():
            return False
        return True

    def _has_required_fields(self) -> bool:
        return not ([self.rent, self.size, self.rooms].count(None) == 3 or self.address is None)

    def _is_rent_in_range(self) -> bool:
        if self.rent and re.findall(r'\d', self.rent):
            rent_value = int(''.join(re.findall(r'\d', self.rent)[:3]))
            return 400 < rent_value < SET_SCRAPE_HOUSING_FILTER_RENT
        return True

    def _is_size_in_range(self) -> bool:
        if self.size and re.findall(r'\d', self.size):
            size_value = int(''.join(re.findall(r'\d', self.size)[:3]))
            return SET_SCRAPE_HOUSING_FILTER_AREA[0] <= size_value <= SET_SCRAPE_HOUSING_FILTER_AREA[1]
        return True

    def _is_rooms_in_range(self) -> bool:
        if self.rooms and re.findall(r'\d', self.rooms):
            rooms_value = int(''.join(re.findall(r'\d', self.rooms)[:2]))
            return SET_SCRAPE_HOUSING_FILTER_ROOMS[0] <= rooms_value <= SET_SCRAPE_HOUSING_FILTER_ROOMS[1]
        return True

    def _has_invalid_plz(self) -> bool:
        plz_match = re.search(r'\b\d{5}\b', self.address)
        return plz_match and hasattr(plz_match, 'group') and plz_match.group() not in SET_SCRAPE_HOUSING_FILTER_PLZ

    def _is_blacklisted(self) -> bool:
        return self.text is not None and any(
            re.search(r'\b' + re.escape(item.lower()) + r'\b', self.text.lower()) for item in SET_SCRAPE_HOUSING_BLACKLIST)
