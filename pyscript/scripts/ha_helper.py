from homeassistant.const import EVENT_CALL_SERVICE

from constants import PATH_LOG_HA, EVENT_FOLDER_WATCHER, SIZE_LOG_ENTRIES, SIZE_LOG_ARCHIVE_ENTRIES 

import asyncio
from aiofiles import open as aopen
from datetime import datetime, timedelta
from pathlib import Path

@service
@task_unique("ha_log_truncate", kill_me=True)
@time_trigger('startup')
@time_trigger('shutdown')
@event_trigger(EVENT_FOLDER_WATCHER) 
async def ha_log_truncate(trigger_type=None, file="", folder="", path=""):
  
  if trigger_type == "event": 
    system_log.clear()
    size_log_entries = 0
  else:
    await task.sleep(1)
    size_log_entries = SIZE_LOG_ENTRIES

  log_truncate(log_file=PATH_LOG_HA, size_log_entries=SIZE_LOG_ENTRIES, size_archive_entries=SIZE_LOG_ARCHIVE_ENTRIES)
  await task.sleep(2)

@service
def log_truncate(log_file, size_log_entries=0, size_archive_entries=0):

  async with aopen(log_file, 'w+') as log_file_object:
    log = log_file_object.readlines()
    
  if ((size_log_entries > 0) and (len(log) > (1.5 * size_log_entries))): 
    log_to_archive = log[:-size_log_entries]
    async with aopen(f"{log_file}.archive", 'a') as archive_file_object:
      await archive_file_object.writelines(log_to_archive)
    async with aopen(f"{log_file}.archive", 'r') as archive_file_object:
      archive = archive_file_object.readlines()
    archive_trunc = archive[-size_archive_entries:]
    async with aopen(f"{log_file}.archive", 'w') as archive_file_object:
      await archive_file_object.writelines(archive_trunc)
    
  log_trunc = log[-size_log_entries:]
  async with aopen(log_file, 'w') as log_file_object:
    await log_file_object.writelines(log_trunc)

# @service
# @time_trigger('startup')
# def ha_env_variables():
#   def get_constants(file):
#     constants = {}
#     with aopen(file, 'r') as f:
#       lines = f.readlines()
#       for line in lines:
#           match = re.match(r'^([A-Z0-9_]+)\s*=\s*(.+)$', line)
#           if match:
#               key = match.group(1)
#               value = match.group(2).strip()
#               constants[key] = value
#     return constants

#   constants = get_constants(PATH_CONSTANTS)

#   for key, value in constants.items():
#       os.environ[key] = value
  

# def ha_py_context(): 
#   for context in pyscript.list_global_ctx():
#     log.info(GlobalContextMgr.items());

# @event_trigger(EVENT_CALL_SERVICE, "domain == 'pyscript' and service == 'reload'")
# def ha_py_reload(**kwargs):
#   if "service_data" in kwargs and kwargs.get("service_data").get("global_ctx") != "*":
#     async with aopen(HA_PATH_LOG, 'r') as log_file:
#       debug = log_file.readlines()
#     browser_mod.popup(browser_id="THIS", content=debug)

# def ha_log_events(**kwargs):
#   log.info(f"[Event] {kwargs}")