import unittest
from unittest.mock import patch, MagicMock
import pyscript
from pyscript import state, task, event, service

class TestConfigControl(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()

  @patch('pyscript.config_control.CONFIG_CONTROL_ENTITIES')
  def test_on_press_factory_integration(self, mock_config_control_entities):
    from pyscript.config_control import on_press_factory
    mock_config_control_entities.return_value = {
      'sensor.test_button': {
        'on': 'scene.test_on',
        'off': 'scene.test_off'
      }
    }
    on_press_factory('sensor.test_button')
    pyscript.state.trigger.assert_called_once()
    pyscript.scene.turn_on.assert_not_called()

  @patch('pyscript.config_control.CONFIG_CONTROL_ENTITIES')
  def test_on_press_integration(self, mock_config_control_entities):
    from pyscript.config_control import on_press_factory
    mock_config_control_entities.return_value = {
      'sensor.test_button': {
        'on': 'scene.test_on',
        'off': 'scene.test_off'
      }
    }
    on_press_factory('sensor.test_button')
    pyscript.state.get.return_value = 'on-press'
    on_press_factory('sensor.test_button')('sensor.test_button', 'on-press')
    pyscript.scene.turn_on.assert_called_once_with(entity_id='scene.test_on')

if __name__ == '__main__':
  unittest.main()