EVENTS = [
    "event_folder_watcher",
    "event_never",
    "event_system_pyscript_reloaded",
    "event_system_started"
]

# Erstelle ein Wörterbuch mit den Events in Großbuchstaben als Schlüssel und den entsprechenden Kleinbuchstaben als Werten
event_constants = {event.upper(): event.lower() for event in EVENTS}

# Füge das Wörterbuch direkt in den globalen Namensraum ein
globals().update(event_constants)