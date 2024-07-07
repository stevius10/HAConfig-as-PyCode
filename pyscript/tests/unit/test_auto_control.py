import unittest
from unittest.mock import patch
from tests.mocks.mock_pyscript import MockPyscript

pyscript = MockPyscript()

class TestAutoControl(unittest.TestCase):

  @patch('custom_components.pyscript.service', new=pyscript.service)
  def test_some_function(self, mock_some_function):
    from pyscript.apps.auto_control import some_function
    result = some_function()
    self.assertTrue(result)

if __name__ == '__main__':
  unittest.main()
