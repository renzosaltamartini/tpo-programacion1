# =========================================
# SISTEMA DE REGISTRO DE ASISTENCIA
# LECTURA Y GUARDADO DE ARCHIVOS
# =========================================

import json
import os


CARPETA = "archivos"
PADRON = "archivos/matriz_alumnos.txt"
CURSADAS = "archivos/cursadas.jsonl"


# =========================================
# FUNCIONES AUXILIARES
# =========================================


def cerrar_archivo(archivo):

    if archivo != None:
        archivo.close()


def leer_registro(archivo):

    # Se devuelve una sola linea convertida a diccionario, no todo el archivo.
    linea = archivo.readline()

    while linea != "" and len(linea.strip()) == 0:
        linea = archivo.readline()

    registro = None

    if linea != "":
        registro = json.loads(linea)
        if "tipo" not in registro:
            raise ValueError("El registro JSONL no contiene el campo tipo.")

    return registro


def linea_json(registro):

    return json.dumps(registro, ensure_ascii=False) + "\n"


# =========================================
# ARCHIVO DE ESTUDIANTES
# =========================================


def leer_estudiante(archivo):
    #lee una sola linea de el archivo, fijandose el final
    linea = archivo.readline()

    while linea != "" and len(linea.strip()) == 0:
        linea = archivo.readline()

    estudiante = None

    if linea != "":
        estudiante = separar_estudiante(linea)

    return estudiante


def separar_estudiante(linea):
    #pasa a una lista los datos de el archivo
    datos = linea.strip().split(",")

    if len(datos) != 2 and len(datos) != 3:
        raise ValueError("Cantidad de campos incorrecta en el padron.")

    legajo = int(datos[0])
    nombre = datos[1].strip()

    if legajo <= 0 or not nombre.replace(" ", "").isalpha():
        raise ValueError("El legajo o el nombre no es valido.")

    # Se admite el estado del formato antiguo, sin modificar su archivo.
    if len(datos) == 3:
        if datos[2].strip() not in ["Activo", "Inactivo"]:
            raise ValueError("El estado antiguo no es valido.")

    estudiante = [legajo, nombre]
    return estudiante


def buscar_estudiante(legajo, ruta_padron=PADRON):

    archivo = None
    encontrado = []

    try:
        archivo = open(ruta_padron, "r", encoding="utf-8-sig")
        estudiante = leer_estudiante(archivo)

        while estudiante != None and len(encontrado) == 0:
            if estudiante[0] == legajo:
                encontrado = estudiante
            else:
                estudiante = leer_estudiante(archivo)

    finally:
        cerrar_archivo(archivo)

    # no hay except porque esta funcion pasa el codigo de error a la funcion que llamo esta funcon es como que se lo da a la que lo llamo
    return encontrado


def agregar_estudiante(legajo, nombre, ruta_padron=PADRON):
    # esta funcion guarda los datos de los alumnos en el archivo 
    archivo = None
    guardado = False
    repetido = False
    nombre = nombre.strip()

    try:
        if legajo <= 0 or not nombre.replace(" ", "").isalpha():
            raise ValueError("El legajo o el nombre no es valido.")

        # Se revisan los registros y el salto final en un solo recorrido.
        archivo = open(ruta_padron, "r", encoding="utf-8-sig")
        ultima_linea = ""

        for linea in archivo:
            if len(linea.strip()) > 0:
                estudiante = separar_estudiante(linea)
                if estudiante[0] == legajo:
                    repetido = True
            ultima_linea = linea

        if repetido == True:
            raise ValueError("El legajo ya se encuentra registrado.")

        archivo.close()
        archivo = None
        archivo = open(ruta_padron, "a", encoding="utf-8")

        if len(ultima_linea) > 0 and ultima_linea[-1] != "\n":
            archivo.write("\n")

        archivo.write(f"{legajo},{nombre}\n")
        archivo.close()
        archivo = None
        guardado = True

    except (OSError, ValueError, TypeError) as error:
        print("No se pudo registrar el estudiante:", error)

    finally:
        cerrar_archivo(archivo)

    return guardado


