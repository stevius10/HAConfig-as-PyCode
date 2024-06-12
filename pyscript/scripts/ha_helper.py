from constants.config import *
from constants.events import EVENT_FOLDER_WATCHER

from utils import *

import aiofiles

from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from datetime import datetime

# Automations

@task_unique("ha_log_truncate", kill_me=True)
@event_trigger(EVENT_FOLDER_WATCHER)
@time_trigger
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", ns=None, ctx=None, **kwargs):
  if trigger_type == "event" and event_type == EVENT_FOLDER_WATCHER:
    if kwargs.get('trigger_type') != "modified": return
    log_ha_size = LOG_HA_SIZE
  elif trigger_type == "time":
    system_log.clear()
    log_ha_size = 0
  else:
    return
    
  try: result = log_truncate(logfile=PATH_LOG_HA, size_log_entries=log_ha_size, size_archive_entries=LOG_ARCHIVE_SIZE)
  except Exception as e: pass
  finally: task.sleep(LOG_TRUNCATE_BLOCK_DELAY)

# Services

@task_unique("log_truncate", kill_me=True)
@event_trigger(EVENT_HOMEASSISTANT_STOP)
@debugged
async def log_truncate(logfile=PATH_LOG_HA, size_log_entries=LOG_HA_SIZE, size_log_tail=LOG_HA_SIZE_TAIL, size_archive_entries=0, log_archive_suffix=LOG_ARCHIVE_SUFFIX, ns=None, ctx=None):
  logs_trunc = []
  logs_truncated = []

  logs = log_read(logfile)
  archive = log_read(f"{logfile}.{log_archive_suffix}")
  
  if logs is not None and len(logs) > size_log_entries: 
    logs_trunc = logs[:-size_log_tail]
    logs_truncated = logs[-size_log_tail:]
    logs_truncated.extend(f"\n# {len(logs_truncated)} / {size_log_entries} at {datetime.now()}\n")
    log_write(logfile, logs_truncated)    
    log(f"{logfile} truncated from {len(logs)} to {len(logs_trunc)}", ns, ctx, "truncated:log")
    
    if archive is not None and len(archive) > 0: 
      logs_trunc.extend(archive)
      log_write(f"{logfile}.{log_archive_suffix}", logs_trunc[-size_archive_entries:])
      log(f"{logfile}.{log_archive_suffix} reseized from {len(archive)} to {len(logs_trunc)}", ns, ctx, "truncated:archive")

# Utils

async def log_read(logfile, ns=None, ctx=None):
  logs = []
  for _ in range(LOG_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode='r+') as l:
        logs = l.readlines()
      return logs
    except AttributeError: pass
    except Exception as e: 
      log(f"{logfile} could not be read ({e})", "failed")
  return []

async def log_write(logfile, lines, mode='w+', ns=None, ctx=None):
  for _ in range(LOG_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode=mode) as l:
        l.writelines(lines)
    except AttributeError: pass
    except: 
      log(f"{logfile} could not be append: {lines} ({e})", "failed")
  return []