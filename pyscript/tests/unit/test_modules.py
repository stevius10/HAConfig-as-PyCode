import unittest
from unittest.mock import MagicMock

from tests.mocks.mock_hass import MockHass
from tests.mocks.mock_pyscript import MockPyscript


class TestConstants(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  def test_constants_import(self):
    self.assertTrue('EXPR_TIME_DAY' in globals())
    self.assertTrue('EXPR_TIME_DAYTIME' in globals())
    self.assertTrue('EXPR_TIME_GENERAL_WORKTIME' in globals())

class TestUtils(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  def test_expr(self):
    from utils import expr
    
    result = expr("entity.state", "on", "==")
    self.assertEqual(result, "entity.state is not None and entity.state not in [\"unavailable\", \"unknown\"] and entity.state == 'on'")

  def test_logs(self):
    from utils import logs
    
    result = logs({"key1": "value1", "key2": "value2"})
    self.assertEqual(result, "key1=value1, key2=value2")

  def test_log_func_format(self):
    from utils import log_func_format
    
    mock_func = MagicMock()
    mock_func.__name__ = "test_func"
    
    result = log_func_format(mock_func, ["arg1", "arg2"], {"kwarg1": "value1"})
    self.assertEqual(result, "test_func(arg1, arg2, kwarg1=value1)")

if __name__ == '__main__':
  unittest.main()