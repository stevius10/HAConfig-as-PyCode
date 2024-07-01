import unittest
from unittest.mock import patch, MagicMock, PropertyMock

class TestAirControl(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    state = MagicMock()
    task = MagicMock()
    event = MagicMock()
    service = MagicMock()
    self.entities = {
      "wz_luft": {
        "fan": "fan.wz_luft",
        "sensor": "sensor.wz_luft",
        "luftung": "switch.wz_luftung",
      },
      "sz_luft": {
        "fan": "fan.sz_luft",
        "sensor": "sensor.sz_luft",
        "luftung": "switch.sz_luftung",
      }
    }

  @patch('air_control.AIR_CONTROL_ENTITIES', new_callable=PropertyMock)
  def test_threshold_on(self, mock_entities):
    from air_control import threshold_on
    mock_entities.return_value = self.entities
    state.get.return_value = "20"
    threshold_on(var_name="sensor.wz_luft", value="20")
    fan.set_percentage.assert_called_once()
    task.sleep.assert_called_once()

  @patch('air_control.AIR_CONTROL_ENTITIES', new_callable=PropertyMock)
  def test_threshold_off(self, mock_entities):
    from air_control import threshold_off
    mock_entities.return_value = self.entities
    state.get.return_value = "5"
    threshold_off(var_name="sensor.wz_luft", value="5")
    fan.turn_off.assert_called_once()
    task.sleep.assert_called_once()

  @patch('air_control.AIR_CONTROL_ENTITIES', new_callable=PropertyMock)
  def test_clean(self, mock_entities):
    from air_control import clean
    mock_entities.return_value = self.entities
    clean(entity=["fan.wz_luft", "fan.sz_luft"])
    fan.turn_on.assert_called()
    task.sleep.assert_called_once()
    fan.set_percentage.assert_called()

  @patch('air_control.AIR_CONTROL_ENTITIES', new_callable=PropertyMock)
  def test_sleep(self, mock_entities):
    from air_control import sleep
    mock_entities.return_value = self.entities
    state.get.return_value = "on"
    sleep(entity=["fan.wz_luft", "fan.sz_luft"])
    fan.turn_off.assert_called_once()
    task.sleep.assert_called_once()

if __name__ == '__main__':
  unittest.main()