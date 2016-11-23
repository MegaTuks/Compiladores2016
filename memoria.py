class VirtualMemory:
    def __init__(self,name):
        self.memory_name = name
        #variables locales de una funcion
        self.functions = dict()
        self.variables = dict()
        self.variablesDim = dict()
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
            print("limite memoria excedido")

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
        self.clase = clase
        self.claseLista = dict()

        self.cont_bool = self.booleanos
        self.cont_ent = self.enteros
        self.cont_real = self.reales
        self.cont_car = self.caracteres

    def insertaBooleano(self,tope = None):
        if(tope is None):
            if(self.clase is None):
                if(self.cont_bool < self.enteros):
                    self.cont_bool = self.cont_bool + 1
                    return self.cont_bool
                else:
                    print("memoria fuera de limites")
            else :
                 self.cont_bool = self.cont_bool + 1
                 return self.cont_bool
        else:
            min = self.cont_bool + 1
            top = self.cont_bool + tope
            if(top < self.enteros):
                self.cont_bool = self.cont_bool + top
                return self.cont_bool
            else: 
                print("memoria fuera de limites")



    def insertaEntero(self,tope = None):
        if(tope is None):
            if(self.clase is None):
                if(self.cont_ent < self.reales):
                    self.cont_ent = self.cont_ent + 1
                    return self.cont_ent
                else:
                    print("memoria fuera de limites")
            else:
                print("memoria solo para clases")
        else:
            min = self.cont_ent + 1
            top = self.cont_ent + tope
            if(top < self.reales):
                self.cont_ent = self.cont_ent + top
                return self.cont_ent
            else: 
                print("memoria fuera de limites")
    
    def insertaReal(self, tope = None):
        if(tope is None):
            if(self.clase is None):
                if(self.cont_real < self.caracteres):
                    self.cont_real = self.cont_real + 1
                    return self.cont_real
                else:
                    print("memoria fuera de limites")
            else:
                print("memoria Exclusiva de clases")
        else:
            min = self.cont_real + 1
            top = self.cont_real + tope
            if(top < self.caracteres):
                self.cont_real = self.cont_real + top
                return self.cont_real
                print("pasas por aqui no?")
            else: 
                print("memoria fuera de limites")        

    def insertaCaracter(self,tope = None):
        if(tope is None):
            if(self.clase is None):
                if(self.cont_car < self.caracteres + 2500):
                    self.cont_car = self.cont_car + 1
                    return self.cont_car
                else:
                    print("memoria fuera de limites")
            else:
                print("memoria Exclusiva de clases")
        else:
            min = self.cont_car + 1
            top = self.cont_car + tope
            if(top < self.caracteres+2500):
                self.cont_car = self.cont_car + top
                return self.cont_car
            else: 
                print("memoria fuera de limites")

    def insertaClase(self, claseID,tope = None):
        claseAux = int(claseID / 10000)
        claseAux = claseAux * 10000
        claseAux = claseAux + 500000
        if (tope is None):
            if (not(claseAux in self.claseLista)):
                self.claseLista[claseAux] = claseAux
                self.claseLista[claseAux] = claseAux + 1
                return self.claseLista[claseAux]
            else:
                if(self.claseLista[claseAux] < (self.booleanos + claseAux + 10000)):
                    self.claseLista[claseAux] = self.claseLista[claseAux] + 1
                    
                    return self.claseLista[claseAux]

                else:
                    print("espacio excedido")
        else:
            if (not(claseAux in self.claseLista)):
                self.claseLista[claseAux] = claseAux
                self.claseLista[claseAux] = claseAux + tope
                return self.claseLista[claseAux]
            else:
                if(self.claseLista[claseAux] < (self.booleanos + claseAux + 10000)):
                    self.claseLista[claseAux] = self.claseLista[claseAux] + tope 
                    return self.claseLista[claseAux]
                else:
                    print("espacio excedido")


    def eliminaTemporales(self,topeBool, topeInt,topeReal, topeCar):
        print("funcion de borrado")
        





    


