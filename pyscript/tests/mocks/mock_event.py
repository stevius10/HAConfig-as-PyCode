from unittest.mock import MagicMock

class MockEvent:
  def __init__(self):
    self.fire = MagicMock()
