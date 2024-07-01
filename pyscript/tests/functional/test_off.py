import unittest
from unittest.mock import patch, MagicMock, PropertyMock

class TestOff(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    state = MagicMock()
    task = MagicMock()
    event = MagicMock()
    service = MagicMock()

  @patch('ha_off.ENTITIES_AIR', new_callable=PropertyMock)
  @patch('ha_off.ENTITIES_HEATING', new_callable=PropertyMock)
  @patch('ha_off.ENTITIES_MEDIA', new_callable=PropertyMock)
  @patch('ha_off.ENTITIES_LIGHT', new_callable=PropertyMock)
  @patch('ha_off.ENTITIES_SWITCHES', new_callable=PropertyMock)
  @patch('ha_off.ENTITIES_TV', new_callable=PropertyMock)
  def test_ha_off(self, mock_tv, mock_switches, mock_light, mock_media, mock_heating, mock_air):
    from ha_off import turnoff
    mock_air.return_value = ["fan.test_air"]
    mock_heating.return_value = ["climate.test_heating"]
    mock_media.return_value = ["media_player.test_media"]
    mock_light.return_value = ["light.test_light"]
    mock_switches.return_value = ["switch.test_switch"]
    mock_tv.return_value = ["media_player.test_tv"]
    turnoff()
    turn_off.assert_called()
    climate.turn_off.assert_called_once()
    scene.turn_off.assert_called()

  @patch('ha_off.ENTITIES_AIR', new_callable=PropertyMock)
  def test_turnoff_air(self, mock_air):
    from ha_off import turnoff_air
    mock_air.return_value = ["fan.test_air"]
    turnoff_air()
    turn_off.assert_called_once_with(entity="fan.test_air")

  @patch('ha_off.ENTITIES_HEATING', new_callable=PropertyMock)
  def test_turnoff_heating(self, mock_heating):
    from ha_off import turnoff_heating
    mock_heating.return_value = ["climate.test_heating"]
    turnoff_heating()
    climate.turn_off.assert_called_once_with(entity_id="climate.test_heating")

  @patch('ha_off.ENTITIES_LIGHT', new_callable=PropertyMock)
  def test_turnoff_lights(self, mock_light):
    from ha_off import turnoff_lights
    mock_light.return_value = ["light.test_light"]
    turnoff_lights()
    scene.turn_off.assert_called()

if __name__ == '__main__':
  unittest.main()