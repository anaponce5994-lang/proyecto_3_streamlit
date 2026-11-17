# Título: Ruta más corta con Dijkstra (versión consola)
# Nombre del autor: Ana Patricia Ponce Santero
# Fecha: 17 de noviembre de 2026
# Descripción: Menú en terminal para calcular rutas y registrar conexiones.

from io_handler import (RUTA_CSV, cargar_grafo, guardar_arista,
                        validar_conexion, validar_nodo)


def mostrar_red(grafo):
    print("\nConexiones registradas:")
    for origen, destino, peso in grafo.aristas:
        print(f"  {origen} <-> {destino}: {peso}")


def calcular_ruta(grafo):
    try:
        inicio = validar_nodo(input("Nodo de origen: "))
        destino = validar_nodo(input("Nodo de destino: "))
        costo, ruta = grafo.dijkstra(inicio, destino)
    except ValueError as error:
        print(f"Error: {error}")
        return
    except KeyError as nodo:
        print(f"Error: el nodo {nodo} no existe en la red.")
        return

    if not ruta:
        print(f"No existe una ruta entre {inicio} y {destino}.")
    else:
        print(f"Costo total: {costo}")
        print("Ruta:", " -> ".join(ruta))


def registrar_conexion(grafo):
    try:
        origen, destino, peso = validar_conexion(
            input("Origen: "), input("Destino: "), input("Peso: "))
        # Primero se guarda en disco y luego en memoria
        guardar_arista(origen, destino, peso)
        grafo.agregar_arista(origen, destino, peso)
        print("Conexión guardada.")
    except ValueError as error:
        print(f"Error: {error}")
    except PermissionError:
        print(f"Error: no hay permiso para escribir en {RUTA_CSV}.")


def main():
    try:
        grafo, advertencias = cargar_grafo()
    except FileNotFoundError:
        print(f"No se encontró {RUTA_CSV}.")
        return
    except KeyError as columnas:
        print(f"A {RUTA_CSV} le faltan las columnas: {columnas}")
        return

    for aviso in advertencias:
        print(aviso)

    opciones = {
        "1": calcular_ruta,
        "2": registrar_conexion,
        "3": mostrar_red,
    }

    while True:
        print("\n1) Calcular ruta  2) Registrar conexión  "
              "3) Ver red  4) Salir")
        opcion = input("Opción: ").strip()
        if opcion == "4":
            break
        if opcion in opciones:
            opciones[opcion](grafo)
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
