# =========================================
# SISTEMA DE REGISTRO DE ASISTENCIA
# CONSULTAS Y ESTADISTICAS
# =========================================


def contar_estado(lista, tipo):
    # Cuenta cuantas veces aparece un estado determinado dentro de una fila de asistencias.
    contador = 0
    for i in lista:
        if tipo == i:
            contador += 1

    return contador


def consultar_estudiante(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    # No se puede realizar la consulta si todavia no hay alumnos cargados.
    if len(matriz_estudiantes) == 0:
        print("No hay alumnos cargados")
        return
    
    # Se solicita el legajo y se valida que sea mayor a cero.
    legajo = int(input("Ingrese el legajo que quieres buscar: "))
    while legajo <= 0:
        print("El legajo no puede ser negativo o cero")
        legajo = int(input("Ingrese el legajo que quieres buscar: "))

    # Se busca la posicion del estudiante para usar la misma fila en la matriz de asistencias.
    posicion = -1
    for i in range(len(matriz_estudiantes)):
        if legajo == matriz_estudiantes[i][0]:
            posicion = i
            break

    if posicion == -1:
        print("El legajo no está cargado")
        return

    # Se muestran los datos generales del estudiante encontrado.
    print(f"===== DATOS DEL ESTUDIANTE =====")
    print(f"Legajo: {matriz_estudiantes[posicion][0]}\nNombre: {matriz_estudiantes[posicion][1]}\nEstado: {matriz_estudiantes[posicion][2]}")

    # Se recorre cada sesion y se informa la asistencia correspondiente al estudiante.
    for i in range(len(matriz_sesiones)):
        print(f"Sesion: {matriz_sesiones[i][0]}\nMateria: {matriz_sesiones[i][2]}")
        asistencia = "Nula"

        # Se reemplaza la letra almacenada por el nombre completo del estado.
        if matriz_asistencias[posicion][i] == "A":
            asistencia = "Ausente"
        elif  matriz_asistencias[posicion][i] == "P":
            asistencia = "Presente"
        elif  matriz_asistencias[posicion][i] == "J":
            asistencia = "Justificado"
        elif  matriz_asistencias[posicion][i] == "T":
            asistencia = "Tarde"

        print(f"Asistencia: {asistencia}")


def consultar_sesion(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    # No se puede consultar una sesion si todavia no hay ninguna cargada.
    if len(matriz_sesiones) == 0:
        print("No hay sesiones cargadas")
        return

    # Se solicita un numero de sesion valido, mayor a cero.
    sesion = int(input("Ingrese el numero de sesion: "))
    while sesion <= 0:
        print("El numero de sesion no puede ser negativo o cero")
        sesion = int(input("Ingrese el numero de sesion: "))

    # Se busca la posicion de la sesion para consultar esa misma columna en asistencias.
    posicion_sesion = -1
    for i in range(len(matriz_sesiones)):
        if sesion == matriz_sesiones[i][0]:
            posicion_sesion = i
            break

    if posicion_sesion == -1:
        print(f"La sesion {sesion}, no existe")
        return

    # Se muestran todos los estudiantes junto con el estado guardado en la sesion seleccionada.
    print(f"==== SESION: {sesion} ====")
    for i in range(len(matriz_estudiantes)):
        print(f"Nombre: {matriz_estudiantes[i][1]}\nAsistencia: {matriz_asistencias[i][posicion_sesion]}")


def calcular_porcentaje(matriz_asistencias, i):

    # Si la fila no tiene columnas significa que no hay clases cargadas para calcular el porcentaje.
    if len(matriz_asistencias[i]) == 0:
        print("No hay clases csrgadas")
        return

    # Se cuentan los presentes y se divide por la cantidad total de clases.
    presentes = contar_estado(matriz_asistencias[i], "P")
    total_clases = len(matriz_asistencias[i])

    pct = (presentes / total_clases) * 100

    print(f"El porcentaje es: {pct}%")
    return pct


def mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_asistencias):

    # La variable permite saber si se encontro al menos un alumno debajo del limite.
    alumnos_en_riesgo = False

    if len(matriz_estudiantes) == 0:
        print(f"No hay alumnos cargados")
        return

    # El usuario elige el porcentaje minimo utilizado como limite.
    pct_de_asistencia = float(input("Ingrese el limite de porcentaje de asistencia (75.0): "))
    while pct_de_asistencia <= 0:
        print("El porcentaje no puede ser negativo o cero")
        pct_de_asistencia = float(input("Ingrese el limite de porcentaje de asistencia (75.0): "))

    # Se calcula el porcentaje de cada estudiante y se muestran los que quedan debajo del limite.
    for i in range(len(matriz_estudiantes)):
        porcentaje = calcular_porcentaje(matriz_asistencias, i)
        if porcentaje <= pct_de_asistencia:
            alumnos_en_riesgo = True
            print(f"==== ALUMNO DEBAJO DEL LIMITE ====")
            print(f"Nombre: {matriz_estudiantes[i][1]}\nLegajo: {matriz_estudiantes[i][0]}\nPorcentaje: {porcentaje}%")

    if not alumnos_en_riesgo:
        print(f"No hay alumnos con menos del {pct_de_asistencia}%")


def menu_consultas(matriz_estudiantes, matriz_sesiones, matriz_asistencias):
    # Menu principal del modulo de consultas y estadisticas.
    opcion = -1
    while opcion != 0:
        print("\n==== MENU DE CONSULTAS ====")
        print("1. Consultar por estudiante")
        print("2. Consultar por sesion")
        print("3. Mostrar estudiante en riesgo")
        print("0. Volver al menu principal")
        
        opcion = int(input("Ingrese una opcion: "))

        # Se valida que la opcion se encuentre dentro del rango del menu.
        while opcion < 0 or opcion > 3:
            print("La opcion es invalida")
            opcion = int(input("Ingrese una opcion: "))

        if opcion == 1:
            consultar_estudiante(matriz_estudiantes, matriz_sesiones, matriz_asistencias)
        elif opcion == 2:
            consultar_sesion(matriz_estudiantes, matriz_sesiones, matriz_asistencias)
        elif opcion == 3:
            mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_asistencias)
        elif opcion == 0:
            print("Volviendo al menu")
