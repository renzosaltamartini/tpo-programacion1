import Archivos

# =========================================
# SISTEMA DE REGISTRO DE ASISTENCIA
# GESTION DE ASISTENCIAS
# =========================================


# =========================================
# FUNCIONES AUXILIARES
# =========================================


def validar_estado(estado, permitir_cancelar=False):

    # Convierte el estado a mayuscula y valida que sea una de las opciones permitidas.
    estado = estado.strip().upper()

    while estado not in ["P", "A", "T", "J"]:

        if permitir_cancelar and estado == "0":
            return None

        print("Estado incorrecto.")

        if permitir_cancelar:
            estado = input("Ingrese P, A, T o J, o 0 para cancelar: ").strip().upper()

        else:
            estado = input("Ingrese P, A, T o J: ").strip().upper()

    return estado


def validar_si_no(respuesta):

    # Valida respuestas de tipo si/no utilizadas para continuar dentro de los menus.
    respuesta = respuesta.strip().upper()

    while respuesta not in ["S", "N"]:
        print("Opción inválida.")
        respuesta = input("Ingrese S o N: ").strip().upper()

    return respuesta


def validar_legajo(legajo):

    # Valida un legajo positivo; el 0 permite cancelar.
    legajo = legajo.strip()

    while not legajo.isdigit():
        print("Legajo inválido.")
        legajo = input("Ingrese un legajo positivo o 0 para volver: ").strip()

    legajo = int(legajo)

    if legajo == 0:
        return None

    return legajo


def mostrar_estados_asistencia():

    # Muestra una referencia de las letras utilizadas para registrar cada estado de asistencia.
    print("\nEstados de asistencia:")
    print("P - Presente")
    print("A - Ausente")
    print("T - Tarde")
    print("J - Justificado")


def buscar_estudiante(ruta_padron, legajo):

    alumno = Archivos.buscar_estudiante(legajo, ruta_padron)
    nombre = None

    if len(alumno) > 0:
        nombre = alumno[1]

    return nombre


def buscar_inscripto(inscriptos, legajo, posicion=0):

    # Si se llega al final, el legajo no esta inscripto.
    if posicion == len(inscriptos):
        return -1

    # Si se encuentra el legajo, se devuelve su posicion.
    if inscriptos[posicion][0] == legajo:
        return posicion

    # Se busca en la siguiente fila mediante una llamada recursiva.
    return buscar_inscripto(inscriptos, legajo, posicion + 1)


def seleccionar_sesion(matriz_sesiones):

    # Muestra las sesiones cargadas y devuelve la posicion de la sesion elegida.
    if len(matriz_sesiones) == 0:
        print("No hay sesiones registradas.")
        return None

    print("\nSesiones disponibles:")

    for sesion in matriz_sesiones:
        print(f"{sesion[0]} - {sesion[1]} - {sesion[2]}")

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

# =========================================
# GESTION DE INSCRIPCIONES
# =========================================


def inscribir_estudiante(ruta_padron, grupo):
    import Estudiantes

    opcion = Estudiantes.elegir_busqueda_estudiante()
    if opcion == 0:
        return

    if opcion == 1:
        alumno = Estudiantes.seleccionar_en_padron(ruta_padron)
        if alumno == None:
            return
        legajo, nombre = alumno
    else:
        legajo = input("\nIngrese el legajo del estudiante (0 para volver): ")
        legajo = validar_legajo(legajo)
        if legajo == None:
            return

        nombre = buscar_estudiante(ruta_padron, legajo)
        if nombre == None:
            print("Estudiante no encontrado en el registro general.")
            return

    # Se comprueba si ya tiene una inscripcion en este grupo.
    posicion = buscar_inscripto(grupo["inscriptos"], legajo)

    if posicion != -1:
        print("El estudiante ya está inscripto en este grupo.")
        return

    print("\nEstudiante:", nombre)

    respuesta = input("¿Confirma la inscripción? (S/N): ")
    respuesta = validar_si_no(respuesta)

    if respuesta == "N":
        print("Inscripción cancelada.")
        return

    # Sin un registro de asistencia, el inscripto figura como pendiente.
    grupo["inscriptos"].append([legajo, "Activo"])

    print("Estudiante inscripto correctamente.")


