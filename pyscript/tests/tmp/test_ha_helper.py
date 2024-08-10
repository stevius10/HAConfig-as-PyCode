import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import importlib
import asyncio
from datetime import datetime

class TestHaHelper(unittest.TestCase):
  patches = []

  @classmethod
  def setUpClass(cls):
    from mocks.mock_pyscript import MockPyscript
    cls.mock_pyscript = MockPyscript()
    
    for attr in dir(cls.mock_pyscript):
      if callable(getattr(cls.mock_pyscript, attr)) and not attr.startswith("__"):
        cls.patches.append(patch.dict('builtins.__dict__', {attr: getattr(cls.mock_pyscript, attr)}))
    for attr in dir(cls.mock_pyscript.task):
      if callable(getattr(cls.mock_pyscript.task, attr)) and not attr.startswith("__"):
        cls.patches.append(patch.dict('builtins.__dict__', {attr: getattr(cls.mock_pyscript.task, attr)}))

    patch.dict('builtins.__dict__', {'task': cls.mock_pyscript.task}).start()

    for p in cls.patches:
      p.start()

    try:
      from ha_helper import ha_log_truncate, log_truncate, log_rotate, file_read, file_write
      cls.ha_log_truncate = ha_log_truncate
      cls.log_truncate = log_truncate
      cls.log_rotate = log_rotate
      cls.file_read = file_read
      cls.file_write = file_write
    except Exception as e:
      print(f"Error importing ha_helper: {e}")

  def setUp(self):
    self.mock_file_read = patch('ha_helper.file_read', new=MagicMock()).start()
    self.mock_file_write = patch('ha_helper.file_write', new=MagicMock()).start()

  def tearDown(self):
    patch.stopall()

  def test_ha_log_truncate_event_modified(self):
    self.mock_file_read.side_effect = [
      ['log1', 'log2', 'log3'],
      ['history1', 'history2']
    ]
    
    async def run_test():
      await self.ha_log_truncate(trigger_type="event", event_type="modified")
      self.mock_file_read.assert_any_call('/config/home-assistant.log')

    asyncio.run(run_test())

  def test_ha_log_truncate_time_trigger(self):
    self.mock_file_read.side_effect = [
      ['log1', 'log2', 'log3'],
      ['history1', 'history2']
    ]
    
    async def run_test():
      await self.ha_log_truncate(trigger_type="time")
      self.mock_file_read.assert_any_call('/config/home-assistant.log')

    asyncio.run(run_test())

  def test_log_truncate(self):
    self.mock_file_read.side_effect = [
      ['line1', 'line2', 'line3', 'line4', 'line5'],
      ['history1', 'history2']
    ]
    
    self.log_truncate(logfile='test.log', log_size_truncated=2, log_tail_size=2, log_history_size=4)
    
    self.mock_file_write.assert_any_call('test.log', ['line4', 'line5', '# 5 / 2 at ' + str(datetime.now()) + '\n'])
    self.mock_file_write.assert_any_call('test.log.history', ['line3', 'line4', 'line5', 'history1', 'history2'])

  def test_log_rotate(self):
    self.mock_file_read.side_effect = [
      ['line1', 'line2', 'line3'],
      ['archive1', 'archive2']
    ]
    
    self.log_rotate(file='test.log')
    
    self.mock_file_write.assert_called_with('test.log.archive', ['line3', 'line2', 'line1', 'archive1', 'archive2'])

if __name__ == '__main__':
  unittest.main()
