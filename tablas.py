# cubo semantico es un diccionario de matrices que tiene de Id los tipos de operador que puede haber
# Ejemplo de como son cada una
# bool=0,int=1,float =2 ,string = 3,clase = 4,error = 5
# +, [
# bool [bool,int,float,string,clase],
# int [bool,int,float,string,clase],
# float [bool, int ,float,string, clase],
# string [bool, int ,float,string, clase],
# Clase [bool, int ,float,string, clase]
# ]

class claseCuboSemantico:
    def __init__(self):
        self.DataTypes = ['bool', 'int', 'real', 'caracter', 'clase', 'error']
        self.Cubo = {'+': [[0, 1, 2, 5, 5], [1, 1, 2, 5, 5], [2, 2, 2, 5, 5], [5, 5, 5, 3, 5], [5, 5, 5, 5, 5]],
                     '-': [[0, 1, 2, 5, 5], [1, 1, 2, 5, 5], [2, 2, 2, 5, 5], [5, 5, 5, 4, 5], [5, 5, 5, 5, 5]],
                     '/': [[0, 1, 2, 5, 5], [1, 1, 2, 5, 5], [2, 2, 2, 5, 5], [5, 5, 5, 3, 5], [5, 5, 5, 5, 5]],
                     '*': [[0, 1, 2, 5, 5], [1, 1, 2, 5, 5], [2, 2, 2, 5, 5], [5, 5, 5, 3, 5], [5, 5, 5, 5, 5]],
                     '=': [[0, 5, 5, 5, 5], [5, 1, 5, 5, 5], [5, 5, 2, 5, 5], [5, 5, 5, 4, 5], [5, 5, 5, 5, 5]],
                     '>': [[5, 5, 5, 5, 5], [5, 0, 0, 5, 5], [5, 0, 0, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
                     '<': [[5, 5, 5, 5, 5], [5, 0, 0, 5, 5], [5, 0, 0, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
                     '&&': [[0, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
                     '||': [[0, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
                     'entrada': [[0, 5, 5, 5, 5], [5, 1, 5, 5, 5], [5, 5, 2, 5, 5], [5, 5, 5, 3, 5], [5, 5, 5, 5, 5]]
                     }

    def Semantica(self, operador, operando1, operando2):
        aux = int(operando1/10000)
        aux2 = int(operando2/10000)
        VerdaderoValor1 = operando1 - aux*10000
        VerdaderoValor2 = operando2 - aux2*10000
        IndexOP1 = 5
        IndexOP2 = 5
        if(VerdaderoValor1 >= 0 and VerdaderoValor1 <= 2500):
            IndexOP1 = 0
        elif(VerdaderoValor1 >= 2501 and VerdaderoValor1 <= 5000):
            IndexOP1 = 1
        elif(VerdaderoValor1 >= 5001 and VerdaderoValor1 <= 7500):
            IndexOP1 = 2
        elif(VerdaderoValor1 >= 7501 and VerdaderoValor1 <= 10000): 
            IndexOP1 = 3  
        if(VerdaderoValor2 >= 0 and VerdaderoValor2 <= 2500):
            IndexOP2 = 0
        elif(VerdaderoValor2 >= 2501 and VerdaderoValor2 <= 5000):
            IndexOP2 = 1
        elif(VerdaderoValor2 >= 5001 and VerdaderoValor2 <= 7500):
            IndexOP2 = 2
        elif(VerdaderoValor2 >= 7501 and VerdaderoValor2 <= 10000): 
            IndexOP2 = 3



        if IndexOP1 < 5 and IndexOP2 < 5:
            sem = self.Cubo[operador][IndexOP1][IndexOP2]
            if sem == 5:
                print("\nERROR TYPE MISMATCH. Los operandos:", operando1, "y", operando2,
                      "no son compatibles con el operador:", operador)
                return 5

            else:
                return sem

        else:
            print("\nERROR. Tipos de datos:", operando1, ",", operando2, "y/o operador:", operador, "desconocidos.")
            return None

class TablaConstantes:
    def __init__(self):
        self.simbolos = dict()

    def insertar(self, id, tipo, memID):
        self.simbolos[id] = {'tipo':tipo,'memo':memID}

    def buscar(self, id):
        return self.simbolos.get(id)

    def imprimir(self):
        print ("Tabla de Constantes",self.simbolos)

class TablaSimbolos:
    def __init__(self,ident=0):
        self.id = ident
        self.simbolos = dict()
        self.hijos = list()
        self.padre = None
        # agregar atributo name?
          
    def insertar(self, id, tipo,memID,limInf = None,limSup = None):
        if(limInf is None):
            self.simbolos[id] = {'tipo':tipo, 'memo':memID}
        else:
             self.simbolos[id] = {'tipo':tipo,'memo':memID,'dimA':limInf,'dimB':limSup}

    def convertirArreglo(self,id,idMax,limInf,limSup = None):
        tipo = self.simbolos[id]['tipo']
        memo = self.simbolos[id]['memo']
        self.simbolos[id] = {'tipo':tipo,'memo':memo,'dimA':limInf,'dimB':limSup}

    def insertarFuncion(self,id,tipo,memID):
        self.simbolos[id] = {'tipo':'funcion', 'memo':memID,'retorno':tipo}

    def insertarClase(self,id,memID,herencia = None):
        if (herencia is None):
            self.simbolos[id] = {'tipo':'clase','memo': memID,'id':id,'herencia':None}
        else:
            self.simbolos[id] = {'tipo':'clase','memo': memID,'id':id,'herencia':herencia}
    
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

class Cuadruplos:
    def __init__(self):
        self.cuadruplos = list()

    def normalCuad(self, operador, operando1 = None, operando2 = None, destino=None):
        self.cuadruplos.append((operador, operando1, operando2, destino))
        print("operador:" ,operador , " op1:",operando1, " op2:", operando2 , " destino:",destino)

    def updateCuad(self, index, operador=None, operando1=None, operando2=None, destino=None):
        self.cuadruplos[index] = (operador, operando1, operando2, destino)

    def AssignCuad(self,operador, operando1, destino):
        self.cuadruplos.append((operador, operando1, None, destino))

    def SaltaCuad(self, Goto, destino=None):
      self.cuadruplos.append((Goto, None, None, destino))
      return len(self.cuadruplos) - 1

    def AgregarSalto(self, indice, expr, destino=None):
      if destino is None:
        destino = len(self.cuadruplos)
      salto = (self.cuadruplos[indice][0], expr, None, destino)
      self.cuadruplos[indice] = salto

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

    def getCuadruplos(self):
        return self.cuadruplos

class Procedimientos:
    def __init__(self):
        self.procedimientos = list()
        self.listParam = dict()

    def normalLista(self, id, parametros, variables, cuadruplo, scope):
        self.procedimientos.append((id, parametros, variables, cuadruplo, scope))
        print("ID Procedimiento:" ,id , " # Param:",parametros, " # Variables:", variables , "Destino:",cuadruplo, "Scope:",scope)

    def updateLista(self, index, id, parametros, variables, destino, scope):
        self.procedimientos[index] = (id, parametros, variables, destino, scope)

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
                  proc[3], 'Scope:', proc[4])
            indice = indice + 1

    def getProcedimientos(self):
        return self.procedimientos