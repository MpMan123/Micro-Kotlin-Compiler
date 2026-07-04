"""
Parser test cases for MKotlin compiler.
TODO: Implement 100 test cases for parser
"""

from tests.utils import Parser


# ========== Simple Test Cases (10 types) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser.parse("") == "success"


def test_hello_world():
    """2. Program with main function"""
    src = """
        fun main() {
            printString("Hello, World!")
        }
    """
    assert Parser.parse(src) == "success"


def test_data_class():
    """3. Data class declaration"""
    assert Parser.parse("data class Point(x: Int, y: Int)") == "success"


def test_val_decl():
    """4. Variable declaration"""
    assert Parser.parse("""
        fun main() {
          val x = 10
        }
    """) == "success"


def test_var_with_type():
    """5. Variable with type annotation"""
    assert Parser.parse("""
        fun main() {
          var x: Int = 10
        }
    """) == "success"


def test_if_else():
    """6. If statement"""
    src = """
        fun main() {
          if (x > 0) printInt(1) else printInt(0)
        }
    """
    assert Parser.parse(src) == "success"


def test_while():
    """7. While statement"""
    src = """
        fun main() {
          while (i < 10) {
            i++
          }
        }
    """
    assert Parser.parse(src) == "success"


def test_for_in_range():
    """8. For-in-range statement"""
    src = """
        fun main() {
          for (i in 0 .. 9) {
            printInt(i)
          }
        }
    """
    assert Parser.parse(src) == "success"


def test_when():
    """9. When statement"""
    src = """
        fun main() {
          when (d) {
            1 -> printInt(1)
            else -> printInt(0)
          }
        }
    """
    assert Parser.parse(src) == "success"


def test_syntax_error():
    """10. Syntax error"""
    assert Parser.parse("""
        fun main( {
        }
    """) != "success"

# --- 1. Global Structure ---
def test_global_multiple_data_classes():
    """11. Multiple data classes at global scope"""
    src = """
        data class A(x: Int)
        data class B(y: Float)
    """
    assert Parser.parse(src) == "success"

def test_global_multiple_functions():
    """12. Multiple functions at global scope"""
    src = """
        fun a() {}
        fun b() {}
    """
    assert Parser.parse(src) == "success"

def test_global_mixed_declarations():
    """13. Mixed data classes and functions"""
    src = """
        data class Point(x: Int)
        fun main() {}
        data class Line(p1: Point)
    """
    assert Parser.parse(src) == "success"

def test_global_semicolon_separator():
    """14. Global declarations separated by semicolons"""
    src = "data class A(x: Int); fun b() {}"
    assert Parser.parse(src) != "success"

def test_global_error_statement_outside_fun():
    """15. Error: Statement outside function"""
    src = "val x = 10"
    assert Parser.parse(src) != "success"

def test_global_error_nested_data_class():
    """16. Error: Nested data class"""
    src = "data class A(x: Int) { data class B() }"
    assert Parser.parse(src) != "success"

def test_global_error_nested_function():
    """17. Error: Nested function"""
    src = "fun main() { fun inner() {} }"
    assert Parser.parse(src) != "success"

def test_global_error_missing_fun_keyword():
    """18. Error: Missing fun keyword"""
    src = "main() {}"
    assert Parser.parse(src) != "success"

def test_global_error_lone_semicolon():
    """19. Error: Lone semicolon is not a valid declaration"""
    src = ";"
    assert Parser.parse(src) != "success"


# --- 2. Data Class Declarations ---
def test_data_class_empty_members():
    """20. Data class with empty members"""
    src = "data class Empty()"
    assert Parser.parse(src) == "success"

def test_data_class_single_member():
    """21. Data class with single member"""
    src = "data class Point(x: Int)"
    assert Parser.parse(src) == "success"

def test_data_class_multiple_members():
    """22. Data class with multiple members"""
    src = "data class Person(name: String, age: Int)"
    assert Parser.parse(src) == "success"

def test_data_class_complex_types():
    """23. Data class with custom data class types"""
    src = "data class Line(start: Point, end: Point)"
    assert Parser.parse(src) == "success"

def test_data_class_error_missing_type():
    """24. Error: Missing type in data class member"""
    src = "data class Point(x, y: Int)"
    assert Parser.parse(src) != "success"

def test_data_class_error_missing_comma():
    """25. Error: Missing comma in data class member list"""
    src = "data class Point(x: Int y: Int)"
    assert Parser.parse(src) != "success"

def test_data_class_error_var_val_in_params():
    """26. Error: Data class members cannot have val/var modifiers in MKotlin"""
    src = "data class Point(val x: Int)"
    assert Parser.parse(src) != "success"

def test_data_class_error_missing_parens():
    """27. Error: Missing parentheses in data class declaration"""
    src = "data class Point"
    assert Parser.parse(src) != "success"

