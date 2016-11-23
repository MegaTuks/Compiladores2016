# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209
from memoria import *
from tablas import *
from maquina import *
# List of token names.   This is always required
tokens = [
    'SEMICOLON', 'PUNTO',
    'COMMA', 'COLON', 'BRACKET_IZQ', 'BRACKET_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'OPERADOR_IGUAL', 'OPERADOR_COMPARATIVO', 'OPERADOR_AND_OR', 'EXP_OPERADOR', 'TERM_OPERADOR', 'IDENTIFICADOR',
    'CONST_NUMERO_ENT',
    'CONST_NUMERO_REAL', 'IDENTIFICADOR_CLASE', 'CONST_CARACTERES', 'CONST_BOOLEANO', 'INTER_IZQ', 'INTER_DER',
]

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
    r'[KEYWORD_VERDADERO|KEYWORD_FALSO]'
    return t


t_CONST_CARACTERES = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!\ ]*\"'


def t_error(t):
    print("Caracter  Ilegal>>> '%s'  <<<<" % t.value[0])
    t.lexer.skip(1)
#memoria de las variables globales y funciones globales
memoriaGlobal = MemoriaReal()
memoriaLocal = MemoriaReal(10001)
memoriaConstante = MemoriaReal(20001)
memoriaTemporal = MemoriaReal(30001)
nuevasClases = 40001
maquinaVirtual = Maquina()
#memoria de IDS DE CLASE
#centenar arriba de 500 000 indica que es tipo clase
#decima indica 5X0000 a  que clase pertenece
#unidad indica arreglos y su tamano.  de clase
memoriaIDClases = MemoriaReal(500000,True)
llavetablactual = ""
llavetablaclase = None  # se usa para asegurar que haya herencia
buscadorClase = None  # se usa para buscar en las tablas clase si existen las variables o funciones a llamar
pilaClase = []  # se usa para guardar la variable de clase hasta acabar las operaciones con ella
stackOperador = []  # se usa para guardar los operadores del momento
stackOperando = []  # se usa para guardar las ,variables, constantes, temporales;
pilaSaltos = [] # se usa para actualizar los saltos, cuando una funcion , ciclo o condicion termina se actualiza
tablaSimbolosActual = TablaSimbolos()

tablaConstantes = TablaConstantes()
cuadruploList = Cuadruplos()
cuadruActual = 0
varLocal = 0
elseDir = 0
proScope = ""
procedimientoList = Procedimientos()
temporales = []
temporales.append(None)
indicetemporales = 0
indiceCondicion = ""
saltoCond = None
claseJumps = []
stackParam = []
auxstackParam = []
stackArreglo = []
paramCont = 1
checkSemantica = claseCuboSemantico()


#memoria virtual a ejecutar
memoriaVirtual = VirtualMemory('global')
#lista que tendra stack de memoriasreales, (donde buscara)
#susdireccciones reales, arreglo 0 son globales,1-
listaMemorias = list()
listaMemorias =[memoriaGlobal,memoriaLocal,memoriaConstante,memoriaTemporal]
tablaSimbolosActual.id = listaMemorias[0].insertaBooleano()
tablaSimbolosActual.insertar('global', 'global',tablaSimbolosActual.id)
tablaGlobal = tablaSimbolosActual
print("id de la tabla simbolos", tablaSimbolosActual.id)
import ply.lex as lex

lexer = lex.lex()


def p_empty(p):
    'empty :'
    pass


def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)

#diagrama de sintaxis Inicial del pograma , Funcion principal 
def p_Programa(t):
    '''
      Programa : Goto_Principal ProgramaA FuncionPrincipal
    '''
    print('La sintaxis del programa paso')
    # print ('Global scope symbols:')

    global tablaSimbolosActual,cuadruploList,stackOperador, procedimientoList, stackOperando, procedimientoList, maquinaVirtual
    print('global scope symbols:', tablaSimbolosActual.simbolos)
    cuadruploList.normalCuad('FIN',None,None,None)
    print("---------------------------------CUADRUPLO LIST-------------------------------------")
    cuadruploList.imprimir()
    print("-------------------------------PROCEDIMIENTO LIST-----------------------------------")
    procedimientoList.imprimir()
    tablaGlobal.imprimir()
    tablaConstantes.imprimir()
    maquinaVirtual.setCuad(cuadruploList.getCuadruplos())
    maquinaVirtual.setProc(procedimientoList.getProcedimientos())
    maquinaVirtual.setSimbolos(tablaGlobal)
    maquinaVirtual.setConstantes(tablaConstantes)
    print('stackOperadores',stackOperador)
    print('stackOperando', stackOperando)


    maquinaVirtual.calculos()
    print("dimensiones",memoriaVirtual.variablesDim)

    
#goto que general el cuadruplo de la funcion principal , hacer uqe sea efectivo.
def p_Goto_Principal(p):
    '''
    Goto_Principal :
    '''
    global cuadruploList,pilaSaltos, procedimientoList
    cuadruploList.normalCuad('Goto',None,None, 'pendiente')
    procedimientoList.normalLista("principal", 0, 0, 0, "principal")

#diagrama de sintaxis de como funciona el programa , puedes ahcer declaraciones, Funciones o clases antes de entrar al main
def p_ProgramaA(t):
    '''
      ProgramaA : Declaracion ProgramaA
      | Funcion ProgramaA
      | Clase ProgramaA
      | empty
    '''

#funcion que corre el programa principal , necesaria para correr nuestro lenguaje
def p_FuncionPrincipal(t):
    '''
    FuncionPrincipal : PrincipalAux INTER_IZQ INTER_DER Bloque FinBloquePrincipal
    '''

