class ForwardException(Exception):
  def __init__(self, exception, context):
    self.exception = exception
    self.context = context
    super(ForwardException, self).__init__(f"[{self.context}] {type(self.exception)}: {self.exception}")

class IORetriesExceededException(Exception):
  def __init__(self, exception):
    self.exception = exception
    super(IORetriesExceededException, self).__init__(str(self.exception))