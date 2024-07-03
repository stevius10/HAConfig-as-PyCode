from datetime import datetime
import aiofiles
import asyncio
import os

from constants.config import *
from constants.mappings import EVENT_FOLDER_WATCHER
from exceptions import IORetriesExceededException
from utils import *

@event_trigger(EVENT_FOLDER_WATCHER)
@time_trigger('shutdown')
@task_unique("ha_log_truncate", kill_me=True)
@debugged
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):
  if trigger_type == "event" and event_type == "modified": 
    log_truncate(size_log_entries=LOG_HA_SIZE)
  if trigger_type == "time": 
    log_rotate()
    log_truncate(size_log_entries=0)
    system_log.clear()
  try: 
    pass
  except Exception: 
    pass
  finally: 
    task.sleep(LOG_TRUNCATE_BLOCK_DELAY)

@debugged
async def log_truncate(logfile=PATH_LOG_HA, size_log_entries=LOG_HA_SIZE, size_log_tail=LOG_HA_SIZE_TAIL, log_archive_suffix=LOG_ARCHIVE_SUFFIX_SHORT):
  logs = log_read(logfile)
  archive = log_read(f"{logfile}.{log_archive_suffix}")
  
  if logs is not None and len(logs) > size_log_entries: 
    logs_trunc = logs[:-size_log_tail]
    logs_truncated = "\n".join([logs[-size_log_tail:]])
    logs_truncated += f"\n# {len(logs_truncated.splitlines())} / {size_log_entries} at {datetime.now()}\n"
    log_write(logfile, [logs_truncated])

    if archive is not None and len(archive) > 0: 
      logs_trunc.extend(archive)
      log_write(f"{logfile}.{log_archive_suffix}", logs_trunc[-size_archive_entries:])

def log_rotate(logfile=PATH_LOG_HA):
  short_suffix = f"{logfile}.{LOG_ARCHIVE_SUFFIX_SHORT}"
  long_suffix = f"{logfile}.{LOG_ARCHIVE_SUFFIX}"

  try:
    if os.path.exists(short_suffix):
      content = log_read(short_suffix)
      if content:
        log_write(long_suffix, content, mode='a+')
        log_write(short_suffix, '')
    log_write(short_suffix, '')

    if os.path.exists(long_suffix):
      content = log_read(long_suffix)
      lines = content.splitlines()
      log2_size = len(content)
      
      if log2_size > LOG_ARCHIVE_SIZE:
        lines_to_remove = int(len(lines) * 0.1)
        lines = lines[lines_to_remove:]
        new_content = '\n'.join(lines) + '\n'
        log_write(long_suffix, new_content)
    else:
      log_write(long_suffix, '')

    if os.path.exists(logfile):
      content = log_read(logfile)
      log_write(short_suffix, content)
      log_write(logfile, '')
    else:
      log_write(logfile, '')

  except Exception as e:
    raise e


# Helper

def log_read(logfile):
  exception = None
  for _ in range(LOG_IO_RETRY):
    try:
      with aiofiles.open(logfile, mode='r') as l:
        return l.read()
    except Exception as e:
      exception = e
  if exception:
    raise IORetriesExceededException(exception)
  return ""

def log_write(logfile, content, mode='w+'):
  exception = None
  for _ in range(LOG_IO_RETRY):
    try:
      with aiofiles.open(logfile, mode=mode) as l:
        l.write(content)
      return True
    except Exception as e:
      exception = e
  if exception:
    raise IORetriesExceededException(exception)
  return False