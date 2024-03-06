from constants import HA_STATES_UNDEFINED

def expr(entity, expression="", defined=True, log=True): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression="", defined=True, log=True)
  
  if expression.isalnum():
    expression = f"== '{expression}'"
    
  statement_condition_defined = f"and {entity} not in {HA_STATES_UNDEFINED}" if defined else ""
  
  expr = f"{entity} {expression} {statement_condition_defined}"
  
  #if log: 
    #pyscript.log_state(expr=expr)
    
  return expr

  
def expressions(entities, expression="", defined=True, log=True):
  exprs = []
  if not expression:
    
    if isinstance(entities, list):
      expr_concatenated = ['(' + expr(entity) + ')' for entity in entities]
      return " or ".join(expr_concatenated)
    
    if isinstance(entities, dict):
      pass

  elif expression.isalnum():
      if isinstance(entities, list):
        pass
      if isinstance(entities, dict):
        pass
  
  if isinstance(entities, list):
    pass
  if isinstance(entities, dict):
    pass