from Asistencias import menu_inscripciones
from Sesiones import seleccionar_materia, seleccionar_grupo


def registrar_estudiantes(matriz_estudiantes):

    # Permite cargar uno o varios estudiantes nuevos hasta que el usuario decida no continuar
    salida = 3
    alumno = []

    generar_titulo_de_todos("REGISTRO DE ESTUDIANTE")

    while salida != 1:
        salida = 3

        print()
        print("-" * 50)

        legajo = validar_inputs("Ingrese el legajo del alumno: ")

        # Se valida que el legajo no exista ya y sea un número válido
        alumno.append(verificacion_legajo(legajo, matriz_estudiantes))

        nombre = input("Ingrese el nombre completo del estudiante: ")

        # Se valida que el nombre contenga letras y espacios
        alumno.append(validar_nombre(nombre, matriz_estudiantes))

        # Pregunta si se desea seguir cargando más alumnos
        while salida != 1 and salida != 0:
            print()
            print("¿Desea registrar otro estudiante?")
            print("  0. Sí")
            print("  1. No")

            salida = validar_inputs("Seleccione una opción: ")

            if salida != 1 and salida != 0:
                print()
                print("Opción inválida. Intente nuevamente.")

        # Se agrega el alumno a la matriz
        matriz_estudiantes.append(alumno)
        alumno = []

    print()
    print("Estudiante(s) registrado(s) correctamente.")
    print()

    return matriz_estudiantes


def verificacion_legajo(legajo, matriz_estudiantes):

    legajos_existentes = [estudiante[0] for estudiante in matriz_estudiantes]
    
    while legajo <= 0 or legajo in legajos_existentes:
        print("\nEl legajo no es válido o ya se encuentra registrado.")
        legajo = validar_inputs("Ingrese un nuevo legajo: ")
        
    return legajo


def validar_nombre(nombre, matriz_estudiantes):

    # Valida letras y espacios. Dos estudiantes pueden tener el mismo nombre.
    salida = 1
    valido = True

    if len(matriz_estudiantes) == 0:
        while not nombre.replace(" ", "").isalpha():
            print()
            nombre = input(
                "El nombre no es válido. Ingrese nuevamente el nombre: "
            )

        return nombre.strip()

    else:
        while salida != 0:
            valido = True

            for i in range(len(matriz_estudiantes)):

                if not nombre.replace(" ", "").isalpha():
                    print()
                    nombre = input(
                        "El nombre no es válido. Ingrese nuevamente el nombre: "
                    )
                    valido = False

            if valido == True:
                salida = 0

    return nombre.strip()


def buscar_estudiantes(matriz_estudiantes):

    # Busca un alumno por legajo o nombre
    generar_titulo_de_todos("BUSCAR ESTUDIANTE")

    opcion = 0
    alumnos = []

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay alumnos cargados.")
        print()
        return matriz_estudiantes

    else:
        print()
        print("¿De qué forma desea buscar al alumno?")
        print()
        print("  1. Por nombre")
        print("  2. Por legajo")
        print("  0. Volver")

        opcion = validar_inputs("\nSeleccione una opción: ")

        while opcion != 0 and opcion != 1 and opcion != 2:
            print()
            print("Opción inválida. Intente nuevamente.")
            print()
            print("¿De qué forma desea buscar al alumno?")
            print()
            print("  1. Por nombre")
            print("  2. Por legajo")
            print("  0. Volver")

            opcion = validar_inputs("\nSeleccione una opción: ")

        if opcion == 0:
            return

        if opcion == 1:
            print()
            nombre = input("Ingrese el nombre o apellido del alumno (0 para volver): ").strip()

            if nombre == "0":
                return

            alumnos = buscar_nombre(matriz_estudiantes, nombre)

            while len(alumnos) == 0:
                print()
                print("No se encontró ningún alumno.")
                print("Intente nuevamente.")

                print()
                nombre = input("Ingrese el nombre o apellido del alumno (0 para volver): ").strip()

                if nombre == "0":
                    return

                alumnos = buscar_nombre(matriz_estudiantes, nombre)

            print()
            print("-" * 50)
            print("{:<8}   {:<20}".format(
                "Legajo", "Nombre"
            ))
            print("-" * 50)

            for i in alumnos:
                print("{:<8}   {:<20}".format(
                    matriz_estudiantes[i][0],
                    matriz_estudiantes[i][1],
                ))

            print("-" * 50)

        elif opcion == 2:

            while len(alumnos) == 0:
                print()
                legajo = validar_inputs("Ingrese el legajo del alumno (0 para volver): ")

                if legajo == 0:
                    return

                alumnos = buscar_legajo(matriz_estudiantes, legajo)

                if len(alumnos) == 0:
                    print()
                    print("Legajo no encontrado. Intente nuevamente.")

                else:
                    print()
                    print("-" * 50)
                    print("{:<8}   {:<20}".format(
                        "Legajo", "Nombre"
                    ))
                    print("-" * 50)

                    print("{:<8}   {:<20}".format(
                        alumnos[0],
                        alumnos[1]
                    ))

                    print("-" * 50)

    return


def buscar_legajo(matriz, legajo):

    alumnos = []

    for i in range(len(matriz)):

        if matriz[i][0] == legajo:
            alumnos.append(matriz[i][0])
            alumnos.append(matriz[i][1])

    return alumnos


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


def modificar_nombre_estudiantes(matriz_estudiantes):

    # Permite modificar el nombre de un alumno
    generar_titulo_de_todos("MODIFICAR NOMBRE ESTUDIANTE")

    buscar = 0
    opcion = 0
    encontrado = 0
    alumno=[]

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay alumnos cargados.")
        print()
        return matriz_estudiantes

    else:
        print()
        buscar = validar_inputs("Ingrese el legajo del alumno (0 para volver): ")

        if buscar == 0:
            return matriz_estudiantes

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0] == buscar:
                encontrado = 1

                while opcion != 1:

                    print()
                    print("Opciones a modificar:")
                    print()
                    print("  1. Nombre")
                    print("  0. Volver")

                    opcion = validar_inputs("\nSeleccione una opción: ")

                    if opcion == 0:
                        return matriz_estudiantes

                    if opcion == 1:
                        print()
                        nombre = input("Ingrese el nombre del alumno: ")

                        matriz_estudiantes[i][1] = validar_nombre(
                            nombre,
                            matriz_estudiantes
                        )

                    if opcion == 1:
                        
                        print()
                        print("Registro del alumno modificado correctamente.")
                        
                        alumno.append(matriz_estudiantes[i])
                        imprimir_la_matriz(alumno)
                        
                        print("-" * 50)

                    else:
                        print()
                        print("Opción inválida. Intente nuevamente.")

        if encontrado == 0:
            print()
            print("El legajo no existe o no es válido.")
            print()

    return matriz_estudiantes


def mostrar_estudiantes(matriz_estudiantes):

    # Muestra por pantalla el listado completo de alumnos cargados
    generar_titulo_de_todos("LISTADO DE ESTUDIANTES")

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay estudiantes registrados.")
        print()
        return

    else:
        
        imprimir_la_matriz(matriz_estudiantes)
        
        print("-" * 50)
        print()


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

    for i in range(len(matriz_estudiantes)):
        print("{:<8}   {:<20}".format(
            matriz_estudiantes[i][0],
            matriz_estudiantes[i][1]
        ))


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
                        grupo = cursadas[materia][nombre_grupo]
                        menu_inscripciones(matriz_estudiantes, grupo)

        else:
            print()
            print("Opción inválida. Intente nuevamente.")

    return matriz_estudiantes
