from config import *
from utils import *

import aiofiles
import asyncio

from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from datetime import datetime
from pathlib import Path

HA_LOG_FILTER = ["custom integration"]

# Automations

@log_context
@service
@task_unique("ha_log_truncate", kill_me=True)
@event_trigger(EVENT_FOLDER_WATCHER) 
<<<<<<< Updated upstream
#@event_trigger(EVENT_HOMEASSISTANT_STOP)
=======
@event_trigger(EVENT_HOMEASSISTANT_STOP)
>>>>>>> Stashed changes
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", ns=None, ctx=None, **kwargs):
  if trigger_type == "event" and event_type == EVENT_FOLDER_WATCHER:
    if kwargs.get('trigger_type') != "modified":
      return {}
  if trigger_type == "time": 
    system_log.clear()
    log_ha_size = 0
  else:
    log_ha_size = LOG_HA_SIZE
  try: 
    result = log_truncate(logfile=PATH_LOG_HA, size_log_entries=log_ha_size, size_archive_entries=LOG_HA_ARCHIVE_SIZE)
  except AttributeError:
    pass
  except Exception as e:
    log(msg=e, level="error")
  finally: 
    task.sleep(LOG_HA_TRUNCATE_BLOCK_DELAY)
<<<<<<< Updated upstream
    return result

# Services

@event_trigger(EVENT_HOMEASSISTANT_STOP)
@task_unique("log_truncate", kill_me=True)
@log_context
@service(supports_response="optional")
async def log_truncate(logfile=PATH_LOG_HA, size_log_entries=LOG_HA_SIZE, size_log_tail=LOG_HA_TAIL, size_archive_entries=0, log_archive_suffix=PATH_LOG_TAIL_SUFFIX, ns=None, ctx=None):
=======

# Services

@log_context
@service(supports_response="optional")
async def log_truncate(logfile, size_log_entries=LOG_HA_SIZE, size_log_tail=LOG_HA_TAIL, size_archive_entries=0, log_archive_suffix=PATH_LOG_TAIL_SUFFIX, ns=None, ctx=None):
>>>>>>> Stashed changes
  logs_trunc = []
  logs_truncated = []
  archive_appended_trunc = []

  logs = log_read(logfile)
  archive = log_read(f"{logfile}.{log_archive_suffix}")
  
  if logs is not None and len(logs) > size_log_entries: 
    logs_trunc = logs[:-size_log_tail]
    logs_truncated = logs[-size_log_tail:]
    logs_truncated.extend(f"\n# {len(logs_truncated)} / {size_log_entries} at {datetime.now()}\n")
    log_write(logfile, logs_truncated)    
<<<<<<< Updated upstream
    log(f"{logfile} truncated from {len(logs)} to {len(logs_trunc)}", ns, ctx, "truncated:log")
=======
    log(f"{logfile} truncated from {size_log_entries} to {len(logs_trunc)}", ns, ctx, "truncated:log")
>>>>>>> Stashed changes
    
    if archive is not None and len(archive) > 0: 
      logs_trunc.extend(archive)
      log_write(f"{logfile}.{log_archive_suffix}", logs_trunc[-size_archive_entries:])
      log(f"{logfile}.{log_archive_suffix} reseized from {len(archive)} to {len(logs_trunc)}", ns, ctx, "truncated:archive")

  return { "log": log_read(logfile), "file": logfile }
  
@log_context
@service
def log_state(expression, level=LOG_LOGGING_LEVEL, ns=None, ctx=None):
  @state_trigger(expression)
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    if old_value not in STATES_HA_UNDEFINED:
      log(f"[{var_name}] {trigger_type}: {value} ({old_value})", level="debug")
  if LOG_DEBUG:
    log_state_trigger.append(log_state)

<<<<<<< Updated upstream
  info = get_trigger_expression(expression)
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass
  log(f"{info}", ns, ctx, "logging")
=======
@log_context
@service
def log_state(expression, level=LOG_LOGGING_LEVEL, ns=None, ctx=None):
  @state_trigger(expression)
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    if old_value not in STATES_HA_UNDEFINED:
      log(f"[{var_name}] {trigger_type}: {value} ({old_value})", level="debug")
  if LOG_DEBUG:
    log_state_trigger.append(log_state)

  info = get_trigger_expression(expression)
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass
  log(f"{info}", ns, ctx, "observe")
>>>>>>> Stashed changes
  
# Utils

@log_context
async def log_read(logfile, ns=None, ctx=None):
  logs = []
  for _ in range(LOG_HA_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode='r+') as l:
        logs = l.readlines()
<<<<<<< Updated upstream
      return logs
    except AttributeError: pass
    except Exception as e: 
      log(f"{logfile} could not be read ({e})", "failed")
  return []
=======
    except Exception as e: 
      if not "_file" in str(e): log(f"{logfile} could not be read ({e})", ns, ctx, "retry") 
      else: pass 
  return logs
>>>>>>> Stashed changes

@log_context
async def log_write(logfile, lines, mode='w+', ns=None, ctx=None):
  for _ in range(LOG_HA_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode=mode) as l:
        l.writelines(lines)
    except AttributeError: pass
    except: 
<<<<<<< Updated upstream
      log(f"{logfile} could not be append: {lines} ({e})", "failed")
  return []
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
=======
      log(f"{logfile} could not be append: {lines} ({e})", ns, ctx, "failed")
  return []
>>>>>>> Stashed changes
