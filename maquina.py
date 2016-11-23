from tablas import *
from memoria import *

class Maquina:

	def __init__(self):
		self.cuad = list()
		self.proc = list()
		self.simbolosMaquina = TablaSimbolos()
		self.constantesMaquina = TablaConstantes()
		self.memoriaTemporal = MemoriaReal(30001)

	def setCuad(self, list=[]):
		self.cuad = list

	def setProc(self, list=[]):
		self.proc = list

	def setSimbolos(self, val):
		self.simbolosMaquina = val

	def setConstantes(self, val):
		self.constantesMaquina = val

	def setMemTemp(self, val):
		self.memoriaTemporal = val

	def calculos(self):
		indiceCuad = 0
		indiceRET = 0
		listParam = []
		last = len(self.cuad) - 1
		listaMemorias = list()
		memoriaVirtual = VirtualMemory("global")
		simbol = self.simbolosMaquina


		while(self.cuad[indiceCuad][0] != 'FIN'):
			cuadru = self.cuad[indiceCuad]

			if cuadru[0] == "+":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (2499 < op1 < 5000):
						op1 = 0
					elif (op1 < 7500):
						op1 = 0.0
				elif(op1 < 20001):
					op1 -= 10000
					if (2499 < op1 < 5000):
						op1 = 1
					elif (op1 < 7500):
						op1 = 0.1
				elif(op1 < 30001):
					op1 -= 20000
					if (2499 < op1 < 5000):
						op1 = 2
					elif (op1 < 7500):
						op1 = 0.2
				else:
					op1 -= 30000
					if (2499 < op1 < 5000):
						op1 = 3
					elif (op1 < 7500):
						op1 = 0.3

				if(op2 < 10001):
					if (2499 < op2 < 5000):
						op2 = 0
					elif (op2 < 7500):
						op2 = 0.0
				elif(op2 < 20001):
					op2 -= 10000
					if (2499 < op2 < 5000):
						op2 = 1
					elif (op2 < 7500):
						op2 = 0.1
				elif(op2 < 30001):
					op2 -= 20000
					if (2499 < op2 < 5000):
						op2 = 2
					elif (op2 < 7500):
						op2 = 0.2
				else:
					op2 -= 30000
					if (2499 < op2 < 5000):
						op2 = 3
					elif (op2 < 7500):
						op2 = 0.3



				result = op1 + op2
				print("suma!", result)

			elif cuadru[0] == "-":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (2499 < op1 < 5000):
						op1 = 0
					elif (op1 < 7500):
						op1 = 0.0
				elif(op1 < 20001):
					op1 -= 10000
					if (2499 < op1 < 5000):
						op1 = 1
					elif (op1 < 7500):
						op1 = 0.1
				elif(op1 < 30001):
					op1 -= 20000
					if (2499 < op1 < 5000):
						op1 = 2
					elif (op1 < 7500):
						op1 = 0.2
				else:
					op1 -= 30000
					if (2499 < op1 < 5000):
						op1 = 3
					elif (op1 < 7500):
						op1 = 0.3

				if(op2 < 10001):
					if (2499 < op2 < 5000):
						op2 = 0
					elif (op2 < 7500):
						op2 = 0.0
				elif(op2 < 20001):
					op2 -= 10000
					if (2499 < op2 < 5000):
						op2 = 1
					elif (op2 < 7500):
						op2 = 0.1
				elif(op2 < 30001):
					op2 -= 20000
					if (2499 < op2 < 5000):
						op2 = 2
					elif (op2 < 7500):
						op2 = 0.2
				else:
					op2 -= 30000
					if (2499 < op2 < 5000):
						op2 = 3
					elif (op2 < 7500):
						op2 = 0.3

				result = op1 - op2
				print("resta!", result)

			elif cuadru[0] == "*":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (2499 < op1 < 5000):
						op1 = 0
					elif (op1 < 7500):
						op1 = 0.0
				elif(op1 < 20001):
					op1 -= 10000
					if (2499 < op1 < 5000):
						op1 = 1
					elif (op1 < 7500):
						op1 = 0.1
				elif(op1 < 30001):
					op1 -= 20000
					if (2499 < op1 < 5000):
						op1 = 2
					elif (op1 < 7500):
						op1 = 0.2
				else:
					op1 -= 30000
					if (2499 < op1 < 5000):
						op1 = 3
					elif (op1 < 7500):
						op1 = 0.3

				if(op2 < 10001):
					if (2499 < op2 < 5000):
						op2 = 0
					elif (op2 < 7500):
						op2 = 0.0
				elif(op2 < 20001):
					op2 -= 10000
					if (2499 < op2 < 5000):
						op2 = 1
					elif (op2 < 7500):
						op2 = 0.1
				elif(op2 < 30001):
					op2 -= 20000
					if (2499 < op2 < 5000):
						op2 = 2
					elif (op2 < 7500):
						op2 = 0.2
				else:
					op2 -= 30000
					if (2499 < op2 < 5000):
						op2 = 3
					elif (op2 < 7500):
						op2 = 0.3

				result = op1 * op2
				print("multiplica!", result)

			elif cuadru[0] == "/":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (2499 < op1 < 5000):
						op1 = 0
					elif (op1 < 7500):
						op1 = 0.0
				elif(op1 < 20001):
					op1 -= 10000
					if (2499 < op1 < 5000):
						op1 = 1
					elif (op1 < 7500):
						op1 = 0.1
				elif(op1 < 30001):
					op1 -= 20000
					if (2499 < op1 < 5000):
						op1 = 2
					elif (op1 < 7500):
						op1 = 0.2
				else:
					op1 -= 30000
					if (2499 < op1 < 5000):
						op1 = 3
					elif (op1 < 7500):
						op1 = 0.3

				if(op2 < 10001):
					if (2499 < op2 < 5000):
						op2 = 0
					elif (op2 < 7500):
						op2 = 0.0
				elif(op2 < 20001):
					op2 -= 10000
					if (2499 < op2 < 5000):
						op2 = 1
					elif (op2 < 7500):
						op2 = 0.1
				elif(op2 < 30001):
					op2 -= 20000
					if (2499 < op2 < 5000):
						op2 = 2
					elif (op2 < 7500):
						op2 = 0.2
				else:
					op2 -= 30000
					if (2499 < op2 < 5000):
						op2 = 3
					elif (op2 < 7500):
						op2 = 0.3

				result = op1 / op2
				print("divide!", result)

			elif cuadru[0] == ">":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (2499 < op1 < 5000):
						op1 = 0
					elif (op1 < 7500):
						op1 = 0.0
				elif(op1 < 20001):
					op1 -= 10000
					if (2499 < op1 < 5000):
						op1 = 1
					elif (op1 < 7500):
						op1 = 0.1
				elif(op1 < 30001):
					op1 -= 20000
					if (2499 < op1 < 5000):
						op1 = 2
					elif (op1 < 7500):
						op1 = 0.2
				else:
					op1 -= 30000
					if (2499 < op1 < 5000):
						op1 = 3
					elif (op1 < 7500):
						op1 = 0.3

				if(op2 < 10001):
					if (2499 < op2 < 5000):
						op2 = 0
					elif (op2 < 7500):
						op2 = 0.0
				elif(op2 < 20001):
					op2 -= 10000
					if (2499 < op2 < 5000):
						op2 = 1
					elif (op2 < 7500):
						op2 = 0.1
				elif(op2 < 30001):
					op2 -= 20000
					if (2499 < op2 < 5000):
						op2 = 2
					elif (op2 < 7500):
						op2 = 0.2
				else:
					op2 -= 30000
					if (2499 < op2 < 5000):
						op2 = 3
					elif (op2 < 7500):
						op2 = 0.3

				result = op1 > op2
				if (result == True):
					print("Verifica >!", "Verdadero")
				else:
					print("Verifica >!", "Falso")

			elif cuadru[0] == "<":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (2499 < op1 < 5000):
						op1 = 0
					elif (op1 < 7500):
						op1 = 0.0
				elif(op1 < 20001):
					op1 -= 10000
					if (2499 < op1 < 5000):
						op1 = 1
					elif (op1 < 7500):
						op1 = 0.1
				elif(op1 < 30001):
					op1 -= 20000
					if (2499 < op1 < 5000):
						op1 = 2
					elif (op1 < 7500):
						op1 = 0.2
				else:
					op1 -= 30000
					if (2499 < op1 < 5000):
						op1 = 3
					elif (op1 < 7500):
						op1 = 0.3

				if(op2 < 10001):
					if (2499 < op2 < 5000):
						op2 = 0
					elif (op2 < 7500):
						op2 = 0.0
				elif(op2 < 20001):
					op2 -= 10000
					if (2499 < op2 < 5000):
						op2 = 1
					elif (op2 < 7500):
						op2 = 0.1
				elif(op2 < 30001):
					op2 -= 20000
					if (2499 < op2 < 5000):
						op2 = 2
					elif (op2 < 7500):
						op2 = 0.2
				else:
					op2 -= 30000
					if (2499 < op2 < 5000):
						op2 = 3
					elif (op2 < 7500):
						op2 = 0.3

				result = op1 < op2
				if (result == True):
					print("Verifica <!", "Verdadero")
				else:
					print("Verifica <!", "Falso")

			elif cuadru[0] == "&&":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (op1 < 2500):
						op1 = True
				elif(op1 < 20001):
					if (op1 < 2500):
						op1 = False
				elif(op1 < 30001):
					if (op1 < 2500):
						op1 = True
				else:
					if (op1 < 2500):
						op1 = False

				if(op2 < 10001):
					if (op2 < 2500):
						op2 = True
				elif(op2 < 20001):
					if (op2 < 2500):
						op2 = False
				elif(op2 < 30001):
					if (op2 < 2500):
						op2 = True
				else:
					if (op2 < 2500):
						op2 = False

				result = op1 and op2
				if (result == True):
					print("Verifica &&!", "Verdadero")
				else:
					print("Verifica &&!", "Falso")

			elif cuadru[0] == "||":
				op1 = cuadru[1]
				op2 = cuadru[2]
				res = cuadru[3]

				if(op1 < 10001):
					if (op1 < 2500):
						op1 = True
				elif(op1 < 20001):
					if (op1 < 2500):
						op1 = False
				elif(op1 < 30001):
					if (op1 < 2500):
						op1 = True
				else:
					if (op1 < 2500):
						op1 = False

				if(op2 < 10001):
					if (op2 < 2500):
						op2 = True
				elif(op2 < 20001):
					if (op2 < 2500):
						op2 = False
				elif(op2 < 30001):
					if (op2 < 2500):
						op2 = True
				else:
					if (op2 < 2500):
						op2 = False

				result = op1 or op2
				if (result == True):
					print("Verifica ||!", "Verdadero")
				else:
					print("Verifica ||!", "Falso")
				

			elif cuadru[0] == "Goto":
				res = cuadru[3]

				indiceCuad = res - 1
				print("INDICE Goto", indiceCuad+1)

			elif cuadru[0] == "GotoF":
				op1 = cuadru[1]
				res = cuadru[3]
				op1 = False

				if op1 is False:
					indiceCuad = res - 1
					print("INDICE GotoF", indiceCuad+1)

			elif cuadru[0] == "Gosub":
				res = cuadru[1]
				proIndex = 0
				indiceRET = indiceCuad
				while(self.proc[proIndex][0] != res):
					proIndex = proIndex + 1
				proced = self.proc[proIndex]
				newIndex = proced[3]
				indiceCuad = newIndex - 1


			elif cuadru[0] == "RET":
				indiceCuad = indiceRET

			elif cuadru[0] == "ERA":
				res = cuadru[1]
				memID = 0
				tipo = simbol.buscarTipo(res, "retorno")

				idValue = int(self.simbolosMaquina.id/10000)
				print("idValue a insertar",idValue)
				if(tipo =='entero'):
					memID = self.memoriaTemporal.insertaEntero()
				elif(tipo =='booleano'):
					memID = self.memoriaTemporal.insertaBooleano()
				elif(tipo =='caracter'):
					memID = self.memoriaTemporal.insertaCaracter()
				elif(tipo =='real'):
					memID = self.memoriaTemporal.insertaReal()
				self.simbolosMaquina.insertar(res, tipo, memID)
				memoriaVirtual.functions[memID] = {'funcion':res}
				

			elif cuadru[0] == "ver":
				op1 = cuadru[1]
				op2 = cuadru[2]
				op3 = cuadru[3]

				if (op1 < op2) and (op1 > op3):
					print("Se sale del rango de memoria")
					indiceCuad = last

			elif cuadru[0] == "salida":
				op1 = cuadru[1]

				print(op1)

			indiceCuad += 1
		print(memoriaVirtual.functions)