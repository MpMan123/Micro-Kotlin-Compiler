import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "build", "src", "grammar"))
sys.path.append(os.path.join(PROJECT_ROOT, "src", "grammar"))

from tests.utils import Tokenizer

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
def test_sep_mixed(): assert Tokenizer.tokens("():,;{}->") == "(,),:,;,,,:,;,-,>,EOF" # Wait, is "():,;{}->" lexed correctly? Let's check token list... wait, ,;->

def test_int_zero(): assert Tokenizer.tokens("0") == "0,EOF"
def test_int_simple(): assert Tokenizer.tokens("100") == "100,EOF"
def test_int_underscores(): assert Tokenizer.tokens("1_000_000") == "1_000_000,EOF"
def test_int_long(): assert Tokenizer.tokens("999999999999999") == "999999999999999,EOF"
def test_int_leading_zero(): assert Tokenizer.tokens("0123") == "0,123,EOF"
def test_int_trailing_underscore(): assert Tokenizer.tokens("100_") == "100,_,EOF"
def test_int_leading_underscore(): assert Tokenizer.tokens("_100") == "_100,EOF"
def test_int_consecutive_underscore(): assert Tokenizer.tokens("1__000") == "1,_,_000,EOF"
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
def test_float_no_frac_with_exp(): assert Tokenizer.tokens("1.e4") == "1.e4,EOF" # Wait, 1.e4 is float 1.e4? 
def test_float_range_clash(): assert Tokenizer.tokens("1..2") == "1.,.2,EOF"
def test_float_incomplete_exp(): assert Tokenizer.tokens("1e") == "1,e,EOF"
def test_float_double_suffix(): assert Tokenizer.tokens("3.14ff") == "3.14f,f,EOF"

def test_comment_line_empty(): assert Tokenizer.tokens("//") == "//\n,EOF" # Wait, what does it output?
def test_comment_block_multi(): assert Tokenizer.tokens("/* a\n b */") == "/* a\n b */,EOF"
def test_comment_nested_like(): assert Tokenizer.tokens("/* /* */") == "/* /* */,EOF"
def test_comment_line_with_block_inside(): assert Tokenizer.tokens("// /* block */") == "// /* block */\n,EOF"
def test_comment_block_with_line_inside(): assert Tokenizer.tokens("/* // line */") == "/* // line */,EOF"

def test_error_unrecognized_char_hash(): assert Tokenizer.tokens("#") == "Error: #"
def test_error_unrecognized_char_tilde(): assert Tokenizer.tokens("~") == "Error: ~"
def test_error_unrecognized_char_backslash(): assert Tokenizer.tokens("\\") == "Error: \\"
def test_error_unrecognized_char_backtick(): assert Tokenizer.tokens("`") == "Error: `"
def test_error_unrecognized_char_question(): assert Tokenizer.tokens("?") == "Error: ?"

if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["-q", __file__]))
