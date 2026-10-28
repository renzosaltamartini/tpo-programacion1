# Se importan las funciones de cada modulo para utilizarlas desde un unico programa principal.
from Estudiantes import *
from Asistencias import *
from Sesiones import *
from Consultas import *


def main():
    # Las tres matrices principales se crean vacias al iniciar el programa.
    # Sus posiciones se mantienen relacionadas durante toda la ejecucion.
    matriz_estudiantes=[]
    matriz_asistencias=[]
    matriz_sesiones=[]

    try:
        with open("archivos/matriz_alumnos.txt","r",encoding="utf-8") as estudiantes:
            for linea in estudiantes:
                datos = linea.strip().split(",")

                if len(datos) >= 2: 
                    legajo = int(datos[0]) if datos[0].isdigit() else datos[0]
                    nombre = datos[1]
                    estado = datos[2] if len(datos) >= 3 else "Activo" ## Modificado por Renzo (Faltaba el estado del alumno)
                    matriz_estudiantes.append([legajo, nombre, estado]) ## Modificado por Renzo (Faltaba el estado del alumno)
    except OSError:
        print("Error, contact al servicio tecnico.")

    salida=1
    while salida!=0:
        print("-"*10,"Gestion de asistencia","-"*10)
        print("\n 1. Menu de estudiantes \n 2. Menu de asistencia \n 3. Menu de sesiones \n 4. Menu de consultas \n 5. Finalizar Programa")

        salida=input("Seleccione una opcion: ").strip()

        while not salida.isdigit():
            print("Opcion invalida, ingrese un numero.")
            salida=input("Seleccione una opcion: ").strip()

        salida=int(salida)

        if salida==1:
            # El menu de estudiantes puede modificar estudiantes y agregar filas a asistencias.
            matriz_estudiantes = menu_estudiantes(matriz_estudiantes) ## Modificado por Renzo
            while len(matriz_asistencias) < len(matriz_estudiantes): ## Modificado por Renzo
                matriz_asistencias.append(["-"] * len(matriz_sesiones)) ## Modificado por Renzo

        elif salida ==2:

            # Para registrar asistencias deben existir estudiantes y sesiones.
            if len(matriz_estudiantes)==0 or len(matriz_sesiones)==0:
                print()
                print("No hay estudiantes o sesiones cargadas")
            else:
                matriz_asistencias=menu_asistencias(matriz_estudiantes,matriz_sesiones,matriz_asistencias)

        elif salida==3:
            # Las sesiones se habilitan una vez que existe al menos un estudiante cargado.
            if len(matriz_estudiantes)==0:
                print()
                print("No hay estudiantes cargados")
            else:
                matriz_sesiones, matriz_asistencias = menu_sesiones(matriz_sesiones, matriz_asistencias) ## Modificado por Renzo

        elif salida==4:
            # Las consultas necesitan que las matrices ya contengan informacion.
            if len(matriz_estudiantes)==0 or len(matriz_sesiones)==0 or len(matriz_asistencias)==0:
                print()
                print("No hay estudiantes o sesiones cargadas")
            else:
                menu_consultas(matriz_estudiantes, matriz_sesiones, matriz_asistencias)

        elif salida==5:
            # La opcion 5 cambia la variable de control y finaliza el programa.
            salida=0
            print()
            print("-"*10,"Programa Finalizado","-"*10)
        else:
            print("Opcion invalida, intente nuevamente")

        try:
            with open("archivos/matriz_alumnos.txt","w",encoding="utf-8") as estudiantes:
                for estudiante in matriz_estudiantes:
                    estado = estudiante[2] if len(estudiante) > 2 else "Activo" ## Modificado por Renzo
                    estudiantes.write(f"{estudiante[0]},{estudiante[1]},{estado}\n") ## Modificado por Renzo
        except:
            print("Error, contacta al servicio tecnico.")



main()