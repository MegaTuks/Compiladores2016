# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209
# List of token names.   This is always required
tokens = [
    'SEMICOLON', 'PUNTO',
    'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'EXP_OPERADOR', 'TERM_OPERADOR', 'OPERADOR_DOSPUNTOS', 'RESI_OPERADOR',
    'IDENTIFICADOR', 'CONST_NUMERO_ENT', 'CONST_NUMERO_REAL', 'IDENTIFICADOR_CLASE',
    'CONST_CARACTERES', 'CONST_BOOLEANO'
]
llavetablactual = ""
llavetablaclase = None # se usa para asegurar que haya herencia
buscadorClase = None #se usa para buscar en las tablas clase si existen las variables o funciones a llamar

reserved = {
    'entero': 'KEYWORD_TYPE_ENTERO',
    'real': 'KEYWORD_TYPE_REAL',
    'booleano': 'KEYWORD_TYPE_BOOLEANO',
    'si': 'KEYWORD_SI',
    'sino': 'KEYWORD_SINO',
    'mientras': 'KEYWORD_MIENTRAS',
    'clase': 'KEYWORD_CLASE',
    'principal': 'KEYWORD_PRINCIPAL',
    'caracter': 'KEYWORD_TYPE_CARACTERES',
    'entrada': 'KEYWORD_ENTRADA',
    'salida': 'KEYWORD_SALIDA',
    'funcion': 'KEYWORD_FUNCION',
    'entonces': 'KEYWORD_ENTONCES',
    'nulo': 'KEYWORD_NULO',
    'retorno': 'KEYWORD_RETORNO',
    'verdadero': 'KEYWORD_VERDADERO',
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
t_OPERADOR_IGUAL = r'\='
t_OPERADOR_COMPARATIVO = r'[>]|[<]'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'
t_RESI_OPERADOR = r'\%'
t_ignore = ' \t\n\r'


def t_CONST_NUMERO_REAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CONST_NUMERO_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFICADOR(t):
    r'[a-z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_IDENTIFICADOR_CLASE(t):
    r'[A-Z][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_CONST_BOOLEANO(t):
    r'[VERDADERO|FALSO]'
    return t


t_CONST_CARACTERES = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!\ ]*\"'


def t_error(t):
    print("Caracter  Ilegal>>> '%s'  <<<<" % t.value[0])
    t.lexer.skip(1)


class TablaSimbolos:
    def __init__(self):
        self.simbolos = dict()
        self.hijos = list()
        self.padre = None
        #agregar atributo name?
    def insertar(self, id, tipo):
        self.simbolos[id] = tipo

    def buscar(self, id):
        return self.simbolos.get(id)

    def agregarHijo(self, hijo):
        self.hijos.append(hijo)

    def agregarPadre(self, pad):
        self.padre = pad

    def devolverPadre(self):
        if(self.padre is None):
            print("no hay padre al cual ir");
        else:
            return self.padre

    def buscarHijos(self,name):
        for hijo in self.hijos:
            existe = hijo.buscar(name)
            if (existe is not None):
                return hijo



   # def __str__(self):


tablaSimbolosActual = TablaSimbolos()
tablaSimbolosActual.insertar('global','global')
tablaGlobal =  tablaSimbolosActual



import ply.lex as lex

lexer = lex.lex()


def p_Programa(t):
    '''
      Programa :  ProgramaA FuncionPrincipal
    '''
    print('La sintaxis del programa paso')
    #print ('Global scope symbols:')
    global  tablaSimbolosActual
    print('global scope symbols:',tablaSimbolosActual.simbolos)
    # print('\n', tablaSimbolosActual.simbolos)

def p_empty(p):
    'empty :'
    pass


def p_error(t):
    print("Syntax error at '%s'" % t.value)


def p_Tipo(t):
    '''Tipo : KEYWORD_TYPE_ENTERO
    | KEYWORD_TYPE_REAL
    | KEYWORD_TYPE_BOOLEANO
    | KEYWORD_TYPE_CARACTERES
    | IDENTIFICADOR_CLASE_AUX
    '''
    t[0] = t[1]

def p_IDENTIFICADOR_CLASE_AUX(t):
    '''
    IDENTIFICADOR_CLASE_AUX : IDENTIFICADOR_CLASE
    '''
    existe = tablaGlobal.buscar(t[1])
    if(existe is None):
        print("Tipo no existente, clase no declarada")
        raise  SyntaxError

def p_Asignacion(t):
    ''' Asignacion : AsignaAux AsignaClass OPERADOR_IGUAL Expresion SEMICOLON
    '''

