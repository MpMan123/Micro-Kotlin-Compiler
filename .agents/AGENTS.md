# Micro-Kotlin Compiler Project Guidelines

This file provides context and rules for agents working on the Micro-Kotlin (MKotlin) Compiler project.

## 1. Project Overview & Key Documents
*   **Purpose**: A compiler for a subset of Kotlin (Micro-Kotlin) built using Python and ANTLR4.
*   **Key References**:
    *   `mkotlin_specification.md`: The primary language specification (grammar, types, statements, etc.).
    *   `mkotlin-semantic_constraints_and_errors.md`: Defines static semantic constraints and the exact 8 error types the static checker must raise.
    *   `mkotlin-ast_representation.md`: Details the AST node structures.
    *   `README.md`: General project overview and setup instructions.

## 2. Build & Test Commands
Use the central `run.py` script for all project tasks:
*   **Setup Environment**: `python run.py setup`
*   **Build Grammar**: `python run.py build` (Generates ANTLR lexer/parser/visitor from `src/grammar/MKotlin.g4`).
*   **Run Lexer Tests**: `python run.py test-lexer`
*   **Run Parser Tests**: `python run.py test-parser`
*   **Run AST Tests**: `python run.py test-ast`
*   **Run Checker Tests**: `python run.py test-checker`
*   **Run Codegen Tests**: `python run.py test-codegen`
*   **Run All Tests**: `python run.py test`

## 3. Important Implementation Details & Quirks
### Lexer (`src/grammar/MKotlin.g4`)
*   **Lexical Errors**: The testing utility (`Tokenizer.tokens` in `tests/utils.py`) catches custom lexical errors (`ErrorToken`, `UncloseString`, `IllegalEscape`) and formats them with an `Error: ` prefix. Tests in `test_lexer.py` **must** assert against this prefix (e.g., `assert Tokenizer.tokens("@") == "Error: @"`).
*   **Comments**: Unlike many grammars where comments are sent to the `HIDDEN` channel or `skip`ped, the current MKotlin grammar emits `INLINE_COMMENT` and `BLOCK_COMMENT` as regular tokens to the parser. Test cases must account for comment tokens in the output string (e.g., `"val,x,// comment,EOF"`).
*   **String Literals (`STRING_LIT`)**:
    *   Strings handle escape sequences explicitly (`\n`, `\t`, `\r`, `\b`, `\f`, `\\`, `\"`, `\$`).
    *   Unescaped `$` signs in strings are not supported and will result in an immediate `ERROR_TOKEN` on the opening quote (yielding `Error: "`).
    *   `ILLEGAL_ESCAPE` errors return the content up to the illegal escape.
    *   `UNCLOSE_STRING` errors return the unclosed content up to the newline or EOF.

### Checker (`src/semantics/static_checker.py`)
*   Must raise one of the 8 specific exceptions defined in `src/semantics/static_error.py`.
*   Error reporting stops at the **first** error encountered during a deterministic traversal (top-to-bottom, left-to-right).

## 4. Coding Standards
*   Write clear, descriptive, and numbered test cases when expanding test suites (e.g., `test_string_empty()`, `test_string_simple()`).
*   Always ensure the code compiles (`python run.py build`) and tests pass before concluding a task.
