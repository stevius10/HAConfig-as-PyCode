EVENTS = [
    "event_folder_watcher",
    "event_never",
    "event_system_pyscript_reloaded",
    "event_system_started"
]

event_constants = {event.upper(): event.lower() for event in EVENTS}
globals().update(event_constants)