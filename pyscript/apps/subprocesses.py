import os
import subprocess
import sys
from datetime import datetime

from constants.data import DATA_SUBPROCESS_SERVICES
from constants.mappings import MAP_EVENT_SYSTEM_STARTED

from utils import *

trigger = []
services = DATA_SUBPROCESS_SERVICES

# Factory

@logged
def subprocess_factory(service):
  name = service
  service = services.get(service)
  commands = service.get("commands")
  statement = service.get("statement")

  @logged
  @service(f"pyscript.subprocess_{name}", supports_response="optional")
  def execute_subprocess(name=name, log_command=False):
    logfile = get_logfile(pyscript.get_global_ctx())

    for command in commands:
      try:
        result = task.executor(subprocess.run,
          command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          shell=True, check=False, text=True
        )
        logfile.log([command if log_command else "", result.stdout, result.stderr])
      except subprocess.CalledProcessError as e:
        logfile.log([e, command, result.stdout, result.stderr])

    return logfile.close()
    
  if statement:
    exec("\n".join(["@service", str(statement), f"def execute_subprocess_{name}(name='{name}'):\n  return execute_subprocess({name})"]))
  else:
    exec(f"@service\ndef execute_subprocess_{name}(name='{name}', log_command=False):\n  return execute_subprocess_{name}, log_command")

  trigger.append(f"execute_subprocess_{name}")

# Initialization

@event_trigger(MAP_EVENT_SYSTEM_STARTED)
def init():
  for service in services.keys():
    subprocess_factory(service)
