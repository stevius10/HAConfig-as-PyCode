import io
import unittest

from utils import *

@service
def run_tests():
  from logfile import Logfile # req. sys setup 
  logfile = Logfile(ctx=pyscript.get_global_ctx())
  try: 
    import os
    import sys
    
    base = '/homeassistant/pyscript'
    dirs = ['', 'apps', 'modules', 'python', 'scripts', 'test']
    
    for d in dirs:
      path = os.path.join(base, d)
      if path not in sys.path:
        sys.path.append(path)
    logfile.log(test_unit())
    logfile.log(test_integration())
    logfile.log(test_functional())
  except e: 
    log(str(e))
  finally:
    return logfile.close()
    
@logged
@service
def test_unit():
  from unit.test_modules import TestConstants, TestUtils
  from unit.test_apps import TestScrape, TestServices, TestSyncGit
  from unit.test_python import TestFilesystem, TestLogfile
  from unit.test_scripts import TestHaSystem, TestHaUtils

  suite = unittest.TestSuite()
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestConstants))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestUtils))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestScrape))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestServices))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestSyncGit))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestFilesystem))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestLogfile))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestHaSystem))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestHaUtils))

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
  from integration.test_auto_entities import TestAutoEntities
  from integration.test_auto_motion import TestAutoMotion
  from integration.test_auto_notify import TestAutoNotify
  from integration.test_auto_control import TestAutoControl

  suite = unittest.TestSuite()
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestAutoEntities))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestAutoMotion))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestAutoNotify))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestAutoControl))

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
  from functional.test_air_control import TestAirControl
  from functional.test_off import TestOff

  suite = unittest.TestSuite()
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestAirControl))
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestOff))

  output = io.StringIO()
  runner = unittest.TextTestRunner(stream=output, verbosity=2)
  result = runner.run(suite)
  
  return {
    "tests": result.testsRun,
    "errors": len(result.errors),
    "details": {f"{test}: {str(error)}" for test, error in result.errors}
  }