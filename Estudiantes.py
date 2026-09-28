def registrar_estudiantes(matriz_estudiantes, matriz_sesiones, matriz_asistencias):
    # Permite cargar uno o varios estudiantes nuevos hasta que el usuario decida no continuar
    salida = 3
    alumno = []
    estado = 0
    estado_add = ""

    print()
    print("=" * 50)
    print("              REGISTRO DE ESTUDIANTES")
    print("=" * 50)

    while salida != 1:
        salida = 3
        estado = 0

        print()
        print("-" * 50)

        legajo = int(input("Ingrese el legajo del alumno: "))

        # Se valida que el legajo no exista ya y sea un número válido
        alumno.append(verificacion_legajo(legajo, matriz_estudiantes))

        nombre = input("Ingrese el nombre completo del estudiante: ")

        # Se valida que el nombre no esté repetido
        alumno.append(validar_nombre(nombre, matriz_estudiantes))

        # Se pide el estado del alumno hasta que se ingrese una opción válida
        while estado != 1 and estado != 2:
            print()
            print("Estado del alumno:")
            print("  1. Activo")
            print("  2. Inactivo")

            estado = int(input("Seleccione una opción: "))

            if estado != 1 and estado != 2:
                print()
                print("Opción inválida. Intente nuevamente.")
            else:
                if estado == 1:
                    estado_add = "Activo"
                else:
                    estado_add = "Inactivo"

                alumno.append(estado_add)

        agregar_fila_asistencia(matriz_asistencias, len(matriz_sesiones))

        # Pregunta si se desea seguir cargando más alumnos
        while salida != 1 and salida != 0:
            print()
            print("¿Desea registrar otro estudiante?")
            print("  0. Sí")
            print("  1. No")

            salida = int(input("Seleccione una opción: "))

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

    if len(matriz_estudiantes) == 0 and legajo > 0:
        return legajo
    else:
        while salida != 0:
            valido = True

            for i in range(len(matriz_estudiantes)):
                if legajo in matriz_estudiantes[i] or legajo < 0 or legajo == 0:
                    print()
                    legajo = int(input("El legajo no es válido. Ingrese uno nuevo: "))
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

                if nombre == matriz_estudiantes[i][1]:
                    print()
                    nombre = input(
                        "El nombre ya existe. Ingrese uno diferente: "
                    )
                    valido = False

                elif not nombre.replace(" ", "").isalpha():
                    print()
                    nombre = input(
                        "El nombre no es válido. Ingrese nuevamente el nombre: "
                    )
                    valido = False

            if valido == True:
                salida = 0

    return nombre


def baja_estudiantes(matriz_estudiantes):
    # Cambia el estado del alumno a Inactivo
    print()
    print("=" * 50)
    print("              BAJA DE ESTUDIANTES")
    print("=" * 50)

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay alumnos cargados.")
        print()
        return matriz_estudiantes

    else:
        print()
        modificar = int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0] == modificar:
                matriz_estudiantes[i][2] = "Inactivo"

                print()
                print("Alumno dado de baja correctamente.")
                print()

                return matriz_estudiantes

    print()
    print("El legajo no existe o no es válido.")
    print()

    return matriz_estudiantes


def buscar_estudiantes(matriz_estudiantes):
    # Busca un alumno por legajo o nombre
    print()
    print("=" * 50)
    print("              BUSCAR ESTUDIANTE")
    print("=" * 50)

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

        opcion = int(input("\nSeleccione una opción: "))

        while opcion != 1 and opcion != 2:
            print()
            print("Opción inválida. Intente nuevamente.")
            print()
            print("¿De qué forma desea buscar al alumno?")
            print()
            print("  1. Por nombre")
            print("  2. Por legajo")

            opcion = int(input("\nSeleccione una opción: "))

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
            print("{:<8}   {:<20}   {:<10}".format(
                "Legajo", "Nombre", "Estado"
            ))
            print("-" * 50)

            for i in alumnos:
                print("{:<8}   {:<20}   {:<10}".format(
                    matriz_estudiantes[i][0],
                    matriz_estudiantes[i][1],
                    matriz_estudiantes[i][2]
                ))

            print("-" * 50)

        elif opcion == 2:

            while len(alumnos) == 0:
                print()
                legajo = int(input("Ingrese el legajo del alumno: "))

                alumnos = buscar_legajo(matriz_estudiantes, legajo)

                if len(alumnos) == 0:
                    print()
                    print("Legajo no encontrado. Intente nuevamente.")

                else:
                    print()
                    print("-" * 50)
                    print("{:<8}   {:<20}   {:<10}".format(
                        "Legajo", "Nombre", "Estado"
                    ))
                    print("-" * 50)

                    print("{:<8}   {:<20}   {:<10}".format(
                        alumnos[0],
                        alumnos[1],
                        alumnos[2]
                    ))

                    print("-" * 50)

    return


def buscar_legajo(matriz, legajo):
    alumnos = []

    for i in range(len(matriz)):

        if matriz[i][0] == legajo:
            alumnos.append(matriz[i][0])
            alumnos.append(matriz[i][1])
            alumnos.append(matriz[i][2])

    return alumnos


