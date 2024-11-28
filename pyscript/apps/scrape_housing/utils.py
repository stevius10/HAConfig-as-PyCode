from constants.mappings import MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING


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
