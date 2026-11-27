# ========================================= 
# SISTEMA DE REGISTRO DE ASISTENCIA 
# GESTION DE MATERIAS, GRUPOS, HORARIOS Y SESIONES 
# ========================================= 

import Archivos

# VALIDACIONES
# ========================================= 


def validar_numero(numero): 
    if len(numero) == 0:
        return False

    validacion = True 

    i = 0

    while i < len(numero):
        if numero[i] < "0" or numero[i] > "9":
            validacion = False 

        i += 1

    return validacion 


def leer_opcion(mensaje, minimo, maximo):
    while True:
        try:
            opcion = int(input(mensaje))

            if minimo <= opcion <= maximo:
                break
            else:
                print("Opcion invalida. Ingrese un numero entre", minimo, "y", maximo)

        except ValueError:
            print("Opcion invalida. Ingrese un numero entero.")

    return opcion


def validar_numero_sesion(numero_sesion, sesiones):
    #Devuelve False si existe, si no existe devuelve True

    existe = False 

    for i in sesiones:
        if i[0] == numero_sesion:
            existe = True 

    return not existe 


def validar_fecha(fecha):
    """
        Valida manualmente el formato DD/MM/AAAA (sin librerias),
        incluyendo que el dia exista de verdad para ese mes y año
        (contempla meses de 30/31 dias y años bisiestos).
        """
    
    validacion = True

    # Verificar longitud
    if len(fecha) != 10:
        validacion = False
    
    else:
        # Verificar separadores
        if fecha[2] != "/" or fecha[5] != "/":
            validacion = False

        else:
            dia = fecha[0:2]
            mes = fecha[3:5]
            año = fecha[6:10]

            # Verificar que dia, mes y año tengan solo numeros
            i = 0
            while i < len(dia):
                if dia[i] < "0" or dia[i] > "9":
                    validacion = False

                i += 1

            i = 0
            while i < len(mes):
                if mes[i] < "0" or mes[i] > "9":
                    validacion = False

                i += 1

            i = 0
            while i < len(año):
                if año[i] < "0" or año[i] > "9":
                    validacion = False

                i += 1

            if validacion:
                dia = int(dia)
                mes = int(mes)
                año = int(año)

                validacion = False

                if año > 0 and 1 <= mes <= 12:

                    if mes == 2:

                        if año % 400 == 0 or (año % 4 == 0 and año % 100 != 0):
                            dias = 29

                        else:
                            dias = 28

                    elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                        dias = 30

                    else:
                        dias = 31

                    if 1 <= dia <= dias:
                        validacion = True

    return validacion


def validar_texto_no_vacio(texto):
    # Valida que un campo de texto (materia, tema) no este vacio.

    if len(texto.strip()) < 1:
        return False

    else:
        return True


def ingresar_texto_no_vacio(mensaje):
    texto = input(mensaje)
    while not validar_texto_no_vacio(texto):
        print("El texto no puede estar vacio.")
        texto = input(mensaje)
    return texto.strip()


def normalizar_nombre(texto):
    # Quita espacios de los extremos y convierte palabras a formato titulo.
    texto = texto.strip()
    palabras = texto.split()
    texto = " ".join(palabras)
    return texto.title()


def pedir_fecha():
    fecha = input("Ingrese la fecha (DD/MM/AAAA): ").strip()
    while not validar_fecha(fecha):
        print("Fecha invalida. Formato esperado: DD/MM/AAAA.")
        fecha = input("Ingrese la fecha nuevamente: ").strip()
    return fecha


# =========================================
# MATERIAS
# =========================================


def crear_materia(cursadas):
    print("\n--- Crear materia ---")

    nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nombre de la materia: "))
    
    while nombre in cursadas:
        print("Ya existe una materia con ese nombre.")
        nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese otro nombre: "))

    guardado = Archivos.agregar_registro({"tipo": "materia", "materia": nombre})

    if guardado == True:
        cursadas[nombre] = {}
        print("Materia creada correctamente.")
    else:
        print("La materia no se guardo.")

    return cursadas
    
    
def listar_materias(cursadas):
    print("\n--- Listado de materias ---")

    if len(cursadas) == 0:
        print("No hay materias cargadas")

    else:
        i = 1

        for materia in cursadas:
            print(i, "-", materia)

            i += 1
    

