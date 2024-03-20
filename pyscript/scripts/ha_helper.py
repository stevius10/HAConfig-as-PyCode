from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_CALL_SERVICE

from constants import LOG_HA_SIZE, LOG_HA_ARCHIVE_SIZE, LOG_ARCHIVE_SUFFIX, PATH_LOG_HA, \
  EVENT_FOLDER_WATCHER

import  aiofiles

from datetime import datetime
from pathlib import Path

ha_log_truncate_block = 60
ha_log_truncate_tail = 10

@service(supports_response="optional")
@task_unique("ha_log_content_truncate", kill_me=True)
@event_trigger(EVENT_FOLDER_WATCHER) 
@event_trigger(EVENT_HOMEASSISTANT_STOP)
async def ha_log_truncate(trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):

  if trigger_type == "event" and event_type == EVENT_FOLDER_WATCHER:
    if kwargs.get('trigger_type') != "modified":
      return {}
  elif trigger_type == "time": 
      system_log.clear()
      size_log_entries = 0
  try: 
    return log_truncate(logfile=PATH_LOG_HA, size_log_entries=LOG_HA_SIZE, size_archive_entries=LOG_HA_ARCHIVE_SIZE)
    
  except Exception as e:
    log.error(e)
  finally: 
    await task.sleep(ha_log_truncate_block)

@service
async def log_truncate(logfile, size_log_entries=LOG_HA_SIZE, size_archive_entries=0, log_archive_suffix=LOG_ARCHIVE_SUFFIX):
  log_content_origin = []
  log_content_truncated = []
  archive_content_origin = []
  try:
    async with aiofiles.open(logfile, 'r+') as logfile_object:
      log_content_origin = logfile_object.readlines()
  
      if log_content_origin is not None and len(log_content_origin) > (2 * size_log_entries): 
        log_content_truncated = log_content_origin[-size_log_entries:]
        log_content_truncated.append( f"\n# {len(log_content_origin)} / {size_log_entries} at {datetime.now()}\n")
        logfile_object.seek(0)
        await logfile_object.writelines(log_content_truncated)
        logfile_object.truncate()
        
        log_to_archive = log_content_origin[:-size_log_entries]
        async with aiofiles.open(f"{logfile}.{log_archive_suffix}", 'a+') as archive_file_object:
          archive_content_origin = archive_file_object.readlines()
          if archive_content_origin is not None: 
            archive_content_origin = log_to_archive
            archive_file_object.seek(0)
            await archive_file_object.writelines(archive_content_origin[-size_archive_entries:])
  except Exception as e:
    log.warn(f"Exception: {e}, Logfile: {logfile}")
    # [consider] revert log order
    
  # Return result
  async with aiofiles.open(logfile, 'r') as logfile_object:
    log_content_origin = logfile_object.readlines()
    if log_content_origin is not None: 
      log_content_origin = log_content_origin[::-1][:10]
  async with aiofiles.open(f"{logfile}.{LOG_ARCHIVE_SUFFIX}", 'r') as archive_file_object:
    archive_content_origin = archive_file_object.readlines()
    if archive_content_origin is not None:
      archive_content_origin = archive_content_origin[::-1][:10]
  return {"log": log_content_origin, "archive": archive_content_origin}
