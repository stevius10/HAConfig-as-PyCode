import unittest
from unittest.mock import patch, MagicMock

from mocks.mock_trigger import MockTrigger


class TestAutoEntities(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    self.mock_trigger = MockTrigger()
    state = MagicMock()
    task = MagicMock()
    event = MagicMock()
    service = MagicMock()
    timer = MagicMock()

  @patch('auto_entities.ENTITIES_AUTO')
  def test_default_factory(self, mock_auto_entities):
    from auto_entities import default_factory
    
    mock_auto_entities.return_value = {
      'light.test': {
        'default': 'off',
        'func': 'light.turn_off'
      }
    }
    
    with patch('auto_entities.state_trigger', self.mock_trigger.state_trigger):
      default_factory('light.test', 'light.turn_off')
    
    self.assertEqual(len(self.mock_trigger.triggers), 1)
    trigger_type, func, args, kwargs = self.mock_trigger.triggers[0]
    self.assertEqual(trigger_type, 'state_trigger')
    
    func('light.test', 'on')
    
    service.call.assert_called_once_with('light', 'turn_off', entity_id='light.test')

  @patch('auto_entities.ENTITIES_AUTO')
  def test_timeout_factory(self, mock_auto_entities):
    from auto_entities import timeout_factory
    
    mock_auto_entities.return_value = {
      'switch.test': {
        'default': 'off',
        'delay': 300
      }
    }
    
    with patch('auto_entities.state_trigger', self.mock_trigger.state_trigger), \
         patch('auto_entities.event_trigger', self.mock_trigger.event_trigger):
      timeout_factory('switch.test', 'off', 300)
    
    self.assertEqual(len(self.mock_trigger.triggers), 3)
    
    for trigger_type, func, args, kwargs in self.mock_trigger.triggers:
      if trigger_type == 'state_trigger' and 'to' in kwargs and kwargs['to'] == 'on':
        func('switch.test', 'on')
        timer.start.assert_called_once_with(entity_id='timer.test', duration=300)
      elif trigger_type == 'event_trigger' and args[0] == 'timer.finished':
        func({'entity_id': 'timer.test'})
        service.call.assert_called_once_with('homeassistant', 'turn_off', entity_id='switch.test')
      elif trigger_type == 'state_trigger' and 'to' in kwargs and kwargs['to'] == 'off':
        func('switch.test', 'off')
        timer.cancel.assert_called_once_with(entity_id='timer.test')

  @patch('auto_entities.ENTITIES_AUTO')
  def test_timeout_factory_system_events(self, mock_auto_entities):
    from auto_entities import timeout_factory
    
    mock_auto_entities.return_value = {
      'switch.test': {
        'default': 'off',
        'delay': 300
      }
    }
    
    with patch('auto_entities.state_trigger', self.mock_trigger.state_trigger), \
         patch('auto_entities.time_trigger', self.mock_trigger.time_trigger), \
         patch('auto_entities.event_trigger', self.mock_trigger.event_trigger):
      timeout_factory('switch.test', 'off', 300)
    
    self.assertEqual(len(self.mock_trigger.triggers), 5)
    
    for trigger_type, func, args, kwargs in self.mock_trigger.triggers:
      if trigger_type == 'time_trigger' and 'startup' in kwargs:
        func()
        state.persist.assert_called_once_with('timer_test', 'idle')
      elif trigger_type == 'event_trigger' and args[0] == 'startup':
        func()
        state.set.assert_called_once_with('timer_test', '')
      elif trigger_type == 'time_trigger' and 'shutdown' in kwargs:
        func()
        timer.pause.assert_called_once_with(entity_id='timer.test')

if __name__ == '__main__':
  unittest.main()