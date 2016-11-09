# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209
# List of token names.   This is always required
tokens = [
    'SEMICOLON', 'PUNTO',
    'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO','OPERADOR_AND_OR', 'EXP_OPERADOR', 'TERM_OPERADOR', 'IDENTIFICADOR', 'CONST_NUMERO_ENT',
    'CONST_NUMERO_REAL', 'IDENTIFICADOR_CLASE', 'CONST_CARACTERES', 'CONST_BOOLEANO', 'INTER_IZQ', 'INTER_DER',
]
llavetablactual = ""
llavetablaclase = None # se usa para asegurar que haya herencia
buscadorClase = None #se usa para buscar en las tablas clase si existen las variables o funciones a llamar
pilaClase = [] # se usa para guardar la variable de clase hasta acabar las operaciones con ella
stackOperador = [] #se usa para guardar los operadores del momento
stackOperando = [] #se usa para guardar las ,variables, constantes, temporales;
#cubo semantico es un diccionario de matrices que tiene de Id los tipos de operador que puede haber
#Ejemplo de como son cada una
#bool=1,int=2,float =3 ,string = 4,clase = 5,error = 6
#+, [
# bool [bool,int,float,string,clase],
# int [bool,int,float,string,clase],
# float [bool, int ,float,string, clase],
# string [bool, int ,float,string, clase],
# Clase [bool, int ,float,string, clase]
# ]

class claseCuboSemantico:
  def _init_(self):
    self.DataTypes = ['bool', 'int', 'real', 'string', 'clase', 'error']
    self.Cubo  = {'+':[[1,2,3,6,6],[2,2,3,6,6],[3,3,3,6,6], [6,6,6,4,6], [6,6,6,6,6]],
                 '-':[[1,2,3,6,6],[2,2,3,6,6],[3,3,3,6,6], [6,6,6,4,6], [6,6,6,6,6]],
                 '/':[[1,2,3,6,6],[2,2,3,6,6],[3,3,3,6,6], [6,6,6,4,6], [6,6,6,6,6]],
                 '*':[[1,2,3,6,6],[2,2,3,6,6],[3,3,3,6,6], [6,6,6,4,6], [6,6,6,6,6]],
                 '=':[[1,6,6,6,6],[6,2,6,6,6],[6,6,3,6,6], [6,6,6,4,6], [6,6,6,6,5]],
                 '>':[[6,6,6,6,6],[6,1,1,6,6],[6,1,1,6,6], [6,6,6,6,6], [6,6,6,6,6]],
                 '<':[[6,6,6,6,6],[6,1,1,6,6],[6,1,1,6,6], [6,6,6,6,6], [6,6,6,6,6]],
                 '&&':[[1,6,6,6,6],[6,6,6,6,6],[6,6,6,6,6], [6,6,6,6,6], [6,6,6,6,6]],
                 '||':[[1,6,6,6,6],[6,6,6,6,6],[6,6,6,6,6], [6,6,6,6,6], [6,6,6,6,6]],
                 'entrada':[[1,6,6,6,6],[6,2,6,6,6],[6,6,3,6,6],[6,6,6,4,6],[6,6,6,6,6]]
                 }

  def Semantica(self, operador, operando1, operando2):

    try:
      IndexOP1 = self.DataTypes.index(operando1)
      IndexOP2 = self.DataTypes.index(operando2)

    except ValueError:
      IndexOP1 = 6
      IndexOP2 = 6

    if IndexOP1 < 6 and IndexOP2 < 6 :
      sem = self.Cubo[operador][IndexOP1][IndexOP2]
      if sem == 0 :
        print("\nERROR TYPE MISMATCH. Los operandos:", operando1, "y", operando2, "no son compatibles con el operador:", operador)
        return None

      else:
        return self.DataTypes[sem]

    else:
      print("\nERROR. Tipos de datos:", operando1, ",", operando2, "y/o operador:", operador, "desconocidos.")
      return None


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
t_INTER_IZQ = r'\¿'
t_INTER_DER = r'\?'
t_OPERADOR_IGUAL = r'\='
t_OPERADOR_COMPARATIVO = r'[>]|[<]'
t_OPERADOR_AND_OR = r'&&|\|\|'
t_EXP_OPERADOR = r'\+|\-'
t_TERM_OPERADOR = r'\*|\/'
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

