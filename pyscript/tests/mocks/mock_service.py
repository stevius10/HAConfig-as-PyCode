from unittest.mock import MagicMock

class MockService:
  def __init__(self):
    self.call = MagicMock()
    self.has_service = MagicMock()
