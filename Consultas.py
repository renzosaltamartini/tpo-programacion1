import Archivos
import Estudiantes


def consultar_estudiante(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo):

    if len(matriz_estudiantes) == 0:
        print("No hay alumnos cargados")
        return
    
    opcion = Estudiantes.elegir_busqueda_estudiante()
    if opcion == 0:
        return

    if opcion == 1:
        posicion_inscripto = Estudiantes.seleccionar_estudiante_por_nombre(matriz_estudiantes)
        if posicion_inscripto == None:
            return
    else:
        while True:
            try:
                legajo = int(input("Ingrese el legajo que quiere buscar (0 para volver): "))
                if legajo == 0:
                    return
                if legajo > 0:
                    break
                print("El legajo debe ser mayor a cero.")
            except ValueError:
                print("Entrada inválida. Debe ingresar un número entero.")

        for posicion_inscripto, estudiante in enumerate(matriz_estudiantes):
            if str(legajo) == str(estudiante[0]):
                break
        else:
            print("El legajo no está cargado")
            return

    # Se obtienen los datos generales asegurando la tercera columna (estado)
    estado_alumno = matriz_estudiantes[posicion_inscripto][2] if len(matriz_estudiantes[posicion_inscripto]) > 2 else "Activo"

    print("===== DATOS DEL ESTUDIANTE =====")
    print(f"Legajo: {matriz_estudiantes[posicion_inscripto][0]}\nNombre: {matriz_estudiantes[posicion_inscripto][1]}\nEstado: {estado_alumno}")

    legajo = matriz_estudiantes[posicion_inscripto][0]
    estados = Archivos.leer_asistencias(materia, nombre_grupo, legajo=legajo)

    for sesion in matriz_sesiones:
        print(f"Sesion: {sesion[0]}\nTema: {sesion[2]}")
        estado = estados.get(sesion[0], "-")
        asistencia = "Nula"

        if estado == "A":
            asistencia = "Ausente"
        elif estado == "P":
            asistencia = "Presente"
        elif estado == "J":
            asistencia = "Justificado"
        elif estado == "T":
            asistencia = "Tarde"

        print(f"Asistencia: {asistencia}")


def consultar_sesion(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo):

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

    estados = Archivos.leer_asistencias(materia, nombre_grupo, sesion=sesion)
    print(f"==== SESION: {sesion} ====")
    for estudiante in matriz_estudiantes:
        estado = estados.get(estudiante[0], "-")
        print(f"Nombre: {estudiante[1]}\nAsistencia: {estado}")


def mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo):

    alumnos_en_riesgo = False

    if len(matriz_estudiantes) == 0:
        print("No hay alumnos cargados")
        return

    while True:
        try:
            pct_de_asistencia = float(input("Ingrese el limite de porcentaje de asistencia (ej: 75.0): "))
            if 0 < pct_de_asistencia <= 100:
                break
            else:
                print("El porcentaje debe ser mayor que 0 y como máximo 100.")
        except ValueError:
            print("Debe ingresar un número decimal válido.")

    total_clases = len(matriz_sesiones)
    if total_clases == 0:
        print("No hay clases cargadas")
        return

    for estudiante in matriz_estudiantes:
        estados = Archivos.leer_asistencias(materia, nombre_grupo, legajo=estudiante[0])
        presentes = 0
        for sesion in matriz_sesiones:
            if estados.get(sesion[0], "-") == "P":
                presentes += 1
        porcentaje = presentes * 100 / total_clases
        if porcentaje < pct_de_asistencia:
            alumnos_en_riesgo = True
            print("==== ALUMNO DEBAJO DEL LIMITE ====")
            print(f"Nombre: {estudiante[1]}\nLegajo: {estudiante[0]}\nPorcentaje: {porcentaje:.2f}%")

    if not alumnos_en_riesgo:
        print(f"No hay alumnos con menos del {pct_de_asistencia}%")


def menu_consultas(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo):
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
            consultar_estudiante(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo)
        elif opcion == 2:
            consultar_sesion(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo)
        elif opcion == 3:
            mostrar_estudiantes_riesgo(matriz_estudiantes, matriz_sesiones, materia, nombre_grupo)
        elif opcion == 0:
            print("Volviendo al menu principal...")
