import unittest
from unittest.mock import patch, MagicMock
from mocks.mock_hass import MockHass
from mocks.mock_pyscript import MockPyscript

import unittest
from unittest.mock import patch, MagicMock
from mocks.mock_hass import MockHass
from mocks.mock_pyscript import MockPyscript

class TestScrape(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  def test_filter(self):
    from apps.scrape import filter
    valid_apartment = {
      "address": "Test Street 1",
      "rent": "500",
      "size": "50",
      "rooms": "2"
    }
    self.assertIsNotNone(filter(valid_apartment))
    invalid_apartment = {
      "address": None,
      "rent": "1000",
      "size": "100",
      "rooms": "3"
    }
    self.assertIsNone(filter(invalid_apartment))

  @patch('apps.scrape.requests.get')
  def test_scrape(self, mock_get):
    from apps.scrape import scrape
    mock_response = MagicMock()
    mock_response.content = "Mocked content"
    mock_get.return_value = mock_response
    result = scrape()
    self.assertIsNotNone(result)

  def test_scrape_housing(self):
    from apps.scrape import scrape_housing
    
    self.mock_pyscript.state.get.return_value = "<html></html>"
    
    scrape_housing("test_provider")
    
    self.mock_pyscript.state.set.assert_called_once()
    self.mock_pyscript.state.persist.assert_called_once()

class TestServices(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  def test_services_auto_factory(self):
    from apps.services import services_auto_factory
    
    services_auto_factory("test.service", "* * * * *")
    
    self.mock_pyscript.time_trigger.assert_called_once_with("* * * * *")
    self.mock_pyscript.service.call.assert_called_once_with("test", "service")

class TestSyncGit(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  @patch('apps.sync_git.subprocess.run')
  def test_git_sync(self, mock_run):
    from apps.sync_git import git_sync
    
    mock_run.return_value = MagicMock(stdout="Test output", stderr="")
    
    result = git_sync("test_ctx", "/config", "/key", "main", "Test commit")
    
    self.assertIn("Test output", result["logs"])
    mock_run.assert_called()

if __name__ == '__main__':
  unittest.main()