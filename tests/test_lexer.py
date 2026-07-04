"""
Lexer test cases for MKotlin compiler.
TODO: Implement 100 test cases for lexer
"""

from tests.utils import Tokenizer


# ========== Simple Test Cases (10 types) ==========
def test_keyword_val():
    """1. Keyword"""
    assert Tokenizer.tokens("val") == "val,EOF"


def test_operator_eq():
    """2. Operator"""
    assert Tokenizer.tokens("==") == "==,EOF"


def test_separator_semi():
    """3. Separator"""
    assert Tokenizer.tokens(";") == ";,EOF"


def test_integer_with_underscores():
    """4. Integer literal"""
    assert Tokenizer.tokens("1_000") == "1_000,EOF"


def test_float_literal():
    """5. Float literal"""
    assert Tokenizer.tokens("3.14") == "3.14,EOF"


def test_string_simple():
    """6. String literal"""
    assert Tokenizer.tokens('"hello"') == "hello,EOF"


def test_identifier_simple():
    """7. Identifier"""
    assert Tokenizer.tokens("foo") == "foo,EOF"


def test_line_comment():
    """8. Line comment"""
    assert Tokenizer.tokens("val x // comment") == "val,x,EOF"


def test_mixed_expression():
    """9. Mixed: operators and literals"""
    assert Tokenizer.tokens("1 + 2") == "1,+,2,EOF"


def test_unrecognized_char():
    """10. Lexical error"""
    assert Tokenizer.tokens("@") == "@"

def test_type():
    """11. type"""
    assert Tokenizer.tokens("Int Float Boolean String Unit") == "Int,Float,Boolean,String,Unit,EOF"

# 12-16 tests
def test_blockComment():
    assert Tokenizer.tokens("/* hehehehe */ */") == "*,/,EOF"
    assert Tokenizer.tokens("//line1\n //line2 /*block*/*/*/") == "EOF"
    assert Tokenizer.tokens("/* halo") == "/,*,halo,EOF"
    assert Tokenizer.tokens("// hehee \n kkk") == "kkk,EOF"
    assert Tokenizer.tokens("Int */ //line1 \n /*kkkk \n*/") == "Int,*,/,EOF"

# 17
def test_basicTokens():
    inp ="data class class continue data else false for fun if in is return true val var when while = + - * / % ++ -- == != < > <= >= || && ! . .. { } ( ) ; , : -> Mai Hong Phuoc"
    assert Tokenizer.tokens(inp) == "data class,class,continue,data,else,false,for,fun,if,in,is,return,true,val,var,when,while,=,+,-,*,/,%,++,--,==,!=,<,>,<=,>=,||,&&,!,.,..,{,},(,),;,,,:,->,Mai,Hong,Phuoc,EOF"

# 18 - 35
def test_float():
    inp = "3.05 -0.5 1e3 2.5e2 1.2e-3 3E8 5. 5.0 .25 3.14f 3.14F"
    assert Tokenizer.tokens(inp) == "3.05,-,0.5,1e3,2.5e2,1.2e-3,3E8,5.,5.0,.25,3.14f,3.14F,EOF"
    assert Tokenizer.tokens("000.000") == "000.000,EOF"

    assert Tokenizer.tokens("1..2") == "1,..,2,EOF"
    assert Tokenizer.tokens(".2e2") == ".2e2,EOF"

    assert Tokenizer.tokens(".123e-10F") == ".123e-10F,EOF"

    assert Tokenizer.tokens("999999999999999999999999e999999") == "999999999999999999999999e999999,EOF"

    assert Tokenizer.tokens("1.e+0") == "1.e+0,EOF"

    assert Tokenizer.tokens("0.0e-000001f") == "0.0e-000001f,EOF"

    assert Tokenizer.tokens("123e") == "123,e,EOF"

    assert Tokenizer.tokens("3.14ff") == "3.14f,f,EOF"

    assert Tokenizer.tokens("1e--2") == "1,e,--,2,EOF"

    assert Tokenizer.tokens("0..1e2") == "0.,.1e2,EOF"

    assert Tokenizer.tokens("5.e") == "5.,e,EOF"

    assert Tokenizer.tokens(".0E+999F") == ".0E+999F,EOF"

    assert Tokenizer.tokens("1e+000000000001") == "1e+000000000001,EOF"

    assert Tokenizer.tokens("123.456.789") == "123.456,.789,EOF"

    assert Tokenizer.tokens("1f") == "1f,EOF"

    assert Tokenizer.tokens(".f") == ".,f,EOF"

