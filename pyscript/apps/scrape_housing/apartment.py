import re

from constants.settings import (
    SET_SCRAPE_HOUSING_BLACKLIST,
    SET_SCRAPE_HOUSING_FILTER_AREA,
    SET_SCRAPE_HOUSING_FILTER_ROOMS,
    SET_SCRAPE_HOUSING_FILTER_RENT,
    SET_SCRAPE_HOUSING_FILTER_PLZ,
)

from utils import *

@debugged
def apartment_create(address, rent=None, size=None, rooms=None, text=None):
    return {
        "address": address,
        "rent": rent,
        "size": size,
        "rooms": rooms,
        "text": text,
    }

def apartment_compare(apartment, address, rent=None, size=None, rooms=None):
    return (
            apartment["address"] == address
            and (not apartment.get("rent") or apartment.get("rent")  == rent)
            and (not apartment.get("size") or apartment.get("size")  == size)
            and (not apartment.get("rooms") or apartment.get("rooms")  == rooms)
    )

def apartment_string(a):
    return "{address} ({rent}{rooms}{size})".format(
        address=a["address"],
        rent="{}, ".format(a["rent"]) if a["rent"] else "",
        rooms="{}, ".format(a["rooms"]) if a["rooms"] else "",
        size="{}".format(a["size"]) if a["size"] else "",
    )[:254].strip(" ()")

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
