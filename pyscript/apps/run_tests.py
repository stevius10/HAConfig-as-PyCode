from constants.config import CFG_PATH_DIR_LOG

from utils import *

@logged
@service
def run_tests():
  from logfile import Logfile
  logfile = Logfile(name="tests", log_dir=CFG_PATH_DIR_LOG)
  try:
    test_results = __run_test("tmp")
    logfile.log(test_results)
  except Exception as e:
    logfile.log(str(e))
  finally:
    return { "result": logfile.close() }

@pyscript_executor
def __run_test(test_type):
  from contextlib import redirect_stdout
  import io
  import unittest
        
  f = io.StringIO()
  with redirect_stdout(f):
    try:
      suite = unittest.TestLoader().discover(f"/config/pyscript/tests/{test_type}")
      unittest.TextTestRunner(stream=f, verbosity=3).run(suite)
    except Exception as e:
      raise e
  return f.getvalue()
