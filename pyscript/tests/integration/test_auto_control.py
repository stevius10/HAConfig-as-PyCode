import unittest
from unittest.mock import patch, MagicMock

from tests.mocks.mock_trigger import MockTrigger


class TestAutoControl(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    self.mock_trigger = MockTrigger()
    state = MagicMock()
    task = MagicMock()
    event = MagicMock()
    service = MagicMock()
    scene = MagicMock()

  @patch('auto_control.AUTO_CONTROL_ENTITIES')
  @patch('auto_control.expr')
  def test_on_press_factory_integration(self, mock_expr, mock_auto_control_entities):
    from auto_control import on_press_factory
    
    mock_auto_control_entities.return_value = {
      'sensor.test_button': {
        'on': 'scene.test_on',
        'off': 'scene.test_off'
      }
    }
    mock_expr.return_value = "mocked_expression"
    
    with patch('auto_control.state_trigger', self.mock_trigger.state_trigger):
      on_press_factory('sensor.test_button')
    
    mock_expr.assert_called_once_with(
      'sensor.test_button', 
      expression=['on-press', 'off-press', 'up-press', 'down-press', 'single-press', 'double-press', 'long-press'],
      comparator="in",
      defined=False
    )
    
    self.assertEqual(len(self.mock_trigger.triggers), 1)
    self.assertEqual(self.mock_trigger.triggers[0]['type'], 'state_trigger')
    self.assertEqual(self.mock_trigger.triggers[0]['args'], ("mocked_expression",))
    
    result = self.mock_trigger.simulate_trigger('state_trigger', 'sensor.test_button', 'on-press')
    
    self.assertIsNotNone(result)
    scene.turn_on.assert_called_once_with(entity_id='scene.test_on')

if __name__ == '__main__':
  unittest.main()