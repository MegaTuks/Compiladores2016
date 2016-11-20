# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209
from memoria import *

# List of token names.   This is always required
tokens = [
    'SEMICOLON', 'PUNTO',
    'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'OPERADOR_AND_OR', 'EXP_OPERADOR', 'TERM_OPERADOR', 'IDENTIFICADOR',
    'CONST_NUMERO_ENT',
    'CONST_NUMERO_REAL', 'IDENTIFICADOR_CLASE', 'CONST_CARACTERES', 'CONST_BOOLEANO', 'INTER_IZQ', 'INTER_DER',
]

# cubo semantico es un diccionario de matrices que tiene de Id los tipos de operador que puede haber
# Ejemplo de como son cada una
# bool=1,int=2,float =3 ,string = 4,clase = 5,error = 6
# +, [
# bool [bool,int,float,string,clase],
# int [bool,int,float,string,clase],
# float [bool, int ,float,string, clase],
# string [bool, int ,float,string, clase],
# Clase [bool, int ,float,string, clase]
# ]

class claseCuboSemantico:
    def __init__(self):
        self.DataTypes = ['bool', 'int', 'real', 'string', 'clase', 'error']
        self.Cubo = {'+': [[1, 2, 3, 6, 6], [2, 2, 3, 6, 6], [3, 3, 3, 6, 6], [6, 6, 6, 4, 6], [6, 6, 6, 6, 6]],
                     '-': [[1, 2, 3, 6, 6], [2, 2, 3, 6, 6], [3, 3, 3, 6, 6], [6, 6, 6, 4, 6], [6, 6, 6, 6, 6]],
                     '/': [[1, 2, 3, 6, 6], [2, 2, 3, 6, 6], [3, 3, 3, 6, 6], [6, 6, 6, 4, 6], [6, 6, 6, 6, 6]],
                     '*': [[1, 2, 3, 6, 6], [2, 2, 3, 6, 6], [3, 3, 3, 6, 6], [6, 6, 6, 4, 6], [6, 6, 6, 6, 6]],
                     '=': [[1, 6, 6, 6, 6], [6, 2, 6, 6, 6], [6, 6, 3, 6, 6], [6, 6, 6, 4, 6], [6, 6, 6, 6, 5]],
                     '>': [[6, 6, 6, 6, 6], [6, 1, 1, 6, 6], [6, 1, 1, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6]],
                     '<': [[6, 6, 6, 6, 6], [6, 1, 1, 6, 6], [6, 1, 1, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6]],
                     '&&': [[1, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6]],
                     '||': [[1, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6]],
                     'entrada': [[1, 6, 6, 6, 6], [6, 2, 6, 6, 6], [6, 6, 3, 6, 6], [6, 6, 6, 4, 6], [6, 6, 6, 6, 6]]
                     }

    def Semantica(self, operador, operando1, operando2):
        print("SALUTATIONS!")
        try:
            IndexOP1 = self.DataTypes.index(operando1)
            IndexOP2 = self.DataTypes.index(operando2)

        except ValueError:
            IndexOP1 = 6
            IndexOP2 = 6

        if IndexOP1 < 6 and IndexOP2 < 6:
            sem = self.Cubo[operador][IndexOP1][IndexOP2]
            print("sem: ", sem)
            if sem == 0:
                print("\nERROR TYPE MISMATCH. Los operandos:", operando1, "y", operando2,
                      "no son compatibles con el operador:", operador)
                return None

            else:
                return sem

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
        # agregar atributo name?

    def insertar(self, id, tipo):
        self.simbolos[id] = tipo

    def buscar(self, id):
        return self.simbolos.get(id)

    def agregarHijo(self, hijo):
        self.hijos.append(hijo)

    def agregarPadre(self, pad):
        self.padre = pad

    def devolverPadre(self):
        if (self.padre is None):
            print("no hay padre al cual ir");
        else:
            return self.padre

    def buscarHijos(self, name):
        for hijo in self.hijos:
            existe = hijo.buscar(name)
            if (existe is not None):
                return hijo

                # def __str__(self):
    def imprimir(self):
        i = 0
        for hijo in self.hijos:
            print("Hijo:",hijo.simbolos)
        print ("tablaGlobal",self.simbolos)



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

    def normalCuad(self, operador, operando1, operando2, destino=None):
        self.cuadruplos.append((operador, operando1, operando2, destino))
        print("operador:" ,operador , " op1:",operando1, " op2:", operando2 , " destino:",destino)

    def updateCuad(self, index, operador=None, operando1=None, operando2=None, destino=None):
        self.cuadruplos[index] = (operador, operando1, operando2, destino)

    def AssignCuad(self,operador, operando1, destino):
        self.cuadruplos.append((operador, operando1, None, destino))

    def SaltaCuad(self, Goto, destino=None):
      self.cuadruplos.append((Goto, None, "1", destino))
      return len(self.cuadruplos) - 1
      print("ver como codigicar saltos")

    def AgregarSalto(self, indice, expr, destino=None):
      if destino is None:
        destino = len(self.cuadruplos)
      salto = (self.cuadruplos[indice][0], expr, "2", destino)
      self.cuadruplos[indice] = salto
      print("darle update al cuadruplo")

    def EspecialCuad(self, operador, operando1, operando2, destino):
        print("cuadruplo a usar en funciones especiales")

    def CuadSize(self):
        return len(self.cuadruplos)

    def Ultimo(self):
        return self.cuadruplos[-1]

    def imprimir(self):
        indice = 0
        for cuad in self.cuadruplos:
            print('indice:', indice, 'operador: ', cuad[0], 'operando1: ', cuad[1], 'operando2: ', cuad[2], 'destino:',
                  cuad[3])
            indice = indice + 1

