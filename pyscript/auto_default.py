from helper import expr
import constants

# Küche: Heizung ausgeschalten
@state_trigger(expr("climate.kuche", "!= 'off'", defined=True), state_check_now=True)
def reset_climate_kuche(var_name=None):
  climate.turn_off(entity_id=var_name)

# Homeassistant

# Adguard angeschalten
@state_trigger(expr("switch.adguard_home_schutz", "== 'off'"), state_hold=constants.AUTO_CONFIG_DEFAULT_RESET_DELAY, state_check_now=True)
def reset_climate_kuche(var_name=None):
  switch.turn_on(entity_id=var_name)