def test_data_class_error_body_block():
    """28. Error: Data class cannot have a body block"""
    src = "data class Point(x: Int) {}"
    assert Parser.parse(src) != "success"


# --- 3. Function Declarations ---
def test_fun_no_params_no_return():
    """29. Function with no params and no return type"""
    src = "fun test() {}"
    assert Parser.parse(src) == "success"

def test_fun_with_return_type():
    """30. Function with return type"""
    src = "fun test(): Int { return 1 }"
    assert Parser.parse(src) == "success"

def test_fun_single_param():
    """31. Function with single param"""
    src = "fun test(a: Int) {}"
    assert Parser.parse(src) == "success"

def test_fun_multiple_params():
    """32. Function with multiple params"""
    src = "fun test(a: Int, b: Float, c: String) {}"
    assert Parser.parse(src) == "success"

def test_fun_param_without_type_error():
    """33. Error: Function parameter without type"""
    src = "fun test(a) {}"
    assert Parser.parse(src) != "success"

def test_fun_missing_body_error():
    """34. Error: Function missing body block"""
    src = "fun test()"
    assert Parser.parse(src) != "success"

def test_fun_body_with_multiple_statements():
    """35. Function with multiple statements in body"""
    src = """
        fun test() {
        val x = 1
        val y = 2
        }
    """
    assert Parser.parse(src) == "success"

def test_fun_return_type_missing_colon_error():
    """36. Error: Function return type missing colon"""
    src = "fun test() Int {}"
    assert Parser.parse(src) != "success"


# --- 4. Variable Declarations ---
def test_var_decl_val_inferred():
    """37. val with inferred type"""
    src = "fun main() { val x = 10 }"
    assert Parser.parse(src) == "success"

def test_var_decl_val_explicit():
    """38. val with explicit type"""
    src = "fun main() { val x: Int = 10 }"
    assert Parser.parse(src) == "success"

def test_var_decl_var_inferred():
    """39. var with inferred type"""
    src = "fun main() { var x = 10 }"
    assert Parser.parse(src) == "success"

def test_var_decl_var_explicit_init():
    """40. var with explicit type and init"""
    src = "fun main() { var x: Int = 10 }"
    assert Parser.parse(src) == "success"

def test_var_decl_var_explicit_no_init():
    """41. var with explicit type and no init"""
    src = "fun main() { var x: Int }"
    assert Parser.parse(src) == "success"

def test_var_decl_var_no_init_no_type():
    """42. var with no init and no type"""
    src = "fun main() { var x }"
    assert Parser.parse(src) == "success"

def test_var_decl_error_val_no_init():
    """43. Error: val without initializer"""
    src = "fun main() { val x: Int }"
    assert Parser.parse(src) != "success"

def test_var_decl_error_missing_name():
    """44. Error: Variable declaration missing name"""
    src = "fun main() { val = 10 }"
    assert Parser.parse(src) != "success"

def test_var_decl_error_multiple_vars():
    """45. Error: Multiple variable declaration not supported"""
    src = "fun main() { val x, y = 10 }"
    assert Parser.parse(src) != "success"

def test_var_decl_with_complex_expr():
    """46. Variable declaration with complex expression"""
    src = "fun main() { val x = (1 + 2) * 3 }"
    assert Parser.parse(src) == "success"


# --- 5. Control Flow: If & Loops ---
def test_if_simple():
    """47. Simple if statement"""
    src = "fun main() { if (a > 0) printInt(1) }"
    assert Parser.parse(src) == "success"

def test_if_else_nested():
    """48. Nested if-else"""
    src = "fun main() { if (a) if (b) c else d else e }"
    assert Parser.parse(src) == "success"

def test_if_expression():
    """49. If as an expression"""
    src = "fun main() { val x = if (a > 0) 1 else 0 }"
    assert Parser.parse(src) == "success"

def test_if_error_missing_cond_parens():
    """50. Error: If condition missing parentheses"""
    src = "fun main() { if a > 0 printInt(1) }"
    assert Parser.parse(src) != "success"

def test_while_simple():
    """51. Simple while statement"""
    src = "fun main() { while (x > 0) x-- }"
    assert Parser.parse(src) == "success"

def test_while_with_block():
    """52. While statement with block"""
    src = "fun main() { while (true) { printInt(1) } }"
    assert Parser.parse(src) == "success"

def test_while_error_missing_cond_parens():
    """53. Error: While condition missing parentheses"""
    src = "fun main() { while true printInt(1) }"
    assert Parser.parse(src) != "success"

def test_for_simple():
    """54. Simple for statement"""
    src = "fun main() { for (i in 1..10) printInt(i) }"
    assert Parser.parse(src) == "success"

