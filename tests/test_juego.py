import random

import pytest

from fantasma_ia import buscar_camino
from juego import Partida
from laberinto import Laberinto


class AzarControlado:
    def __init__(self, tiradas, aparicion=None):
        self.tiradas = iter(tiradas)
        self.aparicion = aparicion

    def randint(self, minimo, maximo):
        assert (minimo, maximo) == (1, 6)
        return next(self.tiradas)

    def choice(self, opciones):
        assert self.aparicion in opciones
        return self.aparicion


class LaberintoConDistanciasEnCache:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.distancias = {}

    def vecinos_accesibles(self, casilla):
        return self.laberinto.vecinos_accesibles(casilla)

    def hay_pared(self, origen, destino):
        return self.laberinto.hay_pared(origen, destino)

    def distancias_desde(self, origen):
        if origen not in self.distancias:
            self.distancias[origen] = self.laberinto.distancias_desde(origen)
        return self.distancias[origen]


@pytest.fixture
def tablero(registros):
    return Laberinto(registros[1]["grid"])


def ruta_completa(tablero):
    return [(0, 0), *buscar_camino(tablero, (0, 0), (14, 14))]


def preparar_dado_jugador(partida):
    valor = partida.tirar_jugador()
    partida.dado_jugador.actualizar(0.6)
    assert partida.terminar_dado_jugador()
    return valor


def preparar_dado_fantasma(partida):
    valor = partida.tirar_fantasma()
    partida.dado_fantasma.actualizar(0.6)
    assert partida.terminar_dado_fantasma()
    return valor


def mover_entre(partida, origen, destino):
    direccion = (destino[0] - origen[0], destino[1] - origen[1])
    return partida.mover_jugador(direccion)


def test_inicio_y_ordenes_invalidas_no_alteran_la_partida(tablero):
    partida = Partida(tablero, semilla=20)

    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.jugador == (0, 0)
    assert partida.fantasma is None
    assert partida.turno == 1
    assert not partida.terminar_turno_jugador()
    assert not partida.tirar_fantasma()
    assert not partida.mover_jugador((1, 0))
    assert partida.estado == "JUGADOR_TIRAR"


def test_pared_y_cero_pasos_no_mueven_al_jugador(tablero):
    partida = Partida(tablero, semilla=20)
    partida.estado = "JUGADOR_MOVER"
    partida.pasos_restantes = 2
    accesibles = set(tablero.vecinos_accesibles(partida.jugador))
    direccion = next(
        (dc, df) for dc, df in ((0, -1), (1, 0), (0, 1), (-1, 0))
        if (dc, df) not in accesibles
    )

    assert not partida.mover_jugador(direccion)
    assert partida.jugador == (0, 0)
    assert partida.pasos_restantes == 2

    partida.pasos_restantes = 0
    direccion = next(
        (casilla[0], casilla[1])
        for casilla in tablero.vecinos_accesibles(partida.jugador)
    )
    assert not partida.mover_jugador(direccion)
    assert partida.jugador == (0, 0)


def test_primer_turno_aparece_fantasma_al_terminar_y_mueve_segun_dado(tablero):
    ruta = ruta_completa(tablero)
    jugador = ruta[2]
    distancias = tablero.distancias_desde(jugador)
    aparicion = max(
        (casilla for casilla, pasos in distancias.items()
         if pasos >= 6 and casilla != (14, 14)),
        key=distancias.get,
    )
    azar = AzarControlado([5, 4], aparicion)
    partida = Partida(tablero, azar_logico=azar, azar_visual=random.Random(9))

    assert partida.tirar_jugador() == 5
    partida.dado_jugador.actualizar(0.6)
    assert partida.terminar_dado_jugador()
    assert mover_entre(partida, ruta[0], ruta[1])
    assert mover_entre(partida, ruta[1], ruta[2])
    assert partida.pasos_restantes == 3
    assert partida.fantasma is None

    assert partida.terminar_turno_jugador()
    assert partida.estado == "APARECE_FANTASMA"
    assert partida.fantasma == aparicion
    assert distancias[partida.fantasma] >= 6
    assert partida.fantasma != (14, 14)
    assert partida.terminar_aparicion_fantasma()

    assert preparar_dado_fantasma(partida) == 4
    assert partida.estado == "FANTASMA_BUSCA"
    camino = partida.camino_fantasma.copy()
    assert camino[-1] == partida.jugador
    assert partida.terminar_busqueda_fantasma()
    pasos = min(4, len(camino))
    for _ in range(pasos):
        assert partida.mover_fantasma_paso()

    assert partida.fantasma == camino[pasos - 1]
    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.turno == 2


def test_fantasma_captura_en_el_paso_tres_y_se_detiene(tablero):
    ruta = ruta_completa(tablero)
    partida = Partida(
        tablero,
        azar_logico=AzarControlado([5]),
        azar_visual=random.Random(9),
    )
    partida.jugador = ruta[3]
    partida.fantasma = ruta[0]
    partida.turno = 2
    partida.estado = "FANTASMA_TIRAR"

    assert preparar_dado_fantasma(partida) == 5
    assert partida.terminar_busqueda_fantasma()
    assert partida.estado == "FANTASMA_MOVER"
    assert partida.pasos_fantasma == 3
    assert partida.mover_fantasma_paso()
    assert partida.fantasma == ruta[1]
    assert partida.estado == "FANTASMA_MOVER"
    assert partida.mover_fantasma_paso()
    assert partida.fantasma == ruta[2]
    assert partida.estado == "FANTASMA_MOVER"
    assert partida.mover_fantasma_paso()
    assert partida.fantasma == partida.jugador
    assert partida.estado == "DERROTA"


