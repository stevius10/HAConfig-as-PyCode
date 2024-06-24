import unittest
from unittest.mock import patch, MagicMock
from mocks.mock_hass import MockHass
from mocks.mock_pyscript import MockPyscript

class TestHaHelper(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()
    
  @patch('pyscript.scripts.ha_helper.aiofiles.open')
  @patch('pyscript.scripts.ha_helper.log')
  async def test_log_truncate(self, mock_log, mock_open):
    from pyscript.scripts.ha_helper import log_truncate
    
    mock_file = MagicMock()
    mock_file.__aenter__.return_value.readlines.return_value = ["log1\n", "log2\n", "log3\n"]
    mock_open.return_value = mock_file
    
    await log_truncate(logfile="/test/log.txt", size_log_entries=2, size_log_tail=1)
    
    mock_open.assert_called()
    mock_file.__aenter__.return_value.writelines.assert_called()
    mock_log.assert_not_called()

class TestHaSystem(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()
    
  @patch('pyscript.scripts.ha_system.sys.path')
  @patch('pyscript.scripts.ha_system.task.sleep')
  def test_event_system_started(self, mock_sleep, mock_path):
    from pyscript.scripts.ha_system import event_system_started
    
    event_system_started()
    
    mock_path.append.assert_called_once()
    mock_sleep.assert_called_once()
    self.mock_pyscript.event.fire.assert_called_once()

  @patch('pyscript.scripts.ha_system.ha_setup_environment')
  @patch('pyscript.scripts.ha_system.ha_setup_files')
  @patch('pyscript.scripts.ha_system.ha_setup_links')
  @patch('pyscript.scripts.ha_system.ha_setup_logging')
  def test_ha_setup(self, mock_logging, mock_links, mock_files, mock_env):
    from pyscript.scripts.ha_system import ha_setup
    
    ha_setup()
    
    mock_env.assert_called_once()
    mock_files.assert_called_once()
    mock_links.assert_called_once()
    mock_logging.assert_called_once()

class TestHaUtils(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()
    
  def test_notify(self):
    from pyscript.scripts.ha_utils import notify
    
    notify("Test message", target="home")
    
    self.mock_pyscript.service.call.assert_called_with("notify", "mobile_app_home", message="Test message", data=None)

  def test_shortcut(self):
    from pyscript.scripts.ha_utils import shortcut
    
    shortcut("Test message", "test_shortcut", input="test_input")
    
    self.mock_pyscript.notify.assert_called_once()

if __name__ == '__main__':
  unittest.main()