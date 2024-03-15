from constants import PATH_CONSTANTS, SYSTEM_FILES

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

import shutil
import os

@event_trigger(EVENT_HOMEASSISTANT_STARTED) # @time_trigger('startup')
def ha_startup_files(): 
  # ha_startup_environment()
  ha_startup_files()
  
def ha_startup_environment(file=PATH_CONSTANTS):
  def get_constants(file):
    constants = {}
    with aopen(file, 'r') as f:
      lines = f.readlines()
      for line in lines:
          match = re.match(r'^([A-Z0-9_]+)\s*=\s*(.+)$', line)
          if match:
              key = match.group(1)
              value = match.group(2).strip()
              constants[key] = value
              
      for key, value in constants.items():
          os.environ[key] = value

def ha_startup_files(file=SYSTEM_FILES):
  try:
    for file in files:
      shutil.copy2(file, files[file])
  except Exception as e:
    log.warn(e)
