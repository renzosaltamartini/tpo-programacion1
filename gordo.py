def registrar_estudiantes(matriz_estudiantes):
    # Permite cargar uno o varios estudiantes nuevos hasta que el usuario decida no continuar
    salida=3
    alumno=[]
    estado=0
    estado_add=""
    while salida!=1:
        salida=3
        estado=0
        print()
        legajo=int(input("ingrese el legajo del alumno "))
        # Se valida que el legajo no exista ya y sea un numero valido (mayor a 0)
        alumno.append(verificacion_legajo(legajo,matriz_estudiantes))

        nombre=input("ingrese el nombre del estudiante: ")
        # Se valida que el nombre no este repetido
        alumno.append(validar_nombre(nombre,matriz_estudiantes))

        # Se pide el estado del alumno hasta que se ingrese una opcion valida (1 o 2)
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

        # Pregunta si se desea seguir cargando mas alumnos (0 = si, 1 = no)
        while salida!=1 and salida!=0:
        
            print()
            print("Desea continuar:  \n 0. si \n 1. no")
            salida=int(input("Seleccione una opcion: "))
            if salida!=1 and salida!=0:
                print("Opicon invalida")

        # Se agrega el alumno armado (legajo, nombre, estado) a la matriz y se reinicia la lista temporal
        matriz_estudiantes.append(alumno)
        alumno=[]

    return matriz_estudiantes

def verificacion_legajo(legajo,matriz_estudiantes):
    # Verifica que el legajo ingresado sea valido (mayor a 0) y que no este repetido en la matriz
    salida=1
    valido=True

    # Si la matriz esta vacia, no hay nada contra que comparar: alcanza con que sea mayor a 0
    if len(matriz_estudiantes)==0 and legajo>0 and legajo!=0:
        return legajo
    else:

        while salida!=0:
            valido=True
            for i in range(len(matriz_estudiantes)):
                # matriz_estudiantes[i] es la lista [legajo, nombre, estado] de cada alumno,
                # por eso "legajo in matriz_estudiantes[i]" chequea si ese legajo ya fue usado
                if legajo in matriz_estudiantes[i] or legajo<0 or legajo==0:
                    legajo=int(input("el legajo no es valido, ingrese uno nuevo: "))
                    i=0  # reinicia el contador para volver a validar el nuevo legajo desde el principio
                    valido=False

            if  valido==True:
                salida=0
                return legajo

def validar_nombre(nombre,matriz_estudiantes):
    # Verifica que el nombre ingresado no este repetido entre los alumnos ya cargados y que el nombre solo contenga letras
    salida=1
    valido=True

    if len(matriz_estudiantes)==0:
        return nombre
    else:

        
            
        while salida!=0:
            valido=True
            for i in range(len(matriz_estudiantes)):
                # matriz_estudiantes[i][1] es la posicion donde se guarda el nombre de cada alumno
                if nombre == matriz_estudiantes[i][1]:
                    i=0  # reinicia el contador para volver a validar el nuevo nombre desde el principio
                    nombre=input("el nombre no es valido, ingrese uno nuevo: ")
                    valido=False
                elif not nombre.isalpha():#verifico que solo haya letras en el nombre
                    i=0  # reinicia el contador para volver a validar el nuevo nombre desde el principio
                    nombre=input("el nombre no es valido, hay numeros dentro del nombre, porfavor ingrese uno nuevo: ")
                    valido=False

            if  valido==True:
                salida=0

    return nombre
    
def baja_estudiantes(matriz_estudiantes):
    # Elimina un alumno de la matriz buscandolo por su legajo
    print()
    print("Baja De Estudiantes")
    

    if len(matriz_estudiantes)==0:
        print()
        print("No hay alumnos cargados")
        return matriz_estudiantes
    else:
        modificar=int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz_estudiantes)):
            # matriz_estudiantes[i][0] es la posicion donde se guarda el legajo de cada alumno
            if matriz_estudiantes[i][0]==modificar:
                matriz_estudiantes.pop(i)
                print()
                print("alumno eliminado con exito")
                return matriz_estudiantes

    # Si termina el for sin encontrar coincidencia, el legajo no existia
    print()
    print("el legajo no existe o no es valido")
    return matriz_estudiantes