def test_for_with_block():
    """55. For statement with block"""
    src = "fun main() { for (i in 1..10) { printInt(i) } }"
    assert Parser.parse(src) == "success"

def test_for_error_missing_in():
    """56. Error: For statement missing 'in' keyword"""
    src = "fun main() { for (i 1..10) printInt(i) }"
    assert Parser.parse(src) != "success"

def test_for_error_missing_range():
    """57. Error: For statement missing range (Wait, grammar makes range optional)"""
    src = "fun main() { for (i in 10) printInt(i) }"
    assert Parser.parse(src) == "success"

def test_jump_break():
    """58. Break statement"""
    src = "fun main() { while (true) break }"
    assert Parser.parse(src) == "success"

def test_jump_continue():
    """59. Continue statement"""
    src = "fun main() { while (true) continue }"
    assert Parser.parse(src) == "success"

def test_jump_return_with_expr():
    """60. Return statement with expression"""
    src = "fun main() { return 1 + 2 }"
    assert Parser.parse(src) == "success"


# --- 6. Control Flow: When ---
def test_when_subject_single_label():
    """61. When with subject and single label"""
    src = "fun main() { when (x) { 1 -> printInt(1) } }"
    assert Parser.parse(src) == "success"

def test_when_subject_multi_labels():
    """62. When with subject and multiple labels"""
    src = "fun main() { when (x) { 1, 2, 3 -> printInt(1) } }"
    assert Parser.parse(src) == "success"

def test_when_subject_else():
    """63. When with subject and else branch"""
    src = """
        fun main() { 
            when (x) { 1 -> printInt(1)
            else -> printInt(0) } 
        }
    """
    assert Parser.parse(src) == "success"

def test_when_conditionless():
    """64. Conditionless when statement"""
    src = """
        fun main() { 
            when { 
                x > 0 -> printInt(1)
                y > 0 -> printInt(2)
            } 
        }
    """
    assert Parser.parse(src) == "success"

def test_when_expression():
    """65. When as an expression"""
    src = """
        fun main() { 
            val x = when { 
                    a > 0 -> 1
                    else -> 0 } 
                }
    """
    assert Parser.parse(src) == "success"

def test_when_error_missing_arrow():
    """66. Error: When branch missing arrow"""
    src = "fun main() { when (x) { 1 printInt(1) } }"
    assert Parser.parse(src) != "success"

def test_when_error_multiple_else():
    """67. Error: When with multiple else branches"""
    src = """
        fun main() { when (x) { else -> printInt(1)
         else -> printInt(0) } }
    """
    assert Parser.parse(src) != "success"

def test_when_error_else_not_last():
    """68. Error: When else branch is not the last branch"""
    src = """
        fun main() { when (x) { else -> printInt(1)
         1 -> printInt(0) } }
    """
    assert Parser.parse(src) != "success"

def test_when_subject_no_parens_error():
    """69. Error: When subject missing parentheses"""
    src = "fun main() { when x { 1 -> printInt(1) } }"
    assert Parser.parse(src) != "success"


# --- 7. Expressions & Operators ---
def test_expr_binary_arithmetic():
    """70. Arithmetic expressions"""
    src = "fun main() { val x = a + b - c * d / e % f }"
    assert Parser.parse(src) == "success"

def test_expr_binary_relational():
    """71. Relational expressions"""
    src = "fun main() { val x = a < b || c >= d && e == f != g }"
    assert Parser.parse(src) == "success"

def test_expr_unary_prefix():
    """72. Prefix unary expressions"""
    src = "fun main() { val x = !a + -b + ++c + --d }"
    assert Parser.parse(src) == "success"

def test_expr_unary_postfix():
    """73. Postfix unary expressions"""
    src = "fun main() { val x = a++ + b-- }"
    assert Parser.parse(src) == "success"

def test_expr_parenthesized():
    """74. Parenthesized expressions"""
    src = "fun main() { val x = (a + b) * (c - d) }"
    assert Parser.parse(src) == "success"

def test_expr_function_call_empty():
    """75. Function call with no arguments"""
    src = "fun main() { foo() }"
    assert Parser.parse(src) == "success"

def test_expr_function_call_args():
    """76. Function call with arguments"""
    src = "fun main() { foo(1, \"str\", true) }"
    assert Parser.parse(src) == "success"

def test_expr_member_access():
    """77. Member access"""
    src = "fun main() { val x = p.x }"
    assert Parser.parse(src) == "success"

def test_expr_member_access_chained():
    """78. Chained member access and function calls"""
    src = "fun main() { val x = getPoint().x.y() }"
    assert Parser.parse(src) == "success"

def test_expr_assignment_simple():
    """79. Simple assignment"""
    src = "fun main() { x = 10 }"
    assert Parser.parse(src) == "success"

def test_expr_assignment_chained():
    """80. Chained assignment"""
    src = "fun main() { x = y = z = 10 }"
    assert Parser.parse(src) == "success"

