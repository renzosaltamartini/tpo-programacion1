import Asistencias
import Sesiones


import Archivos


def pedir_nombre():
    nombre = input("Ingrese el nombre completo: ").strip()
    while not nombre.replace(" ", "").isalpha():
        nombre = input("Use solo letras y espacios. Nombre: ").strip()
    return nombre


def buscar_legajo(ruta_padron, legajo):

    alumno = Archivos.buscar_estudiante(legajo, ruta_padron)
    return alumno


def registrar_estudiantes(ruta_padron):

    generar_titulo_de_todos("REGISTRO DE ESTUDIANTE")
    continuar = 0

    while continuar == 0:
        legajo = validar_inputs("Ingrese el legajo: ")

        while legajo <= 0 or len(buscar_legajo(ruta_padron, legajo)) > 0:
            legajo = validar_inputs("Legajo invalido o repetido. Ingrese otro: ")

        nombre = pedir_nombre()
        guardado = Archivos.agregar_estudiante(legajo, nombre, ruta_padron)

        if guardado == True:
            print("Estudiante registrado.")
        else:
            print("El estudiante no se guardo.")

        continuar = validar_inputs("Registrar otro? (0: Si / 1: No): ")
        while continuar not in [0, 1]:
            continuar = validar_inputs("Ingrese 0 para continuar o 1 para volver: ")

    return ruta_padron




def buscar_estudiantes(ruta_padron):

    opcion = elegir_busqueda_estudiante()

    if opcion == 1:
        texto = input("Nombre o apellido (0 para volver): ").strip()
        if texto != "0":
            mostrar_estudiantes(ruta_padron, texto)

    elif opcion == 2:
        legajo = validar_inputs("Legajo (0 para volver): ")
        if legajo > 0:
            alumno = buscar_legajo(ruta_padron, legajo)
            if len(alumno) > 0:
                imprimir_la_matriz([alumno])
            else:
                print("No se encontro el estudiante.")


def seleccionar_en_padron(ruta_padron):

    texto = input("Nombre o apellido (0 para volver): ").strip()
    elegido = None
    archivo = None

    if texto != "0" and len(texto) > 0:
        clave = texto.lower().replace(" ", "")

        try:
            archivo = open(ruta_padron, "r", encoding="utf-8-sig")
            cantidad = 0
            alumno = Archivos.leer_estudiante(archivo)

            while alumno != None:
                if clave in alumno[1].lower().replace(" ", ""):
                    cantidad += 1
                    ultimo = alumno
                    print(f"{cantidad}. {alumno[1]} (legajo {alumno[0]})")
                alumno = Archivos.leer_estudiante(archivo)

            if cantidad == 0:
                print("No se encontraron estudiantes.")
            elif cantidad == 1:
                elegido = ultimo
            else:
                opcion = validar_inputs("Seleccione un estudiante (0 para volver): ")
                while opcion < 0 or opcion > cantidad:
                    opcion = validar_inputs("Opcion invalida. Seleccione nuevamente: ")

                if opcion > 0:
                    archivo.seek(0)
                    cantidad = 0
                    alumno = Archivos.leer_estudiante(archivo)

                    while alumno != None and elegido == None:
                        if clave in alumno[1].lower().replace(" ", ""):
                            cantidad += 1
                            if cantidad == opcion:
                                elegido = alumno
                        if elegido == None:
                            alumno = Archivos.leer_estudiante(archivo)

        finally:
            Archivos.cerrar_archivo(archivo)

    return elegido


def buscar_nombre(matriz, nombre):

    alumnos = []

    if len(nombre.strip()) == 0:
        return alumnos

    nombre = nombre.lower()
    nombre = nombre.replace(" ", "")

    for i in range(len(matriz)):

        if nombre in matriz[i][1].lower().replace(" ", ""):
            alumnos.append(i)

    return alumnos


def elegir_busqueda_estudiante():
    print("1. Buscar por nombre")
    print("2. Buscar por legajo")
    print("0. Volver")

    opcion = validar_inputs("Seleccione una opción: ")
    while opcion not in (0, 1, 2):
        print("Opción inválida.")
        opcion = validar_inputs("Seleccione una opción: ")
    return opcion


