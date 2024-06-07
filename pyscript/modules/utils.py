from mapping import STATES_UNDEFINED

def expr(entity, expression="", comparator="==", defined=True): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_UNDEFINED}" if defined else ""

  if expression is not None:
    if any([isinstance(expression, (int, float)), '>' in comparator, '<' in comparator]):
      entity = "int({})".format(entity) if entity.isalnum() else 0
    elif expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""
  
  return f"{entity} {expression} {statement_condition_defined}"
  
def expressions(entities, expression=None, comparator="==", defined=True, operator='or'):  
  if expression:
    if isinstance(expression, int):
      for i in range(len(entities)):
        entities[i] = f"{entities[i]}"

    result = f" {operator} ".join([expr(entity, expression, defined=defined, comparator=comparator) for entity in entities])
  else: 
    result = f" {operator} ".join([expr(entity, expression=None, defined=defined) for entity in entities])

  return result