def registrar_estudiantes(matriz_estudiantes):

    # Permite cargar uno o varios estudiantes nuevos hasta que el usuario decida no continuar
    salida = 3
    alumno = []
    estado = 0
    estado_add = ""

    generar_titulo_de_todos("REGISTRO DE ESTUDIANTE")

    while salida != 1:
        salida = 3

        print()
        print("-" * 50)

        legajo = validar_inputs("Ingrese el legajo del alumno: ")

        # Se valida que el legajo no exista ya y sea un número válido
        alumno.append(verificacion_legajo(legajo, matriz_estudiantes))

        nombre = input("Ingrese el nombre completo del estudiante: ")

        # Se valida que el nombre no esté repetido
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

    # Verifica que el legajo ingresado sea válido y que no esté repetido
    salida = 1
    valido = True

    if len(matriz_estudiantes) == 0:
        if legajo > 0:
            return legajo
        else:
            while legajo<=0:
                legajo=validar_inputs("El legajo no es válido. Ingrese uno nuevo: ")
            return legajo
    else:
        while salida != 0:
            valido = True

            for i in range(len(matriz_estudiantes)):
                if legajo == matriz_estudiantes[i][0] or legajo < 0 or legajo == 0:
                    print()
                    legajo = validar_inputs("El legajo no es válido. Ingrese uno nuevo: ")
                    valido = False

            if valido == True:
                salida = 0
                return legajo


def validar_nombre(nombre, matriz_estudiantes):

    # Verifica que el nombre no esté repetido y que solo contenga letras
    salida = 1
    valido = True

    if len(matriz_estudiantes) == 0:
        while not nombre.replace(" ", "").isalpha():
            print()
            nombre = input(
                "El nombre no es válido. Ingrese nuevamente el nombre: "
            )

        return nombre

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

    return nombre


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

        opcion = validar_inputs("\nSeleccione una opción: ")

        while opcion != 1 and opcion != 2:
            print()
            print("Opción inválida. Intente nuevamente.")
            print()
            print("¿De qué forma desea buscar al alumno?")
            print()
            print("  1. Por nombre")
            print("  2. Por legajo")

            opcion = validar_inputs("\nSeleccione una opción: ")

        if opcion == 1:
            print()
            nombre = input("Ingrese el nombre o apellido del alumno: ")

            alumnos = buscar_nombre(matriz_estudiantes, nombre)

            while len(alumnos) == 0:
                print()
                print("No se encontró ningún alumno.")
                print("Intente nuevamente.")

                print()
                nombre = input("Ingrese el nombre o apellido del alumno: ")

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
                legajo = validar_inputs("Ingrese el legajo del alumno: ")

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

    nombre = nombre.lower()
    nombre = nombre.replace(" ", "")

    for i in range(len(matriz)):

        if nombre in matriz[i][1].lower().replace(" ", ""):
            alumnos.append(i)

    return alumnos


def modificar_nombre_estudiantes(matriz_estudiantes):

    # Permite modificar el nombre o el estado de un alumno
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
        buscar = validar_inputs("Ingrese el legajo del alumno: ")

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0] == buscar:
                encontrado = 1

                while opcion != 1:

                    print()
                    print("Opciones a modificar:")
                    print()
                    print("  1. Nombre")

                    opcion = validar_inputs("\nSeleccione una opción: ")

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


def menu_estudiantes(matriz_estudiantes):

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

        else:
            print()
            print("Opción inválida. Intente nuevamente.")

    return matriz_estudiantes