def cambiar_nombre_estudiante(legajo, nombre, ruta_padron=PADRON):

    entrada = None
    salida = None
    encontrado = False
    guardado = False
    temporal_creado = False
    temporal = ruta_padron + ".tmp"
    nombre = nombre.strip()

    try:
        if not nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre no es valido.")

        entrada = open(ruta_padron, "r", encoding="utf-8-sig")
        salida = open(temporal, "w", encoding="utf-8")
        temporal_creado = True

        linea = entrada.readline()

        while linea != "":
            if len(linea.strip()) > 0:
                estudiante = separar_estudiante(linea)

                if estudiante[0] == legajo:
                    if encontrado == True:
                        raise ValueError("El legajo esta repetido.")
                    datos = linea.strip().split(",")
                    datos[1] = nombre
                    salida.write(",".join(datos) + "\n")
                    encontrado = True
                else:
                    salida.write(linea)
            else:
                salida.write(linea)

            linea = entrada.readline()

        entrada.close()
        entrada = None

        salida.close()
        salida = None

        if encontrado == True:
            os.replace(temporal, ruta_padron)
            guardado = True

    except (OSError, ValueError, TypeError) as error:
        print("No se pudo modificar el nombre:", error)

    finally:
        try:
            cerrar_archivo(entrada)
        finally:
            cerrar_archivo(salida)

        if temporal_creado == True and guardado == False:
            try:
                os.remove(temporal)
            except OSError:
                pass

    return guardado


# =========================================
# ARCHIVO JSONL DE CURSADAS
# =========================================


def agregar_registro(registro, ruta_cursadas=CURSADAS):

    archivo = None
    guardado = False

    try:
        # Se comprueba la serializacion antes de abrir la salida.
        if "tipo" not in registro:
            raise ValueError("El registro debe contener el campo tipo.")
        linea_nueva = linea_json(registro)

        archivo = open(ruta_cursadas, "r", encoding="utf-8")
        ultima_linea = ""

        for linea in archivo:
            if len(linea.strip()) > 0:
                datos = json.loads(linea)
                if "tipo" not in datos:
                    raise ValueError("Hay un registro sin campo tipo.")
            ultima_linea = linea

        archivo.close()
        archivo = None
        archivo = open(ruta_cursadas, "a", encoding="utf-8")

        if len(ultima_linea) > 0 and ultima_linea[-1] != "\n":
            archivo.write("\n")

        archivo.write(linea_nueva)
        archivo.close()
        archivo = None
        guardado = True

    except (OSError, ValueError, TypeError) as error:
        print("No se pudo agregar el registro:", error)

    finally:
        cerrar_archivo(archivo)

    return guardado


def obtener_grupo(materia, nombre, ruta_cursadas=CURSADAS):

    archivo = None
    grupo = None

    try:
        archivo = open(ruta_cursadas, "r", encoding="utf-8")
        registro = leer_registro(archivo)

        while registro != None and grupo == None:
            if (registro["tipo"] == "grupo"
                    and registro["materia"] == materia
                    and registro["nombre"] == nombre):
                grupo = registro["datos"]
            else:
                registro = leer_registro(archivo)

        if grupo == None:
            raise ValueError("El grupo seleccionado no existe.")

    finally:
        cerrar_archivo(archivo)

    return grupo


def leer_asistencias(materia, nombre, legajo=None, sesion=None,
                     ruta_cursadas=CURSADAS):

    archivo = None
    estados = {}

    try:
        archivo = open(ruta_cursadas, "r", encoding="utf-8")
        registro = leer_registro(archivo)

        while registro != None:
            if (registro["tipo"] == "asistencia"
                    and registro["materia"] == materia
                    and registro["nombre"] == nombre):
                if legajo != None:
                    if registro["legajo"] == legajo and (sesion == None or registro["sesion"] == sesion):
                        estados[registro["sesion"]] = registro["estado"]
                elif registro["sesion"] == sesion:
                    estados[registro["legajo"]] = registro["estado"]

            registro = leer_registro(archivo)

    finally:
        cerrar_archivo(archivo)

    return estados


