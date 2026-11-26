from Asistencias import menu_inscripciones
from Sesiones import seleccionar_materia, seleccionar_grupo


from Archivos import editar_grupo


def pedir_nombre():
    nombre = input("Ingrese el nombre completo: ").strip()
    while not nombre.replace(" ", "").isalpha():
        nombre = input("Use solo letras y espacios. Nombre: ").strip()
    return nombre


def buscar_legajo(padron, legajo):
    return next((alumno for alumno in padron if alumno[0] == legajo), [])


def registrar_estudiantes(padron):
    generar_titulo_de_todos("REGISTRO DE ESTUDIANTE")
    while True:
        legajo = validar_inputs("Ingrese el legajo: ")
        while legajo <= 0 or buscar_legajo(padron, legajo):
            legajo = validar_inputs("Legajo inválido o repetido. Ingrese otro: ")
        padron.agregar(legajo, pedir_nombre())
        print("Estudiante registrado.")
        if validar_inputs("¿Registrar otro? (0 para continuar): ") != 0:
            return padron


def coincidencias(padron, texto):
    clave = texto.lower().replace(" ", "")
    for legajo, nombre in padron:
        if clave and clave in nombre.lower().replace(" ", ""):
            yield legajo, nombre


def buscar_estudiantes(padron):
    opcion = elegir_busqueda_estudiante()
    if opcion == 1:
        texto = input("Nombre o apellido (0 para volver): ").strip()
        if texto != "0":
            imprimir_la_matriz(coincidencias(padron, texto))
    elif opcion == 2:
        legajo = validar_inputs("Legajo (0 para volver): ")
        if legajo:
            alumno = buscar_legajo(padron, legajo)
            imprimir_la_matriz([alumno] if alumno else [])


def seleccionar_en_padron(padron):
    texto = input("Nombre o apellido (0 para volver): ").strip()
    if texto == "0":
        return None
    cantidad = 0
    for legajo, nombre in coincidencias(padron, texto):
        cantidad += 1
        print(f"{cantidad}. {nombre} (legajo {legajo})")
    if cantidad == 0:
        print("No se encontraron estudiantes.")
        return None
    if cantidad == 1:
        return legajo, nombre
    opcion = validar_inputs("Seleccione un estudiante (0 para volver): ")
    while not 0 <= opcion <= cantidad:
        opcion = validar_inputs("Opción inválida. Seleccione un estudiante: ")
    if opcion:
        for numero, alumno in enumerate(coincidencias(padron, texto), 1):
            if numero == opcion:
                return alumno


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
    nombre = input("Ingrese el nombre o apellido del estudiante (0 para volver): ").strip()
    if nombre == "0":
        return None

    coincidencias = buscar_nombre(matriz_estudiantes, nombre)
    if not coincidencias:
        print("No se encontró ningún estudiante con ese nombre.")
        return None

    if len(coincidencias) == 1:
        return coincidencias[0]

    for numero, posicion in enumerate(coincidencias, start=1):
        legajo, nombre = matriz_estudiantes[posicion][:2]
        print(f"{numero}. {nombre} (legajo {legajo})")

    while True:
        opcion = validar_inputs("Seleccione un estudiante (0 para volver): ")
        if opcion == 0:
            return None
        if 1 <= opcion <= len(coincidencias):
            return coincidencias[opcion - 1]
        print("Opción inválida.")


def modificar_nombre_estudiantes(padron):
    legajo = validar_inputs("Legajo del estudiante (0 para volver): ")
    if legajo:
        if buscar_legajo(padron, legajo):
            padron.cambiar_nombre(legajo, pedir_nombre())
            print("Nombre actualizado.")
        else:
            print("Legajo no encontrado.")
    return padron


def mostrar_estudiantes(padron):
    generar_titulo_de_todos("LISTADO DE ESTUDIANTES")
    imprimir_la_matriz(padron)


def generar_titulo_de_todos(titulo):

    print()
    print("=" * 50)
    print(titulo.center(50))
    print("=" * 50)

    return


def imprimir_la_matriz(matriz_estudiantes):
    print()
    print("{:<8}   {:<20}".format(
        "Legajo", "Nombre"
    ))
    print("-" * 50)

    cantidad = 0
    for legajo, nombre in matriz_estudiantes:
        print(f"{legajo:<8}   {nombre}")
        cantidad += 1
    if cantidad == 0:
        print("No se encontraron estudiantes.")


def validar_inputs(Texto):

    while True:
        try:
            variable = int(input(Texto))
            break
        except ValueError:
            print("Opcion Invalida")

    return variable


def menu_estudiantes(matriz_estudiantes, cursadas=None):

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
            matriz_estudiantes = registrar_estudiantes(matriz_estudiantes)

        elif opcion == 2:
            buscar_estudiantes(matriz_estudiantes)

        elif opcion == 3:
            matriz_estudiantes = modificar_nombre_estudiantes(matriz_estudiantes)

        elif opcion == 4:
            mostrar_estudiantes(matriz_estudiantes)

        elif opcion == 5:
            salida = 0

        elif opcion == 6:

            if cursadas == None:
                print("Las inscripciones se abren desde el programa principal.")

            else:
                materia = seleccionar_materia(cursadas)

                if materia != None:
                    nombre_grupo = seleccionar_grupo(cursadas, materia)

                    if nombre_grupo != None:
                        with editar_grupo(materia, nombre_grupo) as grupo:
                            menu_inscripciones(matriz_estudiantes, grupo)

        else:
            print()
            print("Opción inválida. Intente nuevamente.")

    return matriz_estudiantes
