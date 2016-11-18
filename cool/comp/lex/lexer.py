from comp.util.io_base import BufferManager
from .tokens import Token, Type
import comp.util._is as _is


class Lexer:
  def __init__(self, mgr: BufferManager):
    self.mgr = mgr

  def tokens(self):
    '''
    Returns a generator to all tokens.
    '''
    while True:
      tok = self.next_token()
      yield tok
      # break if we hit EOF
      if tok.typ == Type.EOF:
        break

  def next_token(self) -> Token:
    '''
    Delivers next token.
    '''
    # Read the next ch
    ch = self.mgr.next()

    # Is EOF ?
    if not ch:
      return self.emit(Type.EOF)

    # Is New line ?
    if '\n' == ch:
      return self.emit(Type.NEWLINE)

    # Is Identifier or keyword ?
    if _is.ident_start(ch):
      self.mgr.backup()  # first letter
      return self.lex_identifiers()

    # '+' or '-' ?
    if '+' == ch:
      # Maybe Number ?
      if _is.digit(self.mgr.peek()):
        self.mgr.backup()  # '+'
        return self.lex_numbers()
      return self.emit(Type.ADD)

    if '-' == ch:
      # Maybe Number ?
      if _is.digit(self.mgr.peek()):
        self.mgr.backup()  # '-'
        return self.lex_numbers()
      return self.emit(Type.SUB)

    # Number ?
    if _is.digit(ch):
      self.mgr.backup()  # first number
      return self.lex_numbers()

    # '*' or '/' or '%' ?
    if '*' == ch:
      return self.emit(Type.MUL)
    if '/' == ch:
      return self.emit(Type.DIV)
    if '%' == ch:
      return self.emit(Type.MOD)

    # Is '{' or '}' ?
    if '{' == ch:
      return self.emit(Type.L_BRACE)
    if '}' == ch:
      return self.emit(Type.R_BRACE)

    # Is '[' or ']' ?
    if '[' == ch:
      return self.emit(Type.L_BRACK)
    if ']' == ch:
      return self.emit(Type.R_BRACK)

    # Is '(' or ')' ?
    if '(' == ch:
      return self.emit(Type.L_PAREN)
    if ')' == ch:
      return self.emit(Type.R_PAREN)

    # Is '.' or ',' ?
    if '.' == ch:
      return self.emit(Type.DOT)
    if ',' == ch:
      return self.emit(Type.COMMA)

    # Not something we know right now!
    return self.emit(Type.ERROR)

  #--------------------------------------------------------------------
  # Lexers
  #--------------------------------------------------------------------

  def lex_identifiers(self):
    '''
    Matches identifiers:
      - Keywords: i.e. def, end
      - Function name: i.e. even?, sort!
      - Identifier: i.e. xyz
    '''
    self.accept_all_if(_is.ident)

    # Function name ?
    if self.accept('?!'):
      return self.emit(Type.FUNC_IDENT)

    # Keyword ?
    attr = 'KW_{}'.format(self.mgr.get_text().upper())
    if hasattr(Type, attr):
      return self.emit(getattr(Type, attr))

    # Ok, normal Identifier
    return self.emit(Type.IDENT)

  def lex_numbers(self):
    '''
    Matches numbers:
      Integers(+|-):
        - Binary: i.e. 0b0012, 0B1010
        - Octal: i.e. 0o7234, 0O2322
        - Hexadecimal: 0xabc2, 0X7895
        - Decimals: i.e. 1232, 02323
      Floating-points(+|-):
        - Float: i.e. 0.23, 32e+123
    '''
    # Let's accept the sign
    self.accept('+-')

    is_float = False
    c = self.mgr.next()

    # Maybe bin, oct, or hex, or decimal
    if '0' == c:
      p = self.mgr.peek()

      # Decimal
      if _is.digit(p):
        self.accept_all_if(_is.digit)

      # Binary
      elif self.accept(_is.BIN_CHARS):
        self.accept_all_if(_is.bin_digit)
        return self.emit(Type.INTEGER)

      # Octal
      elif self.accept(_is.OCT_CHARS):
        self.accept_all_if(_is.oct_digit)
        return self.emit(Type.INTEGER)

      # Hexadecimal
      elif self.accept(_is.HEX_CHARS):
        self.accept_all_if(_is.hex_digit)
        return self.emit(Type.INTEGER)

    # Maybe decimal or float
    self.accept_all_if(_is.digit)

    # Found '.' ?
    if self.accept('.'):
      is_float = True
      self.accept_all_if(_is.digit)

    # Found exponent ?
    if self.accept('eE'):
      is_float = True
      # Eat sign if there
      self.accept('+-')
      self.accept_all_if(_is.digit)

    if is_float:
      return self.emit(Type.FLOAT)
    return self.emit(Type.INTEGER)

  #--------------------------------------------------------------------
  # HELPERS
  #--------------------------------------------------------------------

  def accept(self, valid: str):
    '''
    Consumes the next single char if it's in the given set `valid`.
    '''
    if self.mgr.next() in set(valid):
      return True
    self.mgr.backup()
    return False

  def accept_all_if(self, func):
    '''
    Consumes all the next chars if passing them one by one to `func`
    call returns True.
    '''
    while func(self.mgr.next()):
      pass
    self.mgr.backup()

  def emit(self, t: type) -> Token:
    '''
    Emit a `Token` instance of given type `t` with given context.
    '''
    val, loc = self.mgr.emit()
    return Token(typ=t, val=val, loc=loc)
