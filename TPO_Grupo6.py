from Archivos import CARPETA, PADRON, CURSADAS, Padron, registros, escribir, reemplazo, editar_grupo, obtener_grupo
from Estudiantes import buscar_legajo, menu_estudiantes, validar_inputs
from Asistencias import menu_asistencias
from Sesiones import menu_materias_grupos, seleccionar_materia, seleccionar_grupo, validar_fecha
from Consultas import menu_consultas


def abrir_archivos():
    CARPETA.mkdir(exist_ok=True)
    PADRON.touch(exist_ok=True)
    padron = Padron()
    legajos_padron = set()
    for legajo, nombre in padron:
        if legajo in legajos_padron:
            raise ValueError(f"Legajo repetido en el padrón: {legajo}")
        legajos_padron.add(legajo)

    configuracion = {"institucion_predeterminada": "UADE"}
    if not CURSADAS.exists():
        anterior = CARPETA / "cursadas.json"
        if anterior.exists() and anterior.stat().st_size:
            raise ValueError("Hay un cursadas.json anterior con datos. Se requiere convertirlo a JSONL.")
        with reemplazo(CURSADAS) as destino:
            escribir(destino, {"tipo": "configuracion", "datos": configuracion})

    # El índice guarda nombres e instituciones para los menús. Cada planilla se lee por separado.
    indice = {}
    hay_configuracion = False
    for registro in registros():
        tipo = registro["tipo"]
        if tipo == "configuracion":
            configuracion = registro["datos"]
            if hay_configuracion or not isinstance(configuracion, dict):
                raise ValueError("Configuración inválida o repetida.")
            institucion = configuracion.get("institucion_predeterminada")
            if not isinstance(institucion, str) or not institucion.strip():
                raise ValueError("Institución predeterminada inválida.")
            hay_configuracion = True
        elif tipo == "materia":
            materia = registro["materia"]
            if not isinstance(materia, str) or not materia.strip() or materia in indice:
                raise ValueError("Materia inválida o repetida.")
            indice[materia] = {}
        elif tipo == "grupo":
            materia, nombre, grupo = registro["materia"], registro["nombre"], registro["datos"]
            if materia not in indice or nombre in indice[materia]:
                raise ValueError("Grupo repetido o materia inexistente.")
            validar_grupo(nombre, grupo, legajos_padron)
            indice[materia][nombre] = grupo["institucion"]
        else:
            raise ValueError("Tipo de registro desconocido.")
    if not hay_configuracion:
        raise ValueError("Falta la configuración de cursadas.")
    return padron, indice, configuracion


def validar_grupo(nombre_grupo, grupo, legajos_padron):
    if not isinstance(nombre_grupo, str) or len(nombre_grupo.strip()) == 0 or not isinstance(grupo, dict):
        raise ValueError("Hay un grupo con formato incorrecto.")

    for clave in ["institucion", "horarios", "inscriptos", "sesiones", "asistencias"]:
        if clave not in grupo:
            raise ValueError("Falta " + clave + " en el grupo " + nombre_grupo)

    if not isinstance(grupo["institucion"], str) or len(grupo["institucion"].strip()) == 0:
        raise ValueError("Institucion invalida en el grupo " + nombre_grupo)

    if not isinstance(grupo["horarios"], dict):
        raise ValueError("Horarios invalidos en el grupo " + nombre_grupo)

    for dia in grupo["horarios"]:
        if dia not in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"] or grupo["horarios"][dia] not in ["Mañana", "Tarde", "Noche"]:
            raise ValueError("Dia o turno invalido en el grupo " + nombre_grupo)

    for clave in ["inscriptos", "sesiones", "asistencias"]:
        if not isinstance(grupo[clave], list):
            raise ValueError("La lista " + clave + " es invalida en el grupo " + nombre_grupo)

    if len(grupo["inscriptos"]) != len(grupo["asistencias"]):
        raise ValueError("Las filas no coinciden con los inscriptos del grupo " + nombre_grupo)

    legajos = []
    for inscripto in grupo["inscriptos"]:
        if not isinstance(inscripto, list) or len(inscripto) != 2:
            raise ValueError("Inscripcion incompleta en el grupo " + nombre_grupo)
        if type(inscripto[0]) != int or inscripto[0] <= 0 or inscripto[0] in legajos:
            raise ValueError("Legajo invalido o duplicado en el grupo " + nombre_grupo)
        if inscripto[0] not in legajos_padron:
            raise ValueError("Un inscripto no existe en el registro general: " + str(inscripto[0]))
        if inscripto[1] not in ["Activo", "Inactivo"]:
            raise ValueError("Estado de inscripcion invalido en el grupo " + nombre_grupo)
        legajos.append(inscripto[0])

    numeros = []
    for sesion in grupo["sesiones"]:
        if not isinstance(sesion, list) or len(sesion) != 3:
            raise ValueError("Sesion incompleta en el grupo " + nombre_grupo)
        if type(sesion[0]) != int or sesion[0] <= 0 or sesion[0] in numeros:
            raise ValueError("Numero de sesion invalido o duplicado en el grupo " + nombre_grupo)
        if not isinstance(sesion[1], str) or not validar_fecha(sesion[1]):
            raise ValueError("Fecha invalida en el grupo " + nombre_grupo)
        if not isinstance(sesion[2], str) or len(sesion[2].strip()) == 0:
            raise ValueError("Tema vacio o invalido en el grupo " + nombre_grupo)
        numeros.append(sesion[0])

    for fila in grupo["asistencias"]:
        if not isinstance(fila, list) or len(fila) != len(grupo["sesiones"]):
            raise ValueError("Columnas incorrectas en el grupo " + nombre_grupo)
        for estado in fila:
            if estado not in ["P", "A", "T", "J", "-"]:
                raise ValueError("Estado de asistencia invalido en el grupo " + nombre_grupo)


def consultar_grupo(padron, grupo):
    if not grupo["inscriptos"] or not grupo["sesiones"]:
        print("No hay inscriptos o sesiones cargadas en este grupo.")
        return

    alumnos = []
    for legajo, estado in grupo["inscriptos"]:
        alumno = buscar_legajo(padron, legajo)
        alumnos.append([legajo, alumno[1], estado])
    menu_consultas(alumnos, grupo["sesiones"], grupo["asistencias"])


def main():
    try:
        padron, materias, configuracion = abrir_archivos()
        opcion = 0
        while opcion != 5:
            print("\n--- Gestión de asistencia ---")
            print("1. Estudiantes")
            print("2. Asistencia")
            print("3. Materias, grupos y sesiones")
            print("4. Consultas")
            print("5. Finalizar programa")
            opcion = validar_inputs("Seleccione una opción: ")

            if opcion == 1:
                menu_estudiantes(padron, materias)
            elif opcion == 3:
                menu_materias_grupos(materias, configuracion)
            elif opcion in (2, 4):
                materia = seleccionar_materia(materias)
                if materia is not None:
                    nombre = seleccionar_grupo(materias, materia)
                    if nombre is not None:
                        if opcion == 2:
                            with editar_grupo(materia, nombre) as grupo:
                                menu_asistencias(padron, grupo)
                        else:
                            grupo = obtener_grupo(materia, nombre)
                            consultar_grupo(padron, grupo)
            elif opcion != 5:
                print("Opción inválida. Intente nuevamente.")
        print("Programa finalizado.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("No se pudo completar la operación:", error)


if __name__ == "__main__":
    main()