def seleccionar_materia(cursadas):
    if len(cursadas) == 0:
        print("No hay materias cargadas.")
        return None

    materias = []

    for materia in cursadas:
        materias.append(materia)

    print("\n--- Seleccionar materia ---")
    for i in range(len(materias)):
        print(i + 1, "-", materias[i])
    
    opcion = leer_opcion("Seleccione una materia (0 para cancelar): ", 0, len(materias))
    
    if opcion == 0:
        return None
    return materias[opcion - 1]


def modificar_materia(cursadas):
    materia = seleccionar_materia(cursadas)
    
    if materia == None:
        return cursadas

    nuevo_nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nuevo nombre: "))

    if nuevo_nombre != materia and nuevo_nombre in cursadas:
        print("Ya existe una materia con ese nombre.")
    elif nuevo_nombre != materia:
        cambios = {"materia": nuevo_nombre}
        guardado = Archivos.actualizar(materia, None, cambios)
        if guardado == True:
            grupos = cursadas[materia]
            del cursadas[materia]
            cursadas[nuevo_nombre] = grupos
            print("Materia modificada. Se conservaron sus grupos y datos.")
        else:
            print("El cambio de materia no se guardo.")
    else:
        print("El nombre no cambio.")

    return cursadas


# =========================================
# GRUPOS, HORARIOS E INSTITUCIONES
# =========================================


def validar_dia():
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    dia = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el día: "))

    while dia not in dias and dia != "Miércoles" and dia != "Sábado":
        print("Dia invalido.")
        dia = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el día: "))

    if dia == "Miércoles":
        dia = "Miercoles"

    elif dia == "Sábado":
        dia = "Sabado"

    return dia


def validar_turno():
    turnos = ["Mañana", "Tarde", "Noche"]

    turno = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el turno: "))

    while turno not in turnos:
        print("Turno invalido")
        turno = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el turno: "))

    return turno


def registrar_horarios():
    horarios = {}
    respuesta = "S"

    while respuesta == "S":
        dia = validar_dia()
        turno = validar_turno()
        horarios[dia] = turno

        respuesta = input("Desea ingresar un horario? (S/N): ").strip().upper()

        while respuesta.strip().upper() != "S" and respuesta.strip().upper() != "N":
            print("Responda S o N")
            respuesta = input("Desea ingresar un horario? (S/N): ").strip().upper()

    return horarios


def seleccionar_institucion_predeterminada(configuracion):
    institucion = configuracion["institucion_predeterminada"]
    print("Institucion sugerida:", institucion)
    respuesta = input("Desea usar esta institucion? (s/n): ")

    while respuesta.strip().upper() != "S" and respuesta.strip().upper() != "N":
        print("Responda S o N")
        respuesta = input("Desea usar esta institucion? (s/n): ")

    if respuesta.strip().upper() == "S":
        return institucion

    return ingresar_texto_no_vacio("Ingrese la institución: ")


def crear_grupo(cursadas, configuracion, materia=None):
    if materia == None:
        materia = seleccionar_materia(cursadas)

    if materia == None:
        return cursadas

    grupos = cursadas[materia]

    nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nombre del grupo: "))
    while nombre in grupos:
        print("Ya existe un grupo con ese nombre en esta materia.")
        nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese otro nombre: "))

    institucion = seleccionar_institucion_predeterminada(configuracion)

    print("Registe los horarios del grupo")
    horarios = registrar_horarios()

    grupo = {
        "institucion": institucion,
        "horarios": horarios,
        "inscriptos": [],
        "sesiones": []
    }
    registro = {"tipo": "grupo", "materia": materia, "nombre": nombre, "datos": grupo}
    guardado = Archivos.agregar_registro(registro)
    if guardado == True:
        grupos[nombre] = institucion
        print("Grupo creado correctamente")
    else:
        print("El grupo no se guardo.")

    return cursadas


def listar_grupos(cursadas, materia):
    grupos = cursadas[materia]
    print("\n--- Grupos de", materia, "---")

    if len(grupos) == 0:
        print("Esta materia no tiene grupos.")
        return

    for nombre in grupos:
            grupo = Archivos.obtener_grupo(materia, nombre)
            print("\nGrupo:", nombre)
            print("Institucion:", grupo["institucion"])
    
            if len(grupo["horarios"]) == 0:
                print("Horarios: sin registrar")
            else:
                for dia in grupo["horarios"]:
                    print(dia, "-", grupo["horarios"][dia])
    
            print("Inscriptos:", len(grupo["inscriptos"]))
            print("Sesiones:", len(grupo["sesiones"]))


