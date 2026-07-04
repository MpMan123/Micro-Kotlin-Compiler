grammar MKotlin;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
    else:
        return super().emit()
}

options {
	language=Python3;
}

// ===== Luật cú pháp (parser) =====
program: funcdecl+ EOF ;
funcdecl:
    // TODO: viết luật `funcdecl` theo đặc tả (thay HOLE)
    rettyp ID LP ( | params) RP block;
rettyp:
    // TODO: viết luật `rettyp` theo đặc tả (thay HOLE)
    VOID | typ ;
typ: basic (LSQ RSQ)* ;
basic: INT | FLOAT | BOOL ;
params:
    // TODO: viết luật `params` theo đặc tả (thay HOLE)
    param (COMMA params) | param;
param:
    // TODO: viết luật `param` theo đặc tả (thay HOLE)
    basic ID ;
block: LB stmt* RB ;
stmt: vardecl | retstmt | exprstmt | block ;
vardecl: typ ID (EQ expr)? SEMI ;
retstmt: RETURN expr? SEMI ;
exprstmt: expr SEMI ;
expr: ID LP args? RP | ID | INTLIT ;
args: expr (COMMA expr)* ;

// ===== Luật từ vựng (lexer) =====
VOID:'void';
INT:'int';
FLOAT:'float';
BOOL:'bool';
RETURN:'return';
LP:'(';
RP:')';
LB:'{';
RB:'}';
LSQ:'[';
RSQ:']';
COMMA:',';
SEMI:';';
EQ:'=';
ID:[a-zA-Z_][a-zA-Z0-9_]*;
INTLIT:[0-9]+;
HOLE: '@@TODO@@' ; // placeholder cho khung; xoá khi hoàn thành

WS: [ \t\r\n]+ -> skip ;
ERROR_CHAR: . ;