# ========== String Literal Test Cases (20 Cases) ==========

def test_string_empty():
    """1. Empty string literal"""
    assert Tokenizer.tokens('""') == ",EOF"


def test_string_simple():
    """2. Simple string literal without escapes"""
    assert Tokenizer.tokens('"hello"') == "hello,EOF"


def test_string_spaces():
    """3. String literal containing spaces"""
    assert Tokenizer.tokens('"hello world"') == "hello world,EOF"


def test_string_escape_newline():
    """4. String literal with valid newline escape sequence"""
    assert Tokenizer.tokens('"\\n"') == "\\n,EOF"


def test_string_escape_tab():
    """5. String literal with valid horizontal tab escape sequence"""
    assert Tokenizer.tokens('"\\t"') == "\\t,EOF"


def test_string_escape_carriage_return():
    """6. String literal with valid carriage return escape sequence"""
    assert Tokenizer.tokens('"\\r"') == "\\r,EOF"


def test_string_escape_backspace():
    """7. String literal with valid backspace escape sequence"""
    assert Tokenizer.tokens('"\\b"') == "\\b,EOF"


def test_string_escape_formfeed():
    """8. String literal with valid formfeed escape sequence"""
    assert Tokenizer.tokens('"\\f"') == "\\f,EOF"


def test_string_escape_backslash():
    """9. String literal with valid backslash escape sequence"""
    assert Tokenizer.tokens('"\\\\"') == "\\\\,EOF"


def test_string_escape_double_quote():
    """10. String literal with valid double quote escape sequence"""
    assert Tokenizer.tokens('"\\""') == "\\\",EOF"


def test_string_escape_dollar():
    """11. String literal with valid dollar sign escape sequence"""
    assert Tokenizer.tokens('"\\$"') == "\\$,EOF"


def test_string_mixed_valid():
    """12. String literal with mixed text and multiple valid escapes"""
    assert Tokenizer.tokens('"hello\\n\\tworld"') == "hello\\n\\tworld,EOF"


def test_string_consecutive_escapes():
    """12b. String literal with consecutive trailing escape sequences"""
    assert Tokenizer.tokens('"acbd\\n\\t\\b"') == "acbd\\n\\t\\b,EOF"


def test_string_unicode_chars():
    """13. String literal containing raw unicode characters directly"""
    assert Tokenizer.tokens('"hello 🌍"') == "hello 🌍,EOF"


def test_string_illegal_escape():
    """14. String literal containing simple invalid escape sequence"""
    assert Tokenizer.tokens('"\\x"') == "\\x"


def test_string_illegal_escape_unicode():
    """15. String literal containing unsupported unicode escape syntax"""
    assert Tokenizer.tokens('"\\u0041"') == "\\u"


def test_string_illegal_escape_digit():
    """16. String literal containing unsupported octal escape syntax"""
    assert Tokenizer.tokens('"abc\\1"') == "abc\\1"


def test_string_unclosed_eof():
    """17. Unclosed string literal reaching end of file"""
    assert Tokenizer.tokens('"abc') == "abc"


def test_string_unclosed_newline():
    """18. Unclosed string literal terminated by a newline character"""
    assert Tokenizer.tokens('"abc\n') == "abc\n"


def test_string_unclosed_carriage_return():
    """19. Unclosed string literal terminated by a carriage return character"""
    assert Tokenizer.tokens('"abc\r') == "\""


def test_string_unescaped_dollar():
    """20. String literal containing unescaped dollar sign (not supported)"""
    assert Tokenizer.tokens('"$abc"') == "\""


# ========== Generated Test Cases (66+ cases) ==========

def test_kw_break(): assert Tokenizer.tokens("break") == "break,EOF"
def test_kw_class(): assert Tokenizer.tokens("class") == "class,EOF"
def test_kw_continue(): assert Tokenizer.tokens("continue") == "continue,EOF"
def test_kw_data(): assert Tokenizer.tokens("data") == "data,EOF"
def test_kw_else(): assert Tokenizer.tokens("else") == "else,EOF"
def test_kw_false(): assert Tokenizer.tokens("false") == "false,EOF"
def test_kw_for(): assert Tokenizer.tokens("for") == "for,EOF"
def test_kw_fun(): assert Tokenizer.tokens("fun") == "fun,EOF"
def test_kw_if(): assert Tokenizer.tokens("if") == "if,EOF"
def test_kw_in(): assert Tokenizer.tokens("in") == "in,EOF"
def test_kw_is(): assert Tokenizer.tokens("is") == "is,EOF"
def test_kw_return(): assert Tokenizer.tokens("return") == "return,EOF"
def test_kw_true(): assert Tokenizer.tokens("true") == "true,EOF"
def test_kw_val(): assert Tokenizer.tokens("val") == "val,EOF"
def test_kw_var(): assert Tokenizer.tokens("var") == "var,EOF"
def test_kw_when(): assert Tokenizer.tokens("when") == "when,EOF"
def test_kw_while(): assert Tokenizer.tokens("while") == "while,EOF"

