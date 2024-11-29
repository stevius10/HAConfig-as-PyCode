import subprocess
import requests
import sys
import pkgutil
import importlib
import logging

from constants.expressions import *
from constants.secrets import *
from constants.settings import *
from utils import *

from homeassistant.const import EVENT_STATE_CHANGED

@logged
@service(supports_response="optional")
def debug(debug_function=None):
  if debug_function and callable(debug_function):
    return dict(debug_function())

@event_trigger("*")
@logged
def debug_events(service_data=None, **kwargs):
  from logfile import Logfile
  logfile = get_logfile(f"{pyscript.get_global_ctx()}")

  return logfile.close()