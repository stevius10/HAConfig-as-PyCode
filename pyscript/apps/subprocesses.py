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

@debugged
def subprocess_factory(service):
  name = service
  service = services.get(service)
  commands = service.get("commands")
  statement = service.get("statement")

  @debugged
  @service(f"pyscript.subprocess_{name}", supports_response="optional")
  def execute_subprocess(name=name, log_command=False):
    logfile = get_logfile(f"{pyscript.get_global_ctx()}_{name}")
    logfile.log(datetime.now().strftime("[%d.%m.%Y-%H:%M]"))

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
    @time_trigger(statement)
    @service
    def execute_subprocess_triggered(name=name, log_command=False):
      return execute_subprocess(name, log_command)
    trigger.append(execute_subprocess_triggered)
  else:
    trigger.append(execute_subprocess)

# Initialization

@event_trigger(MAP_EVENT_SYSTEM_STARTED)
def init():
  for service in services.keys():
    subprocess_factory(service)
