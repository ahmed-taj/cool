from expects import *
from comp.util.file_buffer import FileBuffer, ENCODING
from specs.helpers import TmpFile


def _nextcl(buf):
  buf.next()
  return buf.emit()


with description('util/FileBuffer'):

  with it("does tokenize input string"):

    with TmpFile("abc\ndef \n ghi") as t:
      buf = FileBuffer(t.name)
      name = t.name

    c, l = _nextcl(buf)
    expect(c).to(equal('a'))
    expect(l.col).to(equal(1))
    expect(l.line).to(equal(1))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('b'))
    expect(l.col).to(equal(2))
    expect(l.line).to(equal(1))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('c'))
    expect(l.col).to(equal(3))
    expect(l.line).to(equal(1))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('\n'))
    expect(l.col).to(equal(4))
    expect(l.line).to(equal(1))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('d'))
    expect(l.col).to(equal(1))
    expect(l.line).to(equal(2))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('e'))
    expect(l.col).to(equal(2))
    expect(l.line).to(equal(2))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('f'))
    expect(l.col).to(equal(3))
    expect(l.line).to(equal(2))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal(' '))
    expect(l.col).to(equal(4))
    expect(l.line).to(equal(2))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('\n'))
    expect(l.col).to(equal(5))
    expect(l.line).to(equal(2))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal(' '))
    expect(l.col).to(equal(1))
    expect(l.line).to(equal(3))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('g'))
    expect(l.col).to(equal(2))
    expect(l.line).to(equal(3))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('h'))
    expect(l.col).to(equal(3))
    expect(l.line).to(equal(3))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal('i'))
    expect(l.col).to(equal(4))
    expect(l.line).to(equal(3))
    expect(l.buffer).to(equal(name))

    c, l = _nextcl(buf)
    expect(c).to(equal(''))
    expect(l.col).to(equal(5))
    expect(l.line).to(equal(3))
    expect(l.buffer).to(equal(name))

  with it("supports backing-up"):
    with TmpFile("abc\nd") as t:
      buff = FileBuffer(t.name)

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

  with it("supports looking-ahead"):
    with TmpFile("a") as t:
      buff = FileBuffer(t.name)

    buff.next()
    expect(buff.peek()).to(equal(''))
