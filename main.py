from Estudiantes import *
from Asistencias import *
from Sesiones import *
from Consultas import *


def main():
    matriz_estudiantes=[]
    matriz_asistencias=[]
    matriz_sesiones=[]

    salida=1
    while salida!=0:
        print("-"*10,"Gestion de asistencia","-"*10)
        print("\n 1. Menu de estudiantes \n 2. Menu de asistencia \n 3. Menu de sesiones \n 4. Menu de consultas \n 5. Finalizar Programa")
        salida=int(input("Seleccione una opcion: "))

        if salida==1:
            matriz_estudiantes,matriz_asistencias=menu_estudiantes(matriz_estudiantes, matriz_sesiones, matriz_asistencias)

        elif salida ==2:

            if len(matriz_estudiantes)==0 or len(matriz_sesiones)==0:
                print()
                print("No hay estudiantes ni sesiones cargadas")
            else:
                matriz_asistencias=menu_asistencias(matriz_estudiantes,matriz_sesiones,matriz_asistencias)

        elif salida==3:
            if len(matriz_estudiantes)==0:
                print()
                print("No hay estudiantes cargados")
            else:
                matriz_sesiones=menu_sesiones(matriz_sesiones,matriz_asistencias)

        elif salida==4:
            if len(matriz_estudiantes)==0 or len(matriz_sesiones)==0 or len(matriz_asistencias)==0:
                print()
                print("No hay estudiantes ni sesiones cargadas")
            else:
                menu_consultas(matriz_estudiantes, matriz_sesiones, matriz_asistencias)

        elif salida==5:
            salida=0
            print()
            print("-"*10,"Programa Finalizado","-"*10)

        else:
            print("Opcion invalida, intente nuevamente")

main()