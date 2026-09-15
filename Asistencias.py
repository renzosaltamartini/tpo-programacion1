# =========================================
# SISTEMA DE REGISTRO DE ASISTENCIA
# GESTION DE ASISTENCIAS
# =========================================


def validar_estado(estado):

    # Convierte el estado a mayuscula y valida que sea una de las opciones permitidas.
    estado = estado.strip().upper()

    while estado not in ["P", "A", "T", "J"]:
        print("Estado incorrecto.")
        estado = input("Ingrese P, A, T o J: ").strip().upper()

    return estado


def validar_si_no(respuesta):

    # Valida respuestas de tipo si/no utilizadas para continuar dentro de los menus.
    respuesta = respuesta.strip().upper()

    while respuesta not in ["S", "N"]:
        print("Opción inválida.")
        respuesta = input("Ingrese S o N: ").strip().upper()

    return respuesta


def mostrar_estados_asistencia():

    # Muestra una referencia de las letras utilizadas para registrar cada estado de asistencia.
    print("\nEstados de asistencia:")
    print("P - Presente")
    print("A - Ausente")
    print("T - Tarde")
    print("J - Justificado")


def seleccionar_sesion(matriz_sesiones):

    # Muestra las sesiones cargadas y devuelve la posicion de la sesion elegida.
    if len(matriz_sesiones) == 0:
        print("No hay sesiones registradas.")
        return None

    print("\nSesiones disponibles:")

    for sesion in matriz_sesiones:
        print(f"{sesion[0]} - {sesion[1]} - {sesion[2]} - {sesion[3]}")

    print("0 - Volver")

    numero = input("¿Qué número de sesión desea seleccionar?: ").strip()

    while True:

        # La opcion 0 permite volver sin seleccionar ninguna sesion.
        if numero == "0":
            return None

        # Se busca el numero real de sesion y se devuelve su posicion dentro de la matriz.
        if numero.isdigit():

            for i in range(len(matriz_sesiones)):

                if str(matriz_sesiones[i][0]) == numero:
                    return i

        print("Sesión inválida.")
        numero = input("Ingrese un número de sesión válido o 0 para volver: ").strip()


def sesion_ya_registrada(matriz_asistencias, posicion_sesion):

    # Si alguna fila de la columna seleccionada tiene un valor distinto de "-",
    # se considera que la asistencia de esa sesion ya fue tomada.
    for fila in matriz_asistencias:

        if fila[posicion_sesion] != "-":
            return True

    return False


def hay_estudiantes_activos(matriz_estudiantes):

    # Verifica que exista al menos un estudiante activo antes de registrar asistencia.
    for estudiante in matriz_estudiantes:

        if estudiante[2] == "Activo":
            return True

    return False


def buscar_posicion_estudiante(matriz_estudiantes, legajo):

    # Busca un estudiante por legajo y devuelve su posicion dentro de la matriz.
    for i in range(len(matriz_estudiantes)):

        if matriz_estudiantes[i][0] == legajo:
            return i

    # Se devuelve -1 cuando el legajo no fue encontrado.
    return -1


def registrar_asistencia(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    # Solo se permite registrar asistencia si existe al menos un estudiante activo.
    if not hay_estudiantes_activos(matriz_estudiantes):
        print("No hay estudiantes activos para registrar asistencia.")
        return

    mostrar_estados_asistencia()

    posicion_sesion = seleccionar_sesion(matriz_sesiones)

    if posicion_sesion == None:
        return

    # No se vuelve a cargar una sesion que ya tenga asistencias registradas.
    if sesion_ya_registrada(matriz_asistencias, posicion_sesion):
        print("La asistencia de esta sesión ya fue registrada.")
        print("Utilice la opción modificar asistencia.")

    else:

        print("\n===== REGISTRO DE ASISTENCIA =====")

        # Se recorre la matriz de estudiantes y se registra solamente a los activos.
        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][2] == "Activo":

                print("\nEstudiante:", matriz_estudiantes[i][1])

                estado = input("Ingrese P, A, T o J: ")
                estado = validar_estado(estado)

                # La fila coincide con el estudiante y la columna con la sesion seleccionada.
                matriz_asistencias[i][posicion_sesion] = estado

        print("\nAsistencia registrada correctamente.")


