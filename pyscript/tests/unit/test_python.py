import unittest
from unittest.mock import patch, MagicMock
from mocks.mock_hass import MockHass
from mocks.mock_pyscript import MockPyscript

class TestFilesystem(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  @patch('shutil.copy2')
  def test_cp(self, mock_copy2):
    from pyscript.python.filesystem import cp
    
    cp("src.txt", "dest.txt")
    
    mock_copy2.assert_called_once_with("src.txt", "dest.txt")

class TestLogfile(unittest.TestCase):
  def setUp(self):
    self.mock_hass = MockHass()
    self.mock_pyscript = MockPyscript()

  @patch('pyscript.python.logfile.logging')
  def test_logfile_initialization(self, mock_logging):
    from pyscript.python.logfile import Logfile
    
    log = Logfile(ctx="test_context")
    
    self.assertIsNotNone(log._logger)
    self.assertEqual(log.name, "test_context")
    self.assertEqual(len(log.history), 0)

  @patch('pyscript.python.logfile.logging')
  def test_logfile_log_method(self, mock_logging):
    from pyscript.python.logfile import Logfile
    
    log = Logfile(ctx="test_context")
    test_message = "Test log message"
    log.log(test_message)
    
    self.assertEqual(len(log.history), 1)
    self.assertEqual(log.history[0], test_message)

if __name__ == '__main__':
  unittest.main()