import random

from helper import expr
from constants import HA_STATES_UNDEFINED

# Monitor

entities = { 
  "sensor.v_friedrichsheim": { "url": "https://www.friedrichsheim-eg.de/category/freie-wohnungen/" }, 
  "sensor.v_bmv": { "url": "https://www.bwv-berlin.de/wohnungsangebote.html" }, 
  "sensor.v_neukolln": { "url": "https://www.gwneukoelln.de/wohnungen/wohnungsangebote/" }, 
  "sensor.v_wbm": { "url": "https://www.wbm.de/wohnungen-berlin/angebote-wbm/" }, 
  "sensor.v_gewobag": { "url": "https://www.wbm.de/wohnungen-berlin/angebote-wbm/" }, 
  "sensor.v_inberlinwohnen": { "url": "https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=neukoelln-rudow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=700&gesamtflaeche_von=50&gesamtflaeche_bis=&zimmer_von=2&zimmer_bis=&sort-by=recent" }
}

@state_trigger(expr(list(entities.keys())))
def notify_immo(**kwargs):
  if(kwargs.get("old_value") not in HA_STATES_UNDEFINED):
    data = {
      "message": kwargs.get("var_name").replace("sensor.", ""), 
      "data": {
        "shortcut": {
          name: "Notification-Monitor",
          input: entities[kwargs.get("var_name")],
          ignore_result: "ignore"
        }
      }
    }
    notify.mobile_app_iphone(data)

# @time_trigger("cron(30 16 * * 1-5)")
def update_sensors(): 
  task.sleep(random.randint(10, 600))
  script.s_update_sensors
