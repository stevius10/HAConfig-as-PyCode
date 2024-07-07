from utils import *

@logged
@service
def run_tests():
  from logfile import Logfile
  logfile = Logfile(name="tests")

  try:
    logfile.log(__run_test("tmp"))
  except Exception as e:
    log(str(e))
    logfile.log(str(e))
  finally:
    return logfile.close()

@pyscript_executor
def __run_test(test_type):
  from contextlib import redirect_stdout
  import io
  import os
  import sys
  import unittest

  os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

  f = io.StringIO()
  with redirect_stdout(f):
    try:
      base_path = "/config/pyscript"
      for subdir in ['apps', 'modules', 'scripts', 'tests']:
        path = os.path.join(base_path, subdir)
        if path not in sys.path:
          sys.path.insert(0, path)

      loader = unittest.TestLoader()
      suite = loader.discover(test_path)
      
      runner = unittest.TextTestRunner(stream=f, verbosity=3)
      result = runner.run(suite)
      
      output = f.getvalue()
      if not result.wasSuccessful():
        return f"Tests failed\n{output}"
    except Exception as e:
      return f"Exception occurred: {str(e)}"
  return f.getvalue()