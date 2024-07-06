import unittest
from unittest.mock import patch, MagicMock
from homeassistant.core import HomeAssistant
from custom_components.pyscript import trigger
import sys
import os

class TestScrapeHousing(unittest.TestCase):
  
  sys.path.append('/config/pyscript/tests')
  from mocks.mock_pyscript import MockPyscript
    
  @classmethod
  def setUpClass(cls):
    sys.path.append('/config/pyscript/apps')
    from scrape_housing import scrape_housing
    
    mock_pyscript = MockPyscript()
    mock_pyscript.setup_environment()

  def setUp(self):
    self.hass = HomeAssistant()
    trigger.setup(self.hass, {})

  def tearDown(self):
    self.hass.stop()

  @patch('scrape_housing.requests.get')
  @patch('scrape_housing.requests.post')
  @patch('custom_components.pyscript.pyscript_executor', return_value=MockPyscript.pyscript_executor)
  @patch('scrape_housing.pyscript.pyscript_executor', return_value=MockPyscript.pyscript_executor)
  def test_scrape_housing(self, mock_pyscript, mock_post, mock_get):
    mock_get.return_value.content = '<html><body><div class="property-container">Test Property</div></body></html>'
    mock_post.return_value.text = json.dumps({'searchresults': '<html><body><div class="property-container">Test Property</div></body></html>'})

    trigger.register_function(self.hass, scrape_housing, "scrape_housing")

    result = trigger.call_function(self.hass, "scrape_housing", "degewo")
    self.assertIn('Test Property', str(result))

    mock_pyscript.pyscript_executor.assert_called_once()

    result = trigger.call_function(self.hass, "scrape_housing", "howoge")
    self.assertIn('Test Property', str(result))

if __name__ == '__main__':
  unittest.main()