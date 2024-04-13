import logging
import time

from config import STATES_HA_UNDEFINED

def expr(entity, expression="", comparator="==", defined=True, logs=False): 
  
  # Catch multiple expressions
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, logs=logs, )
  
  # Catch state logging
  if logs: # ! order
    try: pyscript.log_state(entity=entity, expr=expression)
    except: pass

  # Catch defined expression
  if expression is not None:
    if comparator in ['>', '<', '<=', '>=']: 
      # entity = f"int({entity})" if (entity%1)==0 else f"float({entity})"
      expression = f"{expression}"
    # Catch expressions
    if expression in [True, False]: # bool
      expression = f"{expression}"
    if type(expression) == str: # str
      expression = f"'{expression}'"
    
    expression = f"{comparator} {expression}"
  statement_condition_defined = f"and {entity} not in {STATES_HA_UNDEFINED}" if defined else ""

  expr = f"{entity} {expression} {statement_condition_defined}"
  
  return expr

  
def expressions(entities, expression="", comparator="==", defined=True, operator='or', logs=False):
  exprs = []
  
  if not expression:
    if isinstance(entities, list):
      if expression == "":
        expression = True
      expr_concatenated = ['(' + expr(entity, expression, defined=defined, logs=logs, comparator=comparator) + ')' for entity in entities]
      return (" {} ".format(operator)).join(expr_concatenated)
    
    if isinstance(entities, dict):
      pass

  elif expression.isalnum():
      if isinstance(entities, list):
        expr_concatenated = ['(' + expr(entity, expression, defined=defined, logs=logs, comparator=comparator) + ')' for entity in entities]
        return (" {} ".format(operator)).join(expr_concatenated)
      if isinstance(entities, dict):
        pass
  
  if isinstance(entities, list):
    pass
  if isinstance(entities, dict):
    pass
