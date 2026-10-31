"""Reglas de una partida, controladas mediante órdenes explícitas."""

import random

from dado import Dado
from fantasma_ia import buscar_camino_con_traza


class Partida:
    JUGADOR_TIRAR = "JUGADOR_TIRAR"
    DADO_JUGADOR = "DADO_JUGADOR"
    JUGADOR_MOVER = "JUGADOR_MOVER"
    APARECE_FANTASMA = "APARECE_FANTASMA"
    FANTASMA_TIRAR = "FANTASMA_TIRAR"
    DADO_FANTASMA = "DADO_FANTASMA"
    FANTASMA_BUSCA = "FANTASMA_BUSCA"
    FANTASMA_MOVER = "FANTASMA_MOVER"
    VICTORIA = "VICTORIA"
    DERROTA = "DERROTA"

    DIRECCIONES = ((0, -1), (1, 0), (0, 1), (-1, 0))

    def __init__(self, laberinto, semilla=None, azar_logico=None, azar_visual=None):
        self.laberinto = laberinto
        self.azar_logico = azar_logico if azar_logico is not None else random.Random(semilla)
        self.azar_visual = azar_visual if azar_visual is not None else random.Random()
        self._restablecer()

    def _restablecer(self):
        self.jugador = (0, 0)
        self.fantasma = None
        self.turno = 1
        self.estado = self.JUGADOR_TIRAR
        self.pasos_restantes = 0
        self.pasos_fantasma = 0
        self.camino_fantasma = []
        self.traza_fantasma = []
        self.indice_fantasma = 0
        self.direccion_fantasma = None
        self.dado_jugador = Dado(self.azar_logico, self.azar_visual)
        self.dado_fantasma = Dado(self.azar_logico, self.azar_visual)

    def tirar_jugador(self):
        if self.estado != self.JUGADOR_TIRAR:
            return None

        self.camino_fantasma = []
        self.traza_fantasma = []
        self.indice_fantasma = 0
        valor = self.dado_jugador.tirar()
        self.pasos_restantes = valor
        self.estado = self.DADO_JUGADOR
        return valor

    def terminar_dado_jugador(self):
        if self.estado != self.DADO_JUGADOR or self.dado_jugador.animando:
            return False
        self.estado = self.JUGADOR_MOVER
        return True

    def mover_jugador(self, direccion):
        if (self.estado != self.JUGADOR_MOVER or self.pasos_restantes <= 0
                or direccion not in self.DIRECCIONES):
            return False

        destino = (self.jugador[0] + direccion[0], self.jugador[1] + direccion[1])
        if destino not in self.laberinto.vecinos_accesibles(self.jugador):
            return False

        self.jugador = destino
        self.pasos_restantes -= 1
        if destino == self.fantasma:
            self.estado = self.DERROTA
        elif destino == (14, 14):
            self.estado = self.VICTORIA
        elif self.pasos_restantes == 0:
            self.terminar_turno_jugador()
        return True

    def terminar_turno_jugador(self):
        if self.estado != self.JUGADOR_MOVER:
            return False

        if self.fantasma is None:
            distancias = self.laberinto.distancias_desde(self.jugador)
            candidatas = [
                casilla for casilla, distancia in distancias.items()
                if distancia >= 6 and casilla != (14, 14)
            ]
            if not candidatas:
                raise ValueError("No hay una casilla segura para el fantasma.")
            self.fantasma = self.azar_logico.choice(candidatas)
            self.estado = self.APARECE_FANTASMA
        else:
            self.estado = self.FANTASMA_TIRAR
        return True

    def terminar_aparicion_fantasma(self):
        if self.estado != self.APARECE_FANTASMA:
            return False
        self.estado = self.FANTASMA_TIRAR
        return True

    def tirar_fantasma(self):
        if self.estado != self.FANTASMA_TIRAR:
            return None
        valor = self.dado_fantasma.tirar()
        self.estado = self.DADO_FANTASMA
        return valor

    def terminar_dado_fantasma(self):
        if self.estado != self.DADO_FANTASMA or self.dado_fantasma.animando:
            return False
        self.camino_fantasma, self.traza_fantasma = buscar_camino_con_traza(
            self.laberinto, self.fantasma, self.jugador
        )
        self.estado = self.FANTASMA_BUSCA
        return True

    def terminar_busqueda_fantasma(self):
        if self.estado != self.FANTASMA_BUSCA:
            return False
        if self.fantasma == self.jugador:
            self.estado = self.DERROTA
            return True

        self.indice_fantasma = 0
        self.pasos_fantasma = min(self.dado_fantasma.valor, len(self.camino_fantasma))
        if self.pasos_fantasma == 0:
            self._terminar_turno_fantasma()
        else:
            self.estado = self.FANTASMA_MOVER
        return True

    def mover_fantasma_paso(self):
        if self.estado != self.FANTASMA_MOVER or self.pasos_fantasma <= 0:
            return False

        destino = self.camino_fantasma[self.indice_fantasma]
        self.direccion_fantasma = (
            destino[0] - self.fantasma[0], destino[1] - self.fantasma[1]
        )
        self.fantasma = destino
        self.indice_fantasma += 1
        self.pasos_fantasma -= 1

        if self.fantasma == self.jugador:
            self.estado = self.DERROTA
        elif self.pasos_fantasma == 0:
            self._terminar_turno_fantasma()
        return True

    def _terminar_turno_fantasma(self):
        self.turno += 1
        self.estado = self.JUGADOR_TIRAR

    def reiniciar(self):
        if self.estado not in (self.VICTORIA, self.DERROTA):
            return False
        self._restablecer()
        return True