def seleccionar_estudiante_por_nombre(matriz_estudiantes):

    nombre = input("Nombre o apellido del estudiante (0 para volver): ").strip()
    posicion = None

    if nombre != "0":
        coincidencias = buscar_nombre(matriz_estudiantes, nombre)

        if len(coincidencias) == 0:
            print("No se encontro ningun estudiante.")
        elif len(coincidencias) == 1:
            posicion = coincidencias[0]
        else:
            for numero, indice in enumerate(coincidencias, 1):
                alumno = matriz_estudiantes[indice]
                print(f"{numero}. {alumno[1]} (legajo {alumno[0]})")

            opcion = validar_inputs("Seleccione un estudiante (0 para volver): ")
            while opcion < 0 or opcion > len(coincidencias):
                opcion = validar_inputs("Opcion invalida. Seleccione nuevamente: ")

            if opcion > 0:
                posicion = coincidencias[opcion - 1]

    return posicion


def modificar_nombre_estudiantes(ruta_padron):

    legajo = validar_inputs("Legajo del estudiante (0 para volver): ")

    if legajo > 0:
        if len(buscar_legajo(ruta_padron, legajo)) > 0:
            nombre = pedir_nombre()
            guardado = Archivos.cambiar_nombre_estudiante(legajo, nombre, ruta_padron)
            if guardado == True:
                print("Nombre actualizado.")
            else:
                print("El cambio de nombre no se guardo.")
        else:
            print("Legajo no encontrado.")

    return ruta_padron


def mostrar_estudiantes(ruta_padron, texto=""):

    generar_titulo_de_todos("LISTADO DE ESTUDIANTES")
    archivo = None
    cantidad = 0
    clave = texto.lower().replace(" ", "")

    try:
        archivo = open(ruta_padron, "r", encoding="utf-8-sig")
        alumno = Archivos.leer_estudiante(archivo)
        print(f"{'Legajo':<10}{'Nombre':<25}")

        while alumno != None:
            if clave in alumno[1].lower().replace(" ", ""):
                print(f"{alumno[0]:<10}{alumno[1]:<25}")
                cantidad += 1
            alumno = Archivos.leer_estudiante(archivo)

        if cantidad == 0:
            print("No se encontraron estudiantes.")

    finally:
        Archivos.cerrar_archivo(archivo)


def generar_titulo_de_todos(titulo):

    print()
    print("=" * 50)
    print(titulo.center(50))
    print("=" * 50)

    return


def imprimir_la_matriz(matriz_estudiantes):

    print(f"{'Legajo':<10}{'Nombre':<25}")
    print("-" * 50)

    for legajo, nombre in matriz_estudiantes:
        print(f"{legajo:<10}{nombre:<25}")

    if len(matriz_estudiantes) == 0:
        print("No se encontraron estudiantes.")


def validar_inputs(Texto):

    while True:
        try:
            variable = int(input(Texto))
            break
        except ValueError:
            print("Opcion Invalida")

    return variable


def menu_estudiantes(ruta_padron, cursadas=None):

    # Función principal del menú de estudiantes
    salida = -1
    opcion = 0

    while salida != 0:

        generar_titulo_de_todos("ESTUDIANTES")

        print()
        print("  1. Registrar estudiantes")
        print("  2. Buscar estudiantes")
        print("  3. Modificar nombre de estudiante")
        print("  4. Mostrar estudiantes")
        print("  5. Volver al menú principal")
        print("  6. Gestionar inscripciones en un grupo")
        print()

        opcion = validar_inputs("Seleccione una opcion: ")

        if opcion == 1:
            registrar_estudiantes(ruta_padron)

        elif opcion == 2:
            buscar_estudiantes(ruta_padron)

        elif opcion == 3:
            modificar_nombre_estudiantes(ruta_padron)

        elif opcion == 4:
            mostrar_estudiantes(ruta_padron)

        elif opcion == 5:
            salida = 0

        elif opcion == 6:

            if cursadas == None:
                print("Las inscripciones se abren desde el programa principal.")

            else:
                materia = Sesiones.seleccionar_materia(cursadas)

                if materia != None:
                    nombre_grupo = Sesiones.seleccionar_grupo(cursadas, materia)

                    if nombre_grupo != None:
                        grupo = Archivos.obtener_grupo(materia, nombre_grupo)
                        Asistencias.menu_inscripciones(ruta_padron, grupo)
                        guardado = Archivos.guardar_grupo(materia, nombre_grupo, grupo)
                        if guardado == False:
                            raise OSError("No se pudieron guardar las inscripciones del grupo.")

        else:
            print()
            print("Opción inválida. Intente nuevamente.")

    return ruta_padron
