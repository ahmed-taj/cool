from enum import unique, IntEnum

from comp.util.io_base import Location


@unique
class Type(IntEnum):
  '''
  (Type , Value) pairs of all language categories.
  '''
  # Keywords
  KW_DEF = 1  # 'def'
  KW_END = 2  # 'end'
  KW_RETURN = 3  # 'return'

  # Operators and delimiters
  ADD = 100  # '+'
  SUB = 101  # '-'
  MUL = 102  # '*'
  DIV = 103  # '/'
  MOD = 104  # '%'

  COMMA = 200  # ','
  DOT = 201  # '.'

  L_BRACE = 300  # '{'
  R_BRACE = 301  # '}'
  L_BRACK = 302  # '['
  R_BRACK = 303  # ']'
  L_PAREN = 304  # '('
  R_PAREN = 305  # ')'

  # Specials
  EOF = 1000
  NEWLINE = 1001
  INTEGER = 1002
  FLOAT = 1003
  IDENT = 1004
  FUNC_IDENT = 1005
  ERROR = 1006


class Token:
  '''
  Holds specific token details
  '''

  def __init__(self, typ: Type, loc: Location, val: str):
    self.typ = typ
    self.loc = loc
    self.val = val

  def __str__(self) -> str:
    val = self.val
    typ = self.typ.name
    fmt = "Token ( {0} ) {1} "

    # Don't print EOF or NEWLINE values
    if self.typ != Type.EOF and self.typ != Type.NEWLINE:
      fmt += "=> {}".format(val)

    return fmt.format(typ, self.loc)
