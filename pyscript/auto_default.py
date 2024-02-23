from helper import expr

# Küche: Heizung ausgeschalten
@state_trigger(expr("climate.kuche", "!= 'off'", defined=True), state_check_now=True)
def reset_climate_kuche(var_name=None):
  climate.turn_off(entity_id=var_name)