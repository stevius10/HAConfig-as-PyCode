from unittest.mock import MagicMock

class MockTask:
  def __init__(self):
    self.create = MagicMock()
    self.cancel = MagicMock()
    self.current_task = MagicMock()
    self.name2id = MagicMock()
    self.wait = MagicMock()
    self.add_done_callback = MagicMock()
    self.remove_done_callback = MagicMock()
    self.executor = MagicMock()
    self.sleep = MagicMock()
    self.unique = MagicMock()
    self.wait_until = MagicMock()
