from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_CALL_SERVICE

from constants import LOG_HA_SIZE, LOG_HA_ARCHIVE_SIZE, LOG_ARCHIVE_SUFFIX, PATH_LOG_HA, EVENT_FOLDER_WATCHER, EVENT_SYSTEM_LOG_TRUNCATED

import asyncio

from aiofiles import open as aopen
from datetime import datetime
from pathlib import Path

ha_log_truncate_block = 60
log_truncate_tail = 10

@service(supports_response="optional")
@task_unique("ha_log_truncate", kill_me=True)
@event_trigger(EVENT_FOLDER_WATCHER) 
@event_trigger(EVENT_HOMEASSISTANT_STOP) # @time_trigger('shutdown')
def ha_log_truncate(logfile=PATH_LOG_HA, size_log_entries=LOG_HA_SIZE, size_archive_entries=LOG_HA_ARCHIVE_SIZE, trigger_type=None, event_type=None, file="", folder="", path="", **kwargs):

  if trigger_type == "event" and event_type == EVENT_FOLDER_WATCHER and kwargs.get('trigger_type') != "modified":
    return {}
    
  elif trigger_type == "time": 
      system_log.clear()
      size_log_entries = 0
      
  try: 
    return log_truncate(logfile=logfile, size_log_entries=size_log_entries, size_archive_entries=size_archive_entries)
    
  except Exception as e:
    log.error(e)
  finally: 
    event.fire(event_type=EVENT_SYSTEM_LOG_TRUNCATED, kwargs={logfile: logfile})
    await task.sleep(ha_log_truncate_block)

@service(supports_response="optional")
def log_truncate(logfile=PATH_LOG_HA, size_log_entries=LOG_HA_SIZE, size_archive_entries=0):
    log_content = ""
    log_trunc = ""

    # logfile_object == NoneType
    async with aopen(logfile, 'w+') as logfile_object:
      log_content = await logfile_object.read()
      log_trunc = log_content[-size_log_entries:] if size_log_entries is not 0 else ""
      log_trunc.append(f"# {len(log_content)} / {size_log_entries} at {datetime.now()}\n")
      await logfile_object.writelines(log_trunc)
      
    if ((size_log_entries > 0) and (len(log_content) > (1.25 * size_log_entries))): 
      log_to_archive = log_content[:-size_log_entries]
      async with aopen(f"{logfile}.{LOG_ARCHIVE_SUFFIX}", 'w+') as archive_file_object:
        archive_content = (await archive_file_object.read()) + log_to_archive
        await archive_file_object.write(archive_content[-size_archive_entries:])
    
    # Return
    async with aopen(logfile, 'r') as logfile_object:
      log_content = await logfile_object.read()[-log_truncate_tail:]
    async with aopen(f"{logfile}.{LOG_ARCHIVE_SUFFIX}", 'r') as archive_file_object:
      archive_content = await archive_file_object.read()[-log_truncate_tail:]
    return {"log": log_content, "archive": archive_content}
  

# @service(supports_response="only")
# def ha_run_script(script, **kwargs): 

#   result = { "script": script }

#   result['response'] = service.call("pyscript", script, blocking=True, return_response=True, kwargs=kwargs)

#   async with aopen(PATH_LOG_HA, 'r') as log_ha:
#     result['log'] = log_ha.readlines()

#   log.info(result)
#   return result

# @event_trigger(EVENT_CALL_SERVICE, "domain == 'pyscript' and service == 'reload'")
# def ha_pyscript_reload(**kwargs):
#   debug = {}
#   if "service_data" in kwargs and kwargs.get("service_data").get("global_ctx") != "*":
#     async with aopen(PATH_LOG_HA, 'r') as logfile:
#       debug = logfile.readlines()
#     browser_mod.popup(browser_id="THIS", content=debug)

# def ha_log_events(**kwargs):
#   log_content.info(f"[Event] {kwargs}")