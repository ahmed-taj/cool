from enum import Enum, unique

from comp.util.io_base import Location


@unique
class Type(Enum):
  '''
  (Type , Value) pairs of all language categories.
  '''
  # Keywords
  KW_DEF = 'def'
  KW_END = 'end'
  KW_RETURN = 'return'

  # Operators and delimiters
  ADD = '+'
  SUB = '-'
  MUL = '*'
  DIV = '/'
  MOD = '%'

  COMMA = ','
  DOT = '.'

  L_BRACE = '{'
  R_BRACE = '}'
  L_BRACK = '['
  R_BRACK = ']'
  L_PAREN = '('
  R_PAREN = ')'

  # Specials
  EOF = 'EOF'
  NEWLINE = 'NEWLINE'
  INTEGER = 1
  FLOAT = 2
  IDENT = 3
  FUNC_IDENT = 4
  ERROR = 5


class Token:
  '''
  Holds specific token details
  '''

  def __init__(self, typ: Type, loc: Location, val: str=None):
    self.typ = typ
    self.val = val
    self.loc = loc

  def __str__(self) -> str:
    val = self.val
    typ = self.typ.name
    fmt = "Token ( {0} ) {1} "

    # Don't print EOF or NEWLINE values
    if self.typ != Type.EOF and self.typ != Type.NEWLINE:
      fmt += "=> {}".format(val)

    return fmt.format(typ, self.loc)
