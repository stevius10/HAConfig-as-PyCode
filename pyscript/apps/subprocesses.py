import subprocess
import sys

from constants.data import DATA_SUBPROCESS_SERVICES
from utils import *

trigger = []
services = DATA_SUBPROCESS_SERVICES

# Factory

# @debugged
def subprocess_factory(service):
  name = service
  service = services.get(service)
  commands = service.get("commands")
  statement = service.get("statement")

  # @logged
  @service(f"pyscript.subprocess_{name}")
  def execute_subprocess():
    from logfile import Logfile
    logfile = Logfile(name=name)
    
    for command in commands:
      try:
        result = task.executor(subprocess.run,
          command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          shell=True, check=False, text=True
        )
        logfile.log([command, result.stdout, result.stderr])
      except subprocess.CalledProcessError as e:
        logfile.log([e, command, result.stdout, result.stderr])
    
    return logfile.close()

  if statement:
    execute_subprocess = eval(f"{statement}(execute_subprocess)")
  trigger.append(execute_subprocess)

# Initialization

for service in services.keys():
  subprocess_factory(service)