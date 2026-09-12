def contar_estado(lista, tipo):
    contador = 0
    for i in lista:
        if tipo == i:
            contador += 1

    return contador

def consultar_estudiante(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    if len(matriz_estudiantes) == 0:
        print("No hay alumnos cargados")
        return
    
    legajo = int(input("Ingrese el legajo que quieres buscar: "))
    while legajo <= 0:
        print("El legajo no puede ser negativo o cero")
        legajo = int(input("Ingrese el legajo que quieres buscar: "))

    posicion = -1
    for i in range(len(matriz_estudiantes)):
        if legajo == matriz_estudiantes[i][0]:
            posicion = i
            break

    if posicion == -1:
        print("El legajo no está cargado")
        return

    print(f"===== DATOS DEL ESTUDIANTE =====")
    print(f"Legajo: {matriz_estudiantes[posicion][0]}\nNombre: {matriz_estudiantes[posicion][1]}\nEstado: {matriz_estudiantes[posicion][2]}")

    for i in range(len(matriz_sesiones)):
        print(f"Sesion: {matriz_sesiones[i][0]}\nMateria: {matriz_sesiones[i][2]}")
        asistencia = "Nula"
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

    if len(matriz_sesiones) == 0:
        print("No hay sesiones cargadas")
        return

    sesion = int(input("Ingrese el numero de sesion: "))
    while sesion <= 0:
        print("El numero de sesion no puede ser negativo o cero")
        sesion = int(input("Ingrese el numero de sesion: "))

    posicion_sesion = -1
    for i in range(len(matriz_sesiones)):
        if sesion == matriz_sesiones[i][0]:
            posicion_sesion = i
            break

    if posicion_sesion == -1:
        print(f"La sesion {sesion}, no existe")
        return

    print(f"==== SESION: {sesion} ====")
    for i in range(len(matriz_estudiantes)):
        print(f"Nombre: {matriz_estudiantes[i][1]}\nAsistencia: {matriz_asistencias[i][posicion_sesion]}")

def calcular_porcentaje(matriz_asistencias, i):

    if len(matriz_asistencias[i]) == 0:
        print("No hay clases csrgadas")
        return

    presentes = contar_estado(matriz_asistencias[i], "P")
    total_clases = len(matriz_asistencias[i])

    pct = (presentes / total_clases) * 100

    print(f"El porcentaje es: {pct}%")
    return pct

def mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_asistencias):

    alumnos_en_riesgo = False

    if len(matriz_estudiantes) == 0:
        print(f"No hay alumnos cargados")
        return

    pct_de_asistencia = float(input("Ingrese el limite de porcentaje de asistencia (75.0): "))
    while pct_de_asistencia <= 0:
        print("El porcentaje no puede ser negativo o cero")
        pct_de_asistencia = float(input("Ingrese el limite de porcentaje de asistencia (75.0): "))

    for i in range(len(matriz_estudiantes)):
        porcentaje = calcular_porcentaje(matriz_asistencias, i)
        if porcentaje <= pct_de_asistencia:
            alumnos_en_riesgo = True
            print(f"==== ALUMNO DEBAJO DEL LIMITE ====")
            print(f"Nombre: {matriz_estudiantes[i][1]}\nLegajo: {matriz_estudiantes[i][0]}\nPorcentaje: {porcentaje}%")

    if not alumnos_en_riesgo:
        print(f"No hay alumnos con menos del {pct_de_asistencia}%")

def menu_consultas(matriz_estudiantes, matriz_sesiones, matriz_asistencias):
    opcion = -1
    while opcion != 0:
        print("\n==== MENU DE CONSULTAS ====")
        print("1. Consultar por estudiante")
        print("2. Consultar por sesion")
        print("3. Mostrar estudiante en riesgo")
        print("0. Volver al menu principal")
        
        opcion = int(input("Ingrese una opcion: "))
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

# menu_consultas(matriz_estudiantes, matriz_sesiones, matriz_asistencias)
# Asi llaman el menu