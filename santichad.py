def validar_estado(estado):

    """

    recibe como parametro el estado que se quiero ingresar y verifica que sea valido

    devuelve flag

    """

    estado = estado.upper()

    while estado != "P" and estado != "A" and estado != "T" and estado != "J":

        print("Estado incorrecto.")
        estado = input("Ingrese P, A, T o J: ").upper()

    return estado


def seleccionar_sesion(matriz_sesiones):

    if len(matriz_sesiones) > 0:

        for i in range(len(matriz_sesiones)):
            print(matriz_sesiones[i])

        numero = input("¿Qué número de sesión desea seleccionar?: ")

        while not numero.isdigit() or int(numero) < 1 or int(numero) > len(matriz_sesiones):
            print("Sesión inválida.")
            numero = input("Ingrese número de sesión: ")

        numero = int(numero)

        posicion = numero - 1

        return posicion

    else:
        print("No hay sesiones registradas.")
        return None


def sesion_ya_registrada(matriz_asistencias, posicion_sesion):

    for i in range(len(matriz_asistencias)):

        if matriz_asistencias[i][posicion_sesion] != "":
            return True

    return False


def registrar_asistencia(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    posicion_sesion = seleccionar_sesion(matriz_sesiones)

    if posicion_sesion == None:
        return

    if sesion_ya_registrada(matriz_asistencias, posicion_sesion):
        print("La asistencia de esta sesión ya fue registrada.")
        print("Utilice la opción modificar asistencia.")

    else:

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][3] == "Activo":

                print("Estudiante:", matriz_estudiantes[i][1])

                estado = input("Ingrese P, A, T o J: ")

                estado = validar_estado(estado)

                matriz_asistencias[i][posicion_sesion] = estado

        print("Asistencia registrada correctamente.")


def modificar_asistencia(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    continuar = "S"

    while continuar == "S":

        legajo = input("Ingrese el legajo del estudiante: ")

        posicion_estudiante = -1

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0] == legajo:
                posicion_estudiante = i
                break

        if posicion_estudiante == -1:
            print("Estudiante no encontrado.")

        else:

            posicion_sesion = seleccionar_sesion(matriz_sesiones)

            if posicion_sesion != None:

                estado_actual = matriz_asistencias[posicion_estudiante][posicion_sesion]

                if estado_actual == "":
                    print("No hay una asistencia registrada para modificar.")

                else:

                    print("Estudiante:", matriz_estudiantes[posicion_estudiante][1])
                    print("Estado actual:", estado_actual)

                    nuevo_estado = input("Ingrese el nuevo estado (P, A, T o J): ")

                    nuevo_estado = validar_estado(nuevo_estado)

                    matriz_asistencias[posicion_estudiante][posicion_sesion] = nuevo_estado

                    print("Asistencia modificada correctamente.")

        continuar = input("¿Desea modificar otra asistencia? (S/N): ").upper()

        while continuar != "S" and continuar != "N":
            print("Opción inválida.")
            continuar = input("Ingrese S para continuar o N para volver: ").upper()


def mostrar_planilla_general(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    if len(matriz_estudiantes) == 0:
        print("No hay estudiantes registrados.")
        return

    if len(matriz_sesiones) == 0:
        print("No hay sesiones registradas.")
        return

    print("Legajo\tNombre", end="")

    for i in range(len(matriz_sesiones)):
        print("\tS" + matriz_sesiones[i][0], end="")

    print()

    for i in range(len(matriz_estudiantes)):

        print(matriz_estudiantes[i][0], end="\t")
        print(matriz_estudiantes[i][1], end="\t")

        for j in range(len(matriz_sesiones)):

            estado = matriz_asistencias[i][j]

            if estado == "":
                print("-", end="\t")
            else:
                print(estado, end="\t")

        print()

def menu_asistencias(matriz_estudiantes, matriz_sesiones, matriz_asistencias):

    opcion = ""

    while opcion != "0":

        print("\n===== GESTIÓN DE ASISTENCIAS =====")
        print("1. Registrar asistencia")
        print("2. Modificar asistencia")
        print("3. Mostrar planilla general")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_asistencia(
                matriz_estudiantes,
                matriz_sesiones,
                matriz_asistencias
            )

        elif opcion == "2":
            modificar_asistencia(
                matriz_estudiantes,
                matriz_sesiones,
                matriz_asistencias
            )

        elif opcion == "3":
            mostrar_planilla_general(
                matriz_estudiantes,
                matriz_sesiones,
                matriz_asistencias
            )

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción inválida.")














matriz_estudiantes = [
    ["1001", "Ana Pérez", "A", "Activo"],
    ["1002", "Juan López", "A", "Activo"],
    ["1003", "Sofía Gómez", "A", "Inactivo"]
]

matriz_sesiones = [
    ["1", "01/09/2026", "Programación I", "Matrices"],
    ["2", "08/09/2026", "Programación I", "Funciones"]
]

matriz_asistencias = [
    ["", ""],
    ["", ""],
    ["", ""]
]


menu_asistencias(matriz_estudiantes, matriz_sesiones, matriz_asistencias)