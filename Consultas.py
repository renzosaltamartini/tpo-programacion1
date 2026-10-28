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
    
    # Se solicita el legajo y se valida que sea numérico y mayor a cero
    while True:
        try:
            legajo = int(input("Ingrese el legajo que quiere buscar: "))
            if legajo <= 0:
                print("El legajo no puede ser negativo o cero")
            else:
                break
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")

    posicion = -1
    for i in range(len(matriz_estudiantes)):
        if str(legajo) == str(matriz_estudiantes[i][0]):
            posicion = i
            break

    if posicion == -1:
        print("El legajo no está cargado")
        return

    # Se obtienen los datos generales asegurando la tercera columna (estado)
    estado_alumno = matriz_estudiantes[posicion][2] if len(matriz_estudiantes[posicion]) > 2 else "Activo"

    print("===== DATOS DEL ESTUDIANTE =====")
    print(f"Legajo: {matriz_estudiantes[posicion][0]}\nNombre: {matriz_estudiantes[posicion][1]}\nEstado: {estado_alumno}")

    for i in range(len(matriz_sesiones)):
        print(f"Sesion: {matriz_sesiones[i][0]}\nMateria: {matriz_sesiones[i][2]}")
        asistencia = "Nula"

        if i < len(matriz_asistencias[posicion]):
            estado_asist = matriz_asistencias[posicion][i]
            if estado_asist == "A":
                asistencia = "Ausente"
            elif estado_asist == "P":
                asistencia = "Presente"
            elif estado_asist == "J":
                asistencia = "Justificado"
            elif estado_asist == "T":
                asistencia = "Tarde"

        print(f"Asistencia: {asistencia}")


def consultar_sesion(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    if len(matriz_sesiones) == 0:
        print("No hay sesiones cargadas")
        return

    while True:
        try:
            sesion = int(input("Ingrese el numero de sesion: "))
            if sesion <= 0:
                print("El numero de sesion no puede ser negativo o cero")
            else:
                break
        except ValueError:
            print("Debe ingresar un número entero para la sesión.")

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
        estado = "-"
        if posicion_sesion < len(matriz_asistencias[i]):
            estado = matriz_asistencias[i][posicion_sesion]
        print(f"Nombre: {matriz_estudiantes[i][1]}\nAsistencia: {estado}")


def calcular_porcentaje(matriz_asistencias, i):

    if len(matriz_asistencias[i]) == 0:
        print("No hay clases cargadas")
        return 0

    presentes = contar_estado(matriz_asistencias[i], "P")
    total_clases = len(matriz_asistencias[i])

    pct = (presentes / total_clases) * 100
    return pct


def mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_asistencias):

    alumnos_en_riesgo = False

    if len(matriz_estudiantes) == 0:
        print("No hay alumnos cargados")
        return

    while True:
        try:
            pct_de_asistencia = float(input("Ingrese el limite de porcentaje de asistencia (ej: 75.0): "))
            if pct_de_asistencia <= 0 or pct_de_asistencia > 100:
                print("El porcentaje debe ser un valor entre 1 y 100.")
            else:
                break
        except ValueError:
            print("Debe ingresar un número decimal válido.")

    for i in range(len(matriz_estudiantes)):
        porcentaje = calcular_porcentaje(matriz_asistencias, i)
        if porcentaje <= pct_de_asistencia:
            alumnos_en_riesgo = True
            print("==== ALUMNO DEBAJO DEL LIMITE ====")
            print(f"Nombre: {matriz_estudiantes[i][1]}\nLegajo: {matriz_estudiantes[i][0]}\nPorcentaje: {porcentaje:.2f}%")

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
        
        try:
            opcion = int(input("Ingrese una opcion: "))
            while opcion < 0 or opcion > 3:
                print("La opcion es invalida")
                opcion = int(input("Ingrese una opcion valida (0 a 3): "))
        except ValueError:
            print("Debe ingresar un número entero válido.")
            opcion = -1
            continue

        if opcion == 1:
            consultar_estudiante(matriz_estudiantes, matriz_sesiones, matriz_asistencias)
        elif opcion == 2:
            consultar_sesion(matriz_estudiantes, matriz_sesiones, matriz_asistencias)
        elif opcion == 3:
            mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_asistencias)
        elif opcion == 0:
            print("Volviendo al menu principal...")