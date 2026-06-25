grammar MKotlin;

@lexer::header {
from src.grammar.lexererr import (
    ErrorToken,
    UncloseString,
    IllegalEscape,
)
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit()
        raise UncloseString(result.text[1:])
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        raise IllegalEscape(result.text[1:])
    elif tk == self.ERROR_TOKEN:
        result = super().emit()
        raise ErrorToken(result.text)
    elif tk == self.STRING_LIT:
        result = super().emit()
        result.text = result.text[1:-1]
        return result
    else:
        return super().emit()
}

options {
    language = Python3;
}

// TODO: Define parser rules here
// See mkotlin_specification.md — Grammar Summary
//
// Hints:
// - program: optional leading newlines, declList, EOF
// - decl: dataClassDecl | funcDecl
// - statements separated by sep (NEWLINE | SEMI)
// - expression precedence (low -> high): assignment, ||, &&, ==/!=,
//   </<=/>/>=, +/-, */%, unary, postfix (. / call / ++/--), primary
// - when/if as both statement and expression forms


/****************************************************************************/
/*																	 		*/
/*								1.Program Structure							*/
/* 																			*/
/****************************************************************************/
program
    : (decl | NEWLINE)* EOF
    ;
decl
    : dataClass
    | funcDecl
    ;
funcDecl
    : FUN ID LP parameterList? RP (COLON returnType)? blockStmt
    ;
parameterList
    : parameter (COMMA parameter)*
    ;
parameter
    : ID COLON dataType
    ;
returnType
    : dataType | TYPE_UNIT
    ;
primaryExpr
    : ID | INT_LIT | STRING_LIT | FLOAT_LIT | TRUE | FALSE | LP expr RP | whenExpr | ifExpr;
ifExpr
    : IF LP booleanExpr RP expr ELSE expr;
whenExpr
    : WHEN (LP expr RP)? LB (whenBranch | NEWLINE | SEMICOLON)* elseBranch (NEWLINE | SEMICOLON)* RB
    ;
whenBranch
    : expr (COMMA expr)* ARROW stmt
    ;
elseBranch
    : ELSE ARROW stmt
    ;
functionCallExpr
    : ID LP argumentList? RP;
postfixExpr
    : (primaryExpr | functionCallExpr) (INC | DEC | DOT ID | LP argumentList? RP)*;
unaryExpr
    : (MINUS | PLUS | LOGIC_NOT | INC | DEC) unaryExpr | postfixExpr;
multiplicativeExpr
    : unaryExpr ((MUL | DIV | MOD) multiplicativeExpr)*;
additiveExpr
    : multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)*;
rangeExpr
    : additiveExpr (RANGE additiveExpr)?;
relationalExpr
    : rangeExpr ((LT | GT | GTE | LTE) rangeExpr)*;
equalityExpr
    : relationalExpr ((EQ | NOT_EQ) relationalExpr)*;
logicAndExpr
    : equalityExpr (LOGIC_AND equalityExpr)*;
logicOrExpr
    : logicAndExpr (LOGIC_OR logicAndExpr)*;
assignmentExpr
    : (ID ASSIGN)* logicOrExpr;
expr
    : assignmentExpr;
booleanExpr
    : logicOrExpr;


/****************************************************************************/
/*																	 		*/
/*								1.Type System							    */
/* 																			*/
/****************************************************************************/
//-------Primitive Types-------//
TYPE_INT     : 'Int' ;
TYPE_FLOAT   : 'Float' ;
TYPE_BOOLEAN : 'Boolean' ;
TYPE_STRING  : 'String' ;
TYPE_UNIT    : 'Unit' ;
primitiveType
    : TYPE_INT | TYPE_FLOAT | TYPE_BOOLEAN | TYPE_STRING;

/****************************************************************************/
/*																	 		*/
/*								3. Data Class							    */
/* 																			*/
/****************************************************************************/
dataClass
    : DATA_CLASS ID LP dataClassMemberList?  RP;
dataClassMemberList
    : dataClassMember (COMMA dataClassMember)* COMMA?;
dataClassMember
    : ID COLON dataType;
// datatype created by user
dataType
    : primitiveType | ID;

/****************************************************/
/*													*/
/*              3.1. Data Class Variable            */
/*            Declaration and Construction          */
/* 													*/
/****************************************************/
constructor
    : ID LP argumentList? RP;
argumentList
    : expr (COMMA expr)*;
/****************************************************/
/*													*/
/*                  3.2. Member Access              */
/* 													*/
/****************************************************/
memberAccess
    : ID (DOT ID)+;
/****************************************************************************/
/*																	 		*/
/*							4. Variable Declaration							*/
/* 																			*/
/****************************************************************************/
variableDeclarationExpr
    : VAL ID (COLON dataType)? ASSIGN expr
    | VAR ID (COLON dataType)? (ASSIGN expr)?;

/****************************************************************************/
/*																	 		*/
/*							    4. Statement            	    			*/
/* 																			*/
/****************************************************************************/
variableDeclareStmt
    : variableDeclarationExpr;
