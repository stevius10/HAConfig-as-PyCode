import os
import unittest
import aiofiles
import asyncio
from unittest.mock import patch, AsyncMock, mock_open
import importlib

from mocks.mock_pyscript import MockPyscript

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

class TestHaHelper(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    print("Setting up class TestHaHelper")
    cls.mock_pyscript = MockPyscript()
    cls.mock_pyscript_event_trigger = cls.mock_pyscript.event_trigger

    # Debugging-Ausgabe hinzufügen
    print("Checking custom_components.pyscript.trigger")
    try:
      trigger_module = importlib.import_module('custom_components.pyscript.trigger')
      print("Module imported successfully")
      print("Available attributes in trigger module:", dir(trigger_module))
      if hasattr(trigger_module, 'event_trigger'):
        print("event_trigger is available in trigger module")
      else:
        print("event_trigger is NOT available in trigger module")
    except ImportError as e:
      print(f"Error importing module: {e}")

    cls.patches = [
      patch('custom_components.pyscript.trigger.event_trigger', new=cls.mock_pyscript.event_trigger),
      patch('ha_helper.pyscript.event_trigger', new=cls.mock_pyscript.event_trigger),
      patch('ha_helper.event_trigger', new=cls.mock_pyscript.event_trigger),
      patch('ha_helper.pyscript.event_trigger', new=cls.mock_pyscript.event_trigger)
    ]

    for p in cls.patches:
      print(f"Starting patch: {p}")
      p.start()

    from ha_helper import ha_log_truncate, log_truncate, log_rotate, log_read, log_write
    from constants.config import (
      CFG_LOG_SIZE, CFG_LOG_TAIL, CFG_LOG_HISTORY_SIZE, CFG_PATH_FILE_LOG, 
      CFG_LOG_HISTORY_SUFFIX, CFG_LOG_ARCHIV_SUFFIX, CFG_LOG_SETTINGS_IO_RETRY, 
      CFG_LOG_SETTINGS_DELAY_BLOCK, CFG_LOG_ARCHIV_SIZE)

    cls.ha_log_truncate = ha_log_truncate
    cls.log_truncate = log_truncate
    cls.log_rotate = log_rotate
    cls.log_read = log_read
    cls.log_write = log_write

    cls.mock_task_sleep = patch('ha_helper.task.sleep', new_callable=AsyncMock).start()
    cls.mock_log_read = patch('ha_helper.log_read', new_callable=AsyncMock).start()
    cls.mock_log_write = patch('ha_helper.log_write', new_callable=AsyncMock).start()
    cls.mock_os_path_exists = patch('os.path.exists', return_value=True).start()
    cls.mock_open = patch('aiofiles.open', mock_open(read_data='log_content')).start()

  @classmethod
  def tearDownClass(cls):
    print("Tearing down class TestHaHelper")
    patch.stopall()

  def setUp(self):
    print("Setting up a test method")
    self.loop = asyncio.get_event_loop()

  def tearDown(self):
    print("Tearing down a test method")
    self.loop.close()

  def test_ha_log_truncate_event(self):
    print("Running test_ha_log_truncate_event")
    event = {"trigger_type": "event", "event_type": "modified", "file": "", "folder": "", "path": ""}
    async def run_test():
      await self.ha_log_truncate(**event)
      self.mock_log_write.assert_called_with(CFG_PATH_FILE_LOG, log_size_truncated=CFG_LOG_SIZE)
      self.mock_task_sleep.assert_called_with(CFG_LOG_SETTINGS_DELAY_BLOCK)
    self.loop.run_until_complete(run_test())

  def test_ha_log_truncate_time(self):
    print("Running test_ha_log_truncate_time")
    event = {"trigger_type": "time", "event_type": "", "file": "", "folder": "", "path": ""}
    async def run_test():
      await self.ha_log_truncate(**event)
      self.mock_log_write.assert_called_with(CFG_PATH_FILE_LOG, log_size_truncated=0)
      self.mock_task_sleep.assert_called_with(CFG_LOG_SETTINGS_DELAY_BLOCK)
    self.loop.run_until_complete(run_test())

  def test_log_truncate(self):
    print("Running test_log_truncate")
    self.mock_log_read.side_effect = [['log1', 'log2', 'log3'], ['history1', 'history2']]
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
