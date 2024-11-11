import subprocess
import requests
import sys
import pkgutil
import importlib

from constants.expressions import *
from constants.secrets import *
from constants.settings import *

from utils import *

def get_logfile_name(suffix):
  return f"{pyscript.get_global_ctx().split('.')[1]}.debug.{suffix}"

@logged
@service(supports_response="optional")
def debug(): 
  return dict(debug_function())

@pyscript_executor
def debug_function():
  from logfile import Logfile
  Logfile(get_logfile_name("log")).log(" ".join(sorted(sys.modules.keys()))).log(" ".join([module.name for module in pkgutil.iter_modules()])).close()

@event_trigger("*")
def debug_events(service_data=None, **kwargs):
  from logfile import Logfile
  Logfile(get_logfile_name("events")).log(f"{pyscript.event_name()}: {service_data} ({kwargs})").close()

@time_trigger
@service
def debug_triggers():
  triggers = {}
#   for ctx_name, ctx in pyscript.get_global_ctx().items():
#     ctx_triggers = ctx.get_triggers()
#     if ctx_triggers:
#       triggers[ctx_name] = [str(trig) for trig in ctx_triggers]
  return {"triggers": triggers}