def seleccionar_grupo(cursadas, materia):
    grupos = cursadas[materia]

    if len(grupos) == 0:
        print("Esta materia no tiene grupos.")
        return None

    nombres = []
    for nombre in grupos:
        nombres.append(nombre)

    print("\n--- Seleccionar grupo ---")
    for i in range(len(nombres)):
        print(i + 1, "-", nombres[i], "| Institucion:", grupos[nombres[i]])

    opcion = leer_opcion("Seleccione un grupo (0 para cancelar): ", 0, len(nombres))

    if opcion == 0:
        return None
    return nombres[opcion - 1]


def modificar_grupo(cursadas, materia=None):
    if materia == None:
        materia = seleccionar_materia(cursadas)

    if materia == None:
        return cursadas

    nombre = seleccionar_grupo(cursadas, materia)
    if nombre == None:
        return cursadas

    grupo = Archivos.obtener_grupo(materia, nombre)

    print("\n1. Cambiar nombre")
    print("2. Cambiar institucion")
    print("3. Cambiar horarios")
    print("0. Volver")
    opcion = leer_opcion("Seleccione una opcion: ", 0, 3)

    if opcion == 1:
        nuevo_nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nuevo nombre del grupo: "))
        if nuevo_nombre != nombre and nuevo_nombre in cursadas[materia]:
            print("Ya existe un grupo con ese nombre.")
        elif nuevo_nombre != nombre:
            cambios = {"nombre": nuevo_nombre}
            guardado = Archivos.actualizar(materia, nombre, cambios)
            if guardado == True:
                cursadas[materia][nuevo_nombre] = grupo["institucion"]
                del cursadas[materia][nombre]
                print("Grupo modificado. Se conservaron sus datos.")
            else:
                print("El cambio de nombre del grupo no se guardo.")

    elif opcion == 2:
        grupo["institucion"] = ingresar_texto_no_vacio("Ingrese la nueva institucion: ")
        guardado = Archivos.guardar_grupo(materia, nombre, grupo)
        if guardado == True:
            cursadas[materia][nombre] = grupo["institucion"]
            print("Institucion modificada.")
        else:
            print("El cambio de institucion no se guardo.")

    elif opcion == 3:
        grupo["horarios"] = registrar_horarios()
        guardado = Archivos.guardar_grupo(materia, nombre, grupo)
        if guardado == True:
            print("Horarios modificados.")
        else:
            print("El cambio de horarios no se guardo.")

    return cursadas


def cambiar_institucion_predeterminada(configuracion):
    institucion = ingresar_texto_no_vacio(
        "Ingrese la nueva institucion predeterminada: "
    )
    cambios = {"datos": {"institucion_predeterminada": institucion}}
    guardado = Archivos.actualizar(None, None, cambios)
    if guardado == True:
        configuracion["institucion_predeterminada"] = institucion
        print("La institucion predeterminada se usara como sugerencia para grupos nuevos.")
    else:
        print("La configuracion no se guardo.")


# =========================================
# SESIONES Y MATRIZ DE ASISTENCIAS
# =========================================


def crear_sesion(sesiones):

    print("\n--- Crear nueva sesion ---")

    numero_sesion = input("Ingrese el numero de sesion: ")

    while not validar_numero(numero_sesion) or int(numero_sesion) <= 0:
        print("El numero de sesion debe ser un numero mayor a 0.")
        numero_sesion = input("Ingrese el numero de sesion: ")

    numero_sesion = int(numero_sesion)

    while not validar_numero_sesion(numero_sesion, sesiones):
        print("Ese numero de sesion ya existe.")
        numero_ingresado = input("Ingrese un numero de sesion distinto: ")

        while not validar_numero(numero_ingresado) or int(numero_ingresado) <= 0:
            print("El numero de sesion debe ser un numero mayor a 0.")
            numero_ingresado = input("Ingrese el numero de sesion: ")

        numero_sesion = int(numero_ingresado)

    fecha = pedir_fecha()

    tema = ingresar_texto_no_vacio("Ingrese el tema: ")

    # Se arma la nueva sesion y se agrega a la lista de sesiones
    nueva_sesion = [numero_sesion, fecha, tema]

    sesiones.append(nueva_sesion)


