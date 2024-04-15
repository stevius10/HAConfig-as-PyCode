from config import EVENT_SYSTEM_STARTED, EVENT_SYSTEM_STARTED_DELAY, PATH_LOGS, PYSCRIPT_DIR_NATIVE, SYSTEM_FILES
from utils import log 

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

import datetime
import logging
import inspect
import regex as re
import shutil
import os

# Automations 

@event_trigger(EVENT_SYSTEM_STARTED)
async def ha_setup_files(file=SYSTEM_FILES):
  try:
    for file in files:
      shutil.copy2(file, files[file])
  except Exception as e:
    log.warn(e)

@event_trigger(EVENT_SYSTEM_STARTED)
def ha_setup_environment():
  if PYSCRIPT_DIR_NATIVE not in sys.path:
    sys.path.append(PYSCRIPT_DIR_NATIVE)

# Events

@event_trigger(EVENT_HOMEASSISTANT_STARTED)
async def event_started(): 
  task.sleep(EVENT_HOMEASSISTANT_STARTED_DELAY)
  event.fire(EVENT_SYSTEM_STARTED)
  
# Services 

@service
def log_trigger(entity, expr):
  log_trigger_factory(entity, expr)

# Utils

def log_trigger_factory(entity, expr):
  @state_trigger(f"{entity} {expr}")
  def log_trigger(trigger_type=None, var_name=None, value=None, old_value=None):  
    log(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if LOG_DEBUG or entity in LOG_DEBUG_DEVICES:
    log_trigger.append(log_state) 
  
  info = f"[trigger] {entity} {expr}"
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass