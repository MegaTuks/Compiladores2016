#Andres Marcelo Garza Cantu A00814236
#Ruben Alejandro Hernandez Gonzalez A01175209
# List of token names.   This is always required
tokens = [
   'SEMICOLON', 'PUNTO',
   'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 
   'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'EXP_OPERADOR','TERM_OPERADOR', 'OPERADOR_DOSPUNTOS', 'RESI_OPERADOR',
    'IDENTIFICADOR' , 'CONST_NUMERO_ENT', 'CONST_NUMERO_REAL',
   'CONST_CARACTERES', 'CONST_BOOLEANO'
]

reserved = {
    'programa' : 'KEYWORD_PROGRAMA',
    'entero' : 'KEYWORD_TYPE_ENTERO',    
    'real' : 'KEYWORD_TYPE_REAL',
    'booleano' : 'KEYWORD_TYPE_BOOLEANO',
    'si' : 'KEYWORD_SI',
    'sino' : 'KEYWORD_SINO',
    'mientras' : 'KEYWORD_MIENTRAS',
    'clase' : 'KEYWORD_CLASE',
    'principal' : 'KEYWORD_PRINCIPAL',
    'caracter' : 'KEYWORD_TYPE_CARACTERES',
    'entrada' : 'KEYWORD_ENTRADA',
    'salida' : 'KEYWORD_SALIDA',
    'funcion' : 'KEYWORD_FUNCION',
    'ciclo' : 'KEYWORD_CICLO',
    'entonces' : 'KEYWORD_ENTONCES',
    'nulo' : 'KEYWORD_NULO',
    'retorno' : 'KEYWORD_RETORNO',
    'verdadero':'KEYWORD_VERDADERO',
    'falso': 'KEYWORD_FALSO'
}
tokens += reserved.values()
# Tokens
t_SEMICOLON = r'\;'
t_PUNTO = r'[\.]'
t_COMMA = r'[\,]'
t_COLON = r'\:'
t_BRACKET_IZQ = r'\{'
t_BRACKET_DER = r'\}'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_OPERADOR_IGUAL  = r'\='
t_OPERADOR_DOSPUNTOS  = r'\:'
t_OPERADOR_COMPARATIVO = r'[<][>]|[>]|[<]|[>=]|[<=]|[==]'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'
t_RESI_OPERADOR = r'\%'

def t_CONST_NUMERO_REAL(t):
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

def t_CONST_BOOLEANO(t):
    r'[VERDADERO|FASLO]'
    return t 

t_CONST_CARACTERES = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!]*\"'

def t_error(t):
    print("Caracter  Ilegal'%s'" % t.value[0])
    t.lexer.skip(1)
    t_CONST_STRING = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!]*\"'



import ply.lex as lex
lexer = lex.lex()

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def p_Programa(t):
  '''
    Programa :  ProgramaA FuncionPrincipal
  '''

def p_Tipo(t):
    '''Tipo : KEYWORD_TYPE_ENTERO
    | KEYWORD_TYPE_REAL
    | KEYWORD_TYPE_BOOLEANO
    | KEYWORD_TYPE_CARACTERES
    | IDENTIFICADOR
    '''
def p_Asignacion(t):
    ''' Asignacion : IDENTIFICADOR AsignaClass OPERADOR_IGUAL Expresion SEMICOLON
    '''
def p_AsignaClass(t):
  '''
  AsignaClass :  AsignaA
  | PUNTO IDENTIFICADOR AsignaA
  | empty
  '''
def p_AsignaA(t):
    '''
    AsignaA : CORCHETE_IZQ Expresion CORCHETE_DER AsignaB 
    | empty
    '''
def p_AsignaB(t):
  '''
  AsignaB : CORCHETE_IZQ Expresion CORCHETE_DER
  | empty
  '''
def p_Funcion(t):
  '''
  Funcion : KEYWORD_FUNCION Tipo IDENTIFICADOR PARENTESIS_IZQ FuncionA PARENTESIS_DER Bloque
  '''

def p_FuncionA(t):
  '''
  FuncionA : Parametro FuncionB
    | empty
  '''
def p_FuncionB(t):
  '''
  FuncionB : COMMA FuncionA
    | empty
  '''
def p_Parametro(t):
  '''
  Parametro : Tipo IDENTIFICADOR
  '''

def p_Bloque(t):
  '''
  Bloque : BRACKET_IZQ BloqueA BRACKET_DER
  '''

