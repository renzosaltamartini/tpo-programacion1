import os
import json
from Estudiantes import *
from Asistencias import *
from Sesiones import *
from Consultas import *


def cargar_archivos():

    matriz_estudiantes = []
    cursadas = {}
    configuracion = {"institucion_predeterminada": "UADE"}
    numero_linea = 0
    cantidad_antiguos = 0

    try:
        with open("archivos/matriz_alumnos.txt", "r", encoding="utf-8-sig") as estudiantes:
            for linea in estudiantes:
                numero_linea += 1

                if len(linea.strip()) > 0:
                    datos = linea.strip().split(",")

                    if len(datos) != 2 and len(datos) != 3:
                        raise ValueError("Cantidad de campos incorrecta en la linea " + str(numero_linea))

                    legajo = int(datos[0])
                    nombre = datos[1].strip()

                    if legajo <= 0 or len(buscar_legajo(matriz_estudiantes, legajo)) > 0:
                        raise ValueError("Legajo invalido o repetido en la linea " + str(numero_linea))

                    if not nombre.replace(" ", "").isalpha():
                        raise ValueError("Nombre invalido en la linea " + str(numero_linea))

                    # Se admite el formato anterior, sin convertir su estado en una inscripcion.
                    if len(datos) == 3:
                        if datos[2].strip() not in ["Activo", "Inactivo"]:
                            raise ValueError("Estado antiguo invalido en la linea " + str(numero_linea))
                        cantidad_antiguos += 1

                    matriz_estudiantes.append([legajo, nombre])

    except FileNotFoundError:
        print("Todavia no hay estudiantes guardados.")
    except (OSError, ValueError) as error:
        print("No se pudieron recuperar los estudiantes:", error)
        return None, None, None

    try:
        if os.path.exists("archivos/cursadas.json"):
            with open("archivos/cursadas.json", "r", encoding="utf-8-sig") as archivo:
                contenido = archivo.read()

            # Un archivo vacio se admite como primer inicio sin cursadas.
            if len(contenido.strip()) > 0:
                datos = json.loads(contenido)

                if not isinstance(datos, dict) or "cursadas" not in datos or "configuracion" not in datos:
                    raise ValueError("El archivo de cursadas no tiene las claves necesarias.")

                cursadas = datos["cursadas"]
                configuracion = datos["configuracion"]

                if isinstance(configuracion, dict) and "institucion_predeterminada" not in configuracion:
                    configuracion["institucion_predeterminada"] = "UADE"

    except (OSError, ValueError) as error:
        print("No se pudieron recuperar las cursadas:", error)
        return None, None, None

    if not verificar_cursadas(matriz_estudiantes, cursadas, configuracion):
        return None, None, None

    if cantidad_antiguos > 0:
        print("Se recuperaron registros antiguos de estudiantes.")
        print("El estado se administra por inscripcion; el estado general antiguo no se traslada a grupos.")

    return matriz_estudiantes, cursadas, configuracion


def verificar_cursadas(matriz_estudiantes, cursadas, configuracion):

    # Se comprueban los datos al recuperarlos, antes de abrir los menus.
    try:
        if not isinstance(cursadas, dict) or not isinstance(configuracion, dict):
            raise ValueError("Las cursadas o la configuracion no son diccionarios.")

        institucion = configuracion.get("institucion_predeterminada")
        if not isinstance(institucion, str) or len(institucion.strip()) == 0:
            raise ValueError("La institucion predeterminada no es valida.")

        for materia in cursadas:
            if not isinstance(materia, str) or len(materia.strip()) == 0 or not isinstance(cursadas[materia], dict):
                raise ValueError("Hay una materia con formato incorrecto.")

            for nombre_grupo in cursadas[materia]:
                grupo = cursadas[materia][nombre_grupo]

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
                    if len(buscar_legajo(matriz_estudiantes, inscripto[0])) == 0:
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

    except ValueError as error:
        print("No se pueden utilizar las cursadas:", error)
        return False

    return True


