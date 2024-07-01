from tests.mocks.mock_decorator import MockDecorator
from tests.mocks.mock_hass import MockHass
from tests.mocks.mock_pyscript import MockPyscript
from tests.mocks.mock_trigger import MockTrigger

import unittest
from unittest.mock import patch, MagicMock

class TestHaSystem(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()
    
  @patch('ha_system.sys.path')
  @patch('ha_system.task.sleep')
  def test_event_system_started(self, mock_sleep, mock_path):
    from ha_system import event_system_started
    
    event_system_started()
    
    mock_path.append.assert_called_once()
    mock_sleep.assert_called_once()
    self.mock_event.fire.assert_called_once()

  @patch('ha_system.ha_setup_environment')
  @patch('ha_system.ha_setup_files')
  @patch('ha_system.ha_setup_links')
  @patch('ha_system.ha_setup_logging')
  def test_ha_setup(self, mock_logging, mock_links, mock_files, mock_env):
    from ha_system import ha_setup
    
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
    from ha_utils import notify
    
    notify("Test message", target="home")
    
    self.mock_service.call.assert_called_with("notify", "mobile_app_home", message="Test message", data=None)

  def test_shortcut(self):
    from ha_utils import shortcut
    
    shortcut("Test message", "test_shortcut", input="test_input")
    
    self.mock_notify.assert_called_once()

if __name__ == '__main__':
  unittest.main()