def buscar_estudiantes(matriz_estudiantes):
    # Busca un alumno por legajo y muestra sus datos (legajo, nombre y estado) por pantalla
    print()
    print("Buscar Estudiante")
    buscar=0
    alumno=[]
    encontrado=0

    if len(matriz_estudiantes)==0:
            print()
            print("No hay alumnos cargados")
            return matriz_estudiantes
    else:

        buscar=int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0]==buscar:
                encontrado=1

                # Se copian los datos del alumno encontrado (legajo, nombre, estado) para imprimirlos
                alumno.append(matriz_estudiantes[i][0])
                alumno.append(matriz_estudiantes[i][1])
                alumno.append(matriz_estudiantes[i][2])

                print(" Legajo   Nombre   Estado   ")
                print(" %3d"%alumno[0],"   %3s"%alumno[1],"   %3s"%alumno[2])
                    
    if encontrado==0:
        print()
        print("el legajo no existe o no es valido")



    return

def modificar_estudiantes(matriz_estudiantes):
    # Permite modificar el nombre o el estado de un alumno existente, buscandolo por legajo
    print()
    print("Modificar Estudiantes")
    buscar=0
    estado=0
    opcion=0
    encontrado=0

    if len(matriz_estudiantes)==0:
            print()
            print("No hay alumnos cargados")
            return matriz_estudiantes
    else:

        buscar=int(input("Ingrese el legajo del alumno: "))

        for i in range(len(matriz_estudiantes)):

            if matriz_estudiantes[i][0]==buscar:
                encontrado=1

                while opcion != 1 and opcion !=2:

                    print()
                    print("Opciones a modificar: \n 1. Nombre \n 2. Estado")
                    opcion=int(input("seleccione una opcion: "))

                    if opcion==1:
                        # Se valida el nuevo nombre contra la matriz antes de reemplazarlo
                        nombre=input("ingrese el nombre del Alumno: ")
                        matriz_estudiantes[i][1]=validar_nombre(nombre,matriz_estudiantes)

                    elif opcion==2:
                        print()
                        print(" 1. Activo \n 2. Inactivo")
                        estado=int(input("seleccione el estado del alumno: "))
                        while estado != 1 and estado != 2:
                            estado=int(input("seleccione el estado del alumno: "))
                        if estado==2:
                            estado="Inactivo"
                        else:
                            estado="Activo"
                        matriz_estudiantes[i][2]=estado

                    if opcion==1 or opcion==2:
                        print("registro del alumno modificado: ")
                        print(" Legajo   Nombre   Estado   ")
                        print(" %3d"%matriz_estudiantes[i][0],"   %3s"%matriz_estudiantes[i][1],"   %3s"%matriz_estudiantes[i][2])


                    else:
                        print("opcion invalida, intente nuevamente")
                    
        if encontrado==0:
            print()
            print("el legajo no existe o no es valido")
            

    return matriz_estudiantes

def mostrar_estudiantes(matriz_estudiantes):
    # Muestra por pantalla el listado completo de alumnos cargados
    if len(matriz_estudiantes)==0:
        print("no hay estudiantes registrados")
        return
    else:
        print("%-8s"% "LEGAJO","  ","%-10s"% "NOMBRE","  ","%-10s"% "ESTADO")
        # el porcentaje negativo hace que todo se oriente hacia la izquierda
        for i in range(len(matriz_estudiantes)):
            
            print("%-8d"%matriz_estudiantes[i][0],"  ","%-10s"%matriz_estudiantes[i][1],"  ","%-10s"%matriz_estudiantes[i][2])
    return



def main_estudiantes():
    # Funcion principal: muestra el menu y deriva las opciones a cada funcion segun lo elegido
    salida=-1
    opcion=0
    matriz_estudiantes=[]

    print("Estudiantes")
    print()

    while salida!=0:
        print("Opciones del menu: ")
        print()
        print(" 1. Registrar Estudiantes \n 2. Dar de baja estudiantes \n 3. Buscar Estudiantes \n 4. Modificar estudiantes")
        print(" 5. Mostrar Estudiantes \n 6. Finalizar Programa")
        opcion=int(input("ingrese la opcion que quiera utilizar: "))

        if opcion==1:
            matriz_estudiantes=registrar_estudiantes(matriz_estudiantes)
        elif opcion==2:
            matriz_estudiantes=baja_estudiantes(matriz_estudiantes)
        elif opcion==3:
            buscar_estudiantes(matriz_estudiantes)
        elif opcion==4:
            matriz_estudiantes=modificar_estudiantes(matriz_estudiantes)
        elif opcion==5:
            mostrar_estudiantes(matriz_estudiantes)
        elif opcion==6:
            salida=0
        else:
            print("Opcion invalida, intente nuevamente")
    return matriz_estudiantes

main_estudiantes()