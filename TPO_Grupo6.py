import Archivos
import Estudiantes
import Asistencias
import Sesiones
import Consultas


def abrir_cursadas(ruta_cursadas):

    # Un JSON antiguo con datos no se convierte ni se sobrescribe.
    archivo = None
    anterior = None

    try:
        try:
            archivo = open(ruta_cursadas, "r", encoding="utf-8")
        except FileNotFoundError:
            try:
                anterior = open("archivos/cursadas.json", "r", encoding="utf-8-sig")
            except FileNotFoundError:
                anterior = None

            if anterior != None:
                linea = anterior.readline()
                while linea != "" and len(linea.strip()) == 0:
                    linea = anterior.readline()
                if linea != "":
                    raise ValueError("Hay datos en cursadas.json. Se requiere convertirlos antes de continuar.")

            archivo = open(ruta_cursadas, "a", encoding="utf-8")
            archivo.close()
            archivo = None

    finally:
        try:
            Archivos.cerrar_archivo(archivo)
        finally:
            Archivos.cerrar_archivo(anterior)


def abrir_archivos(ruta_padron=Archivos.PADRON, ruta_cursadas=Archivos.CURSADAS):

    archivo = None
    legajos_padron = set()
    indice = {}
    configuracion = {"institucion_predeterminada": "UADE"}
    hay_configuracion = False
    hay_matrices = False
    cantidad_registros = 0

    try:
        # El modo a crea el padron si falta y conserva los datos si existe.
        archivo = open(ruta_padron, "a", encoding="utf-8")
        archivo.close()
        archivo = None
        archivo = open(ruta_padron, "r", encoding="utf-8-sig")
        estudiante = Archivos.leer_estudiante(archivo)

        while estudiante != None:
            legajo = estudiante[0]
            if legajo in legajos_padron:
                raise ValueError("Legajo repetido en el padron: " + str(legajo))
            legajos_padron.add(legajo)
            estudiante = Archivos.leer_estudiante(archivo)

        archivo.close()
        archivo = None
        abrir_cursadas(ruta_cursadas)
        archivo = open(ruta_cursadas, "r", encoding="utf-8")
        registro = Archivos.leer_registro(archivo)

        while registro != None:
            cantidad_registros += 1
            tipo = registro["tipo"]

            if tipo == "configuracion":
                if hay_configuracion == True:
                    raise ValueError("La configuracion esta repetida.")
                configuracion = registro["datos"]
                institucion = configuracion["institucion_predeterminada"]
                if len(institucion.strip()) == 0:
                    raise ValueError("La institucion predeterminada no es valida.")
                hay_configuracion = True

            elif tipo == "materia":
                materia = registro["materia"]
                if len(materia.strip()) == 0 or materia in indice:
                    raise ValueError("La materia no es valida o esta repetida.")
                indice[materia] = {}

            elif tipo == "grupo":
                materia = registro["materia"]
                nombre = registro["nombre"]
                grupo = registro["datos"]
                if materia not in indice or nombre in indice[materia]:
                    raise ValueError("El grupo esta repetido o su materia no existe.")
                validar_grupo(nombre, grupo, legajos_padron)
                if "asistencias" in grupo:
                    hay_matrices = True
                indice[materia][nombre] = grupo["institucion"]

            elif tipo == "asistencia":
                materia = registro["materia"]
                nombre = registro["nombre"]
                if materia not in indice or nombre not in indice[materia]:
                    raise ValueError("La asistencia no pertenece a un grupo existente.")
                if (registro["legajo"] not in legajos_padron
                        or registro["sesion"] <= 0
                        or registro["sesion"] != int(registro["sesion"])
                        or registro["estado"] not in ["P", "A", "T", "J"]):
                    raise ValueError("Hay un registro de asistencia inválido.")

            else:
                raise ValueError("Tipo de registro desconocido.")

            registro = Archivos.leer_registro(archivo)

    finally:
        Archivos.cerrar_archivo(archivo)

    # Un archivo vacio es un primer inicio. Un archivo con datos pero sin
    # configuracion se informa como error, en lugar de completarlo a ciegas.
    if cantidad_registros == 0:
        registro = {"tipo": "configuracion", "datos": configuracion}
        guardado = Archivos.agregar_registro(registro, ruta_cursadas)
        if guardado == False:
            raise OSError("No se pudo guardar la configuracion inicial.")
    elif hay_configuracion == False:
        raise ValueError("Falta la configuracion de cursadas.")

    if hay_matrices == True:
        if Archivos.actualizar(ruta_cursadas=ruta_cursadas, convertir=True) == False:
            raise OSError("No se pudieron convertir las asistencias guardadas.")

    return ruta_padron, indice, configuracion