def guardar_archivos(matriz_estudiantes, cursadas, configuracion):

    # Primero se completan los dos temporales. Luego se reemplaza cada archivo definitivo.
    try:
        with open("archivos/matriz_alumnos.txt.tmp", "w", encoding="utf-8") as estudiantes:
            for estudiante in matriz_estudiantes:
                estudiantes.write(f"{estudiante[0]},{estudiante[1]}\n")

        with open("archivos/cursadas.json.tmp", "w", encoding="utf-8") as archivo:
            datos = {"cursadas": cursadas, "configuracion": configuracion}
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        # Los alumnos se reemplazan primero para no guardar inscripciones a alumnos aun no guardados.
        os.replace("archivos/matriz_alumnos.txt.tmp", "archivos/matriz_alumnos.txt")
        os.replace("archivos/cursadas.json.tmp", "archivos/cursadas.json")

    except (OSError, TypeError, ValueError) as error:
        print("No se pudieron guardar todos los datos:", error)
        return False

    finally:
        for temporal in ["archivos/matriz_alumnos.txt.tmp", "archivos/cursadas.json.tmp"]:
            if os.path.exists(temporal):
                try:
                    os.remove(temporal)
                except OSError:
                    print("No se pudo quitar el temporal:", temporal)

    print("Datos guardados correctamente.")
    return True


def main():

    # Se trabaja desde la carpeta del programa, aunque se abra desde otra ubicacion.
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.makedirs("archivos", exist_ok=True)
    except OSError as error:
        print("No se pudo abrir la carpeta de datos:", error)
        return

    matriz_estudiantes, cursadas, configuracion = cargar_archivos()

    if matriz_estudiantes == None:
        print("El programa no continuara para evitar guardar sobre datos que no se pudieron recuperar.")
        return

    salida = 1
    while salida != 0:
        print("-" * 10, "Gestion de asistencia", "-" * 10)
        print("\n 1. Menu de estudiantes \n 2. Menu de asistencia \n 3. Materias, grupos y sesiones \n 4. Menu de consultas \n 5. Finalizar Programa")

        salida = validar_inputs("Seleccione una opcion: ")

        if salida == 1:
            matriz_estudiantes = menu_estudiantes(matriz_estudiantes, cursadas)

        elif salida == 2:
            materia = seleccionar_materia(cursadas)

            if materia != None:
                nombre_grupo = seleccionar_grupo(cursadas, materia)

                if nombre_grupo != None:
                    grupo = cursadas[materia][nombre_grupo]
                    menu_asistencias(matriz_estudiantes, grupo)

        elif salida == 3:
            cursadas, configuracion = menu_materias_grupos(cursadas, configuracion)

        elif salida == 4:
            materia = seleccionar_materia(cursadas)

            if materia != None:
                nombre_grupo = seleccionar_grupo(cursadas, materia)

                if nombre_grupo != None:
                    grupo = cursadas[materia][nombre_grupo]

                    if len(grupo["inscriptos"]) == 0 or len(grupo["sesiones"]) == 0:
                        print("No hay inscriptos o sesiones cargadas en este grupo.")

                    else:
                        # Consultas conserva su interfaz actual. Se ordenan sus alumnos segun el grupo.
                        alumnos_grupo = []
                        for inscripto in grupo["inscriptos"]:
                            alumno = buscar_legajo(matriz_estudiantes, inscripto[0])
                            alumnos_grupo.append([alumno[0], alumno[1], inscripto[1]])

                        menu_consultas(alumnos_grupo, grupo["sesiones"], grupo["asistencias"])

        elif salida == 5:
            salida = 0

        else:
            print("Opcion invalida, intente nuevamente")

        if not guardar_archivos(matriz_estudiantes, cursadas, configuracion):
            print("Los cambios siguen en memoria. Vuelva al menu principal para reintentar el guardado.")
            if salida == 0:
                salida = 1

    print()
    print("-" * 10, "Programa Finalizado", "-" * 10)


if __name__ == "__main__":
    main()