class TablaConstantes:
    def __init__(self):
        self.simbolos = dict()

    def insertar(self, id, tipo):
        self.simbolos[id] = tipo

    def buscar(self, id):
        return self.simbolos.get(id)

class Cuadruplos:
    def __init__(self):
        self.cuadruplos = list()
    def normalCuad(self,operador,operando1,operando2,destino=None):
        self.cuadruplos.append((operador,operando1,operando2,destino ))

    def AssignCuad(self,operando1,destino):
        self.cuadruplos.append(('=',operando1,None,destino))

    def SaltaCuad(self,operador, operando1,operando2,destino):
        print("ver como codigicar saltos")

    def AgregarSalto(self,operador, operando1,operando2,destino):
        print("darle update al cuadruplo")

    def EspecialCuad(self,operador,operando1,operando2,destino):
        print("cuadruplo a usar en funciones especiales")

    def CuadSize(self):
        return len(self.cuadruplos)

    def Ultimo(self):
        return self.cuadruplos[-1]

    def imprimir(self):
        indice = 0
        for cuad in self.cuadruplos:
            print('indice:' ,indice, 'operador: ',cuad[0],'operando1: ',cuad[1],'operando2: ',cuad[2], 'destino:',cuad[3])



tablaSimbolosActual = TablaSimbolos()
tablaSimbolosActual.insertar('global','global')
tablaGlobal =  tablaSimbolosActual
tablaConstantes = TablaConstantes()
cuadruploList = Cuadruplos()
temporales = []
indicetemporales = 0
checkSemantica = claseCuboSemantico()

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
    else:
      t[0] = t[1]

def p_Asignacion(t):
    ''' Asignacion : IGUALSIM Expresion SEMICOLON
    '''
    #parte de cuadruplo para expresion
def p_IGUALSIM(t):
    '''
    IGUALSIM : OPERADOR_IGUAL
    '''
    global stackOperador
    stackOperador.append(t[1])