def p_BloqueA(t):
  '''
  BloqueA : Declaracion BloqueB
  | Asignacion BloqueB
  | LlamadaFuncion BloqueB
  | Ciclo BloqueB
  | Condicion BloqueB
  | Entrada BloqueB
  | Salida BloqueB
  | KEYWORD_RETORNO ValorSalida
  '''
def p_BloqueB(t):
  '''
  BloqueB :  BloqueA
  | empty
  '''

def p_Clase(t):
  '''
   Clase : KEYWORD_CLASE IDENTIFICADOR Bloque_Clase
  '''
def p_Bloque_Clase(t):
  '''
    Bloque_Clase : BRACKET_IZQ Bloque_ClaseA BRACKET_DER SEMICOLON
  '''

def p_Bloque_ClaseA(t):
  '''
    Bloque_ClaseA : Bloque_ClaseB Bloque_ClaseC
    | empty
  '''
def p_Bloque_ClaseB(t):
  '''
    Bloque_ClaseB : Declaracion Bloque_ClaseB
    | empty
  '''
def p_Bloque_ClaseC(t):
  '''
    Bloque_ClaseC : Funcion Bloque_ClaseC
    | empty
  '''
def p_Ciclo(t):
  '''
    Ciclo : KEYWORD_MIENTRAS PARENTESIS_IZQ Expresion PARENTESIS_DER Bloque
  '''
def p_Entrada(t):
  '''
    Entrada : KEYWORD_ENTRADA IDENTIFICADOR SEMICOLON
  '''
  
def p_Salida(t):
  '''
    Salida : KEYWORD_SALIDA IDENTIFICADOR Expresion SEMICOLON
  '''

def p_Condicion(t):
  '''
    Condicion : KEYWORD_SI PARENTESIS_IZQ Expresion PARENTESIS_DER Bloque CondicionA
  '''
def p_CondicionA(t):
  '''
    CondicionA : KEYWORD_SINO Bloque
    | empty
  '''

def p_Expresion(t):
  '''
    Expresion : Exp ExpresionA
  '''

def p_ExpresionA(t):
  '''
    ExpresionA : OPERADOR_COMPARATIVO Exp
    | empty
  '''

def p_Exp(t):
  '''
    Exp : Termino ExpA
  '''

def p_ExpA(t):
  '''
    ExpA : EXP_OPERADOR Exp
    | empty
  '''

def p_Termino(t):
  '''
    Termino : Factor TerminoA
    | empty
  '''

def p_TerminoA(t):
  '''
    TerminoA : TERM_OPERADOR Termino
    | empty
  '''

def p_Factor(t):
  '''
    Factor : ValorSalida
    | PARENTESIS_IZQ Exp PARENTESIS_DER
  '''

def p_LlamadaFuncion(p):
  '''
    LlamadaFuncion : IDENTIFICADOR PARENTESIS_IZQ LlamadaFuncionA PARENTESIS_DER
  '''

def p_LlamadaFuncionA(p):
  '''
    LlamadaFuncionA : Expresion LlamadaFuncionB
  '''

def p_LlamadaFuncionB(p):
  '''
    LlamadaFuncionB : COMMA LlamadaFuncionA
    | empty
  '''

def p_Declaracion(t):
   '''
   Declaracion : Parametro AsignaA SEMICOLON
   '''
def p_ProgramaA(t):
  '''
    ProgramaA : Declaracion ProgramaA
    | Funcion ProgramaA
    | Clase ProgramaA
    | empty
  '''
def p_FuncionPrincipal(t):
  '''
  FuncionPrincipal : KEYWORD_FUNCION KEYWORD_PRINCIPAL PARENTESIS_IZQ PARENTESIS_DER Bloque
  '''
def p_ValorSalida(t):
  '''
    ValorSalida : CONST_NUMERO_ENT
    | CONST_CARACTERES
    | CONST_NUMERO_REAL
    | CONST_BOOLEANO
    | KEYWORD_NULO
    | LlamadaFuncion
    | IDENTIFICADOR  ValorSalidaB
  '''
def p_ValorSalidaB(t):
  '''
    ValorSalidaB : PUNTO IDENTIFICADOR ValorSalidaC
    | empty
  '''
def p_ValorSalidaC(t):
  '''
    ValorSalidaC : PARENTESIS_IZQ LlamadaFuncionA PARENTESIS_DER
    | AsignaA ValorSalidaB
    | empty
  '''

import ply.yacc as yacc
parser = yacc.yacc(start= 'Programa')

data = '''
real PATO;
funcion principal()
{
entero numerador;
numerador = 10 - 5;
salida numerador;
}
'''

lexer.input(data)

result = parser.parse(lexer=lexer)
print(result)
