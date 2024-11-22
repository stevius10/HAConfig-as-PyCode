import json
from datetime import datetime
from utils import *

@service(supports_response="optional")
def ml_create_sensors():
  logfile = get_logfile(f"{pyscript.get_global_ctx()}_sensors")

  sensors = {sensor: state.get(sensor) for sensor in state.names()}
  relevant_categories = ["sensor", "binary_sensor", "climate", "light", "fan", "switch"]
  excluded_states = ["unavailable", "unknown", ""]
  excluded_suffixes = ["_version", "_cpu_percent", "_memory_percent", "_newest_version"]

  filtered_sensors = {}
  for key in sensors:
    for cat in relevant_categories:
      if key.startswith(cat):
        if sensors[key] not in excluded_states and not any(key.endswith(suffix) for suffix in excluded_suffixes):
          filtered_sensors[key] = sensors[key]
        break

  filtered_sensors["timestamp"] = datetime.now().isoformat()

  try:
    logfile.log(json.dumps(filtered_sensors, indent=4, ensure_ascii=False))
    return logfile.close()
  except Exception as e:
    log(f"Error processing sensor data: {e}")