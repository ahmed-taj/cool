from .str_buffer import StringBuffer, ENCODING


class FileBuffer(StringBuffer):
  def _prepare_buffer(self):
    # Anything need to be done before start reading from this buffer
    f = open(self._buffer, "r", encoding=ENCODING)
    self.__name = f.name
    # Yes, I know this is a catastrophe
    self._buffer = f.read()
    f.close()

  def _get_name(self) -> str:
    '''
    Get humans readable name of this buffer
    '''
    return self.__name
