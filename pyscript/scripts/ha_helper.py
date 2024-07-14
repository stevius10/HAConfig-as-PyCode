import aiofiles
import os
from datetime import datetime

from constants.config import *
from constants.mappings import MAP_EVENT_FOLDER_WATCHER

from exceptions import IORetriesExceededException
from utils import *

@event_trigger(MAP_EVENT_FOLDER_WATCHER)
@time_trigger('shutdown')
@task_unique("ha_log_truncate", kill_me=True)
@debugged
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):
  try: 
    if trigger_type == "event" and event_type == "modified": 
      log_truncate(log_size_truncated=CFG_LOG_SIZE)
    if trigger_type == "time": 
      log_rotate()
      log_truncate(log_size_truncated=0)
      system_log.clear()
  except Exception as e: 
    raise e
  finally: 
    task.sleep(CFG_LOG_SETTINGS_DELAY_BLOCK)

@debugged
@service
async def log_truncate(logfile=CFG_PATH_FILE_LOG, log_size_truncated=CFG_LOG_SIZE, log_tail_size=CFG_LOG_TAIL, log_history_size=CFG_LOG_HISTORY_SIZE):
  history_file=f"{logfile}.{CFG_LOG_HISTORY_SUFFIX}"
  
  logs = log_read(logfile, lines=True)
  history = log_read(history_file)
  
  if logs is not None and len(logs) > log_size_truncated: 
    logs_trunc = logs[:-log_tail_size]
    logs_truncated = logs[-log_tail_size:]
    logs_truncated.append(f"\n# {len(logs_truncated)} / {log_size_truncated} at {datetime.now()}\n")
    log_write(logfile, logs_truncated)

    if history is not None and len(history) > 0: 
      logs_trunc.extend(history)
      log_write(history_file, logs_trunc[-log_history_size:])

@debugged
@service
def log_rotate(logfile=CFG_PATH_FILE_LOG):
  history_file = f"{logfile}.{CFG_LOG_HISTORY_SUFFIX}"
  archive_file = f"{logfile}.{CFG_LOG_ARCHIV_SUFFIX}"

  try:
    if os.path.exists(history_file):
      history = log_read(history_file)
      if history:
        log_write(archive_file, history, mode='a+')
        log_write(history_file, '')
    log_write(history_file, '')

    if os.path.exists(archive_file):
      archive = log_read(archive_file, lines=True)
      archive_size = len(archive)
      
      if archive_size > CFG_LOG_ARCHIV_SIZE:
        archive_trunc_size = int(len(archive) * 0.1) # shorten ten percent if exceeded
        archive_truncated = archive[archive_trunc_size:]
        archive_truncated = '\n'.join(archive_truncated) + '\n'
        log_write(archive_file, archive_truncated)
    else:
      log_write(archive_file, '')

    if os.path.exists(logfile):
      content = log_read(logfile)
      log_write(history_file, content)
      log_write(logfile, '')
    else:
      log_write(logfile, '')

  except Exception as e:
    raise e

# Helper

async def log_read(logfile, lines=False):
  exception = None
  for _ in range(CFG_LOG_SETTINGS_IO_RETRY):
    try:
      if lines is False:
        async with aiofiles.open(logfile, mode='r') as l:
          content = await l.read()
          return content.splitlines() if '\n' in content else content
      else:
        async with aiofiles.open(logfile, mode='r') as l:
          return await l.readlines()
    except Exception as e:
      exception = e
  if exception:
    raise IORetriesExceededException(exception)
  return ""

async def log_write(logfile, content, mode='w+'):
  exception = None
  for _ in range(CFG_LOG_SETTINGS_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode=mode) as l:
        if isinstance(content, list):
          await l.writelines([f"{line}\n" for line in content])
        else:
          await l.write(content)
      return True
    except Exception as e:
      exception = e
  if exception:
    raise IORetriesExceededException(exception)
  return False
