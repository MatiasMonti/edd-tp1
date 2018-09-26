from menu import Menu
from batalla import Batalla
from elemento import Elemento
from monstruo import Monstruo
from jugador import Jugador
import os
import pickle

CANTIDAD_DE_JUGADORES = 2
CANTIDAD_DE_ELEMENTOS_POR_JUGADORES = 2
NOMBRE_ARCHIVO_BATALLA = "batalla-store"

def main():
    #Limpio Pantalla
    os.system('cls')
    while True:
        menu_inicial = Menu("Bienvenido a la batalla de monstruos. Seleccione una opcion:",{"1":"Crear Partida","2":"Cargar Partida Iniciada","3":"Salir"})
        opcionMenu = menu_inicial.mostrar_y_pedir_input()
        if opcionMenu=="1":
            while True:
                try:
                    batallaEnJuego = Batalla(*[
                            arg for i in range(CANTIDAD_DE_JUGADORES)
                                for arg in __cargar_jugador__(i + 1)])
                    break
                except Exception as e:
                    print("Surgio un problema: %s" % e)
            break
        elif opcionMenu=="2":
            print ("Cargando Partida . . .")
            try:
                archivo = open(NOMBRE_ARCHIVO_BATALLA,"r")
            except Exception as e:
                print("Hubo un error: %s" % e)

            batallaEnJuego = pickle.load(archivo)
            print("Partida cargada")
            break

        elif opcionMenu=="3":
            input("Saliendo de la batalla. \n Hasta luego!")
            return
        else:
            input("De verdad no podes ingresar un simple numero...?\nPulsa una tecla cualquiera para reintentar")
    __jugar_turno__(batallaEnJuego)
        
def __cargar_jugador__(indice):
    print("")
    print ("Creando jugador numero %d" % indice)
    return  (input("Ingresa el nombre del jugador 1 y luego presiona [Enter]: "),
            *(__elegir_elemento__(
                    Menu("Selecciona el %d° elemento para tu monstruo:" % (i + 1),
                         {"1" : "AGUA",
                          "2" : "FUEGO",
                          "3" : "TIERRA",
                          "4" : "AIRE",
                          "5" : "Sin elemento"}))
                    for i in range(CANTIDAD_DE_ELEMENTOS_POR_JUGADORES)))

def __elegir_elemento__(menu):
    while True:
        opcionElemento = menu.mostrar_y_pedir_input()
        if opcionElemento=="1":
            return Elemento.AGUA
        elif opcionElemento=="2":
            return Elemento.FUEGO
        elif opcionElemento=="3":
            return Elemento.TIERRA
        elif opcionElemento=="4":
            return Elemento.AIRE
        elif opcionElemento=="5":
            return Elemento.NADA
        else:
            print("No se ingreso ninguna opcion valida. Reintentando.")

def __jugar_turno__(batalla):
    menu_jugada = Menu("Batalla en progreso.\nSeleccione una acción:",{"1":"Realizar una jugada", "2":"Guardar Batalla actual", "3":"Salir sin guardar"})
    menu_ataque = Menu("Seleccione el tipo de ataque a realizar:", {"1":"Ataque Normal", "2":"Ataque Especial"})
    while not(batalla.termino()):
        mi_monstruo = batalla.__jugador_atacante__.__monstruo__
        menu_elemento = Menu("Seleccione el elemento del monstruo con que atacar:", {"1":str(mi_monstruo.__elementos__[0]), "2":str(mi_monstruo.__elementos__[1])})
        print("")
        opcion_jugada = menu_jugada.mostrar_y_pedir_input()
        if(opcion_jugada == "1"):
            print("")
            opcion_ataque = menu_ataque.mostrar_y_pedir_input()
            if(opcion_ataque == "1"):
                print("")
                opcion_elemento = menu_elemento.mostrar_y_pedir_input()
                if(opcion_elemento == "1"):
                    batalla.jugada(mi_monstruo.generar_ataque(mi_monstruo.__elementos__[0]))
                    print("")
                    print("Estado Vital de '" + batalla.__jugador_atacante__.__nombre__ + "' es " + str(batalla.__jugador_atacante__.__monstruo__.__estado_vital__))
                    print("Estado Vital de '" + batalla.__jugador_defensor__.__nombre__ + "' es " + str(batalla.__jugador_defensor__.__monstruo__.__estado_vital__))
                elif(opcion_elemento == "2"):
                    batalla.jugada(mi_monstruo.generar_ataque(mi_monstruo.__elementos__[1]))
                    print("")
                    print("Estado Vital de '" + batalla.__jugador_atacante__.__nombre__ + "' es " + str(batalla.__jugador_atacante__.__monstruo__.__estado_vital__))
                    print("Estado Vital de '" + batalla.__jugador_defensor__.__nombre__ + "' es " + str(batalla.__jugador_defensor__.__monstruo__.__estado_vital__))
                else:
                    input("Selección inválida. Reiniciando turno.")
            elif(opcion_ataque == "2"):
                print("")
                opcion_elemento = menu_elemento.mostrar_y_pedir_input()
                if(opcion_elemento == "1"):
                    batalla.jugada(mi_monstruo.generar_ataque_especial(mi_monstruo.__elementos__[0]))
                    print("")
                    print("Estado Vital de '" + batalla.__jugador_atacante__.__nombre__ + "' es " + str(batalla.__jugador_atacante__.__monstruo__.__estado_vital__))
                    print("Estado Vital de '" + batalla.__jugador_defensor__.__nombre__ + "' es " + str(batalla.__jugador_defensor__.__monstruo__.__estado_vital__))
                elif(opcion_elemento == "2"):
                    batalla.jugada(mi_monstruo.generar_ataque_especial(mi_monstruo.__elementos__[1]))
                    print("")
                    print("Estado Vital de '" + batalla.__jugador_atacante__.__nombre__ + "' es " + str(batalla.__jugador_atacante__.__monstruo__.__estado_vital__))
                    print("Estado Vital de '" + batalla.__jugador_defensor__.__nombre__ + "' es " + str(batalla.__jugador_defensor__.__monstruo__.__estado_vital__))
                else:
                    input("Selección inválida. Reiniciando turno.")
            else:
                input("Selección inválida. Reiniciando turno.")
        elif(opcion_jugada == "2"):
            __guardar_partida__(batalla)
            break
        elif(opcion_jugada == "3"):
            input("Saliendo de la batalla. \n Hasta luego!")
            return
        else:
            input("Selección inválida. Reiniciando turno.")
    if(batalla.termino()):
        print(batalla.ganador())

def __guardar_partida__(batalla):
    archivo = open(NOMBRE_ARCHIVO_BATALLA,"w")
    pickle.dump(batalla,archivo)
    print("Se ha guardado la partida correctamente.")
    return

if __name__ == '__main__':
    main()