def p_AsignaAux(t):
    '''
   AsignaAux : IDENTIFICADOR
   '''
    global tablaSimbolosActual, tablaGlobal,buscadorClase
    existe  = tablaSimbolosActual.buscar(t[1])
    print ("lectura", existe)
    if (buscadorClase is None):
        if (existe is None):
            print("variable no existe en este punto",buscadorClase)
        elif (not (existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero')):
            if(existe == 'funcion'):
                print("no puedes hacer asignacion con funcion")
            else:
               buscadorClase = tablaGlobal.buscarHijos(existe)
               if(not (buscadorClase is None)):
                   print("buscador Clase:", buscadorClase)
                   
               else:
                   print("clase no encontrada");
                   raise SyntaxError
               
        elif(existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero'):
            buscadorClase = None #funcion que encuentra el valor atomico del chiste
    else:
        existe =  buscadorClase.buscar(t[1])
        print("buscar dentro de clase", existe)
        if (existe is None):
            print("existe is None")
        elif ( existe == 'real' or existe ==  'booleano' or existe ==  'caracter' or existe ==  'entero'):
            print("aqui meter en vector que es una variable de tipo: ", existe)
            buscadorClase = None
        elif (existe == 'funcion'):
            print("aqui meter en vector que es una funcion")
            buscadorClase = None
        else:
            print("guardar en variable , checar meter en stack")
            buscadorClase = tablaGlobal.buscarHijos(existe)
            print("marcar error")

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
    Funcion : FuncionAux INTER_IZQ FuncionA INTER_DER Bloque Fin_Bloque
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
    | DecOAss BloqueB
    | Ciclo BloqueB
    | Condicion BloqueB
    | Entrada BloqueB
    | Salida BloqueB
    | KEYWORD_RETORNO ValorSalida SEMICOLON
    '''

def p_DecOAss(t):
  '''
    DecOAss : AsignaAux AsignaClass DecOAssA
  '''

def p_DecOAssA(t):
  '''
    DecOAssA : LlamadaFuncion SEMICOLON
    | Asignacion
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
            tablaC.insertar(t[2],'clase')
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
      Expresion : Expres ExpresionA
    '''


def p_ExpresionA(t):
    '''
      ExpresionA : OPERADOR_AND_OR expresionAux
      | empty
    '''
    #CUADRUPLO
    global stackOperador
    if(len(t) == 3):
      #condicion si hay operador sacar operador y hacer cuadruplo
      #el operador de == es el de menor prioridad es el utlimo en correrse
      stackOperador.append(t[1])

def p_expresionAux(t):
    '''
       expresionAux : Expresion
    '''
    global stackOperador,stackOperando,cuadruploList,temporales,indicetemporales
    top = stackOperador[len(stackOperador) - 1]
    if(top == '*' or top == '/' ):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        if (checkSemantica.Semantica(op, oper1, oper2) is not 6):
          cuadruploList.normalCuad(op,oper1,oper2,temporales[indicetemporales])
          indicetemporales = indicetemporales + 1


def p_Expres(t):
  '''
    Expres : Exp ExpresA
  '''

def p_ExpresA(t):
  '''
    ExpresA : OPERADOR_COMPARATIVO expresAux
  '''
  #CUADRUPLOS
  #siguiente de menor prioridad solo puede correr sien ambos operandos ya resolvieron suss multiplicacione sy sumas respectivas
  global stackOperador
  if(len(t) == 3):
      stackOperador.append(t[1])

def p_expresAux(t):
    '''
       expresAux : Exp
    '''
    global stackOperador,stackOperando,cuadruploList,temporales,indicetemporales
    top = stackOperador[len(stackOperador) - 1]
    if(top == '*' or top == '/' ):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        if (checkSemantica.Semantica(op, oper1, oper2) is not 6):
          cuadruploList.normalCuad(op,oper1,oper2,temporales[indicetemporales])
          indicetemporales = indicetemporales + 1


def p_Exp(t):
    '''
      Exp : Termino ExpA
    '''


def p_ExpA(t):
    '''
      ExpA : EXP_OPERADOR expAux
      | empty
    '''
    #CUADRUPLOS
    #exp operador  son + - ,
    #casi los de mayor prioridad , debe checar qeu no haya una multiplicacion  o dovision pendeintes antes de sumar
    global stackOperador

    if(len(t) == 3):
      stackOperador.append(t[1])

def p_expAux(t):
    '''
       expAux : Exp
    '''
    global stackOperador,stackOperando,cuadruploList,temporales,indicetemporales
    top = stackOperador[len(stackOperador) - 1]
    if(top == '*' or top == '/' ):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        if (checkSemantica.Semantica(op, oper1, oper2) is not 6):
          cuadruploList.normalCuad(op,oper1,oper2,temporales[indicetemporales])
          indicetemporales = indicetemporales + 1


def p_Termino(t):
    '''
      Termino : Factor TerminoA
      | empty
    '''


def p_TerminoA(t):
    '''
      TerminoA : TERM_OPERADOR terminoAux
      | empty
    '''
    #CUADRUPLO
    #multiplicaion y division debe correr siempre y cuando esten tod sloscomponentes del cuadruplo
    #se resuelven primero los parentesis
    global stackOperador
    if(len(t) == 3):
      stackOperador.append(t[1])

def p_terminoAux(t):
    '''
       terminoAux : Termino
    '''
    global stackOperador,stackOperando,cuadruploList,temporales,indicetemporales
    top = stackOperador[len(stackOperador) - 1]
    if(top == '*' or top == '/' ):
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        if (checkSemantica.Semantica(op, oper1, oper2) is not 6):
          cuadruploList.normalCuad(op,oper1,oper2,temporales[indicetemporales])
          indicetemporales = indicetemporales + 1



def p_Factor(t):
    '''
      Factor : ValorSalida
      | ParentesisInit Exp ParentesisFin
    '''
    #usar parentesis para meterlo como fondo falso
    global stackOperando
    if(len(t) == 1):
        stackOperando.append(t[1])

def p_ParentesisInit(t):
    '''
    ParentesisInit :   PARENTESIS_IZQ
    '''
    global  stackOperador
    stackOperador.append(t[1])

def p_ParentesisFin(t):
    '''
    ParentesisFin :   PARENTESIS_DER
    '''
    global  stackOperador
    stackOperador.pop()

def p_LlamadaFuncion(t):
    '''
      LlamadaFuncion : INTER_IZQ LlamadaFuncionA INTER_DER
    '''


def p_LlamadaFuncionA(t):
    '''
      LlamadaFuncionA : Expresion LlamadaFuncionB
    '''


def p_LlamadaFuncionB(t):
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
    FuncionPrincipal : PrincipalAux INTER_IZQ INTER_DER Bloque FinBloquePrincipal
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
      ValorSalida : NumeroEntero
      | Caracter
      | NumeroReal
      | Booleano
      | KEYWORD_NULO
      | LlamadaFuncion
      | Terminal ValorSalidaB
    '''

def p_NumeroEntero(t):
  '''
    NumeroEntero : CONST_NUMERO_ENT
  '''
  global tablaConstantes
  existe = None
  existe = tablaConstantes.buscar(t[1])
  print("terminal ent", t[1])
  if (existe is None):
    tablaConstantes.insertar(t[1], "entero")
    stackOperando.append(t[1])


def p_Caracter(t):
  '''
    Caracter : CONST_CARACTERES
  '''
  global tablaConstantes
  existe = None
  existe = tablaConstantes.buscar(t[1])
  print("terminal Car", t[1])
  if (existe is None):
    tablaConstantes.insertar(t[1], "caracter")
    stackOperando.append(t[1])

def p_NumeroReal(t):
  '''
    NumeroReal : CONST_NUMERO_REAL
  '''
  global tablaConstantes
  existe = None
  existe = tablaConstantes.buscar(t[1])
  print("terminal Real", t[1])
  if (existe is None):
    tablaConstantes.insertar(t[1], "real")
    stackOperando.append(t[1])

def p_Booleano(t):
  '''
    Booleano : CONST_BOOLEANO
  '''
  global tablaConstantes
  existe = None
  existe = tablaConstantes.buscar(t[1])
  print("terminal bool", t[1])
  if (existe is None):
    tablaConstantes.insertar(t[1], "booleano")
    stackOperando.append(t[1])

def p_Terminal(t):
  '''
    Terminal : IDENTIFICADOR
  '''
  global stackOperando
  existe = None
  existe = tablaSimbolosActual.buscar(t[1])
  print ("terminal id",t[1])
  if (existe is None):
    existe =  tablaSimbolosActual.padre.buscar(t[1])
    if(existe is None):
        print("El termino no ha sido declarado: " ,t[1])
    else:
        stackOperando.append(t[1])
  else:
    stackOperando.append(t[1])



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

    funcion caracter dameSayajin¿?{
     retorno superSayajin;
    }

};
clase Goku:Sayajin{
    entero gohan;
    real vegeta;
    booleano milk;
    funcion caracter nombreMilk¿?{
      salida "da da da";
    }
};
funcion entero perro ¿entero rojo?{
  entero azul;
}
funcion booleano gatito¿?{
 entero verde;
 verde = "bebe be";
}
principal ¿?
{
  entero num;
  real numo;
  Sayajin gok;
  gok.dameSayajin¿?;
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