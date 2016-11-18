# TODO: Make sure we check for unicode letters too, not just ASCII.

import string

OCT_DIGITS = set(string.octdigits)
HEX_DIGITS = set(string.hexdigits)
WHITE_SPACES = set(' \t\r\x0b\x0c')  # Notice no '\n'

BIN_CHARS = 'bB'
OCT_CHARS = 'oO'
HEX_CHARS = 'xX'


def ident(ch: str):
  return ident_start(ch) or digit(ch)


def ident_start(ch: str):
  return alpha(ch) or ch == '_'


def alpha(ch: str):
  return ch.isalpha()


def alphanum(ch: str):
  return ch.isalnum()


def digit(ch: str):
  return ch.isdigit()


def bin_digit(ch: str):
  return '0' == ch or '1' == ch


def oct_digit(ch: str):
  return ch in OCT_DIGITS


def hex_digit(ch: str):
  return ch in HEX_DIGITS


def whitespace(ch: str):
  return ch in WHITE_SPACES
