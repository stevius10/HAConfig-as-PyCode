import unittest
from unittest.mock import patch, MagicMock
import pyscript
from pyscript import state, task, event, service

class TestAutoEntities(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()

  @patch('pyscript.auto_entities.AUTO_ENTITIES')
  def test_default_factory_integration(self, mock_auto_entities):
    from pyscript.auto_entities import default_factory
    mock_auto_entities.return_value = {
      'light.test': {
        'default': 'off',
        'func': 'light.turn_off'
      }
    }
    default_factory('light.test', 'light.turn_off')
    pyscript.state.trigger.assert_called_once()
    pyscript.service.call.assert_called_once_with('light', 'turn_off', entity_id='light.test')

  @patch('pyscript.auto_entities.AUTO_ENTITIES')
  def test_timeout_factory_integration(self, mock_auto_entities):
    from pyscript.auto_entities import timeout_factory
    mock_auto_entities.return_value = {
      'switch.test': {
        'default': 'off',
        'delay': 300
      }
    }
    timeout_factory('switch.test', 'off', 300)
    pyscript.state.trigger.assert_called()
    pyscript.timer.start.assert_called_once()

if __name__ == '__main__':
  unittest.main()