import subprocess
import requests
import sys
import pkgutil
import importlib

from constants.expressions import *
from constants.secrets import *
from constants.settings import *

from utils import *

@logged
@service(supports_response="optional")
def debug(): 
  return dict(debug_function())

@event_trigger("STATE_CHANGED")
@logged
def debug_events(service_data=None, **kwargs):
  from logfile import Logfile
  logfile = Logfile("events.log")
  logfile.log(f": {service_data} ({kwargs})")
  return service_data