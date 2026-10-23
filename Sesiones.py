# ========================================= 
# SISTEMA DE REGISTRO DE ASISTENCIA 
# GESTION DE MATERIAS, GRUPOS, HORARIOS Y SESIONES 
# ========================================= 

import json


ARCHIVO_DATOS = "archivos\\cursadas.json"


# =========================================
# VALIDACIONES
# ========================================= 


def validar_numero(numero): 
    if len(numero) == 0:
        return False

    i = 0

    while i < len(numero):
        if numero[i] < "0" or numero[i] > "9":
            return False 

        i += 1

    return True


def leer_opcion(mensaje, minimo, maximo):
    while True:
        try:
            opcion = int(input(mensaje))

            if minimo <= opcion <= maximo:
                return opcion
            else:
                print("Opcion invalida. Ingrese un numero entre", minimo, "y", maximo)

        except ValueError:
            print("Opcion invalida. Ingrese un numero entero.")


def validar_numero_sesion(numero_sesion, sesiones):
    #Devuelve False si existe, si no existe devuelve True

    for i in sesiones:
        if i[0] == numero_sesion:
            return False 

    return True


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
    fecha = input("Ingrese la fecha (DD/MM/AAAA): ")
    while not validar_fecha(fecha):
        print("Fecha invalida. Formato esperado: DD/MM/AAAA.")
        fecha = input("Ingrese la fecha nuevamente: ")
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

    cursadas[nombre] = {}

    print("Materia creada correctamente.")

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

    print("\\n--- Seleccionar materia ---")
    for i in range(len(materias)):
        print(i + 1, "-", materias[i])
    
    opcion = leer_opcion("Seleccione una materia (0 para cancelar): ", 0, len(materias))
    
    if opcion == 0:
        return None
    return materias[opcion - 1]


def modificar_materia(cursadas):
    materia = seleccionar_materia(cursadas)
    
    if materia is None:
        return cursadas

    nuevo_nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nuevo nombre: "))

    if nuevo_nombre != materia and nuevo_nombre in cursadas:
        print("Ya existe una materia con ese nombre.")
    elif nuevo_nombre != materia:
        grupos = cursadas[materia]
        del cursadas[materia]
        cursadas[nuevo_nombre] = grupos
        print("Materia modificada. Se conservaron sus grupos y datos.")
    else:
        print("El nombre no cambio.")

    return cursadas


# =========================================
# GRUPOS, HORARIOS E INSTITUCIONES
# =========================================


def validar_dia():
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    dia = normalizar_nombre(ingresar_texto_no_vacio("Ingrese la fecha: "))

    while dia not in dias and dia != "Miércoles" and dia != "Sábado":
        print("Dia invalido.")
        dia = normalizar_nombre(ingresar_texto_no_vacio("Ingrese la fecha: "))

    if dia == "Miércoles":
        dia = "Miercoles"

    elif dia == "Sábado":
        dia = "Sabado"

    return dia


def validar_turno():
    turnos = ["Mañana", "Tarde", "Noche"]

    turno = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el turno"))

    while turno not in turnos:
        print("Turno invalido")
        turno = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el turno"))

    return turno


def registrar_horarios():
    horarios = {}
    respuesta = "S"

    while respuesta == "S":
        dia = validar_dia()
        turno = validar_turno()
        horarios[dia] = turno

        respuesta = input("Desea ingresar un usuario? (S/N)")

        while respuesta.strip().upper() != "S" and respuesta.strip().upper() != "N":
            print("Responda S o N")
            respuesta = input("Desea ingresar un usuario? (S/N)")

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
    if materia is None:
        materia = seleccionar_materia(cursadas)

    if materia is None:
        return cursadas

    grupos = cursadas[materia]

    nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nombre del grupo: "))
    while nombre in grupos:
        print("Ya existe un grupo con ese nombre en esta materia.")
        nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese otro nombre: "))

    institucion = seleccionar_institucion_predeterminada(configuracion)

    print("Registe los horarios del grupo")
    horarios = registrar_horarios()

    grupos[nombre] = {
        "institucion": institucion,
            "horarios": horarios,
            "inscriptos": [],
            "sesiones": [],
            "asistencias": []
    }
    print("Grupo creado correctamente")

    return cursadas


def listar_grupos(cursadas, materia):
    grupos = cursadas[materia]
    print("\\n--- Grupos de", materia, "---")

    if len(grupos) == 0:
        print("Esta materia no tiene grupos.")
        return

    for nombre in grupos:
            grupo = grupos[nombre]
            print("\\nGrupo:", nombre)
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

    print("\\n--- Seleccionar grupo ---")
    for i in range(len(nombres)):
        grupo = grupos[nombres[i]]
        print(i + 1, "-", nombres[i], "| Institucion:", grupo["institucion"])

    opcion = leer_opcion("Seleccione un grupo (0 para cancelar): ", 0, len(nombres))

    if opcion == 0:
        return None
    return nombres[opcion - 1]


