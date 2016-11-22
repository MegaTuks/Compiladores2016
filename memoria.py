class VirtualMemory:
    def __init__(self,name):
        self.memory_name = name
        #variables locales de una funcion
        self.functions = dict()
        self.variables = dict()
        self.clases = dict()

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
    def __init__(self, rango = 0,clase = None): 
        self.booleanos = rango
        self.enteros = rango + 2500
        self.reales = rango + 5000
        self.caracteres =  rango + 7500

        self.cont_bool = self.booleanos
        self.cont_ent = self.enteros
        self.cont_real = self.reales
        self.cont_car = self.caracteres

    def insertaBooleano(self):
        if(self.cont_bool < self.enteros):
            self.cont_bool = self.cont_bool + 1
            return self.cont_bool
        else:
            print("memoria fuera de limites")

    def insertaEntero(self):
        if(self.cont_ent < self.reales):
            self.cont_ent = self.cont_ent + 1
            return self.cont_ent
        else:
            print("memoria fuera de limites")
    
    def insertaReal(self):
        if(self.cont_real < self.caracteres):
            self.cont_real = self.cont_real + 1
            return self.cont_real
        else:
            print("memoria fuera de limites")

    def insertaCaracter(self):
        if(self.cont_car < self.caracteres + 2500):
            self.cont_car = self.cont_car + 1
            return self.cont_car
        else:
            print("memoria fuera de limites")

    def eliminaTemporales(self,topeBool, topeInt,topeReal, topeCar):
        print("funcion de borrado")





    