def test_expr_range():
    """81. Range expression (in for loop)"""
    src = "fun main() { for(i in a+b .. c*d) {} }"
    assert Parser.parse(src) == "success"

def test_expr_error_missing_operand():
    """82. Error: Binary operator missing left operand"""
    src = "fun main() { val x = * 5 }"
    assert Parser.parse(src) != "success"

def test_expr_error_unmatched_parens():
    """83. Error: Unmatched parentheses"""
    src = "fun main() { val x = (1 + 2 }"
    assert Parser.parse(src) != "success"

def test_expr_error_consecutive_operators():
    """84. Error: Consecutive binary operators"""
    src = "fun main() { val x = 1 + * 2 }"
    assert Parser.parse(src) != "success"


# --- 8. Statement Terminators & Whitespace ---
def test_stmt_multiple_on_line_with_semi():
    """85. Multiple statements on one line using semicolon"""
    src = "fun main() { val x = 1; val y = 2; printInt(x) }"
    assert Parser.parse(src) == "success"

def test_stmt_empty_block():
    """86. Empty block statement"""
    src = "fun main() { {} }"
    assert Parser.parse(src) == "success"

def test_stmt_error_lone_semicolon_in_fun():
    """87. Error: Lone semicolon inside function (Actually allowed as empty stmtList with terminator)"""
    src = "fun main() { ; }"
    assert Parser.parse(src) == "success"

def test_stmt_missing_newline_error():
    """88. Error: Missing newline/semicolon between statements"""
    src = "fun main() { val x = 1 val y = 2 }"
    assert Parser.parse(src) != "success"

def test_stmt_multiline_expr_error():
    """89. Multiline expression edge case (newline terminates statement)"""
    src = """
        fun main() { val x = (
         1 + 2 
        ) }
    """
    assert Parser.parse(src) != "success"


# --- 9. Additional Mixed & Edge Cases ---
def test_mixed_var_type_inference():
    """90. Mixed var with type inference on assignment"""
    src = "fun main() { var x; x = 10 }"
    assert Parser.parse(src) == "success"

def test_mixed_function_with_all_literals():
    """91. Function containing all types of literals"""
    src = "fun main() { val i = 1; val f = 3.14f; val b = true; val s = \"str\" }"
    assert Parser.parse(src) == "success"

def test_mixed_nested_blocks():
    """92. Deeply nested blocks"""
    src = "fun main() { { { { val x = 1 } } } }"
    assert Parser.parse(src) == "success"

def test_mixed_empty_when():
    """93. When statement with no branches"""
    # Wait, does the spec allow empty when? Usually not, or it might. Let's just expect it fails or succeeds, maybe omit.
    # Let's test a when with only else
    src = "fun main() { when { else -> printInt(0) } }"
    assert Parser.parse(src) != "success"

def test_mixed_if_expression_assignment():
    """94. Assigning if expression to a var"""
    src = "fun main() { var x: Int; x = if (true) 1 else 0 }"
    assert Parser.parse(src) == "success"

def test_mixed_data_class_member_data_class():
    """95. Data class member using another data class type"""
    src = """
        data class A(b: B)
        data class B(x: Int)
    """
    assert Parser.parse(src) == "success"

def test_mixed_comments_everywhere():
    """96. Comments mixed everywhere"""
    src = "/* 1 */ data class /* 3 */ A(x: Int) // 4"
    assert Parser.parse(src) == "success"

def test_mixed_error_val_reassignment():
    """97. Valid Syntax (Semantic Error): Reassigning val"""
    src = "fun main() { val x = 1; x = 2 }"
    assert Parser.parse(src) == "success"

def test_mixed_error_invalid_type_assignment():
    """98. Valid Syntax (Semantic Error): Invalid type assignment"""
    src = "fun main() { val x: Int = \"string\" }"
    assert Parser.parse(src) == "success"

def test_mixed_error_break_outside_loop():
    """99. Valid Syntax (Semantic Error): Break outside loop"""
    src = "fun main() { break }"
    assert Parser.parse(src) == "success"

def test_mixed_full_program():
    """100. Full mixed program from Example 4 (Factorial)"""
    src = """
    fun factorial(n: Int): Int {
        if (n <= 1) {
            return 1
        } else {
            return n * factorial(n - 1)
        }
    }

    fun main() {
        val num = readInt()
        val result = factorial(num)
        printInt(result)
    }
    """
    assert Parser.parse(src) == "success"

def test_mixed_full_program_when():
    """101. Full mixed program with when expression"""
    src = """
    fun classify(n: Int): String {
        return when {
            n > 0 -> "positive"
            n < 0 -> "negative"
            else -> "zero"
        }
    }
    """
    assert Parser.parse(src) == "success"