#diagrama para Identificar cuando entra a la funcion principal , generar tabla de simbolos
def p_PrincipalAux(t):
    '''
    PrincipalAux : KEYWORD_PRINCIPAL
    '''
    global tablaSimbolosActual, claseJumps,listaMemorias, procedimientoList, varLocal, proScope
    proScope = t[1]
    mem =  listaMemorias[1].insertaEntero()
    tablaSimbolosActual.insertarFuncion(t[1], 'entero', mem)
    tablaM = TablaSimbolos()
    tablaM.id = mem
    tablaM.agregarPadre(tablaSimbolosActual)
    tablaSimbolosActual.agregarHijo(tablaM)
    tablaSimbolosActual = tablaM
    cuadruploList.updateCuad(0, "Goto", None, None, cuadruploList.CuadSize())
    procedimientoList.updateLista(0, "principal", 0, varLocal, cuadruploList.CuadSize(), proScope)
    for x in claseJumps:
      cuadruploList.updateCuad(x-1, "Goto", None, None, cuadruploList.CuadSize())

#Regresa a la tabla de simbolos actual
def p_FinBloquePrincipal(t):
    '''
    FinBloquePrincipal :
    '''
    global tablaSimbolosActual, cuadruploList, procedimientoList, proScope
    tablaSimbolosActual = tablaSimbolosActual.padre
    proScope = "global"
    
#Sirve para identificar y devolver el tipo
def p_Tipo(t):
    '''Tipo : KEYWORD_TYPE_ENTERO
    | KEYWORD_TYPE_REAL
    | KEYWORD_TYPE_BOOLEANO
    | KEYWORD_TYPE_CARACTERES
    | IDENTIFICADOR_CLASE_AUX
    '''
    t[0] = t[1]

#sirve para identificar si una clase existe.
def p_IDENTIFICADOR_CLASE_AUX(t):
    '''
    IDENTIFICADOR_CLASE_AUX : IDENTIFICADOR_CLASE
    '''
    existe = tablaGlobal.buscar(t[1])
    if (existe is None):
        print("Tipo no existente, clase no declarada")
        print("verifica generar la clase ANTES de mandarla a llamar")
        raise SyntaxError
    else:
        t[0] =  t[1]

#diagrama de sintaxis usado para asignar valores a una variable.
def p_Asignacion(t):
    ''' Asignacion : IGUALSIM Expresion SEMICOLON 
    '''
    # parte de heacuadruplo para expresion
    global stackOperador,stackOperando,cuadruploList
    op=stackOperador.pop()
    operando = stackOperando.pop()
    destino = stackOperando.pop()
    cuadruploList.AssignCuad(op,operando,destino)


#sirve para meter el operador igual en el stack de operadores.
def p_IGUALSIM(t):
    '''
    IGUALSIM : OPERADOR_IGUAL
    '''
    global stackOperador
    stackOperador.append(t[1])

