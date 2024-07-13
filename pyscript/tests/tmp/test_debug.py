import os
import unittest
from unittest.mock import patch, Mock

class TestAirDebug(unittest.TestCase):

  os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

  @classmethod
  def setUpClass(cls):
    from mocks.mock_pyscript import MockPyscript
    cls.mock_pyscript = MockPyscript()
    
    # cls.patcher = patch('custom_components.pyscript.service', new=cls.mock_pyscript.service)
    # cls.patcher = patch('custom_components.pyscript', new=cls.mock_pyscript)
    cls.patcher = patch('air_control.pyscript', new=cls.mock_pyscript)
    # cls.patcher = patch('air_control.pyscript.service', new=cls.mock_pyscript.service)

    
  @classmethod
  def tearDownClass(cls):
      cls.patcher.stop()

  def test_some_function(self, mock_some_function):
    from pyscript.apps.air_control import some_function
    result = some_function()
    self.assertTrue(result)

if __name__ == '__main__':
  unittest.main()
