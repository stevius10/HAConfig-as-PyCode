from unittest.mock import MagicMock

class MockLog:
  def __init__(self):
    self.debug = MagicMock()
    self.info = MagicMock()
    self.warning = MagicMock()
    self.error = MagicMock()
    self.print = MagicMock()
