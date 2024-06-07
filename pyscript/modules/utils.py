from config import LOG_ENABLED, LOG_LOGGING_LEVEL, LOG_LOGGER_SYS
from constants import *

import datetime
import logging
import os
import regex as re

def expr(entity, expression="", comparator="==", defined=True, logs=LOG_ENABLED): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, logs=logs, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_HA_UNDEFINED}" if defined else ""

  if expression is not None:
    if any([isinstance(expression, (int, float)), '>' in comparator, '<' in comparator]):
      entity = "int({})".format(entity) if entity.isalnum() else 0
    elif expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""
  
  if logs: 
    try: pyscript.log_state(expression=f"{entity} {expression}")
    except: pass
  
  return f"{entity} {expression} {statement_condition_defined}"
  
def expressions(entities, expression=None, comparator="==", defined=True, operator='or', logs=LOG_ENABLED):  
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

# Helper

def call_func(func, **kwargs):
  if service.has_service(func.split(".")[0], func.split(".")[1]):
    service.call(func.split(".")[0], func.split(".")[1], **kwargs)

def ctx_call(func):
  def decorator(ctx):
    current = pyscript.get_global_ctx()
    pyscript.set_global_ctx(ctx)
    result = func()
    log_internal(msg=f"{func} returned {result} in {ctx} from {current}", logger=get_logger())
    pyscript.set_global_ctx(current)

    return result
  return decorator