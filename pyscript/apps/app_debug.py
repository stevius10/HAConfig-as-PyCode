from constants.expressions import *
from constants.secrets import *
from constants.settings import *

import subprocess
import requests

from utils import *

@logged
@service(supports_response="optional")
def debug():
  return dict(debug_function())
 
@pyscript_executor
def debug_function():
  from logfile import Logfile # runtime level due sys path config
  logfile  = Logfile("debug.services")
  
  import sys
  import pkgutil
  import importlib
  
  logfile.log("Loaded modules:")
  for module_name in sorted(sys.modules.keys()):
    logfile.log(module_name)
  
  logfile.log("\nAvailable modules in the environment:")
  available_modules = sorted([module.name for module in pkgutil.iter_modules()])
  for module_name in available_modules:
    logfile.log(module_name)

  return logfile.close()