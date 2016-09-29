# List of token names.   This is always required
tokens = (
   'ENTERO',
   'REAL',
   'BOOLEANO',
   'SI',
   'SINO',
   'MIENTRAS',
   'CLASE',
   'PRINCIPAL',
   'CARACTERES',
   'ENTRADA',
   'GLOBAL',
   'SALIDA',
   'FUNCION',
   'CICLO',
   'ENTONCES',
   'NULO',
   'RETORNO'
)

# Tokens
t_SEMICOLON = r'\;'
t_PUNTO = r'[\.]'
t_COMMA = r'[\,]'
t_COLON = r'\:'
t_BRACKET_IZQ = r'\{'
t_BRACKET_DER = r'\}'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_OPERADOR_IGUAL  = r'\='
t_OPERADOR_COMPARATIVO = r'[<][>]|[>]|[<]'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'

def t_CONST_NUMERO_FLOTANTE(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t
def t_CONST_NUMERO_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_ERROR(t):
    print("Caracter  Ilegal'%s'" % t.value[0])
    t.lexer.skip(1)
t_CONST_STRING = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!]*\"'


import ply.lex as lex
lexer = lex.lex()


TIPO : 'ENTERO'
	 | 'REAL'
	 | 'BOOLEANO'
	 | 'CARACTERES'
	 | id

ASIGNACION : id ASIGNAA ;
	
ASIGNAA : [ EXP ] ASIGNB
	| empty

ASIGNB : [EXP]
	| empty

FUNCION : FUNCION TIPO FUNCIONA BLOQUE

FUNCIONA : ( FUNCIONB )

FUNCIONB : 
	| empty



