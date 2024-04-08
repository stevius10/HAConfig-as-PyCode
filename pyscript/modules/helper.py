import logging
import time

from config import STATES_HA_UNDEFINED

def expr(entity, expression="", comparator="==", defined=True, operator='or', log=False): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression="", defined=True, operator=operator, log=True)
  
  if expression != "":
    expression = f"{comparator} '{expression}'"

  if log and "pyscript" in globals(): 
    pyscript.log_state(entity=entity, expr=expression)

  statement_condition_defined = f"and {entity} not in {STATES_HA_UNDEFINED}" if defined else ""

  expr = f"{entity} {expression} {statement_condition_defined}"
  
  return expr

  
def expressions(entities, expression="", defined=True, operator='or', log=False):
  exprs = []
  
  if not expression:
    if isinstance(entities, list):
      expr_concatenated = ['(' + expr(entity) + ')' for entity in entities]
      return (" {} ".format(operator)).join(expr_concatenated)
    
    if isinstance(entities, dict):
      pass

  elif expression.isalnum():
      if isinstance(entities, list):
        expr_concatenated = ['(' + expr(entity, expression) + ')' for entity in entities]
        return (" {} ".format(operator)).join(expr_concatenated)
      if isinstance(entities, dict):
        pass
  
  if isinstance(entities, list):
    pass
  if isinstance(entities, dict):
    pass
