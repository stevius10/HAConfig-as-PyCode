import unittest
from unittest.mock import patch, MagicMock

from mocks.mock_trigger import MockTrigger


class TestAutoMotion(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    self.mock_trigger = MockTrigger()
    state = MagicMock()
    task = MagicMock()
    event = MagicMock()
    service = MagicMock()
    time_active = MagicMock()
    scene = MagicMock()

  @patch('auto_motion.ENTITIES_MOTION')
  def test_on_motion_factory_integration(self, mock_auto_motion_entities):
    from auto_motion import on_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'on': 'scene.test_on',
        'sun_diff': 30
      }
    }
    with patch('auto_motion.state_trigger', self.mock_trigger.state_trigger):
      with patch('auto_motion.time_active', self.mock_trigger.time_active):
        on_motion_factory('binary_sensor.test_motion')
        self.assertEqual(len(self.mock_trigger.triggers), 2)
        self.assertEqual(self.mock_trigger.triggers[0][0], 'state_trigger')
        self.assertEqual(self.mock_trigger.triggers[1][0], 'time_active')

  @patch('auto_motion.ENTITIES_MOTION')
  def test_off_motion_factory_integration(self, mock_auto_motion_entities):
    from auto_motion import off_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'off': 'scene.test_off',
        'transition': 20
      }
    }
    with patch('auto_motion.state_trigger', self.mock_trigger.state_trigger):
      off_motion_factory('binary_sensor.test_motion')
      self.assertEqual(len(self.mock_trigger.triggers), 1)
      self.assertEqual(self.mock_trigger.triggers[0][0], 'state_trigger')
      scene.turn_on.assert_not_called()

  @patch('auto_motion.ENTITIES_MOTION')
  @patch('auto_motion.sun')
  def test_on_motion_factory_with_sun_condition(self, mock_sun, mock_auto_motion_entities):
    from auto_motion import on_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'on': 'scene.test_on',
        'sun_diff': 30
      }
    }
    mock_sun.elevation = 20
    with patch('auto_motion.state_trigger', self.mock_trigger.state_trigger):
      on_motion_factory('binary_sensor.test_motion')
      self.mock_trigger.simulate_trigger('state_trigger', 'binary_sensor.test_motion', 'on')
      scene.turn_on.assert_called_once_with(entity_id='scene.test_on')

  @patch('auto_motion.ENTITIES_MOTION')
  def test_off_motion_factory_with_transition(self, mock_auto_motion_entities):
    from auto_motion import off_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'off': 'scene.test_off',
        'transition': 20
      }
    }
    with patch('auto_motion.state_trigger', self.mock_trigger.state_trigger):
      off_motion_factory('binary_sensor.test_motion')
      self.mock_trigger.simulate_trigger('state_trigger', 'binary_sensor.test_motion', 'off')
      task.air_control_sleep.assert_called_once_with(20)
      scene.turn_on.assert_called_once_with(entity_id='scene.test_off')

  @patch('auto_motion.ENTITIES_MOTION')
  def test_on_motion_factory_without_sun_diff(self, mock_auto_motion_entities):
    from auto_motion import on_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'on': 'scene.test_on'
      }
    }
    with patch('auto_motion.state_trigger', self.mock_trigger.state_trigger):
      on_motion_factory('binary_sensor.test_motion')
      self.mock_trigger.simulate_trigger('state_trigger', 'binary_sensor.test_motion', 'on')
      scene.turn_on.assert_called_once_with(entity_id='scene.test_on')

  @patch('auto_motion.ENTITIES_MOTION')
  def test_off_motion_factory_without_transition(self, mock_auto_motion_entities):
    from auto_motion import off_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'off': 'scene.test_off'
      }
    }
    with patch('auto_motion.state_trigger', self.mock_trigger.state_trigger):
      off_motion_factory('binary_sensor.test_motion')
      self.mock_trigger.simulate_trigger('state_trigger', 'binary_sensor.test_motion', 'off')
      scene.turn_on.assert_called_once_with(entity_id='scene.test_off')

if __name__ == '__main__':
  unittest.main()
