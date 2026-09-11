# =========================================
# SISTEMA DE REGISTRO DE ASISTENCIA
# INTEGRANTE 2
# GESTION DE SESIONES Y MATRIZ
# =========================================


def validar_numero(numero):
    if len(numero) == 0:
        return False

    i = 0

    while i < len(numero):
        if numero[i] < "0" or numero[i] > "9":
            return False

        i += 1

    return True


def validar_numero_sesion(numero_sesion, sesiones):
    '''Devuelve False si existe, si no existe devuelve True'''

    for i in sesiones:
        if i[0] == numero_sesion:
            return False

    return True


def validar_fecha(fecha):
    """
    Valida manualmente el formato DD/MM/AAAA (sin librerias),
    incluyendo que el dia exista de verdad para ese mes y año
    (contempla meses de 30/31 dias y años bisiestos).
    """

    validacion = True

    # Verificar longitud
    if len(fecha) != 10:
        validacion = False

    else:
        # Verificar separadores
        if fecha[2] != "/" or fecha[5] != "/":
            validacion = False

        else:
            dia = fecha[0:2]
            mes = fecha[3:5]
            año = fecha[6:10]

            # Verificar que dia, mes y año tengan solo numeros
            i = 0
            while i < len(dia):
                if dia[i] < "0" or dia[i] > "9":
                    validacion = False

                i += 1

            i = 0
            while i < len(mes):
                if mes[i] < "0" or mes[i] > "9":
                    validacion = False

                i += 1

            i = 0
            while i < len(año):
                if año[i] < "0" or año[i] > "9":
                    validacion = False

                i += 1

            if validacion:
                dia = int(dia)
                mes = int(mes)
                año = int(año)

                validacion = False

                if año > 0 and 1 <= mes <= 12:

                    if mes == 2:

                        if año % 400 == 0 or (año % 4 == 0 and año % 100 != 0):
                            dias = 29

                        else:
                            dias = 28

                    elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                        dias = 30

                    else:
                        dias = 31

                    if 1 <= dia <= dias:
                        validacion = True

    return validacion



def validar_texto_no_vacio(texto):
    # Valida que un campo de texto (materia, tema) no este vacio.

    if len(texto.strip()) < 1:
        return False

    else:
        return True


def crear_sesion(sesiones, asistencias):

    print("\n--- Crear nueva sesion ---")

    numero_sesion = input("Ingrese el numero de sesion: ")

    while not validar_numero(numero_sesion):
        print("El numero de sesion debe contener solo numeros.")
        numero_sesion = input("Ingrese el numero de sesion: ")

    while not validar_numero_sesion(numero_sesion, sesiones):
        print("Ese numero de sesion ya existe.")
        numero_sesion = input("Ingrese un numero de sesion distinto: ")

        while not validar_numero(numero_sesion):
            print("El numero de sesion debe contener solo numeros.")
            numero_sesion = input("Ingrese el numero de sesion: ")

    fecha = input("Ingrese la fecha (DD/MM/AAAA): ")

    while not validar_fecha(fecha):
        print("Fecha invalida. Formato esperado: DD/MM/AAAA.")
        fecha = input("Ingrese la fecha nuevamente: ")

    materia = input("Ingrese la materia: ")

    while not validar_texto_no_vacio(materia):
        print("La materia no puede estar vacia.")
        materia = input("Ingrese la materia nuevamente: ")

    tema = input("Ingrese el tema: ")

    while not validar_texto_no_vacio(tema):
        print("El tema no puede estar vacio.")
        tema = input("Ingrese el tema nuevamente: ")

    # Se arma la nueva sesion y se agrega a la lista de sesiones
    nueva_sesion = [numero_sesion, fecha, materia, tema]

    sesiones.append(nueva_sesion)

    # Cada sesion nueva agrega una columna a la matriz de asistencias
    agregar_columna_asistencia(asistencias)

    # Chequeo de que la matriz sigue teniendo las dimensiones correctas
    verificar_dimensiones_matriz(asistencias, sesiones)

    return asistencias, sesiones


def listar_sesiones(sesiones):

    # Muestra todas las sesiones registradas.
    print("\n--- Listado de sesiones ---")

    if len(sesiones) == 0:
        print("No hay sesiones cargadas todavia.")
        return

    for i in range(len(sesiones)):
        print("Numero de sesion:", sesiones[i][0],
              "Fecha:", sesiones[i][1],
              "Materia:", sesiones[i][2],
              "Tema:", sesiones[i][3])


def buscar_sesion(sesiones, numero_sesion):

    # Busca una sesion por numero de sesion, recorriendo la matriz.
    encontrado = False

    for i in range(len(sesiones)):

        if sesiones[i][0] == numero_sesion:
            encontrado = True

            print("Sesion encontrada:")
            print("Numero de sesion:", sesiones[i][0])
            print("Fecha:", sesiones[i][1])
            print("Materia:", sesiones[i][2])
            print("Tema:", sesiones[i][3])

    if encontrado == False:
        print("No se encontro ninguna sesion con ese numero")


def agregar_columna_asistencia(asistencias):

    # Agrega una columna nueva (la nueva sesion) a cada fila existente.
    for i in range(len(asistencias)):
        asistencias[i].append("-")


def agregar_fila_asistencia(asistencias, cantidad_sesiones):

    # Agrega una fila nueva (nuevo estudiante),
    # con una columna por cada sesion existente.

    fila_nueva = []

    for i in range(cantidad_sesiones):
        fila_nueva.append("-")

    asistencias.append(fila_nueva)


def verificar_dimensiones_matriz(asistencias, sesiones):

    ok = True

    for i in range(len(asistencias)):

        if len(asistencias[i]) != len(sesiones):
            print("Aviso: una fila de asistencias no tiene la cantidad correcta de columnas.")
            ok = False

    return ok


def menu_sesiones(sesiones, asistencias):

    opcion = -1

    while opcion != 0:

        print("\n=========================================")
        print("        GESTION DE SESIONES")
        print("=========================================")
        print("1. Crear sesion")
        print("2. Listar sesiones")
        print("3. Buscar sesion")
        print("0. Volver al menu principal")
        print("=========================================")

        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            asistencias,sesiones=crear_sesion(sesiones, asistencias)

        elif opcion == 2:
            listar_sesiones(sesiones)

        elif opcion == 3:
            numero_sesion = input("Ingrese el numero de sesion: ")

            while not validar_numero(numero_sesion):
                print("El numero de sesion debe contener solo numeros.")
                numero_sesion = input("Ingrese el numero de sesion: ")

            buscar_sesion(sesiones, numero_sesion)

        elif opcion == 0:
            print("Volviendo al menu principal")

        else:
            print("Opcion invalida. Intentelo de nuevo")

    return sesiones