def validar_grupo(nombre_grupo, grupo, legajos_padron):

    if len(nombre_grupo.strip()) == 0:
        raise ValueError("El nombre del grupo esta vacio.")

    for clave in ["institucion", "horarios", "inscriptos", "sesiones"]:
        if clave not in grupo:
            raise ValueError("Falta " + clave + " en el grupo " + nombre_grupo)

    if len(grupo["institucion"].strip()) == 0:
        raise ValueError("La institucion del grupo esta vacia.")

    for dia in grupo["horarios"]:
        if (dia not in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
                or grupo["horarios"][dia] not in ["Mañana", "Tarde", "Noche"]):
            raise ValueError("Hay un dia o turno invalido.")

    legajos = []
    for inscripto in grupo["inscriptos"]:
        if len(inscripto) != 2:
            raise ValueError("Hay una inscripcion incompleta.")
        legajo = inscripto[0]
        if legajo <= 0 or legajo != int(legajo) or legajo in legajos:
            raise ValueError("Hay un legajo invalido o repetido en el grupo.")
        if legajo not in legajos_padron:
            raise ValueError("Un inscripto no existe en el padron: " + str(legajo))
        if inscripto[1] not in ["Activo", "Inactivo"]:
            raise ValueError("El estado de una inscripcion no es valido.")
        legajos.append(legajo)

    numeros = []
    for sesion in grupo["sesiones"]:
        if len(sesion) != 3:
            raise ValueError("Hay una sesion incompleta.")
        numero = sesion[0]
        if numero <= 0 or numero != int(numero) or numero in numeros:
            raise ValueError("Hay un numero de sesion invalido o repetido.")
        if Sesiones.validar_fecha(sesion[1]) == False or len(sesion[2].strip()) == 0:
            raise ValueError("La fecha o el tema de una sesion no es valido.")
        numeros.append(numero)

    # Validación de archivos guardados antes del cambio de formato.
    if "asistencias" in grupo:
        if len(grupo["inscriptos"]) != len(grupo["asistencias"]):
            raise ValueError("Las filas de asistencias no coinciden con las inscripciones.")

        for fila in grupo["asistencias"]:
            if len(fila) != len(grupo["sesiones"]):
                raise ValueError("Las columnas de asistencias no coinciden con las sesiones.")
            for estado in fila:
                if estado not in ["P", "A", "T", "J", "-"]:
                    raise ValueError("Hay un estado de asistencia invalido.")


def consultar_grupo(ruta_padron, grupo, materia, nombre):

    if len(grupo["inscriptos"]) == 0 or len(grupo["sesiones"]) == 0:
        print("No hay inscriptos o sesiones cargadas en este grupo.")
        return

    # Consultas conserva su interfaz: solo se preparan alumnos de este grupo.
    alumnos = []
    for legajo, estado in grupo["inscriptos"]:
        alumno = Archivos.buscar_estudiante(legajo, ruta_padron)
        if len(alumno) == 0:
            raise ValueError("El alumno del grupo no existe en el padron.")
        alumnos.append([legajo, alumno[1], estado])

    Consultas.menu_consultas(alumnos, grupo["sesiones"], materia, nombre)


def main():

    try:
        ruta_padron, materias, configuracion = abrir_archivos()
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
        print("No se pudieron abrir los datos:", error)
        return

    opcion = 0
    while opcion != 5:
        print("\n--- Gestion de asistencia ---")
        print("1. Estudiantes")
        print("2. Asistencia")
        print("3. Materias, grupos y sesiones")
        print("4. Consultas")
        print("5. Finalizar programa")
        opcion = Estudiantes.validar_inputs("Seleccione una opcion: ")

        try:
            if opcion == 1:
                Estudiantes.menu_estudiantes(ruta_padron, materias)
            elif opcion == 3:
                Sesiones.menu_materias_grupos(materias, configuracion)
            elif opcion in [2, 4]:
                materia = Sesiones.seleccionar_materia(materias)
                if materia != None:
                    nombre = Sesiones.seleccionar_grupo(materias, materia)
                    if nombre != None:
                        grupo = Archivos.obtener_grupo(materia, nombre)
                        if opcion == 2:
                            Asistencias.menu_asistencias(ruta_padron, grupo, materia, nombre)
                        else:
                            consultar_grupo(ruta_padron, grupo, materia, nombre)
            elif opcion != 5:
                print("Opcion invalida. Intente nuevamente.")

        except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
            print("No se pudo completar la operacion:", error)

    print("Programa finalizado.")


# Programa principal
main()
