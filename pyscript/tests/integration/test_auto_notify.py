import unittest
from unittest.mock import patch, MagicMock
import pyscript
from pyscript import state, task, event, service

class TestAutoNotify(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    pyscript.state = MagicMock()
    pyscript.task = MagicMock()
    pyscript.event = MagicMock()
    pyscript.service = MagicMock()

  @patch('pyscript.auto_notify.EVENT_HOUSING_INITIALIZED')
  def test_init_housing_integration(self, mock_event):
    from pyscript.auto_notify import init_housing
    init_housing()
    pyscript.event.trigger.assert_called_once_with(mock_event)

  @patch('pyscript.auto_notify.PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX')
  @patch('pyscript.auto_notify.notify_housing')
  def test_notify_housing_integration(self, mock_notify_housing, mock_prefix):
    from pyscript.auto_notify import notify_housing
    mock_prefix.return_value = 'v_scrape_'
    pyscript.state.names.return_value = ['v_scrape_test']
    notify_housing('test_target', True, 'v_scrape_test', 'new_value', 'old_value')
    pyscript.shortcut.assert_called_once()

if __name__ == '__main__':
  unittest.main()