def p_AsignaAux(t):
    '''
    AsignaAux : IDENTIFICADOR
    '''
    global tablaSimbolosActual, tablaGlobal,buscadorClase
    existe  = tablaSimbolosActual.buscar(t[1])
    if (buscadorClase is None):
        print ("checalo: ", existe)
        if (existe is None):
            print("variable no existe en este punto")
        elif (not (existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero')):
            if(existe is 'funcion'):
                print("no puedes hacer asignacion con funcion")
            else:
               buscadorClase = tablaGlobal.buscarHijos(existe)
        elif(existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero'):
            buscadorClase = None #funcion que encuentra el valor atomico del chiste
    else:
        existe =  buscadorClase.buscar(t[1])
        if (existe is None):
            print("variable no existe en este punto")
        elif (existe is not('real' or 'booleano' or 'caracter' or 'entero')):
            if(existe is 'funcion'):
                print("no puedes hacer asignacion con funcion")
            else:
               buscadorClase = tablaGlobal.buscarHijos(existe)

def p_AsignaClass(t):
    '''
    AsignaClass :  AsignaA
    | PUNTO AsignaAux AsignaA
    '''


def p_AsignaA(t):
    '''
    AsignaA : CORCHETE_IZQ Expresion CORCHETE_DER AsignaB
    | empty
    '''


def p_AsignaB(t):
    '''
    AsignaB : CORCHETE_IZQ Expresion CORCHETE_DER
    '''


def p_Funcion(t):
    '''
    Funcion : FuncionAux PARENTESIS_IZQ FuncionA PARENTESIS_DER Bloque Fin_Bloque
    '''

def p_FuncionAux(t):
    '''
    FuncionAux : KEYWORD_FUNCION Tipo IDENTIFICADOR
    '''
    global tablaSimbolosActual
    existe = tablaSimbolosActual.buscar(t[3])
    if (existe is None):
        tablaSimbolosActual.insertar(t[3], t[1])  # guarda que es Tipo funcion en la tabla de simbolos
        print("insertar funcion en tabla", tablaSimbolosActual.simbolos)
        tablaF = TablaSimbolos()
        tablaF.insertar('funcion','funcion')
        tablaF.insertar(t[3], t[2])
        tablaSimbolosActual.agregarHijo(tablaF)
        tablaF.agregarPadre(tablaSimbolosActual)  #
        tablaSimbolosActual = tablaF
        print("funcion de ahorita", tablaSimbolosActual.simbolos)
    else:
        print("Funcion previamente declarada")
        raise SyntaxError

def p_Fin_Bloque(t):
    '''
    Fin_Bloque :
    '''
    global tablaSimbolosActual
    print("salir de la funcion");
    tablaSimbolosActual = tablaSimbolosActual.padre




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
    global tablaSimbolosActual
    existe = tablaSimbolosActual.buscar(t[2])
    if (existe is None):
        tablaSimbolosActual.insertar(t[2],t[1])
        print("simbolos insertados",tablaSimbolosActual.simbolos)
    else:
        print("variable previamente declarada")
        raise SyntaxError


def p_Bloque(t):
    '''
    Bloque : BRACKET_IZQ BloqueA BRACKET_DER
    '''


def p_BloqueA(t):
    '''
    BloqueA : Declaracion BloqueB
    | Asignacion BloqueB
    | LlamadaFuncionPadre BloqueB
    | LlamadaFuncionClasePadre BloqueB
    | Ciclo BloqueB
    | Condicion BloqueB
    | Entrada BloqueB
    | Salida BloqueB
    | KEYWORD_RETORNO ValorSalida SEMICOLON
    '''


def p_BloqueB(t):
    '''
    BloqueB :  BloqueA
    | empty
    '''


def p_Clase(t):
    '''
     Clase : ClaseAux Bloque_Clase
    '''

def p_ClaseAux(t):
    '''
     ClaseAux : KEYWORD_CLASE IDENTIFICADOR_CLASE ClaseA
    '''
    global tablaSimbolosActual,llavetablaclase
    existe = tablaSimbolosActual.buscar(t[2])
    print("ver tabla antes de entrar a clase", tablaSimbolosActual.simbolos)

    if (existe is None):
        if (llavetablaclase is None):
            tablaSimbolosActual.insertar(t[2], t[1])
            tablaC = TablaSimbolos()
            tablaC.insertar('clase','clase')
            tablaC.agregarPadre(tablaSimbolosActual)
            tablaSimbolosActual.agregarHijo(tablaC)
            tablaSimbolosActual = tablaC
            print("insertaste la clase", tablaSimbolosActual.padre.simbolos)
        else:
            heredado = t[1] + "," + llavetablaclase
            tablaSimbolosActual.insertar(t[2], heredado)
            tablaC = TablaSimbolos()
            tablaC.agregarPadre(tablaSimbolosActual)
            tablaSimbolosActual.agregarHijo(tablaC)
            tablaSimbolosActual = tablaC
            print("insertaste la clase con herencia", tablaSimbolosActual.padre.simbolos)
            llavetablaclase = ""
    else:
        print("Clase ya existente ");
        raise SyntaxError

def p_ClaseA(t):
    '''
    ClaseA : COLON IDENTIFICADOR_CLASE
     | empty
    '''
    global tablaSimbolosActual,llavetablaclase
    if(len(t) == 3):
        existe = tablaSimbolosActual.buscar(t[2])
        print("ver tabla padre", tablaSimbolosActual.simbolos)
        print("existe la clase %s", t[2])
        if(existe is None):
            print("Clase a heredar no existente")
        else:
            stra = existe.split(',');
            if(len(stra) >2):
                print("Herencia maxima de 1 solo nivel");
                raise  SyntaxError
            else:
                llavetablaclase = t[2]
                print("lleva id de la tabla clase",t[2])


def p_Bloque_Clase(t):
    '''
      Bloque_Clase : BRACKET_IZQ Bloque_ClaseA BRACKET_DER SEMICOLON Fin_Bloque_Clase
    '''
    print("haber cuando corriste");


def p_Fin_Bloque_Clase(t):
    '''
    Fin_Bloque_Clase :
    '''
    global tablaSimbolosActual
    print("salir de tabla clase:", tablaSimbolosActual.simbolos);
    tablaSimbolosActual = tablaSimbolosActual.padre
    print("tabla a la que salio",tablaSimbolosActual.simbolos);


def p_Bloque_ClaseA(t):
    '''
      Bloque_ClaseA : Bloque_ClaseB Bloque_ClaseC
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
      Salida : KEYWORD_SALIDA  Expresion SEMICOLON
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

def p_LlamadaFuncionPadre(p):
  '''
    LlamadaFuncionPadre : LlamadaFuncion SEMICOLON
  '''

def p_LlamadaFuncionClasePadre(p):
  '''
    LlamadaFuncionClasePadre : LlamadaFuncionClase SEMICOLON
  '''

def p_LlamadaFuncionClase(p):
  '''
    LlamadaFuncionClase : LlamadaFuncionClaseAux PUNTO LlamadaFuncionClaseA LlamadaFuncion
  '''

def p_LlamadaFuncionClaseAux(p):
  '''
    LlamadaFuncionClaseAux : IDENTIFICADOR_CLASE
  '''

def p_LlamadaFuncionClaseA(p):
  '''
    LlamadaFuncionClaseA : LlamadaFuncionClaseAux PUNTO LlamadaFuncionClaseB
  '''

def p_LlamadaFuncionClaseB(p):
  '''
    LlamadaFuncionClaseB : LlamadaFuncionClaseA
    | empty
  '''

def p_LlamadaFuncion(p):
    '''
      LlamadaFuncion : LlamadaFuncionAux PARENTESIS_IZQ LlamadaFuncionA PARENTESIS_DER
    '''

def p_LlamadaFuncionAux(p):
  '''
    LlamadaFuncionAux : IDENTIFICADOR
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
    FuncionPrincipal : PrincipalAux PARENTESIS_IZQ PARENTESIS_DER Bloque FinBloquePrincipal
    '''


def p_PrincipalAux(t):
    '''
    PrincipalAux : KEYWORD_PRINCIPAL
    '''
    global tablaSimbolosActual
    tablaSimbolosActual.insertar('funcion', t[1])
    tablaM = TablaSimbolos()
    tablaM.agregarPadre(tablaSimbolosActual)
    tablaSimbolosActual.agregarHijo(tablaM)
    tablaSimbolosActual = tablaM

def p_FinBloquePrincipal(t):
    '''
    FinBloquePrincipal :
    '''
    global tablaSimbolosActual
    tablaSimbolosActual = tablaSimbolosActual.padre
    print("Terminar tabla principal")

def p_ValorSalida(t):
    '''
      ValorSalida : CONST_NUMERO_ENT
      | CONST_CARACTERES
      | CONST_NUMERO_REAL
      | CONST_BOOLEANO
      | KEYWORD_NULO
      | LlamadaFuncion
      | LlamadaFuncionClase
      | IDENTIFICADOR  ValorSalidaB
      | KEYWORD_FALSO
      | KEYWORD_VERDADERO
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
    '''


import ply.yacc as yacc

parser = yacc.yacc(start='Programa')

data = '''
real pato;
clase Sayajin{
    entero nivel_de_pelea;
    booleano mono;
    entero superSayajin;

    funcion caracter dameSayajin(){
     retorno superSayajin;
    }

};
clase Goku:Sayajin{
    entero gohan;
    real vegeta;
    booleano milk;
    funcion caracter nombreMilk(){
      salida "da da da";
    }
};
funcion entero perro(entero rojo){
  entero azul;
}
funcion booleano gatito(){
 entero verde;
 verde = "bebe be";
}
principal ()
{
 Goku gok;
 gok.nombreMilk();
  entero num;
  real numo;
  numo = 2.3 + 1;
  si (numo > 2){
    salida num;
  }sino {
    entrada numo;
  }
  num = 10;
  mientras(numo > 2){
    num = num -2;
    salida num;
  }
  caracter ruby;
  salida  ruby + "2";
  salida num;
}
'''

lexer.input(data)
# Tokenize
# while True:
#    tok = lexer.token()
#    if not tok:
#        break      # No more input
#    print(tok)

result = parser.parse(lexer=lexer)
print(result)