def dar_baja_inscripcion(grupo):

    legajo = input("\nIngrese el legajo del estudiante (0 para volver): ")
    legajo = validar_legajo(legajo)

    if legajo == None:
        return

    posicion = buscar_inscripto(grupo["inscriptos"], legajo)

    if posicion == -1:
        print("El estudiante no está inscripto en este grupo.")
        return

    if grupo["inscriptos"][posicion][1] == "Inactivo":
        print("La inscripción ya está inactiva.")
        return

    respuesta = input("¿Confirma la baja? (S/N): ")
    respuesta = validar_si_no(respuesta)

    if respuesta == "N":
        print("Baja cancelada.")
        return

    grupo["inscriptos"][posicion][1] = "Inactivo"

    print("Inscripción dada de baja correctamente.")


def reactivar_inscripcion(grupo):

    legajo = input("\nIngrese el legajo del estudiante (0 para volver): ")
    legajo = validar_legajo(legajo)

    if legajo == None:
        return

    posicion = buscar_inscripto(grupo["inscriptos"], legajo)

    if posicion == -1:
        print("El estudiante no está inscripto en este grupo.")
        return

    if grupo["inscriptos"][posicion][1] == "Activo":
        print("La inscripción ya está activa.")
        return

    grupo["inscriptos"][posicion][1] = "Activo"

    print("Inscripción reactivada correctamente.")


def mostrar_inscriptos(ruta_padron, grupo):

    if len(grupo["inscriptos"]) == 0:
        print("No hay estudiantes inscriptos en este grupo.")
        return

    print("\n===== INSCRIPTOS DEL GRUPO =====\n")
    print(f"{'Legajo':<10}{'Nombre':<25}{'Estado':<12}")

    for inscripto in grupo["inscriptos"]:

        legajo = inscripto[0]
        nombre = buscar_estudiante(ruta_padron, legajo)
        estado = inscripto[1]

        print(f"{legajo:<10}{nombre:<25}{estado:<12}")


def menu_inscripciones(ruta_padron, grupo):

    # Menu independiente para gestionar las inscripciones del grupo seleccionado.
    opcion = ""

    while opcion != "0":

        print("\n===== GESTIÓN DE INSCRIPCIONES =====")
        print("1. Inscribir estudiante")
        print("2. Dar de baja una inscripción")
        print("3. Reactivar una inscripción")
        print("4. Mostrar inscriptos")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            inscribir_estudiante(ruta_padron, grupo)

        elif opcion == "2":

            dar_baja_inscripcion(grupo)

        elif opcion == "3":

            reactivar_inscripcion(grupo)

        elif opcion == "4":

            mostrar_inscriptos(ruta_padron, grupo)

        elif opcion == "0":

            print("Volviendo al menú principal...")

        else:

            print("Opción inválida.")

    return grupo

# =========================================
# GESTION DE ASISTENCIAS
# =========================================


def registrar_asistencia(ruta_padron, grupo, materia, nombre_grupo):

    if len(grupo["sesiones"]) == 0:
        print("No hay sesiones registradas.")
        return

    if len(grupo["inscriptos"]) == 0:
        print("No hay estudiantes inscriptos en este grupo.")
        return

    posicion_sesion = seleccionar_sesion(grupo["sesiones"])

    if posicion_sesion == None:
        return

    sesion = grupo["sesiones"][posicion_sesion][0]
    estados = Archivos.leer_asistencias(materia, nombre_grupo, sesion=sesion)
    mostrar_estados_asistencia()

    print("\n===== REGISTRO DE ASISTENCIA =====")

    cantidad_registradas = 0

    for i in range(len(grupo["inscriptos"])):

        # Solo se registran pendientes de inscriptos activos.
        if grupo["inscriptos"][i][1] == "Activo":

            legajo = grupo["inscriptos"][i][0]
            if estados.get(legajo, "-") == "-":
                nombre = buscar_estudiante(ruta_padron, legajo)

                print("\nLegajo:", legajo)
                print("Estudiante:", nombre)

                estado = input("Ingrese P, A, T o J, o 0 para cancelar: ")
                estado = validar_estado(estado, permitir_cancelar=True)

                if estado == None:
                    print("Registro cancelado. Las asistencias ya cargadas se conservan.")
                    return

                Archivos.guardar_asistencia(materia, nombre_grupo, legajo, sesion, estado)
                cantidad_registradas += 1

    if cantidad_registradas > 0:
        print("\nAsistencias pendientes registradas correctamente.")

    else:
        print("\nNo hay asistencias pendientes de inscriptos activos para esta sesión.")


