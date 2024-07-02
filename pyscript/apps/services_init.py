from constants.config import *

from utils import *

trigger = []

def services_auto_factory(entity, cron): 
  @time_trigger(cron)
  @logged
  def service_auto(entity=entity):
    return service.call(entity.split(".")[0], entity.split(".")[1])

  trigger.append(service_auto)

for entity in SERVICES_AUTO:
  services_auto_factory(entity, SERVICES_AUTO.get(entity))