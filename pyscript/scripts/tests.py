import io
import os
import unittest
import sys
from utils import *

@service
def run_tests():
  from logfile import Logfile
  logfile = Logfile(name=pyscript.get_global_ctx())
  try:
    logfile.log(test_unit())
    # logfile.log(test_integration())
    # logfile.log(test_functional())
  except Exception as e:
    log(str(e))
  finally:
    return logfile.close()

@logged
@service
def test_unit():
  base = '/config/pyscript/tests/unit'
  if base not in sys.path:
    sys.path.append(base)

  loader = unittest.TestLoader()
  suite = loader.discover(start_dir=base, pattern='test_*.py')

  output = io.StringIO()
  runner = unittest.TextTestRunner(stream=output, verbosity=2)
  result = runner.run(suite)

  return {
    "tests": result.testsRun,
    "errors": len(result.errors),
    "details": {f"{test}": str(error) for test, error in result.errors}
  }

@logged
@service
def test_integration():
  base = '/config/pyscript/tests/integration'
  if base not in sys.path:
    sys.path.append(base)

  loader = unittest.TestLoader()
  suite = loader.discover(start_dir=base, pattern='test_*.py')

  output = io.StringIO()
  runner = unittest.TextTestRunner(stream=output, verbosity=2)
  result = runner.run(suite)

  return {
    "tests": result.testsRun,
    "errors": len(result.errors),
    "details": {f"{test}": str(error) for test, error in result.errors}
  }

@logged
@service
def test_functional():
  base = '/config/pyscript/tests/functional'
  if base not in sys.path:
    sys.path.append(base)

  loader = unittest.TestLoader()
  suite = loader.discover(start_dir=base, pattern='test_*.py')

  output = io.StringIO()
  runner = unittest.TextTestRunner(stream=output, verbosity=2)
  result = runner.run(suite)

  return {
    "tests": result.testsRun,
    "errors": len(result.errors),
    "details": {f"{test}": str(error) for test, error in result.errors}
  }