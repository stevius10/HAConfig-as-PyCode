from helper import expr
from  constants import AUTO_CONFIG_RESET_DELAY_ADGUARD, AUTO_CONFIG_RESET_DELAY_HEIZDECKE, \
  AUTO_CONFIG_RESET_DELAY_SOFA, AUTO_CONFIG_RESET_DELAY_BETT

default_trigger = []

# Delayed default configuration

entities = { 
  "switch.adguard_home_schutz": { "default": "on", "delay": AUTO_CONFIG_RESET_DELAY_ADGUARD }, 
  "switch.heizdecke": { "default": "off", "delay": AUTO_CONFIG_RESET_DELAY_HEIZDECKE }, 
  "switch.sofa": { "default": "off", "delay": AUTO_CONFIG_RESET_DELAY_SOFA }, 
  "switch.bett": { "default": "off", "delay": AUTO_CONFIG_RESET_DELAY_BETT } 
}

def on_delay_reset_factory(entity):
  @state_trigger(expr(entity, f"!= {entities.get(entity)['delay']}"))
  def on_delay_reset(var_name=None):
    if entities.get(entity)['default'] == "off":
      switch.turn_off(entity_id=var_name)
    elif entities.get(entity)['default'] == "on":
      switch.turn_on(entity_id=var_name)
  return on_delay_reset

for entity in entities:
  on_delay_reset_factory(entity)

# Default configuration
@state_trigger(expr("climate.kuche", "!= 'off'", defined=True), state_check_now=True)
def reset_climate_kuche(var_name=None):
  climate.turn_off(entity_id=var_name)