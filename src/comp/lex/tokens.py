from enum import Enum

from comp.util.io_base import Location


class Type(Enum):
  '''
  (Type , Value) pairs of all language categories.
  '''
  # Keywords
  KW_DEF = 'def'
  KW_END = 'end'
  KW_RETURN = 'return'

  # Operators and delimiters
  AND = '+'
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
  ERROR = False
  INTEGER = False
  FLOAT = False
  IDENT = False
  FUNC_IDENT = False


class Token:
  '''
  Holds specific token details
  '''

  def __init__(self, typ: Type, loc: Location, val: str=None):
    self.typ = typ
    self.val = val
    self.loc = loc

  def __str__(self) -> str:
    val = self.typ.value or self.val
    if self.typ == Type.ERROR:
      val = self.val

    typ = self.typ.name
    return "Token ({0}) {1} => {2}".format(typ, self.loc, val)
