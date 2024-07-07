import subprocess
from datetime import datetime

from utils import *
from constants.data import DATA_SUBPROCESS_SERVICES

trigger = []

services = DATA_SUBPROCESS_SERVICES

@debugged
def subprocess_factory(service):
  name = service
  service = services.get(service)
  commands = service.get("commands")
  statement = service.get("statement")
  trigger_expr = service.get("trigger")

  @logged
  @service(f"pyscript.subprocess_{service_name}")
  def execute_subprocess(return_command=False, **kwargs):
    logfile = Logfile(name=service_name)

    for command in commands:
      try:
        command = command.format(**kwargs)
        result = task.executor(subprocess.run,
          command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          shell=True, check=False, text=True)
        
        logfile.log([command if return_command else None, result.stdout, result.stderr])
      except subprocess.CalledProcessError as e:
        raise e
    return logfile.close()

  if trigger_expr:
    exec(f"""@time_trigger('{trigger_expr}')
def decorated_execute_subprocess(): return execute_subprocess()
    """, globals())
    decorated_execute_subprocess = globals()['decorated_execute_subprocess']
    trigger.append(decorated_execute_subprocess)
  trigger.append(execute_subprocess)

  if statement:
    exec(f"{statement}(execute_subprocess)", globals())
    execute_subprocess = globals()['execute_subprocess']

# Initialization

for service in services.keys():
  subprocess_factory(service)
