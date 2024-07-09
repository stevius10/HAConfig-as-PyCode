import os
import unittest
from unittest.mock import patch, Mock

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

class TestAirDebug(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    from tests.mocks.mock_pyscript import MockPyscript
    cls.mock_pyscript = Mock()
    
    cls.patcher = patch('service', new=cls.mock_pyscript.service)
    cls.patcher = patch('pyscript.service', new=cls.mock_pyscript.service)
    cls.patcher = patch('custom_components.pyscript.service', new=cls.mock_pyscript.service)
    cls.patcher = patch('air_control', new=cls.mock_pyscript.service)
    cls.patcher = patch('apps.air_control', new=cls.mock_pyscript.service)
    cls.patcher = patch('pyscript.apps.air_control', new=cls.mock_pyscript.service)
    cls.patcher = patch('service', new=cls.mock_pyscript.service)
    cls.patcher = patch('service', new=cls.mock_pyscript.service)
    cls.patcher = patch('service', new=cls.mock_pyscript.service)
    cls.patcher = patch('service', new=cls.mock_pyscript.service)
    cls.patcher = patch('service', new=cls.mock_pyscript.service)

    cls.patcher.start()
    
  @classmethod
  def tearDownClass(cls):
      cls.patcher.stop()

  def test_some_function(self, mock_some_function):
    from pyscript.apps.air_control import some_function
    result = some_function()
    self.assertTrue(result)

if __name__ == '__main__':
  unittest.main()
