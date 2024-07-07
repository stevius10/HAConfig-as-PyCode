from unittest.mock import MagicMock

class MockState:
  def __init__(self):
    self.get = MagicMock()
    self.set = MagicMock()
    self.delete = MagicMock()
    self.getattr = MagicMock()
    self.names = MagicMock()
    self.persist = MagicMock()
    self.setattr = MagicMock()
