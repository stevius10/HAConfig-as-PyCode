import os
import sys
from collections import defaultdict
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from constants.config import CFG_EVENT_STARTED_DELAY, CFG_LOG_SETTINGS_ENVIRONMEMT_LENGTH, CFG_PATH_DIR_PY, CFG_SYSTEM_ENVIRONMENT, CFG_SYSTEM_FILES, CFG_SYSTEM_LINKS
from constants.mappings import MAP_EVENT_SETUP_STARTED, MAP_EVENT_SYSTEM_STARTED
from utils import *

trigger = []

# Startup

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_setup_init(delay=CFG_EVENT_STARTED_DELAY):
  os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
  sys.path.extend([
    path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))] 
    if path not in sys.path
  ])
  task.sleep(delay)
  event.fire(MAP_EVENT_SETUP_STARTED)

# Setup

@event_trigger(MAP_EVENT_SETUP_STARTED)
@service
def ha_setup():
  ha_setup_environment()
  ha_setup_files()
  ha_setup_links()
  event.fire(MAP_EVENT_SYSTEM_STARTED)

# Tasks

@logged
def ha_setup_environment(variables=CFG_SYSTEM_ENVIRONMENT):
  def shorten(val, max_len=CFG_LOG_SETTINGS_ENVIRONMEMT_LENGTH):
    return val if len(val) <= max_len else val[:max_len] + '..'
  
  os.environ.update({k: v for k, v in variables.items() if not (k.startswith('S6') or k.startswith('__'))})
  env_vars = defaultdict(list)
  single_vars = []
  
  for k in sorted(os.environ.keys()):
    if not (k.startswith('S6') or k.startswith('__')):
      env_vars[k[0]].append(f"{k}={shorten(os.environ[k])}")
  
  for key, vals in list(env_vars.items()):
    if len(vals) == 1:
      single_vars.extend(vals)
      del env_vars[key]

  if single_vars:
    for i in range(0, len(single_vars), 2):
      pair = single_vars[i:i + 2]
      env_vars["A"].append(", ".join(pair))
  
  formatted_env_vars = "\n  ".join([", ".join(vals) for vals in env_vars.values()])
  return f"Environment:\n  {formatted_env_vars}"

@logged
def ha_setup_files(files=CFG_SYSTEM_FILES):
  from filesystem import cp
  for src, dest in files.items():
    cp(src, dest)
  
  paths = defaultdict(list)
  for path in sorted(set([f"{os.sep.join(path.split(os.sep)[:4])}/…" if len(path.split(os.sep)) > 4 else path for path in sys.path if not path.startswith('__')])):
    key = os.sep.join(path.split(os.sep)[:2]) if len(path.split(os.sep)) > 1 else path
    paths[key].append(path)
  
  formatted_paths = "\n  ".join([", ".join(vals) for key, vals in paths.items() if key.startswith('/config') and not key.startswith('/config/pyscript')])
  formatted_paths += "\n  " + ", ".join([", ".join(vals) for key, vals in paths.items() if key.startswith('/config/pyscript')])
  formatted_paths += "\n  " + ", ".join([", ".join(vals) for key, vals in paths.items() if not key.startswith('/config')])
  
  return f"System Path:\n  {formatted_paths}"

@logged
def ha_setup_links(links=CFG_SYSTEM_LINKS):
  for src, dest in links.items():
    if not os.path.isdir(dest) and os.path.islink(dest):
      os.unlink(dest)
    os.symlink(src, dest)
  formatted_links = "\n".join([f"{src} <- {dest}" for src, dest in links.items()])
  return f"Sym. Links:\n{formatted_links}"