from datetime import datetime
import re

from constants.settings import SET_SCRAPE_HOUSING_BLACKLIST, SET_SCRAPE_HOUSING_FILTER_AREA, SET_SCRAPE_HOUSING_FILTER_ROOMS, SET_SCRAPE_HOUSING_FILTER_RENT, SET_SCRAPE_HOUSING_FILTER_PLZ

from utils import *

@debugged
def apartment_create(address, rent, size, rooms, text):
    return {
        "address": address,
        "rent": rent,
        "size": size,
        "rooms": rooms,
        "text": text,
        "time": {"first_time": datetime.now(), "last_time": datetime.now()},
    }

def apartment_update(apartment):
    apartment["time"]["last_time"] = datetime.now()

def apartment_compare(a1, a2):
    return (
            a1["address"] == a2["address"]
            and a1["rent"] == a2["rent"]
            and a1["size"] == a2["size"]
            and a1["rooms"] == a2["rooms"]
    )

def apartment_hash(a):
    return hash((a["address"], a["rent"], a["size"], a["rooms"]))

def apartment_string(a):
    return "{address} ({rent}, {rooms}, {size})".format(address=a['address'], rent=", {}".format(a['rent']) if a['rent'] else '', rooms=", {}".format(a['rooms']) if a['rooms'] else '', size=", {}".format(a['size']) if a['size'] else '' )[:254].strip(" ()")

@debugged
def apartment_filter(a):
    if not has_required_fields(a):
        return False
    if not is_rent_in_range(a):
        return False
    if not is_size_in_range(a):
        return False
    if not is_rooms_in_range(a):
        return False
    if has_invalid_plz(a):
        return False
    if is_blacklisted(a):
        return False
    return True

def has_required_fields(a):
    return not ([a["rent"], a["size"], a["rooms"]].count(None) == 3 or a["address"] is None)

def is_rent_in_range(a):
    if a["rent"] and re.findall(r"\d", a["rent"]):
        rent_value = int("".join(re.findall(r"\d", a["rent"])[:3]))
        return 400 < rent_value < SET_SCRAPE_HOUSING_FILTER_RENT
    return True

def is_size_in_range(a):
    if a["size"] and re.findall(r"\d", a["size"]):
        size_value = int("".join(re.findall(r"\d", a["size"])[:3]))
        return SET_SCRAPE_HOUSING_FILTER_AREA <= size_value
    return True

def is_rooms_in_range(a):
    if a["rooms"] and re.findall(r"\d", a["rooms"]):
        rooms_value = int("".join(re.findall(r"\d", a["rooms"])[:2]))
        return SET_SCRAPE_HOUSING_FILTER_ROOMS <= rooms_value
    return True

def has_invalid_plz(a):
    if a["address"]:
        plz_match = re.search(r"\b\d{5}\b", a["address"])
        return plz_match and plz_match.group() not in SET_SCRAPE_HOUSING_FILTER_PLZ
    return False

def is_blacklisted(a):
    if a["text"]:
        for item in SET_SCRAPE_HOUSING_BLACKLIST:
            if re.search(r"\b" + re.escape(item.lower()) + r"\b", a["text"].lower()):
                return True
        return False
    return False

# from datetime import datetime
# import re
#
# from constants.settings import SET_SCRAPE_HOUSING_FILTER_AREA, SET_SCRAPE_HOUSING_FILTER_ROOMS, SET_SCRAPE_HOUSING_FILTER_RENT, SET_SCRAPE_HOUSING_FILTER_PLZ
#
# from utils import *
#
# class Apartment:
#     def __init__(self, address: str, rent: str, size: str, rooms: str, text: str):
#         self.address = address
#         self.rent = rent
#         self.size = size
#         self.rooms = rooms
#         self.text = text
#         self.time = {"first_time": datetime.now(), "last_time": datetime.now()}
#
#     def update(self):
#         self.time["last_time"] = datetime.now()
#
#     @pyscript_compile
#     def __eq__(self, apartment):
#         return (self.address == apartment.address and
#                 self.rent == apartment.rent and
#                 self.size == apartment.size and
#                 self.rooms == apartment.rooms)
#
#     @pyscript_compile
#     def __hash__(self):
#         return hash((self.address, self.rent, self.size, self.rooms))
#
#     @pyscript_compile
#     def __str__(self):
#         return f"{self.address or ''}{', ' if self.rent else ''}{self.rent or ''}{', ' if self.rooms else ''}{self.rooms or ''}{', ' if self.size else ''}{self.size or ''}"[:254].strip(" ()")
#
#     @debugged
#     def filter(self) -> bool:
#         return True
#         if not self._has_required_fields():
#             return False
#         if not self._is_rent_in_range():
#             return False
#         if not self._is_size_in_range():
#             return False
#         if not self._is_rooms_in_range():
#             return False
#         if self._has_invalid_plz():
#             return False
#         if self._is_blacklisted():
#             return False
#         return True
#
#     def _has_required_fields(self) -> bool:
#         return not ([self.rent, self.size, self.rooms].count(None) == 3 or self.address is None)
#
#     def _is_rent_in_range(self) -> bool:
#         if self.rent and re.findall(r'\d', self.rent):
#             rent_value = int(''.join(re.findall(r'\d', self.rent)[:3]))
#             return 400 < rent_value < SET_SCRAPE_HOUSING_FILTER_RENT
#         return True
#
#     def _is_size_in_range(self) -> bool:
#         if self.size and re.findall(r'\d', self.size):
#             size_value = int(''.join(re.findall(r'\d', self.size)[:3]))
#             return SET_SCRAPE_HOUSING_FILTER_AREA[0] <= size_value <= SET_SCRAPE_HOUSING_FILTER_AREA[1]
#         return True
#
#     def _is_rooms_in_range(self) -> bool:
#         if self.rooms and re.findall(r'\d', self.rooms):
#             rooms_value = int(''.join(re.findall(r'\d', self.rooms)[:2]))
#             return SET_SCRAPE_HOUSING_FILTER_ROOMS[0] <= rooms_value <= SET_SCRAPE_HOUSING_FILTER_ROOMS[1]
#         return True
#
#     def _has_invalid_plz(self) -> bool:
#         plz_match = re.search(r'\b\d{5}\b', self.address)
#         return plz_match and hasattr(plz_match, 'group') and plz_match.group() not in SET_SCRAPE_HOUSING_FILTER_PLZ
#
#     def _is_blacklisted(self) -> bool:
#         return self.text is not None and any(
#             re.search(r'\b' + re.escape(item.lower()) + r'\b', self.text.lower()) for item in SET_SCRAPE_HOUSING_BLACKLIST)