def listar_sesiones(sesiones):

    # Muestra todas las sesiones registradas.
    print("\n--- Listado de sesiones ---")

    if len(sesiones) == 0:
        print("No hay sesiones cargadas todavia.")
        return

    for i in range(len(sesiones)):
        print("Numero de sesion:", sesiones[i][0],
              "Fecha:", sesiones[i][1],
              "Tema:", sesiones[i][2])


def buscar_sesion(sesiones, numero_sesion):

    # Busca una sesion por numero de sesion, recorriendo la matriz.
    encontrado = False

    for i in range(len(sesiones)):

        if sesiones[i][0] == numero_sesion:
            encontrado = True

            print("Sesion encontrada:")
            print("Numero de sesion:", sesiones[i][0])
            print("Fecha:", sesiones[i][1])
            print("Tema:", sesiones[i][2])
            return sesiones[i]

    if not encontrado:
        print("No se encontro ninguna sesion con ese numero")

    return None


def menu_sesiones(sesiones):

    opcion = -1

    while opcion != 0:

        print("\n=========================================")
        print("        GESTION DE SESIONES")
        print("=========================================")
        print("1. Crear sesion")
        print("2. Listar sesiones")
        print("3. Buscar sesion")
        print("0. Volver al menu principal")
        print("=========================================")

        opcion = leer_opcion("Seleccione una opcion: ", 0, 3)

        if opcion == 1:
            crear_sesion(sesiones)

        elif opcion == 2:
            listar_sesiones(sesiones)

        elif opcion == 3:
            if len(sesiones) == 0:
                print("No hay sesiones cargadas.")
                continue

            print("Ingrese 0 para volver.")
            numero_sesion = input("Ingrese el numero de sesion: ")

            while not validar_numero(numero_sesion):
                print("El numero de sesion debe contener solo numeros.")
                numero_sesion = input("Ingrese el numero de sesion: ")

            numero_sesion = int(numero_sesion)

            if numero_sesion != 0:
                buscar_sesion(sesiones, numero_sesion)

        elif opcion == 0:
            print("Volviendo al menu principal")

        else:
            print("Opcion invalida. Intentelo de nuevo")

    return sesiones


# =========================================
# RECURSIVIDAD
# =========================================


def contar_sesiones_recursivo(sesiones, posicion=0):
    # Cuenta las sesiones sin modificar la lista.

    if posicion >= len(sesiones):
        return 0
    
    return 1 + contar_sesiones_recursivo(sesiones, posicion + 1)


# =========================================
# MENU DE MATERIAS Y GRUPOS
# =========================================

def menu_materias_grupos(cursadas, configuracion):
    opcion = -1

    while opcion != 0:
        print("\n=========================================")
        print("       GESTION DE MATERIAS Y GRUPOS")
        print("=========================================")
        print("1. Crear materia")
        print("2. Listar materias")
        print("3. Modificar materia")
        print("4. Crear grupo")
        print("5. Listar grupos")
        print("6. Modificar grupo")
        print("7. Gestionar sesiones de un grupo")
        print("8. Cambiar institucion predeterminada")
        print("0. Volver al menu principal")
        print("=========================================")

        opcion = leer_opcion("Seleccione una opcion: ", 0, 8)

        if opcion == 1:
            crear_materia(cursadas)

        elif opcion == 2:
            listar_materias(cursadas)

        elif opcion == 3:
            modificar_materia(cursadas)

        elif opcion == 4:
            crear_grupo(cursadas, configuracion)

        elif opcion == 5:
            materia = seleccionar_materia(cursadas)
            if materia != None:
                listar_grupos(cursadas, materia)

        elif opcion == 6:
            modificar_grupo(cursadas)

        elif opcion == 7:
            materia = seleccionar_materia(cursadas)

            if materia != None:
                nombre_grupo = seleccionar_grupo(cursadas, materia)

                if nombre_grupo != None:
                    grupo = Archivos.obtener_grupo(materia, nombre_grupo)
                    menu_sesiones(grupo["sesiones"])
                    guardado = Archivos.guardar_grupo(materia, nombre_grupo, grupo)
                    if guardado == True:
                        print("Cantidad de sesiones:", contar_sesiones_recursivo(grupo["sesiones"]))
                    else:
                        raise OSError("No se pudieron guardar las sesiones del grupo.")

        elif opcion == 8:
            cambiar_institucion_predeterminada(configuracion)
        
        
        elif opcion == 0:
            print("Volviendo al menu principal.")

    return cursadas, configuracion