def buscar_nombre(matriz, nombre):
    alumnos = []

    nombre = nombre.lower()
    nombre = nombre.replace(" ", "")

    for i in range(len(matriz)):

        if nombre in matriz[i][1].lower().replace(" ", ""):
            alumnos.append(i)

    return alumnos


def modificar_estudiantes(matriz_estudiantes):
    # Permite modificar el nombre o el estado de un alumno
    print()
    print("=" * 50)
    print("             MODIFICAR ESTUDIANTE")
    print("=" * 50)

    buscar = 0
    estado = 0
    opcion = 0
    encontrado = 0

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay alumnos cargados.")
        print()
        return matriz_estudiantes

    else:
        print()
        buscar = int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0] == buscar:
                encontrado = 1

                while opcion != 1 and opcion != 2:

                    print()
                    print("Opciones a modificar:")
                    print()
                    print("  1. Nombre")
                    print("  2. Estado")

                    opcion = int(input("\nSeleccione una opción: "))

                    if opcion == 1:
                        print()
                        nombre = input("Ingrese el nombre del alumno: ")

                        matriz_estudiantes[i][1] = validar_nombre(
                            nombre,
                            matriz_estudiantes
                        )

                    elif opcion == 2:
                        print()
                        print("Seleccione el nuevo estado:")
                        print()
                        print("  1. Activo")
                        print("  2. Inactivo")

                        estado = int(input("\nSeleccione una opción: "))

                        while estado != 1 and estado != 2:
                            print()
                            print("Opción inválida. Intente nuevamente.")
                            estado = int(input("Seleccione una opción: "))

                        if estado == 2:
                            estado = "Inactivo"
                        else:
                            estado = "Activo"

                        matriz_estudiantes[i][2] = estado

                    if opcion == 1 or opcion == 2:
                        print()
                        print("Registro del alumno modificado correctamente.")
                        print()
                        print("-" * 50)
                        print("{:<8}   {:<20}   {:<10}".format(
                            "Legajo", "Nombre", "Estado"
                        ))
                        print("-" * 50)

                        print("{:<8}   {:<20}   {:<10}".format(
                            matriz_estudiantes[i][0],
                            matriz_estudiantes[i][1],
                            matriz_estudiantes[i][2]
                        ))

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
    print()
    print("=" * 50)
    print("              LISTADO DE ESTUDIANTES")
    print("=" * 50)

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay estudiantes registrados.")
        print()
        return

    else:
        print()
        print("{:<8}   {:<20}   {:<10}".format(
            "Legajo", "Nombre", "Estado"
        ))
        print("-" * 50)

        for i in range(len(matriz_estudiantes)):
            print("{:<8}   {:<20}   {:<10}".format(
                matriz_estudiantes[i][0],
                matriz_estudiantes[i][1],
                matriz_estudiantes[i][2]
            ))

        print("-" * 50)
        print()


def agregar_fila_asistencia(asistencias, cantidad_sesiones):
    # Agrega una fila nueva para el estudiante

    fila_nueva = []

    for i in range(cantidad_sesiones):
        fila_nueva.append("-")

    asistencias.append(fila_nueva)


def reactivar_alumno(matriz_estudiantes):
    print()
    print("=" * 50)
    print("           REACTIVACIÓN DE ESTUDIANTE")
    print("=" * 50)

    if len(matriz_estudiantes) == 0:
        print()
        print("No hay alumnos cargados.")
        print()
        return matriz_estudiantes

    else:
        print()
        modificar = int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0] == modificar:
                matriz_estudiantes[i][2] = "Activo"

                print()
                print("Alumno reactivado correctamente.")
                print()

                return matriz_estudiantes

    print()
    print("El legajo no existe o no es válido.")
    print()

    return matriz_estudiantes


def menu_estudiantes(matriz_estudiantes, matriz_sesiones, matriz_asistencias):
    # Función principal del menú de estudiantes

    salida = -1
    opcion = 0

    while salida != 0:

        print()
        print("=" * 50)
        print("                 ESTUDIANTES")
        print("=" * 50)
        print()
        print("  1. Registrar estudiantes")
        print("  2. Dar de baja estudiantes")
        print("  3. Buscar estudiantes")
        print("  4. Modificar estudiantes")
        print("  5. Mostrar estudiantes")
        print("  6. Reactivar estudiante")
        print("  7. Volver al menú principal")
        print()

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            matriz_estudiantes = registrar_estudiantes(
                matriz_estudiantes,
                matriz_sesiones,
                matriz_asistencias
            )

        elif opcion == 2:
            matriz_estudiantes = baja_estudiantes(matriz_estudiantes)

        elif opcion == 3:
            buscar_estudiantes(matriz_estudiantes)

        elif opcion == 4:
            matriz_estudiantes = modificar_estudiantes(matriz_estudiantes)

        elif opcion == 5:
            mostrar_estudiantes(matriz_estudiantes)

        elif opcion == 6:
            matriz_estudiantes = reactivar_alumno(matriz_estudiantes)

        elif opcion == 7:
            salida = 0

        else:
            print()
            print("Opción inválida. Intente nuevamente.")

    return matriz_estudiantes, matriz_asistencias