ifStmt
    : IF LP booleanExpr RP stmt+ (ELSE stmt+)?;
blockStmt
    : LB (stmt | NEWLINE | SEMICOLON)* RB;
whileStmt
    : WHILE booleanExpr (stmt | blockStmt);
forStmt
    : FOR LP ID IN INT_LIT RANGE INT_LIT RP stmt*;
whenStmt
    : WHEN (LP expr RP)? LB (whenBranch | NEWLINE | SEMICOLON)* (elseBranch (NEWLINE | SEMICOLON)*)? RB;
breakStmt
    : BREAK;
continueStmt
    : CONTINUE;
returnStmt
    : RETURN expr?;
expressionStmt
    : expr;
stmt
    : variableDeclareStmt
    | ifStmt
    | whileStmt
    | forStmt
    | whenStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | expressionStmt
    | blockStmt;

// TODO: Define lexer rules here
// Keywords, operators, literals, comments, NEWLINE (statement separator), ...
//
// Hints:
// - Error detection order: ILLEGAL_ESCAPE -> UNCLOSE_STRING -> STRINGLIT -> ...
// - STRINGLIT must strip enclosing quotes: self.text = self.text[1:-1]
// - FLOATLIT must precede INTLIT
// - Keyword/type rules must precede IDENT
// - NEWLINE is a real token — do NOT skip newlines in WS

INLINE_COMMENT: '//' .*? ('\n' | '\r\n' | EOF) -> skip ;
BLOCK_COMMENT: [/][*].*?[*][/] -> skip;

// --- LEXER RULES FOR KEYWORDS ---
DATA_CLASS: 'data class' ;
BREAK    : 'break' ;
CLASS    : 'class' ;
CONTINUE : 'continue' ;
DATA     : 'data' ;
ELSE     : 'else' ;
FALSE    : 'false' ;
FOR      : 'for' ;
FUN      : 'fun' ;
IF       : 'if' ;
IN       : 'in' ;
IS       : 'is' ;
RETURN   : 'return' ;
TRUE     : 'true' ;
VAL      : 'val' ;
VAR      : 'var' ;
WHEN     : 'when' ;
WHILE    : 'while' ;

// --- LEXER RULES FOR OPERATORS ---

// Assignment
ASSIGN   : '=' ;

// Arithmetic
PLUS     : '+' ;
MINUS    : '-' ;
MUL      : '*' ;
DIV      : '/' ;
MOD      : '%' ;

// Unary
INC      : '++' ;
DEC      : '--' ;

// Relational
EQ       : '==' ;
NOT_EQ   : '!=' ;
LT       : '<' ;
GT       : '>' ;
LTE      : '<=' ;
GTE      : '>=' ;

// Logic
LOGIC_OR  : '||' ;
LOGIC_AND : '&&' ;
LOGIC_NOT : '!' ;

DOT      : '.' ;
RANGE    : '..' ;

// --- LEXER RULES FOR SEPARATOR ---
LB      : '{';
RB      : '}';
LP      : '(';
RP      : ')';
SEMICOLON: ';';
COMMA   : ',';
COLON   : ':';
ARROW   : '->';

ID: [a-zA-Z_][a-zA-Z0-9_]*;

// --- FLOAT LITERAL ---
fragment F_DECIMAL: '.'[0-9]+;
fragment F_DIGIT: [0-9]+;
fragment F_EXP: [Ee][+-]?[0-9]+;
fragment F_TRAIL: [Ff];

FLOAT_LIT
        : F_DIGIT F_DECIMAL F_EXP? F_TRAIL?
        | F_DIGIT '.' F_EXP? F_TRAIL?
        | F_DECIMAL F_EXP? F_TRAIL?
        | F_DIGIT F_EXP F_TRAIL?
        | F_DIGIT F_TRAIL
    ;

// --- INTEGER LITERAL ---
INT_LIT: '0' | [1-9][0-9]*('_'[0-9]+)*;

// --- BOOLEAN LITERAL --- 
BOOL_LIT: TRUE | FALSE;



// --- STRING LITERAL ---
// --- LEXICAL ERROR TOKENS --- 
NEWLINE: '\r'?'\n';
HAHA:
    INVALID_ESCAPE;
ILLEGAL_ESCAPE 
    : '"' (CHAR | VALID_ESCAPE)* INVALID_ESCAPE ;
UNCLOSE_STRING
    : '"' (CHAR | VALID_ESCAPE)* (NEWLINE | EOF) ;
STRING_LIT
    : '"' (CHAR | VALID_ESCAPE)* '"';
fragment VALID_ESCAPE
    : '\\' [bfrnt"\\$];
fragment INVALID_ESCAPE
    : '\\' ~[bfrnt"\\$\r\n];
fragment CHAR
    : ~["\\\n\r$];

WS : [ \t\f]+ -> skip ;    

ERROR_TOKEN
    : . ;