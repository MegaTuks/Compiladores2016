# Andres Marcelo Garza Cantu A00814236
# Ruben Alejandro Hernandez Gonzalez A01175209
from memoria import *
from tablas import *
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
    r'[VERDADERO|FALSO]'
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
llavetablactual = ""
llavetablaclase = None  # se usa para asegurar que haya herencia
buscadorClase = None  # se usa para buscar en las tablas clase si existen las variables o funciones a llamar
pilaClase = []  # se usa para guardar la variable de clase hasta acabar las operaciones con ella
stackOperador = []  # se usa para guardar los operadores del momento
stackOperando = []  # se usa para guardar las ,variables, constantes, temporales;
pilaSaltos = [] # se usa para actualizar los saltos, cuando una funcion , ciclo o condicion termina se actualiza
tablaSimbolosActual = TablaSimbolos()
tablaSimbolosActual.insertar('global', 'global',memoriaGlobal.insertaBooleano())
tablaGlobal = tablaSimbolosActual
tablaConstantes = TablaConstantes()
cuadruploList = Cuadruplos()
cuadruActual = 0
varLocal = 0
procedimientoList = Procedimientos()
temporales = []
temporales.append(None)
indicetemporales = 0
indiceCondicion = ""
saltoCond = None
claseJumps = []
stackParam = []
auxstackParam = []
paramCont = 1
checkSemantica = claseCuboSemantico()

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

    global tablaSimbolosActual,cuadruploList,stackOperador, procedimientoList, stackOperando, procedimientoList
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
    global cuadruploList,pilaSaltos, procedimientoList
    cuadruploList.normalCuad('Goto',None,None, 'pendiente')
    procedimientoList.normalLista("principal", 0, 0, 0)

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
    # parte de heacuadruplo para expresion
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
    global tablaSimbolosActual, tablaGlobal, buscadorClase, stackOperando, auxstackParam, procedimientoList
    existe = tablaSimbolosActual.buscar(t[1])
    existeglobal = tablaGlobal.buscar(t[1])
    print('CHINGADERA QUE BUSCO',t[1])
    print("lectura", existe['tipo'])
    print('lecturaGlobal :>>>>>>>',existeglobal)
    print('LectoraClase',buscadorClase)
    if (buscadorClase is None):
        if (existe is None):
            print("variable no existe en este punto", buscadorClase)
        elif (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
            buscadorClase = None  # funcion que encuentra el valor atomico del chiste
            print("el tipo es ", existe['tipo'])
            stackOperando.append(existe['memo'])
        elif (not (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero')):
            if (existe['tipo'] == 'funcion'):
                print("no puedes hacer asignacion con funcion")
            else:
                buscadorClase = tablaGlobal.buscarHijos(existe)
                print("BUSCADORCLASEB")
                if (not (buscadorClase is None)):
                    print("buscador Clase:", buscadorClase)
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
        print('CHINGADERA QUE BUdddSCO',t[1])
        existe = buscadorClase.buscar(t[1])
        print("buscar dentro de clase", existe)
        if (existe is None):
            print("existe is None")
        elif (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
            print("aqui meter en vector que es una variable de tipo: ", existe)
            stackOperando.append(existe['memo'])
            buscadorClase = None
        elif (existe['tipo'] == 'funcion'):
            print("aqui meter en vector que es una funcion")
            buscadorClase = None
        else:
            print("guardar en variable , checar meter en stack")
            buscadorClase = tablaGlobal.buscarHijos(existe['tipo'])
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
    global tablaSimbolosActual, stackParam, cuadruploList, cuadruActual, varLocal,tablaGlobal,listaMemorias
    stackParam = []
    existe = tablaSimbolosActual.buscar(t[3])
    if (existe is None):
        tipoID = t[2]
        memID = 0
        if(not (tipoID == 'entero' or tipoID =='booleano' or tipoID =='caracter' or tipoID =='real')):
            print("algo")
            idValue = int(tablaSimbolosActual.id/10000)
            existe = tablaGlobal.buscarHijos(t[2])
            ########################################################################ACABAR CLASE
        else:
            idValue = int(tablaSimbolosActual.id/10000)
            
            if(tipoID =='entero'):
                memID = listaMemorias[idValue].insertaEntero()
            elif(tipoID =='booleano'):
                memID = listaMemorias[idValue].insertaBooleano()
            elif(tipoID =='caracter'):
                memID = listaMemorias[idValue].insertaCaracter()
            elif(tipoID =='real'):
                memID = listaMemorias[idValue].insertaReal()


        tablaSimbolosActual.insertarFuncion(t[3], t[2], memID)  # guarda que es Tipo funcion en la tabla de simbolos
        print("insertar funcion en tabla", tablaSimbolosActual.simbolos)
        tablaF = TablaSimbolos()
        tablaF.insertar(t[3], t[2],memID)
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
        memID = 0
        tipoID = t[1]
        if(not (tipoID == 'entero' or tipoID =='booleano' or tipoID =='caracter' or tipoID =='real')):
            print("algo")
            idValue = int(tablaSimbolosActual.id/10000)
            existe = tablaGlobal.buscarHijos()
            ##Sacar un id de clase, ver su tabla
            ##generar un id por elemento global
            ########################################################################ACABAR CLASE
        else:
            idValue = int(tablaSimbolosActual.id/10000)
            
            if(tipoID =='entero'):
                memID = listaMemorias[idValue].insertaEntero()
            elif(tipoID =='booleano'):
                memID = listaMemorias[idValue].insertaBooleano()
            elif(tipoID =='caracter'):
                memID = listaMemorias[idValue].insertaCaracter()
            elif(tipoID =='real'):
                memID = listaMemorias[idValue].insertaReal()
        tablaSimbolosActual.insertar(t[2], t[1], memID)
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
    global tablaSimbolosActual, llavetablaclase, cuadruploList, claseJumps,nuevasClases,listaMemorias
    existe = tablaSimbolosActual.buscar(t[2])
    print("ver tabla antes de entrar a clase", tablaSimbolosActual.simbolos)
    if (existe is None):
        nuevaClaseG = MemoriaReal(nuevasClases)
        nuevasClases = nuevasClases + 10000
        nuevaClaseL = MemoriaReal(nuevasClases)
        nuevasClases+10000
        memo = nuevaClaseG.insertaBooleano()
        if (llavetablaclase is None):    
            
            tablaSimbolosActual.insertarClase(t[2], memo)
            tablaC = TablaSimbolos()
            tablaC.insertar(t[2], 'clase',memo)
            tablaC.agregarPadre(tablaSimbolosActual)
            tablaSimbolosActual.agregarHijo(tablaC)
            tablaSimbolosActual = tablaC
            print("insertaste la clase", tablaSimbolosActual.padre.simbolos)
        else:
            heredado = t[1] + "," + llavetablaclase
            tablaSimbolosActual.insertarClase(t[2],memo ,llavetablaclase)
            tablaC = TablaSimbolos()
            tablaC.insertar(t[2], 'clase',memo)
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
        print("ver tabla padre", tablaSimbolosActual.simbolos)
        print("existe la clase %s", t[2])
        if (existe is None):
            print("Clase a heredar no existente")
        else:
            existe['herencia']
            if (not(existe['herencia'] is None)):
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
    cuadruploList.normalCuad('RET')


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
    global cuadruploList, indiceCondicion
    print("TEMPORAL DE CICLO", indiceCondicion)
    Ciclodir, CicloCheck = t[1], t[4]
    cuadruploList.SaltaCuad("Goto", Ciclodir)
    cuadruploList.AgregarSalto(CicloCheck, indiceCondicion)


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
  global cuadruploList, stackOperador, indiceCondicion, stackOperando
  op = stackOperador.pop()
  indiceCondicion = stackOperando.pop()
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
    cuadruploList.normalCuad(op,op1)

def p_Condicion(t):
    '''
      Condicion : CondicionAux PARENTESIS_IZQ Expresion CondicionCheck Bloque CondicionA
    '''
    global cuadruploList, indiceCondicion
    termina = t[4]
    cuadruploList.AgregarSalto(termina, indiceCondicion)


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
  global cuadruploList, stackOperador, saltoCond, indiceCondicion, stackOperando
  op = stackOperador.pop()
  saltoCond = cuadruploList.SaltaCuad(op)
  indiceCondicion = stackOperando.pop()
  t[0] = saltoCond


def p_CondicionA(t):
    '''
      CondicionA : SinoAux SinoCheck SinoBloqueFin
      | empty
    '''
    global cuadruploList, temporales, indicetemporales, indiceCondicion
    salto, SinoDir = t[2], t[3]
    cuadruploList.AgregarSalto(saltoCond, indiceCondicion)
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
      LlamadaFuncion : INTER_IZQ LlamadaFuncionA INTER_DER FinalLlamada
    '''
    global paramCont
    print ("ENTRA ZOOL")
    paramCont = 1



def p_LlamadaFuncionA(t):
    '''
      LlamadaFuncionA : Expresion CorreExpresion LlamadaFuncionB
      | empty
    '''

def p_CorreExpresion(t):
  '''
  CorreExpresion : 
  '''
  global stackOperando, paramCont
  op1 = stackOperando.pop()
  texto = "param" + str(paramCont)
  cuadruploList.normalCuad(texto, op1)
  paramCont = paramCont + 1


def p_LlamadaFuncionB(t):
    '''
      LlamadaFuncionB : COMMA LlamadaFuncionA
      | empty
    '''

def p_FinalLlamada(t):
  '''
    FinalLlamada :
  '''
  global auxstackParam, cuadruploList
  if (auxstackParam):
    print ("ZOOL", auxstackParam)
    cuadruploList.normalCuad("Gosub", auxstackParam.pop(0))
    stackOperador.pop()
    auxstackParam = []

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
    global tablaSimbolosActual, claseJumps,listaMemorias, procedimientoList, varLocal
    mem =  listaMemorias[0].insertaEntero()
    tablaSimbolosActual.insertarFuncion(t[1], 'entero', mem)
    tablaM = TablaSimbolos()
    tablaM.agregarPadre(tablaSimbolosActual)
    tablaSimbolosActual.agregarHijo(tablaM)
    tablaSimbolosActual = tablaM
    cuadruploList.updateCuad(0, "Goto", None, None, cuadruploList.CuadSize())
    procedimientoList.updateLista(0, "principal", 0, varLocal, cuadruploList.CuadSize())
    for x in claseJumps:
      cuadruploList.updateCuad(x-1, "Goto", None, None, cuadruploList.CuadSize())


def p_FinBloquePrincipal(t):
    '''
    FinBloquePrincipal :
    '''
    global tablaSimbolosActual, cuadruploList, procedimientoList
    tablaSimbolosActual = tablaSimbolosActual.padre
    print("Terminar tabla principal")
    

def p_ValorSalida(t):
    '''
      ValorSalida : NumeroEntero
      | Caracter
      | NumeroReal
      | Booleano
      | KEYWORD_NULO
      | LlamadaIDs
    '''

def p_LlamadaIDs(t):
  '''
    LlamadaIDs : LlamadaIDsAux LlamadaIDsA
  '''

def p_LlamadaIDsAux(t):
  '''
  LlamadaIDsAux : IDENTIFICADOR
  '''
  global stackOperando, buscadorClase,pilaClase, procedimientoList, auxstackParam, tablaGlobal, cuadruploList, stackOperador
  existe = None
  existe = tablaSimbolosActual.buscar(t[1])
  existeglobal = tablaGlobal.buscar(t[1])
  print("existeglobal Funcion", existeglobal)
  if (existe is None):
      existe = tablaSimbolosActual.padre.buscar(t[1])
      if (existe is None):
          print("El termino no ha sido declarado: ", t[1])
      elif(not (existeglobal is None)):
          if (existeglobal['tipo'] == 'funcion'):
            print("ZORDON")
            auxstackParam.append(t[1])
            auxstackParam.append(procedimientoList.buscar(t[1]))
            cuadruploList.normalCuad("ERA", t[1])
            #if (auxstackParam[1][0] is not None):
            auxstackParam[1].reverse()
            print("SE TIENEN LOS PARAMETROS EN LA FUNCION: ", auxstackParam)
            stackOperando.append(t[1])
            stackOperador.append("(")

      else:
          if(existe == 'real' or existe == 'booleano' or existe == 'caracter' or existe == 'entero'):
              stackOperando.append(t[1])
          elif(existe =='funcion'):
              print("meter cuadruplo con de gosub a la funcion")
              print("meter a cuadruplo de operando resultado de la funcion?")
              stackOperando.append(t[1])
          else:
              buscadorClase = tablaGlobal.buscarHijos(t[1])
              print("BUSCADORCLASEA")
              if (not (buscadorClase is None)):
                  print("buscador Clase:", buscadorClase)
                  pilaClase.append(t[1])
                  stackOperando.append(t[1])

              else:
                  print("clase no encontrada");
                  raise SyntaxError
  
  else:
      stackOperando.append(t[1])


def p_LlamadaIDsA(t):
  '''
    LlamadaIDsA : Terminal ValorSalidaB
    | LlamadaFuncion
  '''

def p_NumeroEntero(t):
    '''
      NumeroEntero : CONST_NUMERO_ENT
    '''
    global tablaConstantes,stackOperando,listaMemorias
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal ent", t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaEntero()
        tablaConstantes.insertar(t[1], "entero",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])


def p_Caracter(t):
    '''
      Caracter : CONST_CARACTERES
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal Car", t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaCaracter()
        tablaConstantes.insertar(t[1], "caracter",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])


def p_NumeroReal(t):
    '''
      NumeroReal : CONST_NUMERO_REAL
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal Real", t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaReal()
        tablaConstantes.insertar(t[1], "real",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])


def p_Booleano(t):
    '''
      Booleano : CONST_BOOLEANO
    '''
    global tablaConstantes,stackOperando
    existe = None
    existe = tablaConstantes.buscar(t[1])
    print("terminal bool", t[1])
    if (existe is None):
        memID = listaMemorias[2].insertaBooleano()
        tablaConstantes.insertar(t[1], "booleano",memID)
        stackOperando.append(memID)
    else:
        stackOperando.append(existe['memo'])


def p_Terminal(t):
    '''
      Terminal : AsignaA
    '''
    


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
funcion entero perro ¿entero rojo, caracter chokis?{
  entero azul;
  retorno azul + 4;
}
funcion caracter gatito¿?{
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

  num = num + perro¿2 , "galleta"?;
  ruby = gatito¿?;

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