def test_type_Int(): assert Tokenizer.tokens("Int") == "Int,EOF"
def test_type_Float(): assert Tokenizer.tokens("Float") == "Float,EOF"
def test_type_Boolean(): assert Tokenizer.tokens("Boolean") == "Boolean,EOF"
def test_type_String(): assert Tokenizer.tokens("String") == "String,EOF"
def test_type_Unit(): assert Tokenizer.tokens("Unit") == "Unit,EOF"

def test_id_simple(): assert Tokenizer.tokens("myVar") == "myVar,EOF"
def test_id_camel(): assert Tokenizer.tokens("thisIsCamelCase") == "thisIsCamelCase,EOF"
def test_id_pascal(): assert Tokenizer.tokens("PascalCase") == "PascalCase,EOF"
def test_id_underscore(): assert Tokenizer.tokens("_privateVar") == "_privateVar,EOF"
def test_id_with_digits(): assert Tokenizer.tokens("var123name") == "var123name,EOF"
def test_id_trailing_digits(): assert Tokenizer.tokens("name123") == "name123,EOF"
def test_id_only_underscores(): assert Tokenizer.tokens("___") == "___,EOF"
def test_id_keyword_prefix(): assert Tokenizer.tokens("funky") == "funky,EOF"
def test_id_starts_with_underscore(): assert Tokenizer.tokens("_123") == "_123,EOF"
def test_id_long(): assert Tokenizer.tokens("a" * 100) == "a" * 100 + ",EOF"
def test_id_case_sensitive(): assert Tokenizer.tokens("val VAL") == "val,VAL,EOF"

def test_op_arithmetic(): assert Tokenizer.tokens("+ - * / %") == "+,-,*,/,%,EOF"
def test_op_relational(): assert Tokenizer.tokens("< > <= >=") == "<,>,<=,>=,EOF"
def test_op_equality(): assert Tokenizer.tokens("== !=") == "==,!=,EOF"
def test_op_logical(): assert Tokenizer.tokens("&& || !") == "&&,||,!,EOF"
def test_op_assignment(): assert Tokenizer.tokens("=") == "=,EOF"
def test_op_compound_match_1(): assert Tokenizer.tokens(">=>") == ">=,>,EOF"
def test_op_compound_match_2(): assert Tokenizer.tokens("===") == "==,=,EOF"
def test_op_compound_match_3(): assert Tokenizer.tokens("!==") == "!=,=,EOF"
def test_op_compound_match_4(): assert Tokenizer.tokens("+++") == "++,+,EOF"
def test_op_compound_match_5(): assert Tokenizer.tokens("---") == "--,-,EOF"
def test_op_dot(): assert Tokenizer.tokens(".") == ".,EOF"
def test_op_range(): assert Tokenizer.tokens("a..b") == "a,..,b,EOF"

def test_sep_braces(): assert Tokenizer.tokens("{ }") == "{,},EOF"
def test_sep_parens(): assert Tokenizer.tokens("( )") == "(,),EOF"
def test_sep_semi_comma(): assert Tokenizer.tokens("; ,") == ";,,,EOF"
def test_sep_colon(): assert Tokenizer.tokens(":") == ":,EOF"
def test_sep_arrow(): assert Tokenizer.tokens("->") == "->,EOF"
def test_sep_mixed(): assert Tokenizer.tokens("():,;{}->") == "(,),:,,,;,{,},->,EOF"

