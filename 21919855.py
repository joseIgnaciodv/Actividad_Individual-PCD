import random                               # Libreria para generar numeros psuedoaleatorios
import multiprocessing as mp                # Libreria que corresponde con la funcionalidad multiproceso de python
import sys
import time 


#Nombre Autor: Jose Ignacio Del Valle Bustillo
#Expediente: 21919855
#Fecha: 30-06-2020 

# Funcion fib(), Recibe un numero por parametro, fib() se encarga de dividir dicho numero, en el numero de cpu´s
# que disponga la maquina, se lanza un proceso por cada numero segmentado, que invoca la funcion de fib_proceso()

def fib(numero):
    procesos = []                           # Lista de porcesos, donde se van a guardar los procesos con sus trabajos
    num_cpu = mp.cpu_count()                # Numero de cores de la maquina
    size = int(numero/num_cpu)              # Tamaño segmentado del numero
    for i in range(0, numero, size):        # Lanzar num_cpu procesos, desde 0 hasta el numero
        proceso = mp.Process(target = fib_proceso, args = (i,))
        procesos.append(proceso)            # Añadir a la lista de procesos, los procesos y sus trabajos
    for p in procesos:
        p.start()                           # Empezar ejecución procesos
    for p in procesos:
        p.join()                            # Bloquear y esperar la finalización de los procesos de forma asincrona

# Funcion fib_proceso(), calcula el termino n-esimo de la serie de fibonacci, de abajo a arriba, partiendo de los dos
# primeros terminos de la serie de fibonacci, la salida que produce es el termino n-esimo, que corresponde con la ultima
# posición de la lista

def fib_proceso(numero):
    if numero == 0:
        return 0
    lista = [0]*(numero + 1)                # Inicializar lista de tamaño numero + 1, con todo 0´s
    lista[0] = 0                            # Primera posición lista, contiene primer termino serie fibonacci(0)
    lista[1] = 1                            # Segunda posición lista, contiene segundo termino serie fibonacci(1)
 
    for i in range(2, numero + 1):          # Recorrer lista desde el tercer termino de la serie de fibonacci, el siguiente termino es la suma entre el termino anterior y el anterior a ese
        lista[i] = lista[i - 1] + lista[i - 2]
    return lista[numero]                    # Devolver la ultima posicion de la lista, que corresponde con el termino n-esimo de fibonacci  


# Funcion mergesort(), funcion que recibe como parametro, una lista de numeros aleatorios, genera un numero de sublistas,
# correspondiente al numero de cores que disponga la maquina, se lanzan (cpu_count) procesos,
# cada proceso se encarga de ordenar la sublista asignada, usando mergesort como metodo de ordenación

def merge_sort(lista):
    procesos = []                           # La lista que contiene todos los procesos, con sus trabajos correspondientes
    listas = []                             # Definición de sublistas
    num_cpu = mp.cpu_count()                # Numero de CPU´s que dispone la maquina
    size = len(lista)//num_cpu              # El tamaño de cada sublista
    for i in range(0, len(lista), size):    # Recorrer lista desde el principio hasta el final, dando saltos de tamaño (size) en cada iteración
        listas = lista[i: i + size]         # Cada sublista tiene tamaño (size) y cada punto de inicio es la siguiente posicion a la posción inical mas el tamaño(size) 
        proceso = mp.Process(target = merge_sort_paralelo, args = (listas, ))
        procesos.append(proceso)            # Añadir los procesos y sus trabajos, a la lista de procesos
    for p in procesos:
        p.start()                           # Para cada proceso que se ha guardado en la lista de procesos, emepezar la ejecución
    for p in procesos:
        p.join()                            # Esperar hasta que cada proceso haya finalizado su trabajo, para empezar otro proceso

# Función merge_sort_paralelo(), metodo de ordenación donde se recibe una lista por parametro, parte la lista en dos partes,
# y ordena cada una de las partes de forma recursiva, de tal manera que hal final devulve un lista ordenanda         

def merge_sort_paralelo(lista):
    if len(lista) <= 1:
        return lista
    mid = len(lista)//2                     # La posición media de la lista, donde se definen las 2 mitades de la lista
    listaIzq = lista[:mid]                  # Sublista izquierda, una sublista de la lista inicial, que empieza en la posicion 0, acaba en la posicion del medio
    listaDer = lista[mid:]                  # Sublista derecha, una sublista de la lista inicial, que empieza en la posicion medio, acaba en la posicion final de la lista 
    return merge(merge_sort_paralelo(listaIzq), merge_sort_paralelo(listaDer))



def merge(left, right):
    resultados = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] <= right[ri]:
            resultados.append(left[li])
            li += 1
        else:
            resultados.append(right[ri])
            ri += 1
    if li == len(left):
        resultados.extend(right[ri:])
    else:
        resultados.extend(left[li:])
    return resultados

