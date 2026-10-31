import pytest

from fantasma_ia import Evento, buscar_camino, buscar_camino_con_traza


class LaberintoPrueba:
    def __init__(self, conexiones):
        self.conexiones = conexiones

    def vecinos_accesibles(self, casilla):
        return list(self.conexiones.get(casilla, ()))


def test_camino_alcanza_la_meta_en_los_cinco_laberintos(registros):
    from laberinto import Laberinto

    for registro in registros:
        tablero = Laberinto(registro["grid"])
        camino = buscar_camino(tablero, (0, 0), (14, 14))
        assert camino
        assert camino[-1] == (14, 14)


def test_camino_solo_cruza_pasos_abiertos(registros):
    from laberinto import Laberinto

    tablero = Laberinto(registros[1]["grid"])
    camino = buscar_camino(tablero, (0, 0), (14, 14))
    anterior = (0, 0)
    for casilla in camino:
        assert not tablero.hay_pared(anterior, casilla)
        anterior = casilla


def test_origen_igual_a_destino_devuelve_traza_completa():
    casilla = (4, 7)
    camino, traza = buscar_camino_con_traza(LaberintoPrueba({}), casilla, casilla)

    assert camino == []
    assert traza == [
        Evento("apilar", casilla, (casilla,)),
        Evento("encontrado", casilla, (casilla,)),
    ]


def test_traza_registra_retroceso_y_copias_de_pila():
    origen = (1, 1)
    callejon = (1, 0)
    giro = (2, 1)
    destino = (2, 2)
    tablero = LaberintoPrueba({
        origen: [callejon, giro],
        callejon: [origen],
        giro: [origen, destino],
        destino: [giro],
    })

    camino, traza = buscar_camino_con_traza(tablero, origen, destino)

    assert camino == [giro, destino]
    assert traza == [
        Evento("apilar", origen, (origen,)),
        Evento("apilar", callejon, (origen, callejon)),
        Evento("desapilar", callejon, (origen,)),
        Evento("apilar", giro, (origen, giro)),
        Evento("apilar", destino, (origen, giro, destino)),
        Evento("encontrado", destino, (origen, giro, destino)),
    ]
    assert traza[1].pila == (origen, callejon)
    assert traza[2].pila == (origen,)


def test_traza_es_determinista(registros):
    from laberinto import Laberinto

    tablero = Laberinto(registros[1]["grid"])
    primera = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
    segunda = buscar_camino_con_traza(tablero, (0, 0), (14, 14))

    assert segunda == primera


def test_pila_nunca_supera_el_numero_de_casillas(registros):
    from laberinto import Laberinto

    tablero = Laberinto(registros[1]["grid"])
    _, traza = buscar_camino_con_traza(tablero, (0, 0), (14, 14))

    assert all(len(evento.pila) <= 225 for evento in traza)


def test_destino_inalcanzable_lanza_value_error():
    origen = (0, 0)
    destino = (1, 0)
    tablero = LaberintoPrueba({origen: [], destino: []})

    with pytest.raises(ValueError):
        buscar_camino_con_traza(tablero, origen, destino)


def test_buscar_camino_es_atajo_sin_traza(registros):
    from laberinto import Laberinto

    tablero = Laberinto(registros[1]["grid"])

    assert buscar_camino(tablero, (0, 0), (14, 14)) == (
        buscar_camino_con_traza(tablero, (0, 0), (14, 14))[0]
    )
