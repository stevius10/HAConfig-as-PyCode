import unittest
from unittest.mock import patch, MagicMock
import pyscript
from pyscript import state, task, event, service

class TestAutoMotion(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()

  @patch('pyscript.auto_motion.AUTO_MOTION_ENTITIES')
  def test_on_motion_factory_integration(self, mock_auto_motion_entities):
    from pyscript.auto_motion import on_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'on': 'scene.test_on',
        'sun_diff': 30
      }
    }
    on_motion_factory('binary_sensor.test_motion')
    pyscript.state.trigger.assert_called_once()
    pyscript.time_active.assert_called_once()

  @patch('pyscript.auto_motion.AUTO_MOTION_ENTITIES')
  def test_off_motion_factory_integration(self, mock_auto_motion_entities):
    from pyscript.auto_motion import off_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'off': 'scene.test_off',
        'transition': 20
      }
    }
    off_motion_factory('binary_sensor.test_motion')
    pyscript.state.trigger.assert_called_once()
    pyscript.scene.turn_on.assert_not_called()

  @patch('pyscript.auto_motion.AUTO_MOTION_ENTITIES')
  @patch('pyscript.auto_motion.sun')
  def test_on_motion_factory_with_sun_condition(self, mock_sun, mock_auto_motion_entities):
    from pyscript.auto_motion import on_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'on': 'scene.test_on',
        'sun_diff': 30
      }
    }
    mock_sun.elevation = 20
    on_motion_factory('binary_sensor.test_motion')()
    pyscript.scene.turn_on.assert_called_once_with(entity_id='scene.test_on')

  @patch('pyscript.auto_motion.AUTO_MOTION_ENTITIES')
  def test_off_motion_factory_with_transition(self, mock_auto_motion_entities):
    from pyscript.auto_motion import off_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'off': 'scene.test_off',
        'transition': 20
      }
    }
    off_motion_factory('binary_sensor.test_motion')()
    pyscript.task.sleep.assert_called_once_with(20)
    pyscript.scene.turn_on.assert_called_once_with(entity_id='scene.test_off')

  @patch('pyscript.auto_motion.AUTO_MOTION_ENTITIES')
  def test_on_motion_factory_without_sun_diff(self, mock_auto_motion_entities):
    from pyscript.auto_motion import on_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'on': 'scene.test_on'
      }
    }
    on_motion_factory('binary_sensor.test_motion')()
    pyscript.scene.turn_on.assert_called_once_with(entity_id='scene.test_on')

  @patch('pyscript.auto_motion.AUTO_MOTION_ENTITIES')
  def test_off_motion_factory_without_transition(self, mock_auto_motion_entities):
    from pyscript.auto_motion import off_motion_factory
    mock_auto_motion_entities.return_value = {
      'binary_sensor.test_motion': {
        'off': 'scene.test_off'
      }
    }
    off_motion_factory('binary_sensor.test_motion')()
    pyscript.scene.turn_on.assert_called_once_with(entity_id='scene.test_off')

if __name__ == '__main__':
  unittest.main()