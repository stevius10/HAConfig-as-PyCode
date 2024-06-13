EVENTS = [
    "folder_watcher",
    "housing_initialized",
    "never",
    "system_pyscript_reloaded",
    "system_started"
]

event_constants = {f"EVENT_{event.upper()}": event.lower() for event in EVENTS}
globals().update(event_constants)