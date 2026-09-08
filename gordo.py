def registrar_estudiantes(matriz):
    salida=3
    alumno=[]
    estado=0
    estado_add=""
    while salida!=1:
        salida=3
        estado=0
        print()
        legajo=int(input("ingrese el legajo del alumno "))
        alumno.append(verificacion_legajo(legajo,matriz))

        nombre=input("ingrese el nombre del estudiante: ")
        alumno.append(validar_nombre(nombre,matriz))

        while estado!=1 and estado!=2:
        
            print("Estados:  \n 1. Activo \n 2. Inactivo")
            estado=int(input("En que estado esta el alumno: "))
            if estado!=1 and estado!=2:
                print("Opicon invalida")
            else:
                if estado==1:
                    estado_add="Activo"
                else:
                    estado_add="Inactivo"
                alumno.append(estado_add)

        while salida!=1 and salida!=0:
        
            print()
            print("Desea continuar:  \n 0. si \n 1. no")
            salida=int(input("Seleccione una opcion: "))
            if salida!=1 and salida!=0:
                print("Opicon invalida")

        matriz.append(alumno)
        alumno=[]

    return matriz

def verificacion_legajo(legajo,matriz):
    salida=1
    valido=True

    if len(matriz)==0 and legajo>0 and legajo!=0:
        return legajo
    else:

        while salida!=0:
            valido=True
            for i in range(len(matriz)):
                if legajo in matriz[i] or legajo<0 or legajo==0:
                    legajo=int(input("el legajo no es valido, ingrese uno nuevo: "))
                    i=0
                    valido=False

            if  valido==True:
                salida=0
                return legajo

def validar_nombre(nombre,matriz):
    salida=1
    valido=True

    if len(matriz)==0:
        return nombre
    else:

        while salida!=0:
            valido=True
            for i in range(len(matriz)):
                if nombre == matriz[i][1]:
                    i=0
                    nombre=input("el nombre no es valido, ingrese uno nuevo: ")
                    valido=False

            if  valido==True:
                salida=0

    return nombre
    
def baja_estudiantes(matriz):
    print()
    print("Baja De Estudiantes")
    

    if len(matriz)==0:
        print()
        print("No hay alumnos cargados")
        return matriz
    else:
        modificar=int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz)):
            if matriz[i][0]==modificar:
                matriz.pop(i)
                print()
                print("alumno eliminado con exito")
                return matriz

    print()
    print("el legajo no existe o no es valido")
    return matriz


def buscar_estudiantes(matriz):
    print()
    print("Buscar Estudiante")
    buscar=0
    alumno=[]
    encontrado=0

    if len(matriz)==0:
            print()
            print("No hay alumnos cargados")
            return matriz
    else:

        buscar=int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz)):

            if matriz[i][0]==buscar:
                encontrado=1

                alumno.append(matriz[i][0])
                alumno.append(matriz[i][1])
                alumno.append(matriz[i][2])

                print(" Legajo   Nombre   Estado   ")
                print(" %3d"%alumno[0],"   %3s"%alumno[1],"   %3s"%alumno[2])
                    
    if encontrado==0:
        print()
        print("el legajo no existe o no es valido")



    return

def modificar_estudiantes(matriz):
    print()
    print("Modificar Estudiantes")
    buscar=0
    estado=0
    opcion=0
    encontrado=0

    if len(matriz)==0:
            print()
            print("No hay alumnos cargados")
            return matriz
    else:

        buscar=int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz)):

            if matriz[i][0]==buscar:
                encontrado=1

                while opcion != 1 and opcion !=2:

                    print()
                    print("Opciones a modificar: \n 1. Nombre \n 2. Estado")
                    opcion=int(input("seleccione una opcion: "))

                    if opcion==1:

                        nombre=input("ingrese el nombre del Alumno: ")
                        matriz[i][1]=validar_nombre(nombre,matriz)

                    elif opcion==2:
                        print()
                        print(" 1. Activo \n 2. Inactivo")
                        estado=int(input("seleccione el estado del alumno: "))
                        while estado != 1 and estado != 2:
                            estado=int(input("seleccione el estado del alumno: "))
                        matriz[i][2]=estado

                    if opcion==1 or opcion==2:
                        print("registro del alumno modificado: ")
                        print(" Legajo   Nombre   Estado   ")
                        print(" %3d"%matriz[i][0],"   %3s"%matriz[i][1],"   %3s"%matriz[i][2])


                    else:
                        print("opcion invalida, intente nuevamente")
                    
        if encontrado==0:
            print()
            print("el legajo no existe o no es valido")
            

    return matriz

def mostrar_estudiantes(matriz):

    if len(matriz)==0:
        print("no hay estudiantes registrados")
        return
    else:
        print("LEGAJO   NOMBRE  ESTADO")
        for i in range(len(matriz)):
            
            print("%8d"%matriz[i][0],"  ","%8s"%matriz[i][1],"  ","%8d"%matriz[i][2])
    return



def main():
    salida=-1
    opcion=0
    matriz=[]

    print("Estudiantes")
    print()

    while salida!=0:
        print("Opciones del menu: ")
        print()
        print(" 1. Registrar Estudiantes \n 2. Dar de baja estudiantes \n 3. Buscar Estudiantes \n 4. Modificar estudiantes")
        print(" 5. Mostrar Estudiantes \n 6. Finalizar Programa")
        opcion=int(input("ingrese la opcion que quiera utilizar: "))

        if opcion==1:
            matriz=registrar_estudiantes(matriz)
        elif opcion==2:
            matriz=baja_estudiantes(matriz)
        elif opcion==3:
            buscar_estudiantes(matriz)
        elif opcion==4:
            matriz=modificar_estudiantes(matriz)
        elif opcion==5:
            mostrar_estudiantes(matriz)
        elif opcion==6:
            salida=0
        else:
            print("Opcion invalida, intente nuevamente")

main()