def modificar_asistencia(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    # Permite corregir una asistencia ya cargada buscando primero al estudiante por legajo.
    mostrar_estados_asistencia()

    continuar = "S"

    while continuar == "S":

        legajo = input("\nIngrese el legajo del estudiante (0 para volver): ").strip()

        # Se valida que el legajo ingresado contenga solamente numeros.
        while not legajo.isdigit():
            print("Legajo inválido.")
            legajo = input("Ingrese un legajo válido o 0 para volver: ").strip()

        if legajo == "0":
            return

        legajo = int(legajo)

        posicion_estudiante = buscar_posicion_estudiante(matriz_estudiantes, legajo)

        if posicion_estudiante == -1:
            print("Estudiante no encontrado.")

        else:

            posicion_sesion = seleccionar_sesion(matriz_sesiones)

            if posicion_sesion == None:
                return

            estado_actual = matriz_asistencias[posicion_estudiante][posicion_sesion]

            # El guion indica que para ese estudiante y sesion todavia no hay asistencia cargada.
            if estado_actual == "-":
                print("No hay una asistencia registrada para modificar.")

            else:

                print("\nEstudiante:", matriz_estudiantes[posicion_estudiante][1])
                print("Estado actual:", estado_actual)

                nuevo_estado = input("Ingrese el nuevo estado (P, A, T o J) o 0 para cancelar: ").strip()

                if nuevo_estado == "0":
                    print("Modificación cancelada.")
                    return

                nuevo_estado = validar_estado(nuevo_estado)

                # Se reemplaza solamente el estado ubicado en la fila y columna seleccionadas.
                matriz_asistencias[posicion_estudiante][posicion_sesion] = nuevo_estado

                print("Asistencia modificada correctamente.")

        continuar = input("\n¿Desea modificar otra asistencia? (S/N): ")
        continuar = validar_si_no(continuar)


def mostrar_planilla_general(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    # Para mostrar la planilla deben existir estudiantes y sesiones cargadas.
    if len(matriz_estudiantes) == 0:
        print("No hay estudiantes registrados.")
        return

    if len(matriz_sesiones) == 0:
        print("No hay sesiones registradas.")
        return

    print("\n===== PLANILLA GENERAL =====\n")

    # Se imprimen primero las columnas fijas de legajo y nombre.
    print(f"{'Legajo':<10}{'Nombre':<25}", end="")

    # Cada sesion se agrega como una columna de la planilla.
    for sesion in matriz_sesiones:

        titulo_sesion = "S" + str(sesion[0])
        print(f"{titulo_sesion:^8}", end="")

    print()

    # Cada fila corresponde a un estudiante y muestra sus estados por sesion.
    for i in range(len(matriz_estudiantes)):

        print(f"{matriz_estudiantes[i][0]:<10}{matriz_estudiantes[i][1]:<25}", end="")

        for j in range(len(matriz_sesiones)):

            estado = matriz_asistencias[i][j]
            print(f"{estado:^8}", end="")

        print()


def menu_asistencias(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    # Menu principal del modulo de asistencias.
    opcion = ""

    while opcion != "0":

        print("\n===== GESTIÓN DE ASISTENCIAS =====")
        print("1. Registrar asistencia")
        print("2. Modificar asistencia")
        print("3. Mostrar planilla general")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            registrar_asistencia(matriz_estudiantes, matriz_sesiones, matriz_asistencias)

        elif opcion == "2":

            modificar_asistencia(matriz_estudiantes, matriz_sesiones, matriz_asistencias)

        elif opcion == "3":

            mostrar_planilla_general(matriz_estudiantes, matriz_sesiones, matriz_asistencias)

        elif opcion == "0":

            print("Volviendo al menú principal...")

        else:

            print("Opción inválida.")

    return matriz_asistencias