def test_int_zero(): assert Tokenizer.tokens("0") == "0,EOF"
def test_int_simple(): assert Tokenizer.tokens("100") == "100,EOF"
def test_int_underscores(): assert Tokenizer.tokens("1_000_000") == "1_000_000,EOF"
def test_int_long(): assert Tokenizer.tokens("999999999999999") == "999999999999999,EOF"
def test_int_leading_zero(): assert Tokenizer.tokens("0123") == "0,123,EOF"
def test_int_trailing_underscore(): assert Tokenizer.tokens("100_") == "100,_,EOF"
def test_int_leading_underscore(): assert Tokenizer.tokens("_100") == "_100,EOF"
def test_int_consecutive_underscore(): assert Tokenizer.tokens("1__000") == "1,__000,EOF"
def test_int_hex_like(): assert Tokenizer.tokens("0x12") == "0,x12,EOF"
def test_int_binary_like(): assert Tokenizer.tokens("0b10") == "0,b10,EOF"

def test_float_simple_no_exp(): assert Tokenizer.tokens("3.14") == "3.14,EOF"
def test_float_no_int_part(): assert Tokenizer.tokens(".5") == ".5,EOF"
def test_float_no_frac_part(): assert Tokenizer.tokens("1.") == "1.,EOF"
def test_float_exp_only(): assert Tokenizer.tokens("1e4") == "1e4,EOF"
def test_float_exp_negative(): assert Tokenizer.tokens("2.5E-3") == "2.5E-3,EOF"
def test_float_exp_positive(): assert Tokenizer.tokens("5.67e+2") == "5.67e+2,EOF"
def test_float_suffix_f(): assert Tokenizer.tokens("3.14f") == "3.14f,EOF"
def test_float_suffix_F(): assert Tokenizer.tokens("2.5F") == "2.5F,EOF"
def test_float_no_frac_with_exp(): assert Tokenizer.tokens("1.e4") == "1.e4,EOF"
def test_float_range_clash(): assert Tokenizer.tokens("1..2") == "1,..,2,EOF"
def test_float_incomplete_exp(): assert Tokenizer.tokens("1e") == "1,e,EOF"
def test_float_double_suffix(): assert Tokenizer.tokens("3.14ff") == "3.14f,f,EOF"

def test_comment_line_empty(): assert Tokenizer.tokens("hello //") == "hello,EOF"
def test_comment_block_multi(): assert Tokenizer.tokens("ronaldo/* a\n b */") == "ronaldo,EOF"
def test_comment_nested_like(): assert Tokenizer.tokens("ronaldo/* /* and messi */, the legend") == "ronaldo,,,the,legend,EOF"
def test_comment_line_with_block_inside(): assert Tokenizer.tokens("hahaha// /* block */") == "hahaha,EOF"
def test_comment_block_with_line_inside(): assert Tokenizer.tokens("boboiboy/* // line */") == "boboiboy,EOF"

def test_error_unrecognized_char_hash(): assert Tokenizer.tokens("#") == "#"
def test_error_unrecognized_char_tilde(): assert Tokenizer.tokens("~") == "~"
def test_error_unrecognized_char_backslash(): assert Tokenizer.tokens("\\") == "\\"
def test_error_unrecognized_char_backtick(): assert Tokenizer.tokens("`") == "`"
def test_error_unrecognized_char_question(): assert Tokenizer.tokens("?") == "?"

# ========== Mixed / Complex Programs ==========

def test_mixed_program_1(): 
    """Mixed 1: Variable declaration with string literal and comments"""
    assert Tokenizer.tokens('val greeting = "Hello \\"World\\"" // says hello') == "val,greeting,=,Hello \\\"World\\\",EOF"

def test_mixed_program_2():
    """Mixed 2: Function with string literal, integers, and operators"""
    assert Tokenizer.tokens('fun printMsg(count: Int) { printString("Count: " + count) }') == "fun,printMsg,(,count,:,Int,),{,printString,(,Count: ,+,count,),},EOF"

def test_mixed_program_3():
    """Mixed 3: Data class with string literal initialization"""
    assert Tokenizer.tokens('data class Person(name: String); val p = Person("Mai Hong Phuoc")') == "data class,Person,(,name,:,String,),;,val,p,=,Person,(,Mai Hong Phuoc,),EOF"

def test_mixed_program_4():
    """Mixed 4: Multiline string edge case mixed with float and identifiers"""
    assert Tokenizer.tokens('var x = 3.14f; "abc\\ndef" /* float and string */') == "var,x,=,3.14f,;,abc\\ndef,EOF"

def test_mixed_program_5():
    """Mixed 5: Complex expression with unclosed string at the end"""
    assert Tokenizer.tokens('if (true) { x = "unclosed') == "if,(,true,),{,x,=,unclosed"