class Procedimientos:
    def __init__(self):
        self.procedimientos = list()
        self.listParam = dict()

    def normalLista(self, id, parametros, variables, cuadruplo):
        self.procedimientos.append((id, parametros, variables, cuadruplo))
        print("ID Procedimiento:" ,id , " # Param:",parametros, " # Variables:", variables , "Destino:",cuadruplo)

    def updateLista(self, index, id, parametros, variables, destino):
        self.procedimientos[index] = (id, parametros, variables, destino)

    def meteParametros(self, id, lista = []):
        self.listParam[id] = lista

    def buscar(self, id):
        return self.listParam.get(id)

    def ListaSize(self):
        return len(self.procedimientos)

    def Ultimo(self):
        return self.procedimientos[-1]

    def imprimir(self):
        indice = 0
        for proc in self.procedimientos:
            print('indice:', indice, 'ID Procedimiento: ', proc[0], '#Param: ', proc[1], '#Variables: ', proc[2], 'Destino:',
                  proc[3])
            indice = indice + 1


llavetablactual = ""
llavetablaclase = None  # se usa para asegurar que haya herencia
buscadorClase = None  # se usa para buscar en las tablas clase si existen las variables o funciones a llamar
pilaClase = []  # se usa para guardar la variable de clase hasta acabar las operaciones con ella
stackOperador = []  # se usa para guardar los operadores del momento
stackOperando = []  # se usa para guardar las ,variables, constantes, temporales;
pilaSaltos = [] # se usa para actualizar los saltos, cuando una funcion , ciclo o condicion termina se actualiza
tablaSimbolosActual = TablaSimbolos()
tablaSimbolosActual.insertar('global', 'global')
tablaGlobal = tablaSimbolosActual
tablaConstantes = TablaConstantes()
cuadruploList = Cuadruplos()
cuadruActual = 0
varLocal = 0
procedimientoList = Procedimientos()
temporales = []
temporales.append(None)
indicetemporales = 0
indiceCondicion = 0
saltoCond = None
claseJumps = []
stackParam = []
auxstackParam = []
checkSemantica = claseCuboSemantico()
#memoria de las variables globales y funciones globales
memoriaGlobal = MemoriaReal()
memoriaLocal = MemoriaReal(10000)
memoriaConstante = MemoriaReal(20000)
memoriaTemporal = MemoriaReal(30000)
#memoria virtual a ejecutar
memoriaVirtual = VirtualMemory('global')
#lista que tendra stack de memoriasreales, (donde buscara)
#susdireccciones reales, arreglo 0 son globales,1-
listaMemorias = list()
listaMemorias =[memoriaGlobal,memoriaLocal,memoriaConstante,memoriaTemporal]
import ply.lex as lex

