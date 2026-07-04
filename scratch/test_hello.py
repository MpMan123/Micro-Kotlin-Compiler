import sys
sys.path.append('.')
from tests.utils import Tokenizer, _make_lexer, Parser
from antlr4 import CommonTokenStream

src = 'fun main() {\n}'
lexer = _make_lexer(src)
stream = CommonTokenStream(lexer)
stream.fill()
for t in stream.tokens:
    print(repr(t.text), ':', lexer.symbolicNames[t.type] if t.type > 0 else 'EOF')

try:
    print("Parser:", Parser.parse(src))
except Exception as e:
    print("Error:", e)
