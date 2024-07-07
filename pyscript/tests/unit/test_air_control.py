import unittest
from unittest.mock import patch
from tests.mocks.mock_pyscript import MockPyscript

pyscript = MockPyscript()

class TestAirControl(unittest.TestCase):

  @patch('custom_components.pyscript.state_trigger', new=pyscript.state_trigger)
  def test_air_control_with_state_trigger(self, mock_state_trigger):
    from pyscript.apps.air_control import some_state_triggered_function
    result = some_state_triggered_function(value=10, old_value=5)
    self.assertTrue(result)

  @patch('custom_components.pyscript.service', new=pyscript.service)
  def test_some_function(self, mock_some_function):
    from pyscript.apps.air_control import some_function
    result = some_function()
    self.assertTrue(result)

if __name__ == '__main__':
  unittest.main()
