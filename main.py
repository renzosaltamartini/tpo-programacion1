from gordo import *
from santichad import *
from Pollo import *
from renzo import *


def main():
    matriz_estudiantes=[]
    matriz_asistencias=[]
    matriz_sesiones=[]

    salida=0
    while salida!=0:
        print("-"*10,"Gestion de asistencia","-"*10)
        print()
        print("\n 1. Menu de estudiantes \n 2. Menu de asistencia \n 3. Menu de sesiones \n 4. Menu de consultas \n 5. Finalizar Programa")
        salida=int(input("Seleccione una opcion: "))
        if salida==1:
            matriz_estudiantes=main_estudiantes()
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
        else:
            print("Opcion invalida, intente nuevamente")

main()


        
