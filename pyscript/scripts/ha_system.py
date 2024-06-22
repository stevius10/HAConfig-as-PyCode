from constants.config import *
from constants.events import EVENT_SYSTEM_STARTED

import shutil
import sys
import os

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

from utils import *

trigger = []

# Event

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_system_started(delay=SYSTEM_CONFIG_EVENT_STARTED_DELAY): 
  if PATH_DIR_PY_NATIVE not in sys.path:
    sys.path.append(PATH_DIR_PY_NATIVE)
  task.sleep(delay)
  event.fire(EVENT_SYSTEM_STARTED)

# Setup

@event_trigger(EVENT_SYSTEM_STARTED)
@debugged
def ha_setup():
  ha_setup_environment()
  ha_setup_files()
  ha_setup_links()
  ha_setup_logging()

  ha_setup_syslog()

# Tasks
  
@pyscript_executor
def ha_setup_environment(variables=SYSTEM_ENVIRONMENT):
  for variable in variables:
    os.environ[variable] = variables[variable]
  
@pyscript_executor
def ha_setup_files(files=SYSTEM_FILES):
  from filesystem import cp
  for file in files:
    cp(file, files[file])

@pyscript_executor
def ha_setup_links(links=SYSTEM_LINKS):
  for source, target in links.items():
    tmp_target = f"{target}.tmp"
    os.symlink(source, tmp_target)
    os.rename(tmp_target, target) # workaround to overwrite symlink

def ha_setup_logging(): # sync. task due logging scope
  logger.set_level(**{LOG_LOGGER_SYS: LOG_LOGGING_LEVEL})
 
def ha_setup_syslog():
  @callback
  @event_trigger("system_log_event", "message.find('Reloaded /config/pyscript/') != -1")
  def on_script_reload(event):
    global reload
    
    paths = re.search(r'Reloaded (/config/pyscript/.*\.py)', event['message'])
    if paths: scripts.append(paths.group(1))
    
    if not reload:
      reload = True
      task.sleep(1)  
    if reloaded:
      summary = f"# {len(scripts)} reloaded\n"
      summary += "\n".join(f"- {script.split('/')[-1]}" for script in reloaded_scripts)
      log(summary)
    scripts.clear(); reload = False
  trigger.append(on_script_reload)