def test_fantasma_a_distancia_ocho_avanza_solo_cuatro_pasos(tablero):
    ruta = ruta_completa(tablero)
    partida = Partida(
        tablero,
        azar_logico=AzarControlado([4]),
        azar_visual=random.Random(9),
    )
    partida.jugador = ruta[8]
    partida.fantasma = ruta[0]
    partida.turno = 2
    partida.estado = "FANTASMA_TIRAR"

    assert preparar_dado_fantasma(partida) == 4
    assert len(partida.camino_fantasma) == 8
    assert partida.terminar_busqueda_fantasma()
    for _ in range(4):
        assert partida.mover_fantasma_paso()

    assert partida.fantasma == ruta[4]
    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.turno == 3


def test_jugador_pierde_inmediatamente_al_entrar_en_el_fantasma(tablero):
    ruta = ruta_completa(tablero)
    partida = Partida(tablero, semilla=20)
    partida.jugador = ruta[0]
    partida.fantasma = ruta[1]
    partida.estado = "JUGADOR_MOVER"
    partida.pasos_restantes = 5

    assert mover_entre(partida, ruta[0], ruta[1])
    assert partida.jugador == partida.fantasma
    assert partida.pasos_restantes == 4
    assert partida.estado == "DERROTA"


def test_llegar_a_meta_gana_sin_gastar_el_dado_ni_aparecer_fantasma(tablero):
    ruta = ruta_completa(tablero)
    partida = Partida(tablero, semilla=20)
    partida.jugador = ruta[-2]
    partida.estado = "JUGADOR_MOVER"
    partida.pasos_restantes = 4

    assert mover_entre(partida, ruta[-2], ruta[-1])
    assert partida.jugador == (14, 14)
    assert partida.estado == "VICTORIA"
    assert partida.pasos_restantes == 3
    assert partida.fantasma is None


def test_aparicion_segura_en_diez_mil_simulaciones(registros):
    laberinto = LaberintoConDistanciasEnCache(Laberinto(registros[1]["grid"]))
    azar = random.Random(101)
    azar_visual = random.Random(202)
    azar_posiciones = random.Random(303)
    casillas = [(columna, fila) for fila in range(15) for columna in range(15)]

    for _ in range(10_000):
        partida = Partida(laberinto, azar_logico=azar, azar_visual=azar_visual)
        partida.jugador = azar_posiciones.choice(casillas)
        distancias = laberinto.distancias_desde(partida.jugador)
        partida.tirar_jugador()
        partida.dado_jugador.actualizar(0.6)
        assert partida.terminar_dado_jugador()
        assert partida.terminar_turno_jugador()

        assert partida.fantasma != (14, 14)
        assert distancias[partida.fantasma] >= 6


def test_tres_rondas_recalculan_ruta_y_conservan_dados_separados(tablero):
    ruta_meta = ruta_completa(tablero)
    jugador_primera = ruta_meta[2]
    distancias = tablero.distancias_desde(jugador_primera)
    aparicion = max(
        (casilla for casilla, pasos in distancias.items()
         if pasos >= 6 and casilla != (14, 14)),
        key=distancias.get,
    )
    azar = AzarControlado([2, 1, 2, 1, 2, 1], aparicion)
    partida = Partida(tablero, azar_logico=azar, azar_visual=random.Random(9))
    rutas_fantasma = []
    indice_jugador = 0

    for ronda in range(3):
        if ronda:
            assert partida.traza_fantasma
            assert partida.tirar_jugador() == 2
            assert partida.traza_fantasma == []
        else:
            assert partida.tirar_jugador() == 2
        partida.dado_jugador.actualizar(0.6)
        assert partida.terminar_dado_jugador()
        for _ in range(2):
            assert mover_entre(
                partida, ruta_meta[indice_jugador], ruta_meta[indice_jugador + 1]
            )
            indice_jugador += 1

        if ronda == 0:
            assert partida.estado == "APARECE_FANTASMA"
            assert partida.terminar_aparicion_fantasma()
        else:
            assert partida.estado == "FANTASMA_TIRAR"

        assert partida.tirar_fantasma() == 1
        partida.dado_fantasma.actualizar(0.6)
        assert partida.terminar_dado_fantasma()
        rutas_fantasma.append(partida.camino_fantasma.copy())
        assert rutas_fantasma[-1][-1] == partida.jugador
        assert partida.terminar_busqueda_fantasma()
        assert partida.mover_fantasma_paso()
        assert partida.estado == "JUGADOR_TIRAR"
        assert partida.turno == ronda + 2

    assert rutas_fantasma[0] != rutas_fantasma[1]
    assert partida.dado_jugador.valor == 2
    assert partida.dado_fantasma.valor == 1
    assert partida.fantasma != partida.jugador


def test_reiniciar_restaura_estado_inicial_en_el_mismo_mapa(tablero):
    partida = Partida(tablero, semilla=55)
    partida.estado = "DERROTA"
    partida.jugador = (2, 2)
    partida.fantasma = (3, 2)
    partida.turno = 5
    partida.camino_fantasma = [(2, 2)]
    azar_logico = partida.azar_logico

    assert partida.reiniciar()
    assert partida.laberinto is tablero
    assert partida.jugador == (0, 0)
    assert partida.fantasma is None
    assert partida.turno == 1
    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.camino_fantasma == []
    assert partida.azar_logico is azar_logico
