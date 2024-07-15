import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import asyncio
from datetime import datetime

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Print sys.path and current working directory for debugging
print(f"sys.path: {sys.path}")
print(f"Current working directory: {os.getcwd()}")

try:
  from pyscript.tests.mocks.mock_pyscript import MockPyscript
  print("Imported MockPyscript successfully")
except Exception as e:
  print(f"Error importing MockPyscript: {e}")

class TestHaHelper(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    import sys
    sys.modules['custom_components.pyscript'] = pyscript
    from ha_helper import ha_log_truncate, log_truncate, log_rotate
    
    print("Setting up class TestHaHelper")
    cls.mock_pyscript = MockPyscript()
    def mock_event_trigger(event_type, expr=None):
      def decorator(func):
        def wrapper(*args, **kwargs):
          return func(*args, **kwargs)
        return wrapper
      return decorator
    cls.mock_event_trigger = mock_event_trigger
    
    try:
      import custom_components.pyscript as pyscript_module
      print(f"Attributes of custom_components.pyscript: {dir(pyscript_module)}")
    except Exception as e:
      print(f"Error importing custom_components.pyscript: {e}")

    # Adjusted patches based on available attributes
    cls.patches = [
      patch.dict('custom_components.pyscript.trigger.__dict__', {'event_trigger': mock_event_trigger}),
      patch.dict('custom_components.pyscript.__init__.__dict__', {'event_trigger': mock_event_trigger}),
      patch('custom_components.pyscript.trigger.AstEval', new=MagicMock()),
      patch('custom_components.pyscript.trigger.Event.notify_add', new=MagicMock())
    ]

    for p in cls.patches:
      print(f"Starting patch: {p}")
      p.start()

    from ha_helper import ha_log_truncate, log_truncate, log_rotate, log_read, log_write
    from constants.config import (
      CFG_LOG_SIZE, CFG_LOG_TAIL, CFG_LOG_HISTORY_SIZE, CFG_PATH_FILE_LOG, 
      CFG_LOG_HISTORY_SUFFIX, CFG_LOG_ARCHIV_SUFFIX, CFG_LOG_SETTINGS_IO_RETRY, 
      CFG_LOG_SETTINGS_DELAY_BLOCK, CFG_LOG_ARCHIV_SIZE
    )

    cls.ha_log_truncate = ha_log_truncate
    cls.log_truncate = log_truncate
    cls.log_rotate = log_rotate
    cls.log_read = log_read
    cls.log_write = log_write

  def setUp(self):
    self.loop = asyncio.get_event_loop()
    self.mock_log_read = patch('ha_helper.log_read', new=MagicMock()).start()
    self.mock_log_write = patch('ha_helper.log_write', new=MagicMock()).start()
    self.mock_open = patch('builtins.open', new=MagicMock()).start()

  def tearDown(self):
    for p in self.patches:
      p.stop()
    patch.stopall()

  def test_log_truncate(self):
    print("Running test_log_truncate")
    self.mock_log_read.side_effect = [
      ['log1', 'log2'], 
      ['history1', 'history2'], 
      ['log3']
    ]
    async def run_test():
      await self.log_truncate()
      self.mock_log_read.assert_any_call(CFG_PATH_FILE_LOG, lines=True)
      self.mock_log_read.assert_any_call(f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}")
      self.mock_log_write.assert_any_call(CFG_PATH_FILE_LOG, ['log3\n', '# 1 / 1000 at ' + str(datetime.now()) + '\n'])
      self.mock_log_write.assert_any_call(f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}", ['log1', 'log2', 'history1', 'history2'])
    self.loop.run_until_complete(run_test())

  def test_log_rotate(self):
    print("Running test_log_rotate")
    self.mock_log_read.side_effect = [
      ['history1', 'history2'], 
      ['archive1', 'archive2', 'archive3'],
      'log_content'
    ]
    async def run_test():
      await self.log_rotate()
      self.mock_log_read.assert_any_call(f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}")
      self.mock_log_read.assert_any_call(f"{CFG_PATH_FILE_LOG}.{CFG_LOG_ARCHIV_SUFFIX}", lines=True)
      self.mock_log_read.assert_any_call(CFG_PATH_FILE_LOG)
      self.mock_log_write.assert_any_call(f"{CFG_PATH_FILE_LOG}.{CFG_LOG_ARCHIV_SUFFIX}", 'archive2\narchive3\n')
      self.mock_log_write.assert_any_call(f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}", 'log_content')
    self.loop.run_until_complete(run_test())

  def test_log_read(self):
    print("Running test_log_read")
    self.mock_open.return_value.read.return_value = 'log_content'
    async def run_test():
      result = await self.log_read('test_logfile')
      self.assertEqual(result, 'log_content')
      self.mock_open.assert_called_with('test_logfile', mode='r')
    self.loop.run_until_complete(run_test())

  def test_log_write(self):
    print("Running test_log_write")
    async def run_test():
      result = await self.log_write('test_logfile', 'test_content')
      self.assertTrue(result)
      self.mock_open.assert_called_with('test_logfile', mode='w+')
      self.mock_open().write.assert_called_with('test_content')
    self.loop.run_until_complete(run_test())

if __name__ == '__main__':
  unittest.main()
