# Título: Lectura y escritura del archivo de conexiones
# Nombre del autor: Ana Patricia Ponce Santero
# Fecha: 17 de noviembre de 2026
# Descripción: Carga el grafo desde nodos.csv y guarda nuevas conexiones.

import csv
import os

from grafo import Grafo

RUTA_CSV = "nodos.csv"
COLUMNAS = ["origen", "destino", "peso"]


def validar_nodo(texto):
    """Limpia el nombre de un nodo; lanza ValueError si viene vacío."""
    nombre = texto.strip().upper()
    if not nombre:
        raise ValueError("El nombre del nodo no puede estar vacío.")
    if "," in nombre:
        raise ValueError("El nombre del nodo no puede llevar comas.")
    return nombre


def validar_peso(texto):
    """Convierte el peso a número; lanza ValueError si no es válido."""
    try:
        peso = float(texto)
    except (TypeError, ValueError):
        raise ValueError(f"El peso '{texto}' no es un número.")
    if peso < 0:
        raise ValueError("El peso no puede ser negativo.")
    return peso


def validar_conexion(texto_origen, texto_destino, texto_peso):
    """Valida los tres campos de una conexión nueva."""
    origen = validar_nodo(texto_origen)
    destino = validar_nodo(texto_destino)
    peso = validar_peso(texto_peso)
    if origen == destino:
        raise ValueError("El origen y el destino deben ser distintos.")
    return origen, destino, peso


def cargar_grafo(ruta=RUTA_CSV):
    """Lee el CSV y regresa un Grafo.

    Lanza FileNotFoundError si el archivo no existe y KeyError si
    le falta alguna columna. Las filas con datos inválidos se omiten
    y se regresan en la lista de advertencias.
    """
    grafo = Grafo()
    advertencias = []

    with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        faltantes = [c for c in COLUMNAS if c not in (lector.fieldnames or [])]
        if faltantes:
            raise KeyError(", ".join(faltantes))

        for numero, fila in enumerate(lector, start=2):
            try:
                origen = validar_nodo(fila["origen"])
                destino = validar_nodo(fila["destino"])
                peso = validar_peso(fila["peso"])
                grafo.agregar_arista(origen, destino, peso)
            except ValueError as error:
                advertencias.append(f"Fila {numero} omitida: {error}")

    return grafo, advertencias


def guardar_arista(origen, destino, peso, ruta=RUTA_CSV):
    """Agrega una conexión al final del CSV (lo crea si no existe).

    Puede lanzar PermissionError si el archivo está protegido.
    """
    archivo_nuevo = not os.path.exists(ruta)

    with open(ruta, mode="a", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        if archivo_nuevo:
            escritor.writerow(COLUMNAS)
        escritor.writerow([origen, destino, peso])
