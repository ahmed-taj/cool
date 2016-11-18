from .io_base import BufferManager, ENCODING


class StringBuffer(BufferManager):
  def _prepare_buffer(self):
    # Anything need to be done before start reading from this buffer
    pass

  def __getitem__(self, key) -> str:
    '''
    Get the character at the given `key` (i.e. index or slice).
    It should return empty string if EOF is reached.

    :param key: specify the key of char in the buffer.
    :rtype: string of a single char.
    :param etype: KeyError
    '''
    try:
      return self._buffer[key]
    except IndexError:
      raise IndexError("Buffer doesn't have data at '{}'", key)

  def get_line(self, lineno: int) -> str:
    '''
    Get a line at the given `lineno`. It should return empty
    string if invalid `lineno` was given.

    :param lineno: the target line number.
    :rtype: target line's content as string or ''
    '''
    try:
      return self._buffer.splitlines()[lineno - 1]
    except IndexError:
      return ''

  def _get_length(self) -> int:
    '''
    Get the length of this buffer
    '''
    return len(self._buffer)

  def _get_name(self) -> str:
    '''
    Get humans readable name for this buffer
    '''
    return "stdin"

  def __enter__(self):
    '''
    Serves as entry point when using with-statement.
    '''
    return self

  def __exit__(self, type, val, traceback):
    '''
    Serves as exit point when using with-statement.
    '''
    pass
