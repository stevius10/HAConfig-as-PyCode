from constants.config import *
from constants.mappings import EVENT_FOLDER_WATCHER

from utils import *

import aiofiles
from datetime import datetime

# Automations

@event_trigger(EVENT_FOLDER_WATCHER)
@time_trigger('shutdown')
@task_unique("ha_log_truncate", kill_me=True)
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):
  try: 
    if trigger_type == "event" and event_type == "modified": 
      log_truncate(size_log_entries=LOG_HA_SIZE)
    if trigger_type == "time": 
      log_truncate(size_log_entries=0)
      system_log.clear()
    
  except Exception as e: log(str(e))
  finally: task.sleep(LOG_TRUNCATE_BLOCK_DELAY)

# Services

@service
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

    if archive is not None and len(archive) > 0: 
      logs_trunc.extend(archive)
      log_write(f"{logfile}.{log_archive_suffix}", logs_trunc[-size_archive_entries:])

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
      log(msg=f"{logfile} could not be read ({e})")
  return []

async def log_write(logfile, lines, mode='w+', ns=None, ctx=None):
  for _ in range(LOG_TRUNCATE_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode=mode) as l:
        l.writelines(lines)
    except AttributeError: pass
    except Exception as e: 
      log(msg=f"{logfile} could not be appended: {lines} ({e})")
  return []