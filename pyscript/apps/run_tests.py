from utils import *

@logged
@service
def run_tests():
  from logfile import Logfile
  logfile = Logfile(name="tests", component_log=False)
  try:
    test_results = __run_test("tmp")
    logfile.log(test_results)
  except Exception as e:
    log(str(e))
    logfile.log(str(e))
  finally:
    return { "result": logfile.close() }

@pyscript_executor
def __run_test(test_type):
  from contextlib import redirect_stdout
  import io
  import os
  import sys
  import unittest

  os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
  print(f"Current working directory: {os.getcwd()}")  # Debug statement
  print(f"sys.path: {sys.path}")  # Debug statement

  f = io.StringIO()
  with redirect_stdout(f):
    try:
      loader = unittest.TestLoader()
      print(f"Discovering tests in /config/pyscript/tests/{test_type}")  # Debug statement
      suite = loader.discover(f"/config/pyscript/tests/{test_type}")
      
      runner = unittest.TextTestRunner(stream=f, verbosity=3)
      result = runner.run(suite)
    except Exception as e:
      return f"Exception occurred: {str(e)}"
  return f.getvalue()
