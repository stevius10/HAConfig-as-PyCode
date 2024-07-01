import unittest
import sys
import os
import io

from utils import *

@service
def test():
  sys.path.insert(0, "/config/pyscript")
  from logfile import Logfile # req. sys setup 
  logfile = Logfile(ctx=pyscript.get_global_ctx())
  try: 
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
  from tests.unit.test_modules import TestConstants, TestUtils
  from tests.unit.test_apps import TestScrape, TestServices, TestSyncGit
  from tests.unit.test_python import TestFilesystem, TestLogfile
  from tests.unit.test_scripts import TestHaSystem, TestHaUtils

  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestConstants))
  suite.addTest(unittest.makeSuite(TestUtils))
  suite.addTest(unittest.makeSuite(TestScrape))
  suite.addTest(unittest.makeSuite(TestServices))
  suite.addTest(unittest.makeSuite(TestSyncGit))
  suite.addTest(unittest.makeSuite(TestFilesystem))
  suite.addTest(unittest.makeSuite(TestLogfile))
  suite.addTest(unittest.makeSuite(TestHaSystem))
  suite.addTest(unittest.makeSuite(TestHaUtils))

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
  from tests.integration.test_auto_entities import TestAutoEntities
  from tests.integration.test_auto_motion import TestAutoMotion
  from tests.integration.test_auto_notify import TestAutoNotify
  from tests.integration.test_auto_control import TestAutoControl

  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestAutoEntities))
  suite.addTest(unittest.makeSuite(TestAutoMotion))
  suite.addTest(unittest.makeSuite(TestAutoNotify))
  suite.addTest(unittest.makeSuite(TestAutoControl))

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
  from tests.functional.test_air_control import TestAirControl
  from tests.functional.test_off import TestOff

  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestAirControl))
  suite.addTest(unittest.makeSuite(TestOff))

  output = io.StringIO()
  runner = unittest.TextTestRunner(stream=output, verbosity=2)
  result = runner.run(suite)
  
  return {
    "tests": result.testsRun,
    "errors": len(result.errors),
    "details": {f"{test}: {str(error)}" for test, error in result.errors}
  }