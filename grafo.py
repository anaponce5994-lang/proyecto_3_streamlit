# Título: Grafo ponderado y algoritmo de Dijkstra
# Nombre del autor: Ana Patricia Ponce Santero
# Fecha: 17 de noviembre de 2026
# Descripción: Clase Grafo con sus aristas y el cálculo de la ruta más corta.

INFINITO = float("inf")


class Grafo:
    """Grafo ponderado no dirigido guardado como lista de adyacencia."""

    def __init__(self):
        # Cada nodo apunta a un diccionario {vecino: peso}
        self.nodos = {}
        # Lista de conexiones tal como se registraron (para la tabla)
        self.aristas = []

    def agregar_nodo(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = {}

    def agregar_arista(self, origen, destino, peso):
        """Agrega una conexión en ambos sentidos."""
        if peso < 0:
            raise ValueError("El peso no puede ser negativo.")
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos.")

        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen][destino] = peso
        self.nodos[destino][origen] = peso
        self.aristas.append((origen, destino, peso))

    def existe_nodo(self, nombre):
        return nombre in self.nodos

    def dijkstra(self, inicio, destino):
        """Regresa (costo_total, ruta). Si no hay camino: (inf, [])."""
        if not self.existe_nodo(inicio):
            raise KeyError(inicio)
        if not self.existe_nodo(destino):
            raise KeyError(destino)

        distancias = {nombre: INFINITO for nombre in self.nodos}
        anteriores = {nombre: None for nombre in self.nodos}
        visitados = set()
        distancias[inicio] = 0

        while len(visitados) < len(self.nodos):
            # Buscar el nodo no visitado más cercano
            nodo_actual = None
            menor_distancia = INFINITO
            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre

            # Los nodos que quedan no se pueden alcanzar
            if nodo_actual is None or nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            # Revisar si pasando por nodo_actual se llega más rápido
            for vecino, peso in self.nodos[nodo_actual].items():
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        if distancias[destino] == INFINITO:
            return INFINITO, []

        # Reconstruir la ruta caminando hacia atrás desde el destino
        ruta = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = anteriores[nodo]
        ruta.reverse()

        return distancias[destino], ruta
