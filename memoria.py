class VirtualMemory:
    def __init__(self,name):
        self.memory_name = name
        self.booleanos = 101
        self.enteros = 102
        self.reales = 103
        self.caracteres = 104
        self.listaMemo = {self.booleanos:[], self.enteros:[],self.reales:[],self.caracteres:[]}
    
    def insertaBooleano(self,booleano,capacidad):
        if(booleano < capacidad):
            self.listaMemo[101].append(booleano)
        else:
            print("Limite de memoria excedido")

    def insertaEntero(self,entero,capacidad):
        if(entero < capacidad):
            self.listaMemo[102].append(entero)
        else:
            print("Limite de memoria excedido")

    def insertaReales(self,real,capacidad):
        if(real < capacidad):
            self.listaMemo[103].append(real)
        else:
            print("Limite de memoria excedido")

    def insertaCaracteres(self,caracter,capacidad):
        if(caracter < capacidad):
            self.listaMemo[104].append(caracter)
        else:
            print("limite meoria escedido")

    def imprimeMemoriaV(self):
        print("Memoria de :" ,self.memory_name)
        print("booleanos en memoria:", self.listaMemo[101])
        print("enteros en memoria:", self.listaMemo[102])
        print("real en memoria:",self.listaMemo[103])
        print("caracteres en memoria:",self.listaMemo[104])

class MemoriaReal:
    def __init__(self):
        self.inicio = 1000
        self.booleanos = 6000
        self.enteros = 10000
        self.reales = 15000
        self.caracteres = 20000
        self.memoriaAct = dict()

    def insertaBooleano(self,memID,valor):
        if(memID > self.inicio and memID < self.booleanos):
            self.memoriaAct[memID] = valor
        else:
            print("memoria fuera de limites")

    def insertaEnteros(self,memID,valor):
        if(memID > self.booleanos and memID < self.enteros):
            self.memoriaAct[memID] = valor
        else:
            print("memoria fuera de limites")
    
    def insertaReales(self,memID,valor):
        if(memID > self.enteros and memID < self.reales):
            self.memoriaAct[memID] = valor
        else:
            print("memoria fuera de limites")

    def insertaCaracteres(self,memID,valor):
        if(memID > self.reales and memID < self.caracteres):
            self.memoriaAct[memID] = valor
        else:
            print("memoria fuera de limites")




    


