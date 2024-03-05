from homeassistant.const import EVENT_CALL_SERVICE

from constants import PATH_LOG_HA, EVENT_FOLDER_WATCHER, SIZE_LOG_ENTRIES, SIZE_LOG_ARCHIVE_ENTRIES 

import asyncio
from aiofiles import open as aopen
from datetime import datetime, timedelta
from pathlib import Path

@time_trigger('startup')
@time_trigger('shutdown')
@event_trigger(EVENT_FOLDER_WATCHER) 
@service
@task_unique("ha_log_truncate", kill_me=True)
def log_truncate(trigger_type=None, log_file=PATH_LOG_HA, size_log_entries=SIZE_LOG_ENTRIES, size_archive_entries=SIZE_LOG_ARCHIVE_ENTRIES, file="", folder="", path=""):
  try:    
    log_content = ""
    log_trunc = ""
    
    if trigger_type == "time": 
      system_log.clear()
      size_log_entries = 0
      log.error(trigger_type)
  
    async with aopen(log_file, 'r') as log_file_object:
      log_content = log_file_object.readlines()

    if ((size_log_entries > 0) and (len(log_content) > (1.5 * size_log_entries))): 
      log_to_archive = log_content[:-size_log_entries]
      async with aopen(f"{log_file}.archive", 'a') as archive_file_object:
        await archive_file_object.writelines(log_to_archive)
      async with aopen(f"{log_file}.archive", 'r') as archive_file_object:
        archive_content = archive_file_object.readlines()
      archive_trunc = archive_content[-size_archive_entries:]
      async with aopen(f"{log_file}.archive", 'w') as archive_file_object:
        await archive_file_object.writelines(archive_trunc)
    
    log_trunc = log_content[-size_log_entries:]
    if size_log_entries == 0:
      log_trunc = ""      

    async with aopen(log_file, 'w+') as log_file_object:
      await log_file_object.writelines(log_trunc)
      if log_trunc != log_content: 
        await log_file_object.writelines(f"\n\n # {size_log_entries} at {datetime.now()}")

  except Exception as e:
    log.error(e)
  finally: 
    await task.sleep(3)

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

# @event_trigger(EVENT_CALL_SERVICE, "domain == 'pyscript' and service == 'reload'")
# def ha_py_reload(**kwargs):
#   if "service_data" in kwargs and kwargs.get("service_data").get("global_ctx") != "*":
#     async with aopen(HA_PATH_LOG, 'r') as log_file:
#       debug = log_file.readlines()
#     browser_mod.popup(browser_id="THIS", content=debug)

# def ha_log_events(**kwargs):
#   log_content.info(f"[Event] {kwargs}")