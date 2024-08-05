from enum import Enum, auto

from constants.mappings import MAP_RESULT_STATUS, MAP_RESULT_REASON

# Enumerations

RESULT_STATUS = Enum('RESULT_STATUS', {name: name.lower() for name in MAP_RESULT_STATUS})
RESULT_REASON = Enum('RESULT_REASON', {name: name.lower() for name in MAP_RESULT_REASON})

# Exceptions

class ForwardException(Exception):
  def __init__(self, exception, context):
    self.exception = exception
    self.context = context
    super(ForwardException, self).__init__(f"[{self.context}] {type(self.exception)}: {self.exception}")

class IORetriesExceededException(Exception):
  def __init__(self, exception):
    self.exception = exception
    super(IORetriesExceededException, self).__init__(str(self.exception))

# Helper


