import shutil
import os


def write(source, destination):
  if os.path.exists(destination):
    os.remove(destination)
  shutil.copy(source, destination)