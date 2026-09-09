# ========================================= 
# SISTEMA DE REGISTRO DE ASISTENCIA 
# INTEGRANTE 2 
# GESTION DE SESIONES Y MATRIZ 
# =========================================


def validar_numero_sesion(numero, sesiones):
    '''Devuelve False si existe, si no existe devuelve True'''

    for i in sesiones:
        if i[0] == numero:
            print("Ese numero ya existe.")
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
 
            # Verificar que dia, mes y anio tengan solo numeros
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
 
                if año > 0:
                    if mes > 0 and mes <= 12:
                        if mes == 2:
                            if año % 400 == 0:
                                dias = 29
                            elif año % 100 == 0:
                                dias = 28
                            elif año % 4 == 0:
                                dias = 29
                            else:
                                dias = 28
                        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                            dias = 30
                        else:
                            dias = 31
 
                        if dia > 0 and dia <= dias:
                            validacion = True
                        else:
                            validacion = False
                    else:
                        validacion = False
                else:
                    validacion = False
 
    return validacion


def validar_texto_no_vacio(texto):
    """Valida que un campo de texto (materia, tema) no este vacio."""
    if len(texto.strip()) < 1:
        return False 

    else:
        return True


def crear_sesion(sesiones,asistencias, estudiantes):
    print("\n--- Crear nueva sesion ---")

    numero = int(input("Ingrese el numero de sesión: "))
    while not validar_numero_sesion(numero, sesiones):
        print("Ese legajo ya existe")
        numero = int(input("Ingrese un numero de sesión distinto: "))

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
        tema = input("Ingrese el tema nuevamente")

    # Se arma la nueva sesión y se agrega a la lista de seisiones 
    nueva_sesion = [numero, fecha, materia, tema]
    sesiones.append(nueva_sesion)

    # Cada sesion nueva agrega una columna a la matriz de asistencias
    agregar_columna_asistencia(asistencias)
 
    # Chequeo de que la matriz sigue teniendo las dimensiones correctas
    verificar_dimensiones_matriz(asistencias, estudiantes, sesiones)


def listar_sesiones(sesiones):
    # Muestra todas las sesiones registradas.
    print("\n--- Listado de sesiones ---")

    if len(sesiones) == 0:
        print("No hay sesiones cargadas todavia.")
        return

    for i in range(len(sesiones)):
        print("ID: ",sesiones[i][0], "Fecha: ", sesiones[i][1], "Materia: ", sesiones[i][2], "Tema: ", sesiones[i][3])


def buscar_sesion(sesiones, numero):
    # Busca una sesion por numero, recorriendo la matriz.
    encontrado = False

    for i in range(len(sesiones)):
        if sesiones[i][0] == numero:
            encontrado = True
            print("Sesión encontrada:")
            print("ID", sesiones[i][0])
            print("Fecha", sesiones[i][1])
            print("Materia", sesiones[i][2])
            print("Tema", sesiones[i][3])

    if encontrado == False:
        print("No se encontro ninguna sesión con ese numero")


def agregar_columna_asistencia(asistencias):
    # Agrega una columna nueva (la nueva sesion) a cada fila existente.
    for i in range(len(asistencias)):
        asistencias[i].append("-")


def agregar_fila_asistencia(asistencias, cantidad_sesiones):
    # Agrega una fila nueva (nuevo estudiante), con una columna por sesion existente
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
    opcion = 0
    while opcion != -1:
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
            crear_sesion(sesiones,asistencias, estudiantes)

        elif opcion == 2:
            listar_sesiones(sesiones)

        elif opcion == 3:
            buscar_sesion(sesiones, numero)

        elif opcion == 0:
            print("Voliviendo al menu principal ")

        else: 
            print("Opcion invalid. Intentelo de nuevo ")

