import string
from expects import *
import comp.util._is as _is

with description("util/_is helper"):
  with it("checks for binary digits"):
    expect(_is.bin_digit('0')).to(equal(True))
    expect(_is.bin_digit('1')).to(equal(True))
    expect(_is.bin_digit('10')).to(equal(False))
    expect(_is.bin_digit('')).to(equal(False))

  with it("checks for octal digits"):
    for c in string.octdigits:
      expect(_is.oct_digit(c)).to(equal(True))

    expect(_is.oct_digit('8')).to(equal(False))
    expect(_is.oct_digit(7)).to(equal(False))

  with it("checks for hexadecimal digits"):
    for c in string.hexdigits:
      expect(_is.hex_digit(c)).to(equal(True))

    expect(_is.oct_digit('')).to(equal(False))
    expect(_is.oct_digit(7)).to(equal(False))

  with it("checks for start of identifier chars"):
    for c in string.ascii_letters:
      expect(_is.ident_start(c)).to(equal(True))

    expect(_is.ident_start('_')).to(equal(True))
    expect(_is.ident_start('3')).to(equal(False))

  with it("checks for identifier chars"):
    for c in string.ascii_letters:
      expect(_is.ident(c)).to(equal(True))

    for c in string.digits:
      expect(_is.ident(c)).to(equal(True))

    expect(_is.oct_digit('')).to(equal(False))
    expect(_is.oct_digit(7)).to(equal(False))

  with it("checks for white space chars"):
    for c in string.whitespace:
      if c == '\n':
        expect(_is.whitespace(c)).to(equal(False))
      else:
        expect(_is.whitespace(c)).to(equal(True))
