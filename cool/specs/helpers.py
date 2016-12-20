# But here any common used things for testing to reuse.
from os import unlink
from tempfile import NamedTemporaryFile


class TmpFile:
  def __init__(self, txt):
    self.tmp = NamedTemporaryFile('w', encoding='utf-8', delete=False)
    self.tmp.write(txt)
    self.tmp.close()

  def __enter__(self):
    return self.tmp

  def __exit__(self, *args, **kwargs):
    unlink(self.tmp.name)
