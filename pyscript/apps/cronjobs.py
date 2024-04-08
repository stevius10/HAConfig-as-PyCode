from helper import expr

SERVICES_AUTO_CRON_FILEBACKUP = "cron(0 1 * * *)"
SERVICES_AUTO = {
  'shell_command.ha_filebackup': SERVICES_AUTO_CRON_FILEBACKUP
}

trigger_services_auto = []

def services_auto_factory(entity, cron): 
  @time_trigger(cron)
  def service_auto(entity):
    service.call(entity.split(".")[0], entity.split(".")[1])

  trigger_services_auto.append(service_auto)

for entity in SERVICES_AUTO:
  services_auto_factory(entity, SERVICES_AUTO.get(entity))