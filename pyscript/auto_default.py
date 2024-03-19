from helper import expr
from defaults import AUTO_ENTITIES_DEFAULT

default_trigger = []
entities = AUTO_ENTITIES_DEFAULT

ha_service_turn_off = "homeassistant.turn_off"
def default_factory(entity, func):
  
  @state_trigger(expr(entity, entities.get(entity)['default'], comparator="!="), func)
  def default(func):
    service.call(func.split(".")[0], func.split(".")[1], entity_id=entity)
  
  default_trigger.append(default)

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities[entity]["func"] = ha_service_turn_off
    default_factory(entity, entities.get(entity)['func'])