#identificador de llamadas, o asignaciones.
def p_AsignaAux(t):
    '''
   AsignaAux : IDENTIFICADOR
   '''
    global tablaSimbolosActual, tablaGlobal, buscadorClase, stackOperando, auxstackParam, procedimientoList,cuadruploList
    existe = tablaSimbolosActual.buscar(t[1])
    existeglobal = tablaGlobal.buscar(t[1])
    if (buscadorClase is None):
        if (existe is None):
            print("variable no existe en este punto", buscadorClase)
        elif (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
            stackOperando.append(existe['memo'])
        elif (not (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero')):
            if (existe['tipo'] == 'funcion'):
                print("no puedes hacer asignacion con funcion")
            else:
                buscadorClase = tablaGlobal.buscarHijos(existe['tipo'])
                if (not (buscadorClase is None)):
                    stackOperando.append(existe['memo'])
                else:
                    print("clase no encontrada");
                    raise SyntaxError
        if(not(existeglobal is None)):
            if (existeglobal['tipo'] == 'funcion'):
                print("ZORDON")
                auxstackParam.append(t[1])
                auxstackParam.append(procedimientoList.buscar(t[1]))
            if (auxstackParam[1][0] is not None):
                auxstackParam[1].reverse()
                print("SE TIENEN LOS PARAMETROS EN LA FUNCION: ", auxstackParam)
    else:
        print('LectoraClase',buscadorClase.simbolos)
        existe = buscadorClase.buscar(t[1])
        print("buscar dentro de clase", existe)
        if (existe is None):
            print("Clase No encontrada")
            raise SyntaxError
        elif (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
            print("aqui meter en vector que es una variable de tipo: ", existe)
            if(stackOperador[len(stackOperador)-1]== '.'):
                op = stackOperador.pop()
                op1 = stackOperando.pop()
                cuadruploList.normalCuad(op,op1,None,existe['memo'])
                stackOperando.append(existe['memo'])
                buscadorClase = None
        elif (existe['tipo'] == 'funcion'):
            buscadorClase = None
        else:
            buscadorClase = tablaGlobal.buscarHijos(existe['tipo'])
            if(buscadorClase is None):
                print("Error de sintaxis clase no existe")
            else:
                buscadorClase.id
            
            print("marcar error")
            

#diagrama utilizado para encontrar las llamadas a funcion de una clase, o accesso de varaibles
def p_AsignaClass(t):
    '''
    AsignaClass :  AsignaA
    | PuntoAux AsignaAux AsignaA
    '''
    


#diagrama usado para instanciar vectores.
def p_AsignaA(t):
    '''
    AsignaA : CORCHETE_IZQ Expresion CORCHETE_DER AsignaB
    | empty
    '''

#diagrama usado para instanciar matrices
def p_AsignaB(t):
    '''
    AsignaB : CORCHETE_IZQ Expresion CORCHETE_DER
    | empty
    '''

#diagrama para generar los parametros dentro de una funcion.
def p_Funcion(t):
    '''
    Funcion : FuncionAux INTER_IZQ FuncionA INTER_DER Bloque Fin_Bloque
    '''
    
#diagrama para generar e instanciar funciones
def p_FuncionAux(t):
    '''
    FuncionAux : KEYWORD_FUNCION Tipo IDENTIFICADOR
    '''
    global tablaSimbolosActual, stackParam, cuadruploList, cuadruActual, varLocal,tablaGlobal,listaMemorias
    stackParam = []
    existe = tablaSimbolosActual.buscar(t[3])
    if (existe is None):
        tipoID = t[2]
        memID = 0
        if(not (tipoID == 'entero' or tipoID =='booleano' or tipoID =='caracter' or tipoID =='real')):
            idValue = tablaSimbolosActual.id+10000
            idValue =int(idValue/10000)
            existe = tablaGlobal.buscarHijos(t[2])
            if(existe is None):
                print("Tipo de clase no ha sido declarada")
            else:
                memID = memoriaIDClases.insertarClase(idValue+10000)
            ########################################################################ACABAR CLASE
        else:
            idValue = int(tablaSimbolosActual.id/10000)
            idValue =idValue + 1
            if(tipoID =='entero'):
                memID = listaMemorias[idValue].insertaEntero()
            elif(tipoID =='booleano'):
                memID = listaMemorias[idValue].insertaBooleano()
            elif(tipoID =='caracter'):
                memID = listaMemorias[idValue].insertaCaracter()
            elif(tipoID =='real'):
                memID = listaMemorias[idValue].insertaReal()
        tablaSimbolosActual.insertarFuncion(t[3], t[2], memID)  # guarda que es Tipo funcion en la tabla de simbolos
        tablaF = TablaSimbolos()
        tablaF.id = memID
        tablaF.insertar(t[3], t[2],memID)
        tablaSimbolosActual.agregarHijo(tablaF)
        tablaF.agregarPadre(tablaSimbolosActual)  #
        tablaSimbolosActual = tablaF
        stackParam.append(t[3])
        cuadruActual = cuadruploList.CuadSize()
        varLocal = 0
    else:
        print("Funcion previamente declarada")
        raise SyntaxError

#diagrama para salir de un bloque , preferiblemente de funciones
def p_Fin_Bloque(t):
    '''
    Fin_Bloque :
    '''
    global tablaSimbolosActual,cuadruploList, stackParam, procedimientoList, cuadruActual, varLocal, proScope
    tablaSimbolosActual = tablaSimbolosActual.padre
    cuadruploList.normalCuad('RET',None,None,None)
    functId = stackParam.pop(0)
    procedimientoList.meteParametros(functId, stackParam)
    if (stackParam[0] is None):
      cantParam = 0;
    else:
      cantParam = len(stackParam)
    procedimientoList.normalLista(functId, cantParam, varLocal, cuadruActual, proScope)


    #algo similar a declaraA
def p_FuncionA(t):
    '''
    FuncionA : DeclaraBase  FuncionB
    | empty
    '''
    global stackParam

    stackParam.append(t[1])

#instancias multiples parametros de variables
def p_FuncionB(t):
    '''
    FuncionB : COMMA FuncionA
      | empty
    '''

#tipo devuelve el tipo y junto con identificador , instancia un objeto en la tabla de variables
def p_Parametro(t):
    '''
    Parametro : Tipo IDENTIFICADOR
    '''
    
    global tablaSimbolosActual,tablaGlobal,memoriaIDClases,stackOperando
    existe = tablaSimbolosActual.buscar(t[2])
    if (existe is None):
        existe = tablaSimbolosActual.padre
        if(not(tablaSimbolosActual.padre is None)):
            existe = tablaSimbolosActual.padre.buscar(t[2])
            if(existe is None):
                stackOperando.append(t[2])
                t[0] = t[1]
        else:
            stackOperando.append(t[2])
            t[0] = t[1]
        
    else:
        print("variable previamente declarada")
        raise SyntaxError

#inicio de un bloque
def p_Bloque(t):
    '''
    Bloque : BRACKET_IZQ BloqueA BRACKET_DER
    '''

#cosas que puede hacer dentro de un bloque
#ciclos, Asignacoin, llamadas a funcion , condiciones, inputs de entrada, inputs de salida, y retorno
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
# guarda el retorno en el stack de operadores 
def p_Retorno(t):
  '''
  Retorno : KEYWORD_RETORNO
  '''
  global stackOperador
  stackOperador.append(t[1])
#genera el cuadruplo corespondiente a retorno
def p_FinRetorno(t):
  '''
  FinRetorno : 
  '''
  global cuadruploList,stackOperando,stackOperador
  op = stackOperador.pop()
  op1 = stackOperando.pop()
  cuadruploList.normalCuad(op,op1,None,None)
    
#diagrama para hacer o una llamada funcion o una asignacion
def p_DecOAss(t):
    '''
      DecOAss : AsignaAux AsignaClass DecOAssA
    '''

#diagrama complementario del pasado
def p_DecOAssA(t):
    '''
      DecOAssA :  LlamadaFuncion SEMICOLON
      | Asignacion
    '''

#diagrama para manejar la recursion de elemento sdentro de un bloque
def p_BloqueB(t):
    '''
    BloqueB :  BloqueA
    | empty
    '''

#diagrama para empezar a instanciar una clase
def p_Clase(t):
    '''
     Clase : ClaseAux Bloque_Clase
    '''

#diagrama complementario del anterior
def p_ClaseAux(t):
    '''
     ClaseAux : KEYWORD_CLASE IDENTIFICADOR_CLASE ClaseA
    '''
    global tablaSimbolosActual, llavetablaclase, cuadruploList, claseJumps,nuevasClases,listaMemorias, proScope
    proScope = t[2]
    existe = tablaSimbolosActual.buscar(t[2])
    if (existe is None):
        nuevaClaseG = MemoriaReal(nuevasClases)
        nuevasClases = nuevasClases + 10000
        nuevaClaseL = MemoriaReal(nuevasClases)
        nuevasClases = nuevasClases + 10000
        memo = nuevaClaseG.insertaBooleano()
        listaMemorias.append(nuevaClaseG)
        listaMemorias.append(nuevaClaseL)
        memob = nuevaClaseL.insertaBooleano()
        if (llavetablaclase is None):    
            tablaSimbolosActual.insertarClase(t[2], memo)
            tablaC = TablaSimbolos()
            tablaC.insertar(t[2], 'clase',memo)
            tablaC.id = memo
            tablaC.agregarPadre(tablaSimbolosActual)
            tablaSimbolosActual.agregarHijo(tablaC)
            tablaSimbolosActual = tablaC
        else:
            heredado = t[1] + "," + llavetablaclase
            tablaSimbolosActual.insertarClase(t[2],memo ,llavetablaclase)
            tablaC = TablaSimbolos()
            tablaC.insertar(t[2], 'clase',memo)
            tablaC.agregarPadre(tablaSimbolosActual)
            tablaC.id = memo
            tablaSimbolosActual.agregarHijo(tablaC)
            tablaSimbolosActual = tablaC
            llavetablaclase = ""
        cuadruploList.normalCuad('Goto',None, None, 'pendienteClase')
        claseJumps.append(cuadruploList.CuadSize())
    else:
        print("Clase ya existente");
        raise SyntaxError

#{'tipo':'clase','memo': memID,'id':id,'herencia':herencia}
#Funcion para definir herencia
def p_ClaseA(t):
    '''
    ClaseA : COLON IDENTIFICADOR_CLASE
     | empty
    '''
    global tablaSimbolosActual, llavetablaclase
    if (len(t) == 3):
        existe = tablaSimbolosActual.buscar(t[2])
        if (existe is None):
            print("Clase a heredar no existente")
        else:
            existe['herencia']
            if (not(existe['herencia'] is None)):
                print("Herencia maxima de 1 solo nivel");
                raise SyntaxError
            else:
                llavetablaclase = t[2]

#como bloque , mas enfocado a las clases , con la diferencia uqe un bloque de clase termina en semicolon
def p_Bloque_Clase(t):
    '''
      Bloque_Clase : BRACKET_IZQ Bloque_ClaseA BRACKET_DER SEMICOLON Fin_Bloque_Clase
    '''
    print("haber cuando corriste");

#regresar a la tabla global despues de salir de clases.
def p_Fin_Bloque_Clase(t):
    '''
    Fin_Bloque_Clase :
    '''
    global tablaSimbolosActual, cuadruploList, proScope
    tablaSimbolosActual = tablaSimbolosActual.padre
    cuadruploList.normalCuad('RET')
    proScope = "global"

#funcion para manerar si asignar declaracion o funciones dentro de la clase objeto
def p_Bloque_ClaseA(t):
    '''
      Bloque_ClaseA : Bloque_ClaseB Bloque_ClaseC
    '''

#diagrama especifico para Declaracion
def p_Bloque_ClaseB(t):
    '''
      Bloque_ClaseB : Declaracion Bloque_ClaseB
      | empty
    '''

#diagrama especifico para clase
def p_Bloque_ClaseC(t):
    '''
      Bloque_ClaseC : Funcion Bloque_ClaseC
      | empty
    '''

#diagrama para las reglas de Ciclo
#ciclo check termina generando el cuadruplo de ciclo
def p_Ciclo(t):
    '''
      Ciclo : CicloAux PARENTESIS_IZQ Expresion CicloCheck Bloque
    '''
    global cuadruploList, indiceCondicion
    Ciclodir, CicloCheck = t[1], t[4]
    cuadruploList.SaltaCuad("Goto", Ciclodir)
    cuadruploList.AgregarSalto(CicloCheck, indiceCondicion)

#mete al stack de operadores la keyword mientras comoGotoF
def p_CicloAux(t):
  '''
    CicloAux : KEYWORD_MIENTRAS
  '''
  global stackOperador, cuadruploList
  stackOperador.append("GotoF")
  t[0] = cuadruploList.CuadSize()

#termina el cuadruplo de ciclo
def p_CicloCheck(t):
  '''
    CicloCheck : PARENTESIS_DER
  '''
  global cuadruploList, stackOperador, indiceCondicion, stackOperando
  op = stackOperador.pop()
  indiceCondicion = stackOperando.pop()
  t[0] = cuadruploList.SaltaCuad(op)

#diagrama para generar inputs de entrada
def p_Entrada(t):
    '''
      Entrada : KEYWORD_ENTRADA IDENTIFICADOR SEMICOLON
    '''

#diagrama para generar salida de variables y expresiones a terminal
def p_Salida(t):
    '''
      Salida : Salida_Key_Aux  Expresion SEMICOLON Salida_fin
    '''
#Agrega Salida al stack de operadores
def p_Salida_Key_Aux(t):
    '''
    Salida_Key_Aux : KEYWORD_SALIDA
    '''
    global stackOperador
    stackOperador.append(t[1])

#funcion que finaliza el cuadruplo
def p_Salida_fin(t):
    '''
    Salida_fin :
    '''
    global cuadruploList,stackOperando,stackOperador
    op = stackOperador.pop()
    op1 = stackOperando.pop()
    cuadruploList.normalCuad(op,op1)

#diagrama de condicion
def p_Condicion(t):
    '''
      Condicion : CondicionAux PARENTESIS_IZQ Expresion CondicionCheck Bloque TerminaCondicion CondicionA
    '''
    global cuadruploList, indiceCondicion, elseDir
    termina = t[4]
    cuadruploList.AgregarSalto(termina, indiceCondicion, elseDir)

#diagrama para meter al stack de operadores un gotof si se encuentra con un Si
def p_CondicionAux(t):
  '''
    CondicionAux : KEYWORD_SI
  '''
  global stackOperador
  stackOperador.append("GotoF")
  

#actualiza el cuadruplo
def p_CondicionCheck(t):
  '''
    CondicionCheck : PARENTESIS_DER
  '''
  global cuadruploList, stackOperador, saltoCond, indiceCondicion, stackOperando
  op = stackOperador.pop()
  saltoCond = cuadruploList.SaltaCuad(op)
  indiceCondicion = stackOperando.pop()
  t[0] = saltoCond

#diagrama para cargar la instruccion Goto al terminar la condicion
def p_TerminaCondicion(t):
  '''
  TerminaCondicion :
  '''
  global cuadruploList
  cuadruploList.SaltaCuad("Goto")

#corre el bloque sino si es que no se cumple la condicion de si
def p_CondicionA(t):
    '''
      CondicionA : SinoAux Bloque SinoBloqueFin
      | empty
    '''

#corre los los contadores de tamano de cuadruplo para saber donde ir al empezar sino
def p_SinoAux(t):
  '''
    SinoAux : KEYWORD_SINO
  '''
  global cuadruploList, elseDir
  elseDir = cuadruploList.CuadSize()
  
#se actualiza la direccion de salto al terminar el bloque de sino
def p_SinoBloqueFin(t):
  '''
    SinoBloqueFin :
  '''
  global cuadruploList
  cuadruploList.AgregarSalto(elseDir-1, None, cuadruploList.CuadSize())

#cuadro principal de expresion
def p_Expresion(t):
    '''
      Expresion : Expresion ExpresionA
      | Expres
    '''

    #Llama auxiliar y la siguiente parte de la expresion
def p_ExpressionA(t):
    '''
    ExpresionA : ExpresionAux Expres
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO AND OR", stackOperador)
    if (top == '&&' or top == '||'):
        temporales[indicetemporales] = "temporalExpresion"
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1, oper2)
        memID = 0
        if(sem == 0):
            memID = listaMemorias[3].insertaBooleano()
        elif(sem == 1):
            memID = listaMemorias[3].insertaEntero()
        elif(sem == 2):
            memID = listaMemorias[3].insertaReal()
        elif(sem == 3):
            memID = listaMemorias[3].insertaCaracter()
        elif (sem == 5):
            print("ERROR, los tipos de datos proveidos no son compatibles entre si.")
        cuadruploList.normalCuad(op, oper1, oper2, memID)
        #INSERTAR FUNCION DE CHEQUEO DE SEMANTICA, INSERTAR TEMPORALES ADECUADOS
        stackOperando.append(memID)

#recibe los operadores And y Or
def p_ExpresionAux(t):
    '''
    ExpresionAux : OPERADOR_AND_OR
    '''
    global stackOperador
    stackOperador.append(t[1])

#siguiente parte de expresion, corre otras jerarquias de expresion
def p_Expres(t):
    '''
    Expres : Expres ExpresA
    | Exp
    '''

#llama la auxiliar de expresion y un nivel mas abajo de expresion
def p_ExpresA(t):
    '''
    ExpresA : ExpresAux Exp
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO COMPARATIVO", stackOperador)
    if (top == '<' or top == '>'):
        temporales[indicetemporales] = "temporalExpres"
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1, oper2)
        memID = 0
        if(sem == 0):
            memID = listaMemorias[3].insertaBooleano()
        elif(sem == 1):
            memID = listaMemorias[3].insertaEntero()
        elif(sem == 2):
            memID = listaMemorias[3].insertaReal()
        elif(sem == 3):
            memID = listaMemorias[3].insertaCaracter()
        elif (sem == 5):
            print("ERROR, los tipos de datos proveidos no son compatibles entre si.")
        cuadruploList.normalCuad(op, oper1, oper2, memID)
        #INSERTAR FUNCION DE CHEQUEO DE SEMANTICA, INSERTAR TEMPORALES ADECUADOS
        stackOperando.append(memID)
        indicetemporales = indicetemporales + 1
        temporales.append(None)

#carga los operadores comparativos
def p_ExpresAux(t):
    '''
    ExpresAux : OPERADOR_COMPARATIVO
    '''
    global stackOperador
    stackOperador.append(t[1])

#carga siguientes niveles de expresion
def p_Exp(t):
    '''
    Exp : Exp ExpA
    | Termino
    '''
#carga el siguiente nivel de expresion
def p_ExpA(t):
    '''
    ExpA : ExpAux Termino
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    if (top == '+' or top == '-'):
        temporales[indicetemporales] = "temporalExp"
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        memID = 0
        sem = checkSemantica.Semantica(op,oper1, oper2)
        if(sem == 0):
            memID = listaMemorias[3].insertaBooleano()
        elif(sem == 1):
            memID = listaMemorias[3].insertaEntero()
        elif(sem == 2):
            memID = listaMemorias[3].insertaReal()
        elif(sem == 3):
            memID = listaMemorias[3].insertaCaracter()
        elif (sem == 5):
            print("ERROR, los tipos de datos proveidos no son compatibles entre si.")
        cuadruploList.normalCuad(op, oper1, oper2, memID)
        #INSERTAR FUNCION DE CHEQUEO DE SEMANTICA, INSERTAR TEMPORALES ADECUADOS
        stackOperando.append(memID)
        indicetemporales = indicetemporales + 1
        temporales.append(None)

#carga los operadores de suma y resta
def p_ExpAux(t):
    '''
    ExpAux : EXP_OPERADOR
    '''
    global stackOperador
    stackOperador.append(t[1])

#carga la siguientes partes de expresion
def p_Termino(t):
    '''
    Termino : Termino TerminoA
    | Factor
    '''
#siguiente nivel de expresion compara
# el * e / y general el cuadruplo correcto
def p_TerminoA(t):
    '''
    TerminoA : TerminoAux Factor
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    if (top == '*' or top == '/'):
        temporales[indicetemporales] = "temporalTermino"
        op = stackOperador.pop()
        oper2 = stackOperando.pop()
        oper1 = stackOperando.pop()
        sem = checkSemantica.Semantica(op,oper1, oper2)
        memID = 0
        if(sem == 0):
            memID = listaMemorias[3].insertaBooleano()
        elif(sem == 1):
            memID = listaMemorias[3].insertaEntero()
        elif(sem == 2):
            memID = listaMemorias[3].insertaReal()
        elif(sem == 3):
            memID = listaMemorias[3].insertaCaracter()
        elif (sem == 5):
            print("ERROR, los tipos de datos proveidos no son compatibles entre si.")
        #INSERTAR FUNCION DE CHEQUEO DE SEMANTICA, INSERTAR TEMPORALES ADECUADOS
        cuadruploList.normalCuad(op, oper1, oper2, memID)
        stackOperando.append(memID)
        indicetemporales = indicetemporales + 1
        temporales.append(None)

#inserta los terminos * y / en el stack de operadores
def p_TerminoAux(t):
    '''
    TerminoAux : TERM_OPERADOR
    '''
    global stackOperador
    stackOperador.append(t[1])
#Factor es el valor "atmopico de una operacion, el caul es el resultaod de algo entre parentesis"
# o de los elementos atomicos
def p_Factor(t):
    '''
      Factor : ValorSalida
      | ParentesisInit Expresion ParentesisFin
    '''
    # usar parentesis para meterlo como fondo falso
    # usar parentesis para meterlo como fondo falso

#mete un fondo falso a la pila de operadores
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

#atributos de llamda funcion para llamar adecuadamente a la funcion apropiadamente
def p_LlamadaFuncion(t):
    '''
      LlamadaFuncion : INTER_IZQ LlamadaFuncionA INTER_DER FinalLlamada
    '''
    global paramCont
    paramCont = 1


#diagrama de sintaxis para asignar multiples parametros a una llamada de funcion
def p_LlamadaFuncionA(t):
    '''
      LlamadaFuncionA : Expresion CorreExpresion LlamadaFuncionB
      | empty
    '''
#genera cuadruplo de los parametros instanciados
def p_CorreExpresion(t):
  '''
  CorreExpresion : 
  '''
  global stackOperando, paramCont
  op1 = stackOperando.pop()
  texto = "param" + str(paramCont)
  cuadruploList.normalCuad(texto, op1)
  paramCont = paramCont + 1

#recursion para manejar los parametros que sean necesarios
def p_LlamadaFuncionB(t):
    '''
      LlamadaFuncionB : COMMA LlamadaFuncionA
      | empty
    '''
#genera cuadruplo final
#cuadruplo gosub que te lleva a la funcion
def p_FinalLlamada(t):
  '''
    FinalLlamada :
  '''
  global auxstackParam, cuadruploList,stackOperador
  if (auxstackParam):
    print ("ZOOL", auxstackParam)
    auxstackParam.pop()
    cuadruploList.normalCuad("Gosub", stackOperando.pop())
    stackOperador.pop()
    auxstackParam = []

#Diagrama para generar rapidamente las llamadas de parametro ,sean ,sencillas
#llamadas a funcion, o inclusive arreglos
def p_DeclaraBase(t):
    '''
    DeclaraBase : Parametro DeclaraA
    '''
    global varLocal,tablaSimbolosActual,stackOperando,memoriaVirtual
    varLocal = varLocal + 1
    if(not(t[2] is None)):
        limInf = t[2]['dimensionA']
        limSup = t[2]['dimensionB']
        tipo = t[1]
        memID = 0
        tipoID = 0
        total = limInf*limSup
        inferior = total - 1
        op = stackOperando.pop()
        t[0] = op
        existe = tablaSimbolosActual.buscar(op)
        if(existe is None):
            if(tablaSimbolosActual.padre is None):
                if(not (tipo=='entero' or tipo =='booleano' or tipo =='caracter'or tipo =='real')):
                    existe = tablaGlobal.buscarHijos(t[1])
                    if( not (existe is None)):
                        #idValue = existe['memo']
                        memID = memoriaIDClases.insertaClase(existe.simbolos[t[1]]['memo'],total)
                        tablaSimbolosActual.insertar(op,t[1],memID)
                        ##Sacar un id de clase, ver su tabla
                        ##generar un id por elemento global
                    else:
                        print("TIPO DECLARADO NO EXISTENTE");
                        raise SyntaxError
                else:
                    idValue = int(tablaSimbolosActual.id/10000)
                    if(tipo =='entero'):
                        memID = listaMemorias[idValue].insertaEntero(total)
                    elif(tipo =='booleano'):
                        memID = listaMemorias[idValue].insertaBooleano(total)
                    elif(tipo =='caracter'):
                        memID = listaMemorias[idValue].insertaCaracter(total)
                    elif(tipo =='real'):
                        memID = listaMemorias[idValue].insertaReal(total)


                    tablaSimbolosActual.insertar(op,tipo,memID,limInf,limSup)
                    memoriaVirtual.variablesDim[memID] = {'limInf':limInf,'limSup':limSup}
            else:
                existe = tablaSimbolosActual.padre.buscar(op)
                if(existe is None):
                    if(not (tipo=='entero' or tipo =='booleano' or tipo =='caracter'or tipo =='real')):
                        existe = tablaGlobal.buscarHijos(t[1])
                        if( not (existe is None)):
                            #idValue = existe['memo']
                            memID = memoriaIDClases.insertaClase(existe.simbolos[t[1]]['memo'],total)
                            tablaSimbolosActual.insertar(op,t[1],memID,limInf,limSup)
                            memoriaVirtual.variablesDim[memID] = {'limInf':limInf,'limSup':limSup}
                            ##Sacar un id de clase, ver su tabla
                            ##generar un id por elemento global
                        else:
                            print("TIPO DECLARADO NO EXISTENTE");
                            raise SyntaxError
                    else:
                        idValue = int(tablaSimbolosActual.id/10000)
                        print("idValue a insertar",idValue)
                        if(tipo =='entero'):
                            memID = listaMemorias[idValue].insertaEntero(total)
                        elif(tipo =='booleano'):
                            memID = listaMemorias[idValue].insertaBooleano(total)
                        elif(tipo =='caracter'):
                            memID = listaMemorias[idValue].insertaCaracter(total)
                        elif(tipo =='real'):
                            memID = listaMemorias[idValue].insertaReal(total)
                        tablaSimbolosActual.insertar(op,tipo,memID,limInf,limSup)
                        memoriaVirtual.variablesDim[memID] = {'limInf':limInf,'limSup':limSup}
                else:
                    print("VARIABLE PREVIAMENTE DECLARADA")
                    raise SyntaxError
        else:
            print("VARIABLE PREVIAMENTE DECLARADA")
            raise SyntaxError
    else:
        tipo = t[1]
        op = stackOperando.pop()
        t[0] = op
        existe = tablaSimbolosActual.buscar(op)
        if(existe is None):
            if(tablaSimbolosActual.padre is None):
                if(not (tipo=='entero' or tipo =='booleano' or tipo =='caracter'or tipo =='real')):
                    existe = tablaGlobal.buscarHijos(t[1])
                    if( not (existe is None)):
                        #idValue = existe['memo']
                        memID = memoriaIDClases.insertaClase(existe.simbolos[t[1]]['memo'])
                        tablaSimbolosActual.insertar(op,t[1],memID)
                        ##Sacar un id de clase, ver su tabla
                        ##generar un id por elemento global
                    else:
                        print("TIPO DECLARADO NO EXISTENTE");
                        raise SyntaxError
                else:
                    idValue = int(tablaSimbolosActual.id/10000)
                    if(tipo =='entero'):
                        memID = listaMemorias[idValue].insertaEntero()
                    elif(tipo =='booleano'):
                        memID = listaMemorias[idValue].insertaBooleano()
                    elif(tipo =='caracter'):
                        memID = listaMemorias[idValue].insertaCaracter()
                    elif(tipo =='real'):
                        memID = listaMemorias[idValue].insertaReal()
                    tablaSimbolosActual.insertar(op,tipo,memID)
            else:
                existe = tablaSimbolosActual.padre.buscar(op)
                if(existe is None):
                    if(not (tipo=='entero' or tipo =='booleano' or tipo =='caracter'or tipo =='real')):
                        existe = tablaGlobal.buscarHijos(t[1])
                        if( not (existe is None)):
                            #idValue = existe['memo']
                            memID = memoriaIDClases.insertaClase(existe.simbolos[t[1]]['memo'])
                            tablaSimbolosActual.insertar(op,t[1],memID)
                            ##Sacar un id de clase, ver su tabla
                            ##generar un id por elemento global
                        else:
                            print("TIPO DECLARADO NO EXISTENTE");
                            raise SyntaxError
                    else:
                        idValue = int(tablaSimbolosActual.id/10000)
                        if(tipo =='entero'):
                            memID = listaMemorias[idValue].insertaEntero()
                        elif(tipo =='booleano'):
                            memID = listaMemorias[idValue].insertaBooleano()
                        elif(tipo =='caracter'):
                            memID = listaMemorias[idValue].insertaCaracter()
                        elif(tipo =='real'):
                            memID = listaMemorias[idValue].insertaReal()
                        tablaSimbolosActual.insertar(op,tipo,memID)

                else:
                    print("VARIABLE PREVIAMENTE DECLARADA")
                    raise SyntaxError
        else:
            print("VARIABLE PREVIAMENTE DECLARADA")
            raise SyntaxError


#iagrama de declaracion de variables a nivel global
#o dentor de un scope , pero no como atrbutos de una funcion
def p_Declaracion(t):
    '''
    Declaracion : DeclaraBase SEMICOLON
    '''
#diagram de sintaxis para un vector    
def p_DeclaraA(t):
    '''
    DeclaraA : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER DeclaraB
    | empty
    '''
    if(len(t) == 5):
        t[0] = {'dimensionA':t[2],'dimensionB':t[4]['dimensionB']}
        limInf = t[2]
    elif(len(t) == 4):
        t[0] = {'dimensionA':t[2],'dimensionB':1}
    else:
        t[0] =  None

#diagrama de sintaxis para una matriz
def p_DeclaraB(t):
    '''
    DeclaraB : CORCHETE_IZQ CONST_NUMERO_ENT CORCHETE_DER 
    | empty
    '''
    if(t[1] == '['):
        t[0] = {"dimensionB":t[2]}
    else:
        t[0] =  {"dimensionB":1}
#diagrama que devuele los valores atomicos de una expresion
def p_ValorSalida(t):
    '''
      ValorSalida : NumeroEntero
      | Caracter
      | NumeroReal
      | Booleano
      | KEYWORD_NULO
      | LlamadaIDs
    '''
#diagrama para la generaciond e llamadas id y llamadas de una funcion dentro para el uso de Valor Salida
def p_LlamadaIDs(t):
  '''
    LlamadaIDs : LlamadaIDsAux LlamadaIDsA
  '''
#Diagrama donde se anexa el identificador como una variable dentro del stack de operandos
def p_LlamadaIDsAux(t):
  '''
  LlamadaIDsAux : IDENTIFICADOR
  '''
  global stackOperando, buscadorClase,pilaClase, procedimientoList, auxstackParam, tablaGlobal, cuadruploList, stackOperador
  existe = None
  existe = tablaSimbolosActual.buscar(t[1])
  this = stackOperador[len(stackOperador)-1]
  if (existe is None):
      existe = tablaSimbolosActual.padre.buscar(t[1])
      if (existe is None and (not (this == "."))):
          print("El termino no ha sido declarado: ", t[1])  
      elif(not(existe is None)):
          if(existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
              stackOperando.append(existe['memo'])
          elif(existe['tipo'] =='funcion'):
              auxstackParam.append(t[1])
              auxstackParam.append(procedimientoList.buscar(t[1]))
              cuadruploList.normalCuad("ERA", t[1])
              #if (auxstackParam[1][0] is not None):
              auxstackParam[1].reverse()
              stackOperando.append(existe['memo']) 
              stackOperador.append("(")
              stackOperando.append(t[1])
          else:
              buscadorClase = tablaGlobal.buscar(t[1])
              pilaClase.append(t[1])
              stackOperando.append(existe['memo'])
      elif(not (len(stackOperador) == 0)):
        if (this == '.'):
            op1 = stackOperando.pop()
            op = stackOperador.pop()
            exis = tablaGlobal.buscar(op1)
            if(exis is None):
                print("Llamada no posible, clase no identificada")
                raise SyntaxError
            else:
                cuadruploList.normalCuad(op, op1)
                if(not(exis.buscar(t[1]) is None)):
                    exis = exis.buscar(t[1])
                    if(exis['tipo'] == 'real' or exis['tipo'] == 'entero' or exis['tipo'] == 'booleano' or exis['tipo'] == 'caracter'):
                        stackOperando.append(exis['memo']) 
                    elif(exis['tipo'] == 'funcion'):
                        auxstackParam.append(exis['memo'])
                        auxstackParam.append(procedimientoList.buscar(t[1]))
                        cuadruploList.normalCuad("ERA", t[1])
                        #if (auxstackParam[1][0] is not None):
                        auxstackParam[1].reverse()
                        stackOperando.append(t[1]) 
                        stackOperador.append("(")  

  else:
    #see t[1]
    if(existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):      
        stackOperando.append(existe['memo'])
    elif(existe['tipo'] == 'funcion'):
        print("NO PUEDES GENERAR UNA FUNCION DENTRO DE OTRA")
        raise SyntaxError
    else:
        buscadorClase = tablaGlobal.buscarHijos(existe['tipo'])
        stackOperando.append(existe['memo'])



def p_LlamadaIDsA(t):
  '''
    LlamadaIDsA : Terminal
    | LlamadaFuncion
  '''
#anexa constante entera a la tabla de simbolos,
#asigna valor de memoria ,y la mete al stack de operandos
def p_NumeroEntero(t):
    '''
      NumeroEntero : CONST_NUMERO_ENT
    '''
    global tablaConstantes,stackOperando,listaMemorias
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaEntero()
        tablaConstantes.insertar(t[1], "entero",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])

#anexa constante caracter a la tabla de simbolos,
#asigna valor de memoria ,y la mete al stack de operandos
def p_Caracter(t):
    '''
      Caracter : CONST_CARACTERES
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaCaracter()
        tablaConstantes.insertar(t[1], "caracter",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])

#anexa constante real a la tabla de simbolos,
#asigna valor de memoria ,y la mete al stack de operandos
def p_NumeroReal(t):
    '''
      NumeroReal : CONST_NUMERO_REAL
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaReal()
        tablaConstantes.insertar(t[1], "real",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])

#anexa constante Booleana a la tabla de simbolos,
#asigna valor de memoria ,y la mete al stack de operandos
def p_Booleano(t):
    '''
      Booleano : CONST_BOOLEANO
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaBooleano()
        tablaConstantes.insertar(t[1], "booleano",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])

#para manejar dentro de llamadas ids, arreglos , llamadas a funcion , llamadas a atributos de clase
def p_Terminal(t):
    '''
      Terminal : AsignaClass
    '''
    

#meter el punto como operador para accesar rapidamente las variables de clase y obtener las direcciones de memoria respectivas
def p_PuntoAux(t):
    '''
    PuntoAux : PUNTO
    '''
    global stackOperador
    stackOperador.append(t[1])





import ply.yacc as yacc

parser = yacc.yacc(start='Programa')

fileload = input('Nombre del archivo de entrada: ')

with open(fileload) as fileval:
  result = parser.parse(fileval.read())
  lexer.input(fileval.read())

# Tokenize
# while True:
#    tok = lexer.token()
#    if not tok:
#        break      # No more input
#    print(tok)

print(result)