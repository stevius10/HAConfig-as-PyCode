import json
from datetime import datetime
import pandas as pd
from utils import *

global_sensor_data = pd.DataFrame()

@service(supports_response="optional")
def ml_create_sensors():
  global global_sensor_data
  logfile = get_logfile(f"{pyscript.get_global_ctx()}_sensors")

  sensors = [entity for entity in state.names() ] # if entity.startswith("sensor.")]
  try:
    data = {sensor: state.get(sensor) for sensor in sensors}
    data["timestamp"] = datetime.now().isoformat()

    def process_sensor_data(json_data, existing_df=None):
      new_data = pd.DataFrame([json_data])
      new_data["timestamp"] = pd.to_datetime(new_data["timestamp"])
      if existing_df is not None:
        combined_df = pd.concat([existing_df, new_data], ignore_index=True)
        combined_df["timestamp"] = pd.to_datetime(combined_df["timestamp"])
        combined_df.set_index("timestamp", inplace=True)
        return combined_df
      new_data.set_index("timestamp", inplace=True)
      return new_data

    global_sensor_data = process_sensor_data(data, existing_df=global_sensor_data)

    numerical_cols = global_sensor_data.select_dtypes(include=["float", "int"]).columns
    global_sensor_data[numerical_cols] = (
      global_sensor_data[numerical_cols] - global_sensor_data[numerical_cols].mean()
    ) / global_sensor_data[numerical_cols].std()

    categorical_cols = global_sensor_data.select_dtypes(include=["object"]).columns
    global_sensor_data = pd.get_dummies(global_sensor_data, columns=categorical_cols)

    logfile.log(json.dumps(data, indent=4, ensure_ascii=False))
    return logfile.close()

  except Exception as e:
    log(f"Error processing sensor data: {e}")
