import json
import unittest
from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup

from constants.mappings import *


class TestUnit(unittest.TestCase):

  def setUp(self):
    self.apartment = {
      "address": "Musterstraße 1",
      "rent": "500 €",
      "size": "50 m²",
      "rooms": "2 Zimmer",
      "details": "Schöne Wohnung",
      "text": "Schöne Wohnung in der Musterstraße 1, 500 €, 50 m², 2 Zimmer"
    }
    self.content = BeautifulSoup('<div class="item">Schöne Wohnung in der Musterstraße 1, 500 €, 50 m², 2 Zimmer</div>', 'html.parser')
    self.provider = "test_provider"
    self.housing_provider = {
      self.provider: {
        "url": "http://example.com",
        "structure": {
          "item": ".item",
          "address_selector": None,
          "rent_selector": None,
          "size_selector": None,
          "rooms_selector": None,
          "details_selector": None
        }
      }
    }

  @patch('requests.get')
  def test_fetch(self, mock_get):
    mock_response = MagicMock()
    mock_response.content = json.dumps({'searchresults': '<div class="item">Schöne Wohnung in der Musterstraße 1, 500 €, 50 m², 2 Zimmer</div>'})
    mock_get.return_value = mock_response

    with patch.dict('builtins.housing_provider', self.housing_provider):
      content = fetch(self.provider)
      self.assertIsInstance(content, BeautifulSoup)
      self.assertIn('Schöne Wohnung in der Musterstraße 1, 500 €, 50 m², 2 Zimmer', content.text)

  def test_filtering(self):
    filtered_apartment = filtering(self.apartment)
    self.assertIsNotNone(filtered_apartment)
    self.assertIn("address", filtered_apartment)
    self.assertIn("rent", filtered_apartment)

  def test_scrape(self):
    apartments = scrape(self.content, ".item", None, None, None, None, None)
    self.assertIn("Musterstraße 1 (500 €, 2 Zimmer, 50 m²)", apartments)

  @patch('random.randint', return_value=1)
  @patch('requests.get')
  @patch('state.set')
  @patch('state.persist')
  def test_scrape_housing(self, mock_persist, mock_set, mock_get, mock_randint):
    mock_response = MagicMock()
    mock_response.content = '<div class="item">Schöne Wohnung in der Musterstraße 1, 500 €, 50 m², 2 Zimmer</div>'
    mock_get.return_value = mock_response

    with patch.dict('builtins.housing_provider', self.housing_provider):
      apartments = scrape_housing(self.provider)
      self.assertIn("test_provider: Musterstraße 1 (500 €, 2 Zimmer, 50 m²)", apartments)

  def test_get_entity(self):
    entity = get_entity(self.provider)
    self.assertEqual(entity, f"pyscript.{PERSISTENCE_PREFIX_SENSOR_SCRAPE_HOUSING}_{self.provider}")

  def test_get_or_default(self):
    element = self.content.select_one('.item')
    address = get_or_default(element, None, "default_address")
    self.assertEqual(address, "default_address")

if __name__ == '__main__':
  unittest.main()