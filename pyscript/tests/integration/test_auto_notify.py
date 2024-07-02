import unittest
from unittest.mock import patch, MagicMock

from tests.mocks.mock_trigger import MockTrigger


class TestAutoNotify(unittest.TestCase):
  def setUp(self):
    self.mock_pyscript = MagicMock()
    self.mock_trigger = MockTrigger()
    state = MagicMock()
    task = MagicMock()
    event = MagicMock()
    service = MagicMock()
    shortcut = MagicMock()

  @patch('auto_notify.EVENT_HOUSING_INITIALIZED')
  def test_init_housing_integration(self, mock_event):
    from auto_notify import init_housing
    init_housing()
    event.trigger.assert_called_once_with(mock_event)

  @patch('auto_notify.PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX', 'v_scrape_')
  @patch('auto_notify.SERVICE_SCRAPE_HOUSING_PROVIDERS')
  @patch('auto_notify.state_trigger', new=MockTrigger().state_trigger)
  def test_notify_housing_integration(self, mock_providers, mock_prefix):
    from auto_notify import notify_housing
    
    mock_providers.return_value = {
      'test_provider': {'url': 'https://test.com'}
    }

    state.names.return_value = ['v_scrape_test_provider']
    state.get.return_value = 'New apartment available'

    notify_housing()
    
    self.mock_trigger.simulate_trigger('state_trigger', 'v_scrape_test_provider', 'New apartment available')
    
    shortcut.assert_called_once_with(
      message='v_scrape_test_provider: New apartment available',
      shortcut='SC-HA-Notify-Housing',
      input='https://test.com'
    )

if __name__ == '__main__':
  unittest.main()