def modificar_grupo(cursadas, materia=None):
    if materia is None:
        materia = seleccionar_materia(cursadas)

    if materia is None:
        return cursadas

    nombre = seleccionar_grupo(cursadas, materia)
    if nombre is None:
        return cursadas

    grupo = cursadas[materia][nombre]

    print("\\n1. Cambiar nombre")
    print("2. Cambiar institucion")
    print("3. Cambiar horarios")
    print("0. Volver")
    opcion = leer_opcion("Seleccione una opcion: ", 0, 3)

    if opcion == 1:
        nuevo_nombre = normalizar_nombre(ingresar_texto_no_vacio("Ingrese el nuevo nombre del grupo: "))
        if nuevo_nombre != nombre and nuevo_nombre in cursadas[materia]:
            print("Ya existe un grupo con ese nombre.")
        elif nuevo_nombre != nombre:
            cursadas[materia][nuevo_nombre] = grupo
            del cursadas[materia][nombre]
            print("Grupo modificado. Se conservaron sus datos.")

    elif opcion == 2:
        grupo["institucion"] = ingresar_texto_no_vacio("Ingrese la nueva institucion: ")
        print("Institucion modificada.")

    elif opcion == 3:
        grupo["horarios"] = registrar_horarios()
        print("Horarios modificados.")

    return cursadas


def cambiar_institucion_predeterminada(configuracion):
    configuracion["institucion_predeterminada"] = ingresar_texto_no_vacio(
        "Ingrese la nueva institucion predeterminada: "
    )
    print("La institucion predeterminada se usara como sugerencia para grupos nuevos.")


# =========================================
# SESIONES Y MATRIZ DE ASISTENCIAS
# =========================================


def agregar_columna_asistencia(asistencias):
    # Agrega una columna nueva (la nueva sesion) a cada fila existente.
    for i in range(len(asistencias)):
        asistencias[i].append("-")


def agregar_fila_asistencia(asistencias, cantidad_sesiones):
    # Agrega una fila nueva (nuevo estudiante),
    # con una columna por cada sesion existente.

    fila_nueva = []

    for i in range(cantidad_sesiones):
        fila_nueva.append("-")

    asistencias.append(fila_nueva)


def verificar_dimensiones_matriz(asistencias, sesiones):

    ok = True

    for i in range(len(asistencias)):

        if len(asistencias[i]) != len(sesiones):
            print("Aviso: una fila de asistencias no tiene la cantidad correcta de columnas.")
            ok = False

    return ok

def crear_sesion(sesiones, asistencias):

    print("\n--- Crear nueva sesion ---")

    numero_sesion = input("Ingrese el numero de sesion: ")

    while not validar_numero(numero_sesion) or int(numero_sesion) <= 0:
        print("El numero de sesion debe ser un numero mayor a 0.")
        numero_sesion = input("Ingrese el numero de sesion: ")

    numero_sesion = int(numero_sesion)

    while not validar_numero_sesion(numero_sesion, sesiones):
        print("Ese numero de sesion ya existe.")
        numero_sesion = input("Ingrese un numero de sesion distinto: ")

        while not validar_numero(numero_sesion) or int(numero_sesion) <= 0:
            print("El numero de sesion debe ser un numero mayor a 0.")
            numero_sesion = input("Ingrese el numero de sesion: ")

        numero_sesion = int(numero_sesion)

    fecha = input("Ingrese la fecha (DD/MM/AAAA): ")

    while not validar_fecha(fecha):
        print("Fecha invalida. Formato esperado: DD/MM/AAAA.")
        fecha = input("Ingrese la fecha nuevamente: ")

    tema = input("Ingrese el tema: ")

    while not validar_texto_no_vacio(tema):
        print("El tema no puede estar vacio.")
        tema = input("Ingrese el tema nuevamente: ")

    # Se arma la nueva sesion y se agrega a la lista de sesiones
    nueva_sesion = [numero_sesion, fecha, tema]

    sesiones.append(nueva_sesion)

    # Cada sesion nueva agrega una columna a la matriz de asistencias
    agregar_columna_asistencia(asistencias)

    # Chequeo de que la matriz sigue teniendo las dimensiones correctas
    verificar_dimensiones_matriz(asistencias, sesiones)

    return asistencias, sesiones


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

    if encontrado == False:
        print("No se encontro ninguna sesion con ese numero")


def menu_sesiones(sesiones, asistencias):

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

        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            asistencias,sesiones = crear_sesion(sesiones, asistencias)

        elif opcion == 2:
            listar_sesiones(sesiones)

        elif opcion == 3:
            numero_sesion = input("Ingrese el numero de sesion: ")

            while not validar_numero(numero_sesion):
                print("El numero de sesion debe contener solo numeros.")
                numero_sesion = input("Ingrese el numero de sesion: ")

            numero_sesion = int(numero_sesion)

            buscar_sesion(sesiones, numero_sesion)

        elif opcion == 0:
            print("Volviendo al menu principal")

        else:
            print("Opcion invalida. Intentelo de nuevo")

    return sesiones, asistencias