def modificar_asistencia(ruta_padron, grupo, materia, nombre_grupo):

    if len(grupo["sesiones"]) == 0:
        print("No hay sesiones registradas.")
        return

    if len(grupo["inscriptos"]) == 0:
        print("No hay estudiantes inscriptos en este grupo.")
        return

    mostrar_estados_asistencia()

    continuar = "S"

    while continuar == "S":

        legajo = input("\nIngrese el legajo del estudiante (0 para volver): ")
        legajo = validar_legajo(legajo)

        if legajo == None:
            return

        posicion_estudiante = buscar_inscripto(grupo["inscriptos"], legajo)

        if posicion_estudiante == -1:
            print("El estudiante no está inscripto en este grupo.")

        else:

            posicion_sesion = seleccionar_sesion(grupo["sesiones"])

            if posicion_sesion == None:
                return

            nombre = buscar_estudiante(ruta_padron, legajo)
            sesion = grupo["sesiones"][posicion_sesion][0]
            estados = Archivos.leer_asistencias(materia, nombre_grupo, legajo=legajo, sesion=sesion)
            estado_actual = estados.get(sesion, "-")

            print("\nEstudiante:", nombre)
            print("Estado actual:", estado_actual)

            if estado_actual == "-":
                print("La asistencia está pendiente de registrar.")

            nuevo_estado = input("Ingrese P, A, T o J, o 0 para cancelar: ").strip()

            if nuevo_estado == "0":
                print("Modificación cancelada.")
                return

            nuevo_estado = validar_estado(nuevo_estado, permitir_cancelar=True)

            if nuevo_estado == None:
                print("Modificación cancelada.")
                return

            # Se modifica solamente la asistencia seleccionada.
            Archivos.guardar_asistencia(materia, nombre_grupo, legajo, sesion, nuevo_estado)

            print("Asistencia modificada correctamente.")

        continuar = input("\n¿Desea modificar otra asistencia? (S/N): ")
        continuar = validar_si_no(continuar)


def mostrar_planilla_general(ruta_padron, grupo, materia, nombre_grupo):

    # Para mostrar la planilla deben existir inscriptos y sesiones cargadas.
    if len(grupo["inscriptos"]) == 0:
        print("No hay estudiantes inscriptos en este grupo.")
        return

    if len(grupo["sesiones"]) == 0:
        print("No hay sesiones registradas.")
        return

    print("\n===== PLANILLA GENERAL =====\n")

    # Se imprimen primero las columnas fijas de legajo, nombre y estado de inscripcion.
    print(f"{'Legajo':<10}{'Nombre':<25}{'Estado':<12}", end="")

    # Cada sesion se agrega como una columna de la planilla.
    for sesion in grupo["sesiones"]:

        titulo_sesion = "S" + str(sesion[0])
        print(f"{titulo_sesion:^8}", end="")

    print()

    # Se muestran todos los inscriptos, incluidos los inactivos.
    for i in range(len(grupo["inscriptos"])):

        legajo = grupo["inscriptos"][i][0]
        nombre = buscar_estudiante(ruta_padron, legajo)
        estado_inscripcion = grupo["inscriptos"][i][1]

        print(f"{legajo:<10}{nombre:<25}{estado_inscripcion:<12}", end="")

        estados = Archivos.leer_asistencias(materia, nombre_grupo, legajo=legajo)
        for sesion in grupo["sesiones"]:
            estado = estados.get(sesion[0], "-")
            print(f"{estado:^8}", end="")

        print()

    print("\n- : asistencia sin registrar.")


def menu_asistencias(ruta_padron, grupo, materia, nombre_grupo):

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

            registrar_asistencia(ruta_padron, grupo, materia, nombre_grupo)

        elif opcion == "2":

            modificar_asistencia(ruta_padron, grupo, materia, nombre_grupo)

        elif opcion == "3":

            mostrar_planilla_general(ruta_padron, grupo, materia, nombre_grupo)

        elif opcion == "0":

            print("Volviendo al menú principal...")

        else:

            print("Opción inválida.")

    return grupo
