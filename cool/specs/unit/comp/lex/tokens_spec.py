import string
from expects import *
import comp.lex.tokens as tok
import comp.util.io_base as io

with description("lex/Token"):
  with it("holds Token's info"):
    t = tok.Type.EOF
    l = io.Location('a file', 1, 1)
    v = 'dump'
    tk = tok.Token(t, l, v)
    expect(tk.typ).to(equal(tok.Type.EOF))
    expect(str(tk.loc)).to(equal(str(l)))
    expect(tk.val).to(equal(v))

  with it("prints tokens"):
    t = tok.Type.KW_DEF
    l = io.Location('a file', 1, 13)
    v = 'Def'
    tk = tok.Token(t, l, v)
    exp = "Token ( KW_DEF ) <a file> (1:13)"
    expect(str(tk)).to(contain(exp))
