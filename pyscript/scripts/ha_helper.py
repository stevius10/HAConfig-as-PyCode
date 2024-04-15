from config import (
  EVENT_FOLDER_WATCHER, EVENT_SYSTEM_STARTED, LOG_ARCHIVE_SUFFIX, 
  LOG_DEBUG, LOG_DEBUG_DEVICES, LOG_HA_ARCHIVE_SIZE, LOG_HA_SIZE,
  LOG_HA_TAIL, LOG_HA_TRUNCATE_BLOCK_DELAY, LOG_HA_TRUNCATE_IO_RETRY,
  LOG_LOGGING_LEVEL, LOG_SYS_LOGGER, PATH_LOG_HA, STATES_HA_UNDEFINED
)
from utils import log

import aiofiles
import asyncio

from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_CALL_SERVICE

from datetime import datetime
from pathlib import Path

log_trigger = []

HA_LOG_FILTER = ["custom integration", "reload"]

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
    log(msg=e, level="error")
  finally: 
    task.sleep(LOG_HA_TRUNCATE_BLOCK_DELAY)

@service
def log(msg, level=LOG_LOGGING_LEVEL, logger=LOG_SYS_LOGGER):
  system_log.write(message=msg, logger=logger, level=level)
  
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

@event_trigger(EVENT_SYSTEM_STARTED)
async def log_filter(logfile, filters=HA_LOG_FILTER):
  logs = log_read(logfile)
  lines = [line for line in logs if not any(filtering in line for filtering in filters)]
  if logs != lines: 
    lines.append(f"[removed] log_filter: {filters}")
    log_write(logfile, lines)