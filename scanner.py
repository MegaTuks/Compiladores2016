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
tablaSimbolosActual.id = memoriaGlobal.insertaBooleano()
tablaSimbolosActual.insertar('global', 'global',tablaSimbolosActual.id)
tablaGlobal = tablaSimbolosActual
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


def p_empty(p):
    'empty :'
    pass


def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)

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

    
#goto que general el cuadruplo de la funcion principal , hacer uqe sea efectivo.
def p_Goto_Principal(p):
    '''
    Goto_Principal :
    '''
    global cuadruploList,pilaSaltos, procedimientoList
    cuadruploList.normalCuad('Goto',None,None, 'pendiente')
    procedimientoList.normalLista("principal", 0, 0, 0, "principal")

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


def p_FinBloquePrincipal(t):
    '''
    FinBloquePrincipal :
    '''
    global tablaSimbolosActual, cuadruploList, procedimientoList, proScope
    tablaSimbolosActual = tablaSimbolosActual.padre
    print("Terminar tabla principal")
    proScope = "global"
    

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
        print("verifica generar la clase ANTES de mandarla a llamar")
        raise SyntaxError
    else:
        t[0] =  t[1]


def p_Asignacion(t):
    ''' Asignacion : IGUALSIM Expresion SEMICOLON 
    '''
    # parte de heacuadruplo para expresion
    global stackOperador,stackOperando,cuadruploList
    print("stack operando antes de lista", stackOperando)
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
    global tablaSimbolosActual, tablaGlobal, buscadorClase, stackOperando, auxstackParam, procedimientoList,cuadruploList
    existe = tablaSimbolosActual.buscar(t[1])
    existeglobal = tablaGlobal.buscar(t[1])
    print("lectura", existe)
    print('lecturaGlobal',existeglobal)
    if (buscadorClase is None):
        if (existe is None):
            print("variable no existe en este punto", buscadorClase)
        elif (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
            print("el tipo es ", existe['tipo'])
            print('el nombre es',existe)
            stackOperando.append(existe['memo'])
        elif (not (existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero')):
            if (existe['tipo'] == 'funcion'):
                print("no puedes hacer asignacion con funcion")
            else:
                buscadorClase = tablaGlobal.buscarHijos(existe['tipo'])
                print("Se puso a buscar clase :", buscadorClase)
                print("a ver cual es existe",existe)
                if (not (buscadorClase is None)):
                    print("buscador Clase:", buscadorClase)
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
                print("operacion de cuadruplo . ")
                cuadruploList.normalCuad(op,op1,None,existe['memo'])
                stackOperando.append(existe['memo'])
                buscadorClase = None
        elif (existe['tipo'] == 'funcion'):
            print("aqui meter en vector que es una funcion")
            buscadorClase = None
        else:
            print("guardar en variable , checar meter en stack")
            buscadorClase = tablaGlobal.buscarHijos(existe['tipo'])
            if(buscadorClase is None):
                print("Error de sintaxis clase no existe")
            else:
                buscadorClase.id
            
            print("marcar error")
            


def p_AsignaClass(t):
    '''
    AsignaClass :  AsignaA
    | PuntoAux AsignaAux AsignaA
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
            idValue = tablaSimbolosActual.id+10000
            print("idValue antes",idValue)
            idValue =int(idValue/10000)
            print("idValue",idValue)
            existe = tablaGlobal.buscarHijos(t[2])
            if(existe is None):
                print("Tipo de clase no ha sido declarada")
            else:
                memID = memoriaIDClases.insertarClase(idValue+10000)
            ########################################################################ACABAR CLASE
        else:
           
            print("id de la tablaSimbolos", tablaSimbolosActual.id)
            idValue = int(tablaSimbolosActual.id/10000)
            idValue =idValue + 1
            print("el id value es", idValue)
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
        tablaF.id = memID
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
    global tablaSimbolosActual,cuadruploList, stackParam, procedimientoList, cuadruActual, varLocal, proScope
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
    procedimientoList.normalLista(functId, cantParam, varLocal, cuadruActual, proScope)



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
    global tablaSimbolosActual,tablaGlobal,memoriaIDClases
    existe = tablaSimbolosActual.buscar(t[2])
    if (existe is None):
        memID = 0
        tipoID = t[1]
        if(not (tipoID == 'entero' or tipoID =='booleano' or tipoID =='caracter' or tipoID =='real')):
            existe = tablaGlobal.buscarHijos(t[1])
            if( not (existe is None)):
                #idValue = existe['memo']
                print("idValue",existe.simbolos[t[1]]['memo'])
                memID = memoriaIDClases.insertaClase(existe.simbolos[t[1]]['memo'])
                print('memID',memID)
                tablaSimbolosActual.insertar(t[2],t[1],memID)
            ##Sacar un id de clase, ver su tabla
            ##generar un id por elemento global
            else:
                print("TIPO DECLARADO NO EXISTENTE");
                raise SyntaxError
            ########################################################################ACABAR CLASE
        else:
            idValue = int(tablaSimbolosActual.id/10000)
            print("idValue a insertar",idValue)
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
    global tablaSimbolosActual, llavetablaclase, cuadruploList, claseJumps,nuevasClases,listaMemorias, proScope
    proScope = t[2]
    existe = tablaSimbolosActual.buscar(t[2])
    print("ver tabla antes de entrar a clase", tablaSimbolosActual.simbolos)
    if (existe is None):
        nuevaClaseG = MemoriaReal(nuevasClases)
        nuevasClases = nuevasClases + 10000
        nuevaClaseL = MemoriaReal(nuevasClases)
        nuevasClases+10000
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
            print("insertaste la clase", tablaSimbolosActual.padre.simbolos)
        else:
            heredado = t[1] + "," + llavetablaclase
            tablaSimbolosActual.insertarClase(t[2],memo ,llavetablaclase)
            tablaC = TablaSimbolos()
            tablaC.insertar(t[2], 'clase',memo)
            tablaC.agregarPadre(tablaSimbolosActual)
            tablaC.id = memo
            tablaSimbolosActual.agregarHijo(tablaC)
            tablaSimbolosActual = tablaC
            print("insertaste la clase con herencia", tablaSimbolosActual.padre.simbolos)
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
    global tablaSimbolosActual, cuadruploList, proScope
    print("salir de tabla clase:", tablaSimbolosActual.simbolos);
    tablaSimbolosActual = tablaSimbolosActual.padre
    print("tabla a la que salio", tablaSimbolosActual.simbolos);
    cuadruploList.normalCuad('RET')
    proScope = "global"


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
      Condicion : CondicionAux PARENTESIS_IZQ Expresion CondicionCheck Bloque TerminaCondicion CondicionA
    '''
    global cuadruploList, indiceCondicion, elseDir
    termina = t[4]
    cuadruploList.AgregarSalto(termina, indiceCondicion, elseDir)

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

def p_TerminaCondicion(t):
  '''
  TerminaCondicion :
  '''
  global cuadruploList
  cuadruploList.SaltaCuad("Goto")


def p_CondicionA(t):
    '''
      CondicionA : SinoAux Bloque SinoBloqueFin
      | empty
    '''

def p_SinoAux(t):
  '''
    SinoAux : KEYWORD_SINO
  '''
  global cuadruploList, elseDir
  elseDir = cuadruploList.CuadSize()
  

def p_SinoBloqueFin(t):
  '''
    SinoBloqueFin :
  '''
  global cuadruploList
  cuadruploList.AgregarSalto(elseDir-1, None, cuadruploList.CuadSize())


def p_Expresion(t):
    '''
      Expresion : Expresion ExpresionA
      | Expres
    '''
def p_ExpressionA(t):
    '''
    ExpresionA : ExpresionAux Expres
    '''
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO AND OR", stackOperador)
    if (top == '&&' or top == '||'):
        temporales[indicetemporales] = "temporalExpresion"
        print("TEMPORAL DE && O ||", temporales[indicetemporales])
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
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO COMPARATIVO", stackOperador)
    if (top == '<' or top == '>'):
        temporales[indicetemporales] = "temporalExpres"
        print("TEMPORAL DE < O >", temporales[indicetemporales])
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
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO + -", stackOperador)
    if (top == '+' or top == '-'):
        temporales[indicetemporales] = "temporalExp"
        print("TEMPORAL DE + O -", temporales[indicetemporales])
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
    global stackOperador, stackOperando, cuadruploList, temporales, indicetemporales, checkSemantica,listaMemorias
    top = stackOperador[len(stackOperador) - 1]
    print("OPERADORES HASTA EL MOMENTO * /", stackOperador)
    if (top == '*' or top == '/'):
        temporales[indicetemporales] = "temporalTermino"
        print("TEMPORAL DE * O /", temporales[indicetemporales])
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
    print ("ENTRA UN NUEVO GUERRERO")
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
  print("entraste aqui verdad?")
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
  global auxstackParam, cuadruploList,stackOperador
  print('final de llamada',stackOperador,'operandos',stackOperando)
  if (auxstackParam):
    print ("ZOOL", auxstackParam)
    auxstackParam.pop()
    cuadruploList.normalCuad("Gosub", stackOperando.pop())
    stackOperador.pop()
    auxstackParam = []

def p_Declaracion(t):
    '''
    Declaracion : Parametro DeclaraA SEMICOLON
    '''
    global varLocal,TablaSimbolos
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
  this = stackOperador[len(stackOperador)-1]
  print("IDENTIFICADOR", t[1], "tope de pila",this)
  print("existe la cosa", existe)
  if (existe is None):
      existe = tablaSimbolosActual.padre.buscar(t[1])
      print("haber que lee este existe",existe)
      if (existe is None and (not (this == "."))):
          print("El termino no ha sido declarado: ", t[1])  
      elif(not(existe is None)):
          if(existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
              stackOperando.append(existe['memo'])
          elif(existe['tipo'] =='funcion'):
              print(t[1],"es una funcion!!!")
              auxstackParam.append(t[1])
              auxstackParam.append(procedimientoList.buscar(t[1]))
              cuadruploList.normalCuad("ERA", t[1])
              #if (auxstackParam[1][0] is not None):
              auxstackParam[1].reverse()
              print("SE TIENEN LOS PARAMETROS EN LA FUNCION: ", auxstackParam)

              stackOperando.append(existe['memo']) 
              stackOperador.append("(")
              print("meter cuadruplo con de gosub a la funcion")
              print("print: operandos",stackOperando, "operadores:",stackOperador)
              stackOperando.append(t[1])
          else:
              print("buscador Clase:", buscadorClase)
              buscadorClase = tablaGlobal.buscar(t[1])
              pilaClase.append(t[1])
              stackOperando.append(existe['memo'])
      elif(not (len(stackOperador) == 0)):
        if (this == '.'):
            op1 = stackOperando.pop()
            op = stackOperador.pop()
            exis = tablaGlobal.buscar(op1)
            if(exis is None):
                print("Llamada no posible,clase no identificada")
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
                        print("SE TIENEN LOS PARAMETROS EN LA FUNCION: ", auxstackParam)
                        stackOperando.append(t[1]) 
                        stackOperador.append("(")  

  else:
    #see t[1]

    print("a meter : ",t[1])
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
      Terminal : AsignaClass
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
    global stackOperando, buscadorClase,pilaClase, procedimientoList, auxstackParam, tablaGlobal, cuadruploList, stackOperador
    existe = None
    existe = tablaSimbolosActual.buscar(t[1])
    print("existe la cosa", existe)
    if (existe is None):
      existe = tablaSimbolosActual.padre.buscar(t[1])
      if (existe is None):
          print("El termino no ha sido declarado: ", t[1])  
      elif(not (len(stackOperador) == 0)):
        this = stackOperador[len(stackOperador)-1]
        if (this == '.'):
            op1 = stackOperando.pop()
            op = stackOperador.pop()
            exis = tablaGlobal.buscar(op1)
            if(exis is None):
                print("LlamadaFuncion no posible,clase no identificada")
            else:
                cuadruploList.normalCuad(op, op1)
                if(not(exis.buscar(t[1]) is None)):
                    auxstackParam.append(t[1])
                    auxstackParam.append(procedimientoList.buscar(t[1]))
                    cuadruploList.normalCuad("ERA", t[1])
                    #if (auxstackParam[1][0] is not None):
                    auxstackParam[1].reverse()
                    print("SE TIENEN LOS PARAMETROS EN LA FUNCION: ", auxstackParam)
                    stackOperando.append(t[1]) 
                    stackOperador.append("(")

      else:
          if(existe['tipo'] == 'real' or existe['tipo'] == 'booleano' or existe['tipo'] == 'caracter' or existe['tipo'] == 'entero'):
              stackOperando.append(existe['memo'])
          elif(existe['tipo'] =='funcion'):
              auxstackParam.append(t[1])
              auxstackParam.append(procedimientoList.buscar(t[1]))
              cuadruploList.normalCuad("ERA", t[1])
              #if (auxstackParam[1][0] is not None):
              auxstackParam[1].reverse()
              print("SE TIENEN LOS PARAMETROS EN LA FUNCION: ", auxstackParam)
              stackOperando.append(t[1]) 
              stackOperador.append("(")
              print("meter cuadruplo con de gosub a la funcion")
              print("meter a cuadruplo de operando resultado de la funcion?")
              stackOperando.append(t[1])
          else:
              print("buscador Clase:", buscadorClase)
              pilaClase.append(t[1])
              stackOperando.append(existe['memo'])
    else:
        #see t[1]
        print("a meter : ",t[1])
        stackOperando.append(existe['memo'])

def p_PuntoAux(t):
    '''
    PuntoAux : PUNTO
    '''
    global stackOperador
    stackOperador.append(t[1])
    print("inserto el punto .")


def p_ValorSalidaC(t):
    '''
      ValorSalidaC : INTER_IZQ  LlamadaFuncionA INTER_DER
      | AsignaA ValorSalidaB
    '''


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