EVENTS = [
    "event_folder_watcher",
    "event_never",
    "event_system_pyscript_reloaded",
    "event_system_started"
]

for event in EVENTS:
    globals()[event.upper()] = event.lower()