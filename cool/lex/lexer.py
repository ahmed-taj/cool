from cool.util.io_base import BufferManager
from .tokens import Token, Type


class Lexer:
  def __init__(self, mgr: BufferManager):
    self.mgr = mgr

  def tokens(self):
    while True:
      tok = self._next()
      yield tok
      # break if we hit EOF
      if tok.typ == Type.EOF:
        break

  def _next(self) -> Token:
    '''
    Delivers next token.
    '''
    pass

  def accept(self, valid):
    '''
    Consumes the next single char if it's in the given set `valid`.
    '''
    if self.mgr.next() in valid:
      return True
    self.mgr.backup()
    return False

  def accept_all(self, valid):
    '''
    Consumes all the next chars that are in the given set `valid`.
    '''
    while self.mgr.next() in valid:
      pass
    self.mgr.backup()

  def emit(self, t: type):
    '''
    Emit a `Token` instance of given type `t` with given context.
    '''
    val, loc = self.mgr.emit()
    return Token(t, loc, val)
