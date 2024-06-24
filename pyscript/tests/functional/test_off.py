import unittest
from unittest.mock import patch, MagicMock
import pyscript
from pyscript import state, task, event, service

class TestOffScript(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()

  @patch('pyscript.scripts.script_off.ENTITIES_AIR', new_callable=PropertyMock)
  @patch('pyscript.scripts.script_off.ENTITIES_HEATING', new_callable=PropertyMock)
  @patch('pyscript.scripts.script_off.ENTITIES_MEDIA', new_callable=PropertyMock)
  @patch('pyscript.scripts.script_off.ENTITIES_LIGHT', new_callable=PropertyMock)
  @patch('pyscript.scripts.script_off.ENTITIES_SWITCHES', new_callable=PropertyMock)
  @patch('pyscript.scripts.script_off.ENTITIES_TV', new_callable=PropertyMock)
  def test_script_off(self, mock_tv, mock_switches, mock_light, mock_media, mock_heating, mock_air):
    from pyscript.scripts.script_off import script_off
    mock_air.return_value = ["fan.test_air"]
    mock_heating.return_value = ["climate.test_heating"]
    mock_media.return_value = ["media_player.test_media"]
    mock_light.return_value = ["light.test_light"]
    mock_switches.return_value = ["switch.test_switch"]
    mock_tv.return_value = ["media_player.test_tv"]
    script_off()
    pyscript.turn_off.assert_called()
    pyscript.climate.turn_off.assert_called_once()
    pyscript.scene.turn_off.assert_called()

  @patch('pyscript.scripts.script_off.ENTITIES_AIR', new_callable=PropertyMock)
  def test_script_off_air(self, mock_air):
    from pyscript.scripts.script_off import script_off_air
    mock_air.return_value = ["fan.test_air"]
    script_off_air()
    pyscript.turn_off.assert_called_once_with(entity="fan.test_air")

  @patch('pyscript.scripts.script_off.ENTITIES_HEATING', new_callable=PropertyMock)
  def test_script_off_heating(self, mock_heating):
    from pyscript.scripts.script_off import script_off_heating
    mock_heating.return_value = ["climate.test_heating"]
    script_off_heating()
    pyscript.climate.turn_off.assert_called_once_with(entity_id="climate.test_heating")

  @patch('pyscript.scripts.script_off.ENTITIES_LIGHT', new_callable=PropertyMock)
  def test_script_off_lights(self, mock_light):
    from pyscript.scripts.script_off import script_off_lights
    mock_light.return_value = ["light.test_light"]
    script_off_lights()
    pyscript.scene.turn_off.assert_called()

if __name__ == '__main__':
  unittest.main()