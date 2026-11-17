# Título: Interfaz web para rutas óptimas con Streamlit
# Nombre del autor: Ana Patricia Ponce Santero
# Fecha: 17 de noviembre de 2026
# Descripción: Frontend que calcula rutas con Dijkstra y registra conexiones.

import pandas as pd
import streamlit as st

from grafo import Grafo
from io_handler import (RUTA_CSV, cargar_grafo, guardar_arista,
                        validar_conexion, validar_nodo)

st.set_page_config(page_title="Rutas con Dijkstra", page_icon="🗺️")


def inicializar_estado():
    """Lee el CSV una sola vez y guarda el grafo en session_state."""
    if "grafo" in st.session_state:
        return

    st.session_state.mensajes_carga = []
    try:
        grafo, advertencias = cargar_grafo(RUTA_CSV)
        st.session_state.mensajes_carga = advertencias
    except FileNotFoundError:
        grafo = Grafo()
        st.session_state.mensajes_carga = [
            f"No se encontró {RUTA_CSV}. Se creará al registrar "
            "la primera conexión."
        ]
    except KeyError as columnas:
        grafo = Grafo()
        st.session_state.mensajes_carga = [
            f"A {RUTA_CSV} le faltan las columnas: {columnas}"
        ]

    st.session_state.grafo = grafo
    st.session_state.lecturas_csv = 1


def tabla_conexiones(grafo):
    """Arma un DataFrame con las conexiones que hay en memoria."""
    return pd.DataFrame(grafo.aristas, columns=["Origen", "Destino", "Peso"])


def vista_calcular(grafo):
    st.subheader("Calcular ruta óptima")
    col_origen, col_destino = st.columns(2)
    texto_origen = col_origen.text_input("Nodo origen", placeholder="CUGDL")
    texto_destino = col_destino.text_input("Nodo destino",
                                           placeholder="UNIVER")

    if not st.button("Calcular ruta", type="primary"):
        return

    try:
        origen = validar_nodo(texto_origen)
        destino = validar_nodo(texto_destino)
        costo, ruta = grafo.dijkstra(origen, destino)
    except ValueError as error:
        st.warning(str(error))
        return
    except KeyError as nodo:
        st.error(f"El nodo {nodo} no existe en la red.")
        return

    if not ruta:
        st.error(f"No existe una ruta posible entre {origen} y {destino}.")
        return

    col_costo, col_paradas = st.columns(2)
    col_costo.metric("Costo total mínimo", f"{costo:g}")
    col_paradas.metric("Nodos en el recorrido", len(ruta))
    st.success(" ➜ ".join(ruta))

    with st.expander("Ver detalle por tramo"):
        tramos = [
            (ruta[i], ruta[i + 1], grafo.nodos[ruta[i]][ruta[i + 1]])
            for i in range(len(ruta) - 1)
        ]
        st.dataframe(
            pd.DataFrame(tramos, columns=["Desde", "Hasta", "Peso"]),
            hide_index=True,
        )


def vista_registrar(grafo):
    st.subheader("Registrar nueva conexión")
    with st.form("form_registro", clear_on_submit=True):
        col_origen, col_destino, col_peso = st.columns(3)
        texto_origen = col_origen.text_input("Origen")
        texto_destino = col_destino.text_input("Destino")
        texto_peso = col_peso.text_input("Peso", placeholder="5.5")
        enviado = st.form_submit_button("Guardar conexión")

    if not enviado:
        return

    try:
        origen, destino, peso = validar_conexion(
            texto_origen, texto_destino, texto_peso)
        # Primero se guarda en disco y luego en memoria
        guardar_arista(origen, destino, peso, RUTA_CSV)
        grafo.agregar_arista(origen, destino, peso)
    except ValueError as error:
        st.warning(str(error))
    except PermissionError:
        st.error(f"No hay permiso para escribir en {RUTA_CSV}.")
    else:
        st.success(f"Conexión {origen} ↔ {destino} ({peso:g}) guardada.")


def vista_red(grafo):
    st.subheader("Red actual")
    if not grafo.aristas:
        st.info("Todavía no hay conexiones registradas.")
        return

    st.dataframe(tabla_conexiones(grafo), hide_index=True)

    with st.expander("Ver vecinos de cada nodo"):
        vecinos = [
            (nodo, ", ".join(sorted(conexiones)))
            for nodo, conexiones in sorted(grafo.nodos.items())
        ]
        st.dataframe(
            pd.DataFrame(vecinos, columns=["Nodo", "Conectado con"]),
            hide_index=True,
        )


def barra_lateral(grafo):
    with st.sidebar:
        st.header("Resumen de la red")
        st.metric("Nodos", len(grafo.nodos))
        st.metric("Conexiones", len(grafo.aristas))
        st.caption(f"Archivo: {RUTA_CSV}")
        st.caption(
            f"Lecturas del CSV en esta sesión: "
            f"{st.session_state.lecturas_csv}"
        )
        if grafo.nodos:
            st.write("**Nodos disponibles:**")
            st.write(", ".join(sorted(grafo.nodos)))


def main():
    inicializar_estado()
    grafo = st.session_state.grafo

    st.title("🗺️ Rutas óptimas con Dijkstra")
    for mensaje in st.session_state.mensajes_carga:
        st.warning(mensaje)

    barra_lateral(grafo)

    pestana_ruta, pestana_registro, pestana_red = st.tabs(
        ["Calcular ruta", "Registrar conexión", "Ver red"])
    with pestana_ruta:
        vista_calcular(grafo)
    with pestana_registro:
        vista_registrar(grafo)
    with pestana_red:
        vista_red(grafo)


main()