# =========================================
# RECURSIVIDAD
# =========================================


def contar_sesiones_recursivo(sesiones, posicion=0):
    # Cuenta las sesiones sin modificar la lista.

    if posicion >= len(sesiones):
        return 0
    
    return 1 + contar_sesiones_recursivo(sesiones, posicion + 1)


# =========================================
# ARCHIVOS Y JSON
# La persistencia general se debe coordinar con el integrante responsable.
# =========================================


def guardar_datos(cursadas, configuracion, archivo=ARCHIVO_DATOS):
    arch = None 

    try:
        arch = open(archivo, "w", encoding="utf-8")
        datos = {
            "cursadas": cursadas,
            "configuracion": configuracion
        }
        json.dump(datos, arch, ensure_ascii=False, indent=4)

    except (OSError, TypeError, ValueError) as error:
        print("No se pudieron guardar los datos:", error)
        return False

    else:
        print("Datos guardados correctamente.")
        return True

    finally:
        if arch != None:
            try:
                arch.close()
            except OSError:
                print("No se pudo cerrar correctamente el archivo.")


def cargar_datos(archivo=ARCHIVO_DATOS):
    arch = None

    try:
        arch = open(archivo, "r", encoding="utf-8")
        datos = json.load(arch)

        if "cursadas" not in datos or "configuracion" not in datos:
            raise ValueError("El archivo no contiene las claves necesarias.")

        if not isinstance(datos["cursadas"], dict):
            raise ValueError("La informacion de cursadas no tiene el formato esperado.")

        if not isinstance(datos["configuracion"], dict):
            raise ValueError("La configuracion no tiene el formato esperado.")

    except FileNotFoundError:
        print("Todavia no existe un archivo guardado. Se iniciara sin datos.")
        return {}, {"institucion_predeterminada": "UADE"}

    except json.JSONDecodeError:
        print("El archivo JSON esta vacio o tiene un formato incorrecto.")
        return {}, {"institucion_predeterminada": "UADE"}

    except (OSError, TypeError, ValueError, KeyError) as error:
        print("No se pudieron cargar los datos:", error)
        return {}, {"institucion_predeterminada": "UADE"}

    else:
        cursadas = datos["cursadas"]
        configuracion = datos["configuracion"]

        if "institucion_predeterminada" not in configuracion:
            configuracion["institucion_predeterminada"] = "UADE"

        # Completa claves faltantes de grupos antiguos sin borrar datos.
        for materia in cursadas:
            for nombre_grupo in cursadas[materia]:
                grupo = cursadas[materia][nombre_grupo]
                if "institucion" not in grupo:
                    grupo["institucion"] = configuracion["institucion_predeterminada"]
                if "horarios" not in grupo:
                    grupo["horarios"] = {}
                if "inscriptos" not in grupo:
                    grupo["inscriptos"] = []
                if "sesiones" not in grupo:
                    grupo["sesiones"] = []
                if "asistencias" not in grupo:
                    grupo["asistencias"] = []

        print("Datos recuperados correctamente.")
        return cursadas, configuracion

    finally:
        if arch is not None:
            try:
                arch.close()
            except OSError:
                print("No se pudo cerrar correctamente el archivo.")


# =========================================
# MENU DE MATERIAS Y GRUPOS
# =========================================

def menu_materias_grupos(cursadas, configuracion):
    opcion = -1

    while opcion != 0:
        print("\\n=========================================")
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
        print("9. Guardar datos")
        print("0. Volver al menu principal")
        print("=========================================")

        opcion = leer_opcion("Seleccione una opcion: ", 0, 9)

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
            if materia is not None:
                listar_grupos(cursadas, materia)

        elif opcion == 6:
            modificar_grupo(cursadas)

        elif opcion == 7:
            materia = seleccionar_materia(cursadas)

            if materia is not None:
                nombre_grupo = seleccionar_grupo(cursadas, materia)

                if nombre_grupo is not None:
                    grupo = cursadas[materia][nombre_grupo]
                    grupo["sesiones"], grupo["asistencias"] = menu_sesiones(
                        grupo["sesiones"],
                        grupo["asistencias"],
                        )
                    
                    print("Cantidad de sesiones:", contar_sesiones_recursivo(grupo["sesiones"]))
        
        elif opcion == 8:
            cambiar_institucion_predeterminada(configuracion)
        
        elif opcion == 9:
            guardar_datos(cursadas, configuracion)
        
        elif opcion == 0:
            print("Volviendo al menu principal.")

    return cursadas, configuracion