import unittest
from tests.mocks.mock_pyscript import MockPyscript

pyscript = MockPyscript()

class TestUtils(unittest.TestCase):
  def test_placeholder(self):
    self.assertTrue(True)
