"""Búsqueda de caminos con una traza de la pila de backtracking."""

from typing import Literal, NamedTuple

Casilla = tuple[int, int]


class Evento(NamedTuple):
    tipo: Literal["apilar", "desapilar", "encontrado"]
    casilla: Casilla
    pila: tuple[Casilla, ...]


def buscar_camino_con_traza(laberinto, origen: Casilla, destino: Casilla):
    pila = [origen]
    visitadas = {origen}
    traza = [Evento("apilar", origen, tuple(pila))]

    while pila:
        actual = pila[-1]
        if actual == destino:
            traza.append(Evento("encontrado", destino, tuple(pila)))
            return pila[1:], traza

        vecino = next(
            (casilla for casilla in laberinto.vecinos_accesibles(actual)
             if casilla not in visitadas),
            None,
        )
        if vecino is not None:
            pila.append(vecino)
            visitadas.add(vecino)
            traza.append(Evento("apilar", vecino, tuple(pila)))
        else:
            casilla = pila.pop()
            traza.append(Evento("desapilar", casilla, tuple(pila)))

    raise ValueError("No existe un camino entre las casillas.")


def buscar_camino(laberinto, origen: Casilla, destino: Casilla):
    return buscar_camino_con_traza(laberinto, origen, destino)[0]
