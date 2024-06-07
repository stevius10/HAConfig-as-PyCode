from log import *

trigger = []

def services_auto_factory(entity, cron): 
  @service() # (service_name=entity.split(".")[1])
  @time_trigger(cron)
  @log_context
  def service_auto(entity=entity, ns=None, ctx=None):
    result = service.call(entity.split(".")[0], entity.split(".")[1])
    log(f"{result}", ns, ctx, title=f"{entity} called")

  trigger.append(service_auto)

for entity in SERVICES_AUTO:
  services_auto_factory(entity, SERVICES_AUTO.get(entity))