import aiofiles
import os
from datetime import datetime

from constants.config import *
from constants.mappings import MAP_EVENT_FOLDER_WATCHER

from utils import *

from generic import IORetriesExceededException

# Automation

@event_trigger(MAP_EVENT_FOLDER_WATCHER)
@time_trigger
@task_unique("ha_log_truncate", kill_me=True)
@debugged
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):
  try: 
    if trigger_type == "event" and event_type == "modified": 
      log_truncate(log_size_truncated=CFG_LOG_SIZE)
    if trigger_type == "time": 
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
  
  logs = file_read(logfile, lines=True)
  history = file_read(history_file)
  
  if logs is not None and len(logs) > log_size_truncated: 
    logs_trunc = logs[:-log_tail_size]
    logs_truncated = logs[-log_tail_size:]
    logs_truncated.append(f"\n# {len(logs)} / {len(logs_truncated)} at {datetime.now()}\n")
    file_write(logfile, logs_truncated)

    if history is not None and len(history) > 0: 
      logs_trunc.extend(history)
      file_write(history_file, logs_trunc[-log_history_size:])
    
    if len(logs_trunc) > log_history_size:
      log_rotate()

@debugged
@service
def log_rotate(file=CFG_PATH_FILE_LOG):
  history_file = f"{file}.{CFG_LOG_HISTORY_SUFFIX}"
  archive_file = f"{file}.{CFG_LOG_ARCHIV_SUFFIX}"

  try:
    if os.path.exists(history_file):
      history = file_read(history_file)
      archive = file_read(archive_file)
      if history:
        history.reverse()
        file_write(archive_file, history+archive)
        file_write(history_file, '')
    file_write(history_file, '')

    if os.path.exists(archive_file):
      archive = file_read(archive_file, lines=True)
      archive_size = len(archive)
      
      if archive_size > CFG_LOG_ARCHIV_SIZE:
        archive_trunc_size = int(len(archive) * 0.2) # shorten twenty percent if exceeded
        archive_truncated = archive[archive_trunc_size:]
        archive_truncated = '\n'.join(archive_truncated) + '\n'
        archive_truncated.seek(0, 0)
        file_write(archive_file, archive_truncated)
    else:
      file_write(archive_file, '')

    if os.path.exists(file):
      content = file_read(file)
      file_write(history_file, content)
      # file_write(file)
    else:
      file_write(file, '')

  except Exception as e:
    raise e

# Helper

async def file_read(logfile, lines=False):
  exception = None
  for _ in range(CFG_LOG_SETTINGS_IO_RETRY):
    try:
      if lines is False:
        async with aiofiles.open(logfile, mode='r') as l:
          content = l.read()
        return content.splitlines() if '\n' in content else content
      else:
        async with aiofiles.open(logfile, mode='r') as l:
          content = l.readlines()
        return content
    except Exception as e:
      exception = e
  if exception:
    raise IORetriesExceededException(exception)
  return ""

async def file_write(logfile, lines, mode='w+'):
  exception = None
  for _ in range(CFG_LOG_SETTINGS_IO_RETRY):
    try:
      async with aiofiles.open(logfile, mode=mode) as l:
        if isinstance(lines, list):
          await l.writelines([line + '\n' for line in lines])
        else:
          await l.write(lines)
      return True
    except Exception as e:
      exception = e
  if exception:
    raise IORetriesExceededException(exception)
  return False