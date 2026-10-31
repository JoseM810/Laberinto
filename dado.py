"""Tiradas lógicas y animación independiente de las caras del dado."""

import random


class Dado:
    def __init__(self, azar_logico, azar_visual=None):
        self._azar_logico = azar_logico
        self._azar_visual = azar_visual if azar_visual is not None else random.Random()
        self.valor = None
        self.cara = None
        self.animando = False
        self._tiempo = 0.0
        self._proxima_cara = 0.06

    def tirar(self):
        if self.animando:
            return None

        self.valor = self._azar_logico.randint(1, 6)
        self.cara = self._azar_visual.randint(1, 6)
        self._tiempo = 0.0
        self._proxima_cara = 0.06
        self.animando = True
        return self.valor

    def actualizar(self, delta):
        if not self.animando:
            return False

        self._tiempo += max(0.0, delta)
        if self._tiempo >= 0.6 - 1e-9:
            self._tiempo = 0.6
            self.animando = False
            self.cara = self.valor
            return True

        while self._tiempo + 1e-9 >= self._proxima_cara:
            self.cara = self._azar_visual.randint(1, 6)
            self._proxima_cara += 0.06
        return False
