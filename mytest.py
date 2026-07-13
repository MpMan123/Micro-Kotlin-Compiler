#!/usr/bin/env python3

import sys
import os

from src.grammar.lexererr import (
    ErrorToken,
    UncloseString,
    IllegalEscape,
)


# Add paths to generated grammar files
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "build", "src", "grammar"))
sys.path.append(os.path.join(PROJECT_ROOT, "src", "grammar"))
sys.path.append(os.path.join(PROJECT_ROOT, "tests"))


from antlr4 import *
from MKotlinLexer import MKotlinLexer
from src.grammar.lexererr import LexerError, ErrorToken, UncloseString, IllegalEscape
from tests.utils import Tokenizer, Parser
from tests.utils import ASTGenerator

if __name__ == '__main__':
    # CÁCH 1: Định nghĩa sẵn danh sách các input muốn test trực tiếp trong code
    # inp = 'fun main() {\n    printString("Hello, World!")\n}'
    inp = "data class Point(x: Int, y: Int)"
    try:
        # lexer = MKotlinLexer(InputStream(inp))
        # token_stream = CommonTokenStream(lexer)
        # token_stream.fill()
        # # 4. Duyệt qua tất cả các Token thu được và in ra màn hình (Chi tiết)
        # for token in token_stream.tokens:
        #     token_name = lexer.symbolicNames[token.type] if token.type != Token.EOF else "EOF"
        #     if token_name == "EOF":
        #         print(f"<{token_name}> (Type ID: {token.type})")
        #     else:
        #         print(f"Token: '{token.text}' (Type ID: {token.type}, Name: {token_name})")
        # print(Tokenizer.tokens(inp))
        # print(Parser.parse(inp))
        print(repr(ASTGenerator.gen(inp)))
        
    except (LexerError, ErrorToken, UncloseString, IllegalEscape) as e:
        raise e