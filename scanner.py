# List of token names.   This is always required
tokens = (
   'ENTERO', 'REAL', 'BOOLEANO', 'SI', 'SINO', 'MIENTRAS', 'CLASE', 'PRINCIPAL', 'CARACTERES',
   'ENTRADA', 'GLOBAL', 'SALIDA', 'FUNCION', 'CICLO', 'ENTONCES', 'NULO', 'RETORNO', 'SEMICOLON', 'PUNTO',
   'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'EXP_OPERADOR',
   'TERM_OPERADOR', 'RESI_OPERADOR', 'KEYWORD_PROGRAM', 'KEYWORD_TYPE_ENTERO', 'KEYWORD_TYPE_REAL', 'KEYWORD_TYPE_BOOLEANO',
   'KEYWORD_SI', 'KEYWORD_SINO', 'KEYWORD_MIENTRAS', 'KEYWORD_CLASE', 'KEYWORD_PRINCIPAL', 'KEYWORD_TYPE_CARACTERES',
   'KEYWORD_ENTRADA', 'KEYWORD_SALIDA', 'KEYWORD_FUNCION', 'KEYWORD_CICLO', 'KEYWORD_ENTONCES', 'KEYWORD_NULO', 'KEYWORD_RETORNO',
)

reserved = {
    'program' : 'KEYWORD_PROGRAM',
    'int' : 'KEYWORD_TYPE_ENTERO',
    'float' : 'KEYWORD_TYPE_REAL',
    'bool' : 'KEYWORD_TYPE_BOOLEANO',
    'if' : 'KEYWORD_SI',
    'else' : 'KEYWORD_SINO',
    'while' : 'KEYWORD_MIENTRAS',
    'class' : 'KEYWORD_CLASE',
    'main' : 'KEYWORD_PRINCIPAL',
    'char' : 'KEYWORD_TYPE_CARACTERES',
    'input' : 'KEYWORD_ENTRADA',
    'print' : 'KEYWORD_SALIDA',
    'function' : 'KEYWORD_FUNCION',
    'for' : 'KEYWORD_CICLO',
    'else' : 'KEYWORD_ENTONCES',
    'null' : 'KEYWORD_NULO',
    'return' : 'KEYWORD_RETORNO',
}

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
t_OPERADOR_COMPARATIVO = r'[<][>]|[>]|[<]|[>=]|[<=]|[==]'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'
t_RESI_OPERADOR = r'\%'

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

def p_Tipo(t):
    '''Tipo : KEYWORD_TYPE_ENTERO
    | KEYWORD_TYPE_REAL
    | KEYWORD_TYPE_BOOLEANO
    | KEYWORD_TYPE_CARACTERES
    | IDENTIFICADOR
    '''
def p_Asignacion(t):
    ''' Asignacion : IDENTIFICADOR AsignaA OPERADOR_IGUAL Expression SEMICOLON

    '''
def p_Declaracion(t):
   '''
   Declaracion: 
   '''
def p_AsignaA(t):
    '''
    ASIGNAA: BRACKET_IZQ Expression BRACKET_DER AsignaB 
    |
    | empty
    '''
def p_AsignaB(t):
  '''
  AsignaB: BRACKET_IZQ Expression BRACKET_DER
  | empty
  '''
def p_Funcion(t):
  '''
  Funcion : KEYWORD_FUNCTION Tipo Funcion Bloque
  '''

def p_FuncionA(t):
  '''
  FuncionA : PARENTESIS_IZQ FuncionB PARENTESIS_DER
  '''
def p_FuncionB(t):
  '''
  FuncionB: Parametro FuncionC
    | empty
  '''
def p_FuncionC(t):
  '''
  FuncionC: COMMA Parametro
    | empty
  '''
def p_Parametro(t):
  '''
  Parametro: TIPO IDENTIFICADOR
  '''

def p_Clase(t):
  '''
   Clase: KEYWORD_CLASE IDENTIFICADOR Bloque_Clase
  '''

def p_Bloque_Clase(t):
'''
  Bloque_Clase: BRACKET_IZQ Bloque_ClaseA BRACKET_DER SEMICOLON
'''

def p_Bloque_ClaseA(t):
'''
  Bloque_ClaseA: Bloque_ClaseB Bloque_ClaseC
  | empty
'''

def p_Bloque_ClaseB(t):
'''
  Bloque_ClaseB: Declaracion_Variable
  | empty
'''

def p_Bloque_ClaseC(t):
'''
  Bloque_ClaseC: Funcion
  | empty
'''

def p_Ciclo(t):
'''
  Ciclo: KEYWORD_MIENTRAS PARENTESIS_IZQ Expresion PARENTESIS_DER Bloque
'''

def p_Entrada(t):
'''
  Entrada: KEYWORD_ENTRADA IDENTIFICADOR SEMICOLON
'''