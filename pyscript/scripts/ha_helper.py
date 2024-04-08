from config import LOG_HA_SIZE, LOG_HA_TAIL, PATH_LOG_HA, \
   LOG_HA_TRUNCATE_BLOCK_DELAY, LOG_HA_TRUNCATE_IO_RETRY, \
   LOG_HA_ARCHIVE_SIZE, LOG_ARCHIVE_SUFFIX, EVENT_FOLDER_WATCHER, \
   LOG_SYS_LOGGER, LOG_DEBUG, LOG_DEBUG_DEVICES, STATES_HA_UNDEFINED

import aiofiles
import asyncio
import inspect

from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_CALL_SERVICE

from datetime import datetime
from pathlib import Path

log_trigger = []

@service(supports_response="optional")
@task_unique("ha_log_content_truncate", kill_me=True)
@event_trigger(EVENT_FOLDER_WATCHER) 
@event_trigger(EVENT_HOMEASSISTANT_STOP)
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):
  if trigger_type == "event" and event_type == EVENT_FOLDER_WATCHER:
    if kwargs.get('trigger_type') != "modified":
      return {}
  if trigger_type == "time": 
    system_log.clear()
    log_ha_size = 0
  else:
    log_ha_size = LOG_HA_SIZE
  try: 
    log_truncate(logfile=PATH_LOG_HA, size_log_entries=log_ha_size, size_archive_entries=LOG_HA_ARCHIVE_SIZE)

  except AttributeError:
    pass
  except Exception as e:
    log.error(e)
  finally: 
    task.sleep(LOG_HA_TRUNCATE_BLOCK_DELAY)

async def log_read(logfile):
  for _ in range(LOG_HA_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode='r+') as l:
        logs = l.readlines()
      return logs
    except: 
      pass
  return []

async def log_write(logfile, lines, mode='w+'):
  for _ in range(LOG_HA_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode=mode) as l:
        l.writelines(lines)
    except: 
      pass
  return []
  
@service
async def log_truncate(logfile, size_log_entries=LOG_HA_SIZE, size_log_tail=LOG_HA_TAIL, size_archive_entries=0, log_archive_suffix=LOG_ARCHIVE_SUFFIX):
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
    
    if archive is not None and len(archive) > 0: 
      archive.extend(logs_trunc)
      log_write(f"{logfile}.{log_archive_suffix}", archive[-size_archive_entries:])

# Log: Trigger

def log_trigger_factory(entity, expr):
  
  @state_trigger(f"{entity} {expr}")
  def log_trigger(trigger_type=None, var_name=None, value=None, old_value=None):  
    log.info(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if LOG_DEBUG or entity in LOG_DEBUG_DEVICES:
    log_trigger.append(log_state) 
  
  info = f"[trigger] {entity} {expr}"
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass   
  
@service
def log_trigger(entity, expr):
  log_trigger_factory(entity, expr)

@service
def log(msg, level="info", logger=LOG_SYS_LOGGER):
  line = inspect.currentframe().f_back.f_lineno
  func = inspect.currentframe().f_back.f_code.co_name
  system_log.write(message=f"[{func} ({line})] {msg}", logger=logger, level=level)