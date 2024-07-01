import unittest
from unittest.mock import patch, MagicMock

class TestAutoEntities(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()
    pyscript.timer = MagicMock()

  @patch('pyscript.auto_entities.AUTO_ENTITIES')
  @patch('pyscript.auto_entities.state_trigger')
  def test_default_factory(self, mock_state_trigger, mock_auto_entities):
    from pyscript.auto_entities import default_factory
    mock_auto_entities.return_value = {
      'light.test': {
        'default': 'off',
        'func': 'light.turn_off'
      }
    }
    mock_state_trigger.return_value = lambda x: x
    default_factory('light.test', 'light.turn_off')
    mock_state_trigger.assert_called_once()
    decorated_func = mock_state_trigger.return_value
    decorated_func('light.turn_off')
    pyscript.service.call.assert_called_once_with('light', 'turn_off', entity_id='light.test')

  @patch('pyscript.auto_entities.AUTO_ENTITIES')
  @patch('pyscript.auto_entities.state_trigger')
  @patch('pyscript.auto_entities.event_trigger')
  def test_timeout_factory(self, mock_event_trigger, mock_state_trigger, mock_auto_entities):
    from pyscript.auto_entities import timeout_factory
    mock_auto_entities.return_value = {
      'switch.test': {
        'default': 'off',
        'delay': 300
      }
    }
    mock_state_trigger.return_value = lambda x: x
    mock_event_trigger.return_value = lambda x: x
    pyscript.state.get.side_effect = ['on', 'on', 'off']
    timeout_factory('switch.test', 'off', 300)
    self.assertEqual(mock_state_trigger.call_count, 2)
    self.assertEqual(mock_event_trigger.call_count, 1)
    start_timer = mock_state_trigger.return_value
    start_timer()
    pyscript.timer.start.assert_called_once_with(entity_id='timer.test', duration=300)
    timer_stop = mock_event_trigger.return_value
    timer_stop()
    pyscript.service.call.assert_called_once_with('homeassistant', 'turn_off', entity_id='switch.test')
    timer_reset = mock_state_trigger.return_value
    timer_reset()
    pyscript.timer.cancel.assert_called_once_with(entity_id='timer.test')

  @patch('pyscript.auto_entities.AUTO_ENTITIES')
  @patch('pyscript.auto_entities.state_trigger')
  @patch('pyscript.auto_entities.time_trigger')
  @patch('pyscript.auto_entities.event_trigger')
  def test_timeout_factory_system_events(self, mock_event_trigger, mock_time_trigger, mock_state_trigger, mock_auto_entities):
    from pyscript.auto_entities import timeout_factory
    mock_auto_entities.return_value = {
      'switch.test': {
        'default': 'off',
        'delay': 300
      }
    }
    mock_state_trigger.return_value = lambda x: x
    mock_time_trigger.return_value = lambda x: x
    mock_event_trigger.return_value = lambda x: x
    timeout_factory('switch.test', 'off', 300)
    self.assertEqual(mock_time_trigger.call_count, 2)
    self.assertEqual(mock_event_trigger.call_count, 2)
    timer_init = mock_time_trigger.return_value
    timer_init()
    pyscript.state.persist.assert_called_once_with('pyscript.timer_test', 'idle')
    timer_restore = mock_event_trigger.return_value
    timer_restore()
    pyscript.state.set.assert_called_once_with('pyscript.timer_test', '')
    timer_persist = mock_time_trigger.return_value
    timer_persist()
    pyscript.timer.pause.assert_called_once_with(entity_id='timer.test')

if __name__ == '__main__':
  unittest.main()