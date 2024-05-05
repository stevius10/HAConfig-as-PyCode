from config import STATES_HA_UNDEFINED

log_enabled = True

def expr(entity, expression="", comparator="==", defined=True, logs=log_enabled): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, logs=logs, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_HA_UNDEFINED}" if defined else ""

  if expression is not None:
    if any([isinstance(expression, (int, float)), '>' in comparator, '<' in comparator]):
      entity = "int({})".format(entity)
    elif expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""
  
  if logs: 
    try: pyscript.log_state(expression=f"{entity} {expression}")
    except: pass
  
  return f"{entity} {expression} {statement_condition_defined}"
  
def expressions(entities, expression=None, comparator="==", defined=True, operator='or', logs=log_enabled):  
  if expression:
    if isinstance(expression, int):
      for i in range(len(entities)):
        entities[i] = f"{entities[i]}"

    result = f" {operator} ".join([expr(entity, expression, defined=defined, logs=False, comparator=comparator) for entity in entities])
  else: 
    result = f" {operator} ".join([expr(entity, expression=None, defined=defined, logs=False) for entity in entities])
    
  if logs: 
    try: pyscript.log_state(expression=result)
    except: pass

  return result