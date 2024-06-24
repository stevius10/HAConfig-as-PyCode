import unittest
from unittest.mock import patch, MagicMock
import pyscript
from pyscript import state, task, event, service

class TestAirCleaner(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()
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

  @patch('pyscript.scripts.script_air_cleaner.SCRIPT_AIR_CLEANER_ENTITIES', new_callable=PropertyMock)
  def test_script_air_cleaner_threshold_on(self, mock_entities):
    from pyscript.scripts.script_air_cleaner import script_air_cleaner_threshold_on
    mock_entities.return_value = self.entities
    pyscript.state.get.return_value = "20"
    script_air_cleaner_threshold_on(var_name="sensor.wz_luft", value="20")
    pyscript.fan.set_percentage.assert_called_once()
    pyscript.task.sleep.assert_called_once()

  @patch('pyscript.scripts.script_air_cleaner.SCRIPT_AIR_CLEANER_ENTITIES', new_callable=PropertyMock)
  def test_script_air_cleaner_threshold_off(self, mock_entities):
    from pyscript.scripts.script_air_cleaner import script_air_cleaner_threshold_off
    mock_entities.return_value = self.entities
    pyscript.state.get.return_value = "5"
    script_air_cleaner_threshold_off(var_name="sensor.wz_luft", value="5")
    pyscript.fan.turn_off.assert_called_once()
    pyscript.task.sleep.assert_called_once()

  @patch('pyscript.scripts.script_air_cleaner.SCRIPT_AIR_CLEANER_ENTITIES', new_callable=PropertyMock)
  def test_script_air_cleaner_clean(self, mock_entities):
    from pyscript.scripts.script_air_cleaner import script_air_cleaner_clean
    mock_entities.return_value = self.entities
    script_air_cleaner_clean(entity=["fan.wz_luft", "fan.sz_luft"])
    pyscript.fan.turn_on.assert_called()
    pyscript.task.sleep.assert_called_once()
    pyscript.fan.set_percentage.assert_called()

  @patch('pyscript.scripts.script_air_cleaner.SCRIPT_AIR_CLEANER_ENTITIES', new_callable=PropertyMock)
  def test_script_air_cleaner_sleep(self, mock_entities):
    from pyscript.scripts.script_air_cleaner import script_air_cleaner_sleep
    mock_entities.return_value = self.entities
    pyscript.state.get.return_value = "on"
    script_air_cleaner_sleep(entity=["fan.wz_luft", "fan.sz_luft"])
    pyscript.fan.turn_off.assert_called_once()
    pyscript.task.sleep.assert_called_once()

if __name__ == '__main__':
  unittest.main()