# Funcion menu(), muestra la estetica del menu principal del programa, muestra datos del estudiante, y las opciones
# de los 2 algoritmos

def menu():                                 
    miNombre = "Jose Ignacio"               # El nombre del estudiante
    misApellidos = "Del Valle Bustillo"     # Los apellidos del estudiante
    miExpediente = "21919855"               # El numero de expediente del estudiante
    
    print("\n****************** UNIVERSIDAD EUROPEA DE MADRID ******************")
    print("\tEscuela de Ingenieria Arquitectura y Diseño\n")
    print("\n****************** MENU ******************\n")
    
    print("\nESTUDIANTE:")
    print(" * Apellidos:\t", misApellidos)  # Mostrar datos del estudiante de forma clara y limpia, por pantalla
    print(" * Nombre:\t", miNombre)
    print(" * Expediente:\t", miExpediente)

    print("\n\tA). Ejercicio A (MERGE SORT)")
    print("\tB). Ejercicio B (FIBONACCI)")  # Los distintos ejercicios mostrados por pantalla
    print("\tC). Salir(Pulse la letra S para salir)\n") 


# Funcion lista_aleatorios(), genera una lista de numeros aleatorios, en funcion del numero pasado por parametro.
# Es decir, genera una lista de tamaño (num), de numeros entre 0 y 30000 aleatorios

def crear_lista(num):
    lista_aleatorios = []                   # La lista creada de numeros aleatorios

    for i in range(0,num):
        randNum = random.randint(0,30000)   # Genera un numero aleatorio entre 0 y 30000 en cada iteracion, se van a generar numeros aleatorios
        lista_aleatorios.append(randNum)    # desde 0 hasta el numero introducido como parametro (num)
    return lista_aleatorios                 # Devuelve la lista generada de numeros aleatorios

if __name__ == "__main__":
    numExp = 15000                          # El numero de expediente
    lista = crear_lista(numExp)             # Lista de numeros aleatorios
    opcionValida = False                    # Control de opciones
    salir = False                           # Contol acabar programa
    nombre = ""                             # Nombre que se mostrara por pantalla al iniciar sesion
    opcion = ''                             # La letra que se va a introducir, para seleccionar una opcion del menu
    
    print("================== USUARIO ==================\n")
    print("Nombre usario: ", "direccion correo electronico")
    print("Contraseña: ", "Numero Expediente: 21919855\n")
    
    print("================== LOGIN ==================\n")
    email = input("Introduzca su direccion de correo: ")
    password = input("Introduzca su contrasena: ")
    print("\n===========================================")

    if(email == "christianvladimi.sucuzhanay@universidadeuropea.es"):
        nombre = "Christian"
    elif (email == "joseignaciodelvallebustillo@gmail.com"):
        nombre = "Jose Ignacio"

    if(password == "21919855" and (email == "joseignaciodelvallebustillo@gmail.com" or email == "christianvladimi.sucuzhanay@universidadeuropea.es")):
        print("\nBienvenido: ", nombre)
        menu()                              # Se mostrara el menu principal, siempre y cuando el correo del usuario(Jose Ignacio, Christian) y la contraseña sean correctas
    else:
        salir = True                        # En caso contrario, el flag salir de control sera TRUE

    if(salir == True):                      # Si el flag de control de acabar programa es TRUE, el programa acabara
        sys.exit("\nDireccion de correo electronico o contrasena no son correctas, no autorizado")

    while(opcionValida == False or opcion != 'S'):
        opcion = input("Eliga una opcion: ").upper()
        if(opcion == 'A'):                  # Convertir la letra introducida por pantalla en letra mayuscula
            print("\n================== Algoritmo Merge-Sort ==================\n")
            t_inicio = time.time()
            merge_sort(lista)               # Seleccionar la letra 'A', ejecutara el metodo 'Merge-Sort', y mostrara el menu principal una vez finalizado la ejecucion de mergesort
            t_fin = time.time()
            print("Tiempo transcurrido algortimo Merge Sort en paralelo, ", t_fin - t_inicio)
            opcionValida = True
            menu()
        elif(opcion == 'B'):
            print("\n================== Algoritmo Fibonacci ==================\n")
            t_inicio = time.time()
            fib(numExp)                     # Seleccionar la letra 'B', ejecutara el metodo 'Fib', y mostrara el menu principal una vez finalizado la ejecucion de fibonacci
            t_fin = time.time()
            print("Tiempo transcurrido algortimo Fibonacci en paralelo, ", t_fin - t_inicio)
            opcionValida = True
            menu()
        elif(opcion == 'S'):                # Seleccionar la letra 'S', el programa saldra y parara la ejecucion
            sys.exit("Gracias, hasta luego")
        else:
            print("Letra no valida")        # Simpre que la letra introducida no sea valida
            opcionValida = False            # Cuando la letra no sea la letra 'A' o la letra 'B', el programa pedira que se introduzca otra vez