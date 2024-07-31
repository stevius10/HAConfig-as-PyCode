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
    for p in cls.patches:
      p.start()
    patch.dict('builtins.__dict__', {'service': cls.mock_pyscript.service}).start()
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

  def test_ha_log_truncate(self):
    self.mock_file_read.side_effect = [
      ['log1', 'log2'],
      ['history1', 'history2'],
      'log3\n# 1 / 1000 at ' + str(datetime.now()) + '\n'
    ]
    async def run_test():
      await self.ha_log_truncate()
      self.mock_file_read.assert_any_call('/config/home-assistant.log')

if __name__ == '__main__':
  unittest.main()