def guardar_asistencia(materia, nombre, legajo, sesion, estado,
                       ruta_cursadas=CURSADAS):

    registro = {"tipo": "asistencia", "materia": materia, "nombre": nombre,
                "legajo": legajo, "sesion": sesion, "estado": estado}
    if actualizar(materia, nombre, {"estado": estado}, ruta_cursadas,
                  asistencia=registro) == False:
        raise OSError("No se pudo guardar la asistencia.")


def actualizar(materia_actual=None, nombre_actual=None, cambios=None,
               ruta_cursadas=CURSADAS, asistencia=None, convertir=False):

    entrada = None
    salida = None
    encontrado = False
    guardado = False
    temporal_creado = False
    temporal = ruta_cursadas + ".tmp"

    try:
        if convertir == False and (cambios == None or len(cambios) == 0):
            raise ValueError("No se indicaron cambios para guardar.")

        entrada = open(ruta_cursadas, "r", encoding="utf-8")
        salida = open(temporal, "w", encoding="utf-8")
        temporal_creado = True

        registro = leer_registro(entrada)

        while registro != None:
            coincide = False

            if convertir == True:
                # Cada estado registrado de la matriz anterior pasa a su propia linea.
                if registro["tipo"] == "grupo" and "asistencias" in registro["datos"]:
                    grupo = registro["datos"]
                    matriz = grupo.pop("asistencias")
                    salida.write(linea_json(registro))

                    for i in range(len(grupo["inscriptos"])):
                        legajo = grupo["inscriptos"][i][0]
                        for j in range(len(grupo["sesiones"])):
                            estado = matriz[i][j]
                            if estado != "-":
                                nueva = {"tipo": "asistencia",
                                         "materia": registro["materia"],
                                         "nombre": registro["nombre"],
                                         "legajo": legajo,
                                         "sesion": grupo["sesiones"][j][0],
                                         "estado": estado}
                                salida.write(linea_json(nueva))

                    del matriz
                    encontrado = True
                    registro = leer_registro(entrada)
                    continue
            elif asistencia != None:
                coincide = (registro["tipo"] == "asistencia"
                            and registro["materia"] == materia_actual
                            and registro["nombre"] == nombre_actual
                            and registro["legajo"] == asistencia["legajo"]
                            and registro["sesion"] == asistencia["sesion"])
            elif materia_actual == None:
                coincide = registro["tipo"] == "configuracion"
            elif nombre_actual == None:
                coincide = registro.get("materia") == materia_actual
            else:
                coincide = (registro.get("materia") == materia_actual
                            and registro.get("nombre") == nombre_actual
                            and (registro["tipo"] == "grupo"
                                 or (registro["tipo"] == "asistencia" and "nombre" in cambios)))

            if coincide == True:
                for clave in cambios:
                    registro[clave] = cambios[clave]
                encontrado = True

            salida.write(linea_json(registro))
            registro = leer_registro(entrada)

        if asistencia != None and encontrado == False:
            salida.write(linea_json(asistencia))
            encontrado = True

        entrada.close()
        entrada = None

        salida.close()
        salida = None

        if encontrado == True:
            os.replace(temporal, ruta_cursadas)
            guardado = True

    except (OSError, ValueError, TypeError, KeyError) as error:
        print("No se pudieron actualizar los datos:", error)

    finally:
        try:
            cerrar_archivo(entrada)
        finally:
            cerrar_archivo(salida)

        if temporal_creado == True and guardado == False:
            try:
                os.remove(temporal)
            except OSError:
                pass

    return guardado


def guardar_grupo(materia, nombre, grupo, ruta_cursadas=CURSADAS):

    cambios = {"datos": grupo}
    guardado = actualizar(materia, nombre, cambios, ruta_cursadas)

    return guardado
