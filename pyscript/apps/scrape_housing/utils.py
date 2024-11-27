from constants.mappings import MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING

def format_apartment(apartment):
    return f"{apartment.get('address', '')} ({apartment.get('rent', '')}{', ' if apartment.get('rent') and apartment.get('rooms') else ''}{apartment.get('rooms', '')}{', ' if (apartment.get('rent') or apartment.get('rooms')) and apartment.get('size') else ''}{apartment.get('size', '')})"[:254].strip(" ()")

def format_apartments(apartments):
    return ", ".join([apartment for apartment in apartments])[:254]

def get_entity(provider):
    return f"pyscript.{MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING}_{provider}"

def get_or_default(element, selector, default=None):
    if not selector:
        return default
        item = element.select_one(selector)
        return item.get_text().strip() if item else default
    elif callable(selector):
        return selector(element)
    return default

def get_or_default_format(text):
    text = text.replace("\n", ", ")
    text = text.replace(" | ", ", ")
    return text
