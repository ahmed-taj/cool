from abc import ABCMeta, abstractmethod
from typing import Tuple

ENCODING = 'UTF-8-sig'


class Location:
  """
  Used to store source buffer position information such as line number,
  file name, and column number.
  """

  def __init__(self, buffer, line, col):
    self.buffer = buffer
    self.line = line
    self.col = col

  def __str__(self):
    return "<{}> ({}:{})".format(self.buffer, self.line, self.col)


class BufferManager(metaclass=ABCMeta):
  """
  Provides an abstract managing to the source buffer, it's the base class of
  FileManager, StringManager, ..etc
  """

  def __init__(self, buffer):
    self._buffer = buffer
    # Start position since the last `emit` call
    # default line, and columns numbers
    self.start = 0
    self.start_ln = 1
    self.start_col = 1

    # The current position
    self.pos = 0

    # Width of the char
    # Currently just for readability
    self.width = 1

    # Do we need to do anything before getting started!
    self._prepare_buffer()

    # How many chars do we have to read
    self.length = self._get_length()

    # Attributes needed to calculate location
    self._line = 1
    self._col = 1
    self._lines_widths = {}

  def next(self):
    # Check if we reached the end
    if self.pos >= self.length:
      self.width = 0
      return ''  # blank str indicates EOF

    # Consume the next available encoded
    ch = self[self.pos]

    # Calculate location
    self._calc_loc(ch)

    self.pos += self.width
    return ch

  def peek(self) -> str:
    c = self.next()
    self.backup()
    return c

  def backup(self):
    self.pos -= self.width

    # restore location
    if self._col > 1:
      self._col -= 1
    else:
      self._line -= 1
      self._col = self._lines_widths[self._line]

  def ignore(self):
    '''
    Skips the current part of the buffer.
    '''
    self.start = self.pos
    self.start_ln = self._line
    self.start_col = self._col

  def emit(self) -> Tuple[str, Location]:
    '''
    Emits the current scanned part of the buffer and it's start Location
    '''
    # get current scanned buffer
    buf = self[self.start:self.pos]
    loc = self._get_loc()

    # skip it
    self.ignore()

    return buf, loc

  def get_text(self) -> str:
    '''
    Returns the current scanned text of the buffer.
    '''
    return self[self.start:self.pos]

  def _calc_loc(self, ch: str):
    # We hit end of line?
    if ch == '\n':
      # store matrix info (line number, width)
      self._lines_widths[self._line] = self._col

      # advance the location
      self._line += 1
      self._col = 1

    else:
      self._col += 1

  def _get_loc(self) -> Location:
    # Get the location of `self.start`
    return Location(self._get_name(), self.start_ln, self.start_col)

  @abstractmethod
  def _prepare_buffer(self):
    # Anything need to be done before start reading from this buffer
    # i.e. open the file
    raise NotImplementedError

  @abstractmethod
  def __getitem__(self, key) -> str:
    '''
    Gets the character at the given `key` (i.e. index or slice).
    It should return empty string if EOF is reached.

    :param key: specify the key of char in the buffer.
    :rtype: string of a single char.
    :param etype: KeyError
    '''
    raise NotImplementedError

  @abstractmethod
  def get_line(self, lineno: int) -> str:
    '''
    Gets a line at the given `lineno`. It should return empty
    string if invalid `lineno` was given.

    :param lineno: the target line number.
    :rtype: target line's content as string or ''
    '''
    raise NotImplementedError

  @abstractmethod
  def _get_length(self) -> int:
    '''
    Gets the length of this buffer
    '''
    raise NotImplementedError

  @abstractmethod
  def _get_name(self) -> str:
    '''
    Gets humans readable name for this buffer
    '''
    raise NotImplementedError

  def __enter__(self):
    '''
    Serves as entry point when using with-statement.
    '''
    raise NotImplementedError

  def __exit__(self, type, val, traceback):
    '''
    Serves as exit point when using with-statement.
    '''
    raise NotImplementedError
