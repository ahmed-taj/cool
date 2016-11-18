import string
from expects import *
from comp.util.str_buffer import StringBuffer


def _nextcl(buf):
  buf.next()
  return buf.emit()


with description('util/StringBuffer'):

  with it("does tokenize input string"):
    s = "abc\ndef \n ghi"
    buf = StringBuffer(s)

    c, l = _nextcl(buf)
    expect(c).to(equal('a'))
    expect(l.col).to(equal(1))
    expect(l.line).to(equal(1))
    expect(l.buffer).to(equal('stdin'))

    c, l = _nextcl(buf)
    expect(c).to(equal('b'))
    expect(l.col).to(equal(2))
    expect(l.line).to(equal(1))

    c, l = _nextcl(buf)
    expect(c).to(equal('c'))
    expect(l.col).to(equal(3))
    expect(l.line).to(equal(1))

    c, l = _nextcl(buf)
    expect(c).to(equal('\n'))
    expect(l.col).to(equal(4))
    expect(l.line).to(equal(1))

    c, l = _nextcl(buf)
    expect(c).to(equal('d'))
    expect(l.col).to(equal(1))
    expect(l.line).to(equal(2))

    c, l = _nextcl(buf)
    expect(c).to(equal('e'))
    expect(l.col).to(equal(2))
    expect(l.line).to(equal(2))

    c, l = _nextcl(buf)
    expect(c).to(equal('f'))
    expect(l.col).to(equal(3))
    expect(l.line).to(equal(2))

    c, l = _nextcl(buf)
    expect(c).to(equal(' '))
    expect(l.col).to(equal(4))
    expect(l.line).to(equal(2))

    c, l = _nextcl(buf)
    expect(c).to(equal('\n'))
    expect(l.col).to(equal(5))
    expect(l.line).to(equal(2))

    c, l = _nextcl(buf)
    expect(c).to(equal(' '))
    expect(l.col).to(equal(1))
    expect(l.line).to(equal(3))

    c, l = _nextcl(buf)
    expect(c).to(equal('g'))
    expect(l.col).to(equal(2))
    expect(l.line).to(equal(3))

    c, l = _nextcl(buf)
    expect(c).to(equal('h'))
    expect(l.col).to(equal(3))
    expect(l.line).to(equal(3))

    c, l = _nextcl(buf)
    expect(c).to(equal('i'))
    expect(l.col).to(equal(4))
    expect(l.line).to(equal(3))

    c, l = _nextcl(buf)
    expect(c).to(equal(''))
    expect(l.col).to(equal(5))
    expect(l.line).to(equal(3))

  with it("does support backing-up"):
    s = "abc\nd"
    buff = StringBuffer(s)
    buff.next()
    buff.backup()
    expect(buff.next()).to(equal('a'))

    buff.next()  # b
    buff.next()  # c
    buff.next()  # \n
    buff.next()  # d
    buff.backup()
    buff.backup()
    expect(buff.next()).to(equal('\n'))
