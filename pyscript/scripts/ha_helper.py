from homeassistant.const import EVENT_CALL_SERVICE
from custom_components.pyscript.global_ctx import GlobalContext, GlobalContextMgr

from constants import EVENT_FOLDER_WATCHER, HA_PATH_LOG, HA_PATH_LOG_ARCHIVE, PATH_CONSTANTS, SIZE_LOG_ENTRIES, SIZE_LOG_ARCHIVE_ENTRIES

import asyncio
from aiofiles import open as aopen
from datetime import datetime, timedelta
from pathlib import Path

@service
@time_trigger('startup')
def ha_env_variables():
  def get_constants(file):
    constants = {}
    with aopen(file, 'r') as f:
      lines = f.readlines()
      for line in lines:
          match = re.match(r'^([A-Z0-9_]+)\s*=\s*(.+)$', line)
          if match:
              key = match.group(1)
              value = match.group(2).strip()
              constants[key] = value
    return constants

  constants = get_constants(PATH_CONSTANTS)

  for key, value in constants.items():
      os.environ[key] = value
  
# Show Pyscript trigger
@service
def ha_py_context(): 
  for context in pyscript.list_global_ctx():
    log.info(GlobalContextMgr.items());

# Debug on Python reload
@event_trigger(EVENT_CALL_SERVICE, "domain == 'pyscript' and service == 'reload'")
def ha_py_reload(**kwargs):
  if "service_data" in kwargs and kwargs.get("service_data").get("global_ctx") != "*":
    log.info("Debug single script")
    async with aopen(HA_PATH_LOG, 'r') as log_file:
      debug = log_file.readlines()
    browser_mod.popup(browser_id="THIS", content=debug)

# Trunc logs
@task_unique("ha_logs_truncate_reload", kill_me=True)
@event_trigger(EVENT_FOLDER_WATCHER) 
async def ha_logs_truncate_reload(file, folder, path, **kwargs):

  # async with aopen(HA_PATH_LOG, 'r') as log_file:
    # logs = log_file.readlines
    # if log_entry_recently(logs, "Reloaded", 1): 
      #pass
      # ha_py_reload()
      # pyscript.reload(global_ctx="*")
  await task.sleep(1)
  ha_logs_truncate()
  await task.sleep(2)

# Helper

@service
@task_unique("ha_logs_truncate", kill_me=True)
@time_trigger('startup')
@time_trigger('shutdown')
def ha_logs_truncate(trigger_type=None):
  log_size = SIZE_LOG_ENTRIES
  archive_size = SIZE_LOG_ARCHIVE_ENTRIES
  
  if trigger_type == "event": 
    system_log.cleat()
    log_size = 0

  async with aopen(HA_PATH_LOG, 'r') as log_file:
    log = log_file.readlines()

  if len(log) > (1.5 * log_size):

    # Copy logs to archive
    log_to_archive = log[:-log_size]
  
    async with aopen(HA_PATH_LOG_ARCHIVE, 'a') as archive_file:
      await archive_file.writelines(log_to_archive)
    async with aopen(HA_PATH_LOG_ARCHIVE, 'r') as read_archive_file:
      archive = read_archive_file.readlines()
  
    # Truncate log files
    log_trunc = log[-log_size:]
    archive_trunc = archive[-archive_size:]
  
    async with aopen(HA_PATH_LOG, 'w') as log_file:
      await log_file.writelines(log_trunc)
  
    async with aopen(HA_PATH_LOG_ARCHIVE, 'w') as log_file:
      await log_file.writelines(archive_trunc)
  
  if trigger_type == "event":
    system_log.clear()

# def log_entry_recently(logs, entry, minutes_ago):
#     current_time = datetime.now()
#     recent_time = current_time - timedelta(minutes=minutes_ago)
#     log.info(logs)
#     for line in logs:
#       try:
#         if entry in line:
#           timestamp = datetime.strptime(line.split(" ")[1], "%H:%M:%S.%f")
#           if timestamp >= recent_time:
#             return True
#       except Exception as e:
#         log.error(e)
#         await task.sleep(5)
#         continue
#     return False

# @event_trigger("") 
def ha_log_events(**kwargs):
  log.info(f"[Event] {kwargs}")