lexer = lex.lex()


def p_Programa(t):
    '''
      Programa : Goto_Principal ProgramaA FuncionPrincipal
    '''
    print('La sintaxis del programa paso')
    # print ('Global scope symbols:')
    global tablaSimbolosActual,cuadruploList,stackOperador, procedimientoList,stackOperando
    print('global scope symbols:', tablaSimbolosActual.simbolos)
    cuadruploList.normalCuad('FIN',None,None,None)
    cuadruploList.imprimir()
    procedimientoList.imprimir()
    print('stackOperadores',stackOperador)
    print('stackOperando', stackOperando)
    tablaGlobal.imprimir()

#goto que general el cuadruplo de la funcion principal , hacer uqe sea efectivo.
def p_Goto_Principal(p):
    '''
    Goto_Principal :
    '''
    global cuadruploList,pilaSaltos
    cuadruploList.normalCuad('Goto',None,None, 'pendiente')

def p_empty(p):
    'empty :'
    pass


def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)


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
    if (existe is None):
        print("Tipo no existente, clase no declarada")
        raise SyntaxError
    else:
        t[0] = t[1]


def p_Asignacion(t):
    ''' Asignacion : IGUALSIM Expresion SEMICOLON 
    '''
    # parte de cuadruplo para expresion
    global stackOperador,stackOperando,cuadruploList
    op=stackOperador.pop()
    operando = stackOperando.pop()
    print("operando",operando)
    destino = stackOperando.pop()
    print("destino", destino)
    cuadruploList.AssignCuad(op,operando,destino)



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
    global tablaSimbolosActual, tablaGlobal, buscadorClase,stackOperando, procedimientoList, auxstackParam
    existe = tablaSimbolosActual.buscar(t[1])
    existeglobal = tablaGlobal.buscar(t[1])
    print("lectura", existe)
    if (buscadorClase is None):
        if (existe is None):
            print("variable no existe en este punto", buscadorClase)
        elif (not (existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero')):
            if (existe == 'funcion'):
                print("no puedes hacer asignacion con funcion")
                #auxstackParam.append(procedimientoList.buscar(t[1]))
                #print("SE PASA LA PILA DE TIPOS", auxstackParam)
            else:
                buscadorClase = tablaGlobal.buscarHijos(existe)
                if (not (buscadorClase is None)):
                    print("buscador Clase:", buscadorClase)

                else:
                    print("clase no encontrada");
                    raise SyntaxError

        elif (existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero'):
            buscadorClase = None  # funcion que encuentra el valor atomico del chiste
            stackOperando.append(t[1])
    else:
        existe = buscadorClase.buscar(t[1])
        print("buscar dentro de clase", existe)
        if (existe is None):
            print("existe is None")
        elif (existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero'):
            print("aqui meter en vector que es una variable de tipo: ", existe)
            stackOperando.append(t[1])
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
    global tablaSimbolosActual, stackParam, cuadruploList, cuadruActual, varLocal
    stackParam = []
    existe = tablaSimbolosActual.buscar(t[3])
    if (existe is None):
        tablaSimbolosActual.insertar(t[3], t[1])  # guarda que es Tipo funcion en la tabla de simbolos
        print("insertar funcion en tabla", tablaSimbolosActual.simbolos)
        tablaF = TablaSimbolos()
        tablaF.insertar('funcion', 'funcion')
        tablaF.insertar(t[3], t[2])
        tablaSimbolosActual.agregarHijo(tablaF)
        tablaF.agregarPadre(tablaSimbolosActual)  #
        tablaSimbolosActual = tablaF
        print("funcion de ahorita", tablaSimbolosActual.simbolos)
        stackParam.append(t[3])
        cuadruActual = cuadruploList.CuadSize()
        varLocal = 0
    else:
        print("Funcion previamente declarada")
        raise SyntaxError


def p_Fin_Bloque(t):
    '''
    Fin_Bloque :
    '''
    global tablaSimbolosActual,cuadruploList, stackParam, procedimientoList, cuadruActual, varLocal
    print("salir de la funcion");
    tablaSimbolosActual = tablaSimbolosActual.padre
    cuadruploList.normalCuad('RET',None,None,None)
    functId = stackParam.pop(0)
    print("TIPOS A MANDAR",stackParam)
    procedimientoList.meteParametros(functId, stackParam)
    if (stackParam[0] is None):
      cantParam = 0;
    else:
      cantParam = len(stackParam)
    procedimientoList.normalLista(functId, cantParam, varLocal, cuadruActual)



def p_FuncionA(t):
    '''
    FuncionA : Parametro FuncionB
    | empty
    '''
    global stackParam
    stackParam.append(t[1])


def p_FuncionB(t):
    '''
    FuncionB : COMMA FuncionA
      | empty
    '''


def p_Parametro(t):
    '''
    Parametro : Tipo IDENTIFICADOR
    '''
    t[0] = t[1]
    global tablaSimbolosActual
    existe = tablaSimbolosActual.buscar(t[2])
    if (existe is None):
        tablaSimbolosActual.insertar(t[2], t[1])
        print("simbolos insertados", tablaSimbolosActual.simbolos)
        
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
    | Retorno Expresion SEMICOLON FinRetorno
    '''

def p_Retorno(t):
  '''
  Retorno : KEYWORD_RETORNO
  '''
  global stackOperador
  stackOperador.append(t[1])

def p_FinRetorno(t):
  '''
  FinRetorno : 
  '''
  global cuadruploList,stackOperando,stackOperador
  op = stackOperador.pop()
  op1 = stackOperando.pop()
  cuadruploList.normalCuad(op,op1,None,None)
    

def p_DecOAss(t):
    '''
      DecOAss : AsignaAux AsignaClass DecOAssA
    '''


def p_DecOAssA(t):
    '''
      DecOAssA :  LlamadaFuncion SEMICOLON
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
    global tablaSimbolosActual, llavetablaclase, cuadruploList, claseJumps
    existe = tablaSimbolosActual.buscar(t[2])
    print("ver tabla antes de entrar a clase", tablaSimbolosActual.simbolos)
    if (existe is None):
        if (llavetablaclase is None):
            tablaSimbolosActual.insertar(t[2], t[1])
            tablaC = TablaSimbolos()
            tablaC.insertar(t[2], 'clase')
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
        cuadruploList.normalCuad('Goto',None,None, 'pendienteClase')
        claseJumps.append(cuadruploList.CuadSize())
    else:
        print("Clase ya existente ");
        raise SyntaxError


def p_ClaseA(t):
    '''
    ClaseA : COLON IDENTIFICADOR_CLASE
     | empty
    '''
    global tablaSimbolosActual, llavetablaclase
    if (len(t) == 3):
        existe = tablaSimbolosActual.buscar(t[2])
        print("ver tabla padre", tablaSimbolosActual.simbolos)
        print("existe la clase %s", t[2])
        if (existe is None):
            print("Clase a heredar no existente")
        else:
            stra = existe.split(',');
            if (len(stra) > 2):
                print("Herencia maxima de 1 solo nivel");
                raise SyntaxError
            else:
                llavetablaclase = t[2]
                print("lleva id de la tabla clase", t[2])


def p_Bloque_Clase(t):
    '''
      Bloque_Clase : BRACKET_IZQ Bloque_ClaseA BRACKET_DER SEMICOLON Fin_Bloque_Clase
    '''
    print("haber cuando corriste");


def p_Fin_Bloque_Clase(t):
    '''
    Fin_Bloque_Clase :
    '''
    global tablaSimbolosActual, cuadruploList
    print("salir de tabla clase:", tablaSimbolosActual.simbolos);
    tablaSimbolosActual = tablaSimbolosActual.padre
    print("tabla a la que salio", tablaSimbolosActual.simbolos);
    cuadruploList.normalCuad('RET',None,None,None)


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
      Ciclo : CicloAux PARENTESIS_IZQ Expresion CicloCheck Bloque
    '''
    global cuadruploList, temporales, indicetemporales
    print("TEMPORAL DE CICLO", temporales[indicetemporales - 1])
    Ciclodir, CicloCheck = t[1], t[4]
    cuadruploList.SaltaCuad("Goto", Ciclodir)
    cuadruploList.AgregarSalto(CicloCheck, temporales[indicetemporales - 1])


def p_CicloAux(t):
  '''
    CicloAux : KEYWORD_MIENTRAS
  '''
  global stackOperador, cuadruploList
  stackOperador.append("GotoF")
  print("OPERADORES HASTA EL MOMENTO GOTOF", stackOperador)
  t[0] = cuadruploList.CuadSize()

def p_CicloCheck(t):
  '''
    CicloCheck : PARENTESIS_DER
  '''
  global cuadruploList, stackOperador
  op = stackOperador.pop()
  t[0] = cuadruploList.SaltaCuad(op)

def p_Entrada(t):
    '''
      Entrada : KEYWORD_ENTRADA IDENTIFICADOR SEMICOLON
    '''


def p_Salida(t):
    '''
      Salida : Salida_Key_Aux  Expresion SEMICOLON Salida_fin
    '''

def p_Salida_Key_Aux(t):
    '''
    Salida_Key_Aux : KEYWORD_SALIDA
    '''
    global stackOperador
    stackOperador.append(t[1])

def p_Salida_fin(t):
    '''
    Salida_fin :
    '''
    global cuadruploList,stackOperando,stackOperador
    op = stackOperador.pop()
    op1 = stackOperando.pop()
    cuadruploList.normalCuad(op,op1,None,None)

def p_Condicion(t):
    '''
      Condicion : CondicionAux PARENTESIS_IZQ Expresion CondicionCheck Bloque CondicionA
    '''
    global cuadruploList, temporales, indicetemporales, indiceCondicion
    termina = t[4]
    indiceCondicion = indicetemporales - 1
    cuadruploList.AgregarSalto(termina, temporales[indiceCondicion])


def p_CondicionAux(t):
  '''
    CondicionAux : KEYWORD_SI
  '''
  global stackOperador
  stackOperador.append("GotoF")
  print("OPERADORES HASTA EL MOMENTO GOTOF", stackOperador)
  

def p_CondicionCheck(t):
  '''
    CondicionCheck : PARENTESIS_DER
  '''
  global cuadruploList, stackOperador, saltoCond
  op = stackOperador.pop()
  saltoCond = cuadruploList.SaltaCuad(op)
  t[0] = saltoCond


def p_CondicionA(t):
    '''
      CondicionA : SinoAux SinoCheck SinoBloqueFin
      | empty
    '''
    global cuadruploList, temporales, indicetemporales, indiceCondicion
    salto, SinoDir = t[2], t[3]
    cuadruploList.AgregarSalto(saltoCond, temporales[indiceCondicion])
    cuadruploList.AgregarSalto(salto, None, SinoDir)

def p_SinoAux(t):
  '''
    SinoAux : KEYWORD_SINO
  '''
  global stackOperador
  stackOperador.append("Goto")
  print("OPERADORES HASTA EL MOMENTO GOTO", stackOperador)

def p_SinoCheck(t):
  '''
    SinoCheck : Bloque
  '''
  global cuadruploList, stackOperador
  op = stackOperador.pop()
  t[0] = cuadruploList.SaltaCuad(op)

def p_SinoBloqueFin(t):
  '''
    SinoBloqueFin :
  '''
  global cuadruploList
  t[0] = cuadruploList.CuadSize()


def p_Expresion(t):
    '''
      Expresion : Expresion ExpresionA
      | Expres
    '''
def p_ExpressionA(t):
    '''
    ExpresionA : ExpresionAux Expres
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO AND OR", stackOperador)
    if (top == '&&' or top == '||'):
        temporales[indicetemporales] = "temporalExpresion"
        print("TEMPORAL DE && O ||", temporales[indicetemporales])
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        cuadruploList.normalCuad(op, oper1, oper2, temporales[indicetemporales])
        stackOperando.append(temporales[indicetemporales])
        indicetemporales = indicetemporales + 1
        temporales.append(None)

def p_ExpresionAux(t):
    '''
    ExpresionAux : OPERADOR_AND_OR
    '''
    global stackOperador
    stackOperador.append(t[1])

def p_Expres(t):
    '''
    Expres : Expres ExpresA
    | Exp
    '''

def p_ExpresA(t):
    '''
    ExpresA : ExpresAux Exp
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO COMPARATIVO", stackOperador)
    if (top == '<' or top == '>'):
        temporales[indicetemporales] = "temporalExpres"
        print("TEMPORAL DE < O >", temporales[indicetemporales])
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        cuadruploList.normalCuad(op, oper1, oper2, temporales[indicetemporales])
        stackOperando.append(temporales[indicetemporales])
        indicetemporales = indicetemporales + 1
        temporales.append(None)

def p_ExpresAux(t):
    '''
    ExpresAux : OPERADOR_COMPARATIVO
    '''
    global stackOperador
    stackOperador.append(t[1])

def p_Exp(t):
    '''
    Exp : Exp ExpA
    | Termino
    '''

def p_ExpA(t):
    '''
    ExpA : ExpAux Termino
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO + -", stackOperador)
    if (top == '+' or top == '-'):
        temporales[indicetemporales] = "temporalExp"
        print("TEMPORAL DE + O -", temporales[indicetemporales])
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        cuadruploList.normalCuad(op, oper1, oper2, temporales[indicetemporales])
        stackOperando.append(temporales[indicetemporales])
        indicetemporales = indicetemporales + 1
        temporales.append(None)

def p_ExpAux(t):
    '''
    ExpAux : EXP_OPERADOR
    '''
    global stackOperador
    stackOperador.append(t[1])

def p_Termino(t):
    '''
    Termino : Termino TerminoA
    | Factor
    '''

def p_TerminoA(t):
    '''
    TerminoA : TerminoAux Factor
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO * /", stackOperador)
    if (top == '*' or top == '/'):
        temporales[indicetemporales] = "temporalTermino"
        print("TEMPORAL DE * O /", temporales[indicetemporales])
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        cuadruploList.normalCuad(op, oper1, oper2, temporales[indicetemporales])
        stackOperando.append(temporales[indicetemporales])
        indicetemporales = indicetemporales + 1
        temporales.append(None)

def p_TerminoAux(t):
    '''
    TerminoAux : TERM_OPERADOR
    '''
    global stackOperador
    stackOperador.append(t[1])

def p_Factor(t):
    '''
      Factor : ValorSalida
      | ParentesisInit Expresion ParentesisFin
    '''
    # usar parentesis para meterlo como fondo falso
    # usar parentesis para meterlo como fondo falso


def p_ParentesisInit(t):
    '''
    ParentesisInit :   PARENTESIS_IZQ
    '''
    global stackOperador
    stackOperador.append(t[1])


def p_ParentesisFin(t):
    '''
    ParentesisFin :   PARENTESIS_DER
    '''
    global stackOperador
    stackOperador.pop()


def p_LlamadaFuncion(t):
    '''
      LlamadaFuncion : INTER_IZQ LlamadaFuncionA INTER_DER
    '''


def p_LlamadaFuncionA(t):
    '''
      LlamadaFuncionA : Expresion LlamadaFuncionB
      | empty
    '''


def p_LlamadaFuncionB(t):
    '''
      LlamadaFuncionB : COMMA LlamadaFuncionA
      | empty
    '''


def p_Declaracion(t):
    '''
    Declaracion : Parametro DeclaraA SEMICOLON
    '''
    global varLocal
    varLocal = varLocal + 1

def p_DeclaraA(t):
    '''
    DeclaraA : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER DeclaraB
    | empty
    '''
def p_DeclaraB(t):
    '''
    DeclaraB : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER 
    | empty
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
    global tablaSimbolosActual, claseJumps
    tablaSimbolosActual.insertar('funcion', t[1])
    tablaM = TablaSimbolos()
    tablaM.agregarPadre(tablaSimbolosActual)
    tablaSimbolosActual.agregarHijo(tablaM)
    tablaSimbolosActual = tablaM
    cuadruploList.updateCuad(0, "Goto", None, None, cuadruploList.CuadSize())
    for x in claseJumps:
      cuadruploList.updateCuad(x-1, "Goto", None, None, cuadruploList.CuadSize())


def p_FinBloquePrincipal(t):
    '''
    FinBloquePrincipal :
    '''
    global tablaSimbolosActual, cuadruploList
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
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal ent", t[1])
    if (existe is None):
        tablaConstantes.insertar(t[1], "entero")
        stackOperando.append(t[1])
    else:
        stackOperando.append(t[1])


def p_Caracter(t):
    '''
      Caracter : CONST_CARACTERES
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal Car", t[1])
    if (existe is None):
        tablaConstantes.insertar(t[1], "caracter")
        stackOperando.append(t[1])
    else:
        stackOperando.append(t[1])


def p_NumeroReal(t):
    '''
      NumeroReal : CONST_NUMERO_REAL
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal Real", t[1])
    if (existe is None):
        tablaConstantes.insertar(t[1], "real")
        stackOperando.append(t[1])
    else:
        stackOperando.append(t[1])


def p_Booleano(t):
    '''
      Booleano : CONST_BOOLEANO
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal bool", t[1])
    if (existe is None):
        tablaConstantes.insertar(t[1], "booleano")
        stackOperando.append(t[1])


def p_Terminal(t):
    '''
      Terminal : IDENTIFICADOR AsignaA
    '''
    global stackOperando, buscadorClase,pilaClase
    existe = None
    existe = tablaSimbolosActual.buscar(t[1])
    print("terminal id", t[1])
    if (existe is None):
        existe = tablaSimbolosActual.padre.buscar(t[1])
        if (existe is None):
            print("El termino no ha sido declarado: ", t[1])
        else:
            if(existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero'):
                stackOperando.append(t[1])
            elif(existe =='funcion'):
                print("meter cuadruplo con de gosub a la funcion")
                print("meter a cuadruplo de operando resultado de la funcion?")
                stackOperando.append(t[1])
            else:
                buscadorClase = tablaGlobal.buscarHijos(existe)
                if (not (buscadorClase is None)):
                    print("buscador Clase:", buscadorClase)
                    pilaClase.append(t[1])
                    stackOperando.append(t[1])

                else:
                    print("clase no encontrada");
                    raise SyntaxError

    else:
        stackOperando.append(t[1])


def p_ValorSalidaB(t):
    '''
      ValorSalidaB : PuntoAux IdentificadorAux ValorSalidaC
      | empty
    '''

def p_IdentificadorAux(t):
    '''
    IdentificadorAux : IDENTIFICADOR
    '''
    global stackOperador ,stackOperando,tablaSimbolosActual,TablaGlobal
    stackOperador
    if (stackOperador[len(stackOperador) - 1] == "."):
        print("detecto el punto!")
        stackOperador.pop()
        opPadre = stackOperando.pop()
        print("==================================PADRE", opPadre)
        siClase = tablaGlobal.buscarHijos(opPadre)
        if (not (siClase is None)):
            # op hijo debe devolver su direccion
            # para cuando ya se maneje memoria
           existe = siClase.buscar(t[1])
           if(existe is None):
            stackOperando.append(t[1])

def p_PuntoAux(t):
    '''
    PuntoAux : PUNTO
    '''
    global stackOperador
    stackOperador.append(t[1])


def p_ValorSalidaC(t):
    '''
      ValorSalidaC : INTER_IZQ  LlamadaFuncionA INTER_DER
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
     entero sol;
      sol = superSayajin+3;
      retorno sol;
    }

};
clase Goku:Sayajin{
    entero gohan;
    real vegeta;
    booleano milk;
    funcion booleano nombreMilk¿?{
    entero azulado;
    salida azulado + 5;

    retorno milk;
    }
};
funcion entero perro ¿entero rojo?{
  entero azul;
  retorno azul + 4;
}
funcion booleano gatito¿?{
 caracter verde;
 verde = "bebe be";
 retorno verde;
}

principal ¿?
{
  entero num;
  real numo;
  Sayajin gok;
  numo = 2.3 + 1;
  numo  = 2.5*3 + 8/2;
  num = 10;
  num =  num + (8+3)*7;
  salida num;
  caracter ruby;
  perro¿?;

  si(num < 100){
    num = 1;
  }
  sino{
    num = 2;
  }

  mientras(numo > (10.5 * 10 + 2 -4 / numo + (numo-10)  ) * 50 && num > 2){
    numo = numo - gok.nombreMilk¿?;
  }

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