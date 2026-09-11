from gordo import *
from santichad import *
from pollo import *


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
            main_estudiantes()
        elif salida ==2:
            menu_asistencias()

        
