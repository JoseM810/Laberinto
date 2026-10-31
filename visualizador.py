"""Reproducción temporal de una traza, independiente de pygame."""


class ReproductorTraza:
    def __init__(self, traza=(), mostrar=True):
        self.traza = tuple(traza)
        self.intervalo = max(0.03, 4.0 / len(self.traza)) if self.traza else 0.03
        self.velocidad = 1.0
        self.pausado = False
        self.evento_actual = None
        self.pila_visible = ()
        self.camino_encontrado = ()
        self.encontrado = False
        self.apilados = 0
        self.desapilados = 0
        self.profundidad_maxima = 0
        self._en_pila = set()
        self._descartadas = set()
        self._indice = 0
        self._acumulado = 0.0
        self.terminado = not self.traza

        if not mostrar:
            self.saltar()

    @property
    def cima(self):
        return self.pila_visible[-1] if self.pila_visible else None

    @property
    def tiempo_evento(self):
        return self._acumulado

    @property
    def duracion_evento(self):
        return min(0.12, self.intervalo / self.velocidad)

    def estado_casilla(self, casilla):
        if casilla in self._en_pila:
            return "en_pila"
        if casilla in self._descartadas:
            return "descartada"
        return None

    def actualizar(self, delta):
        if self.terminado or self.pausado:
            return

        self._acumulado += max(0.0, delta) * self.velocidad
        while self._acumulado + 1e-9 >= self.intervalo and not self.terminado:
            self._acumulado -= self.intervalo
            self._consumir_evento()

    def pausar(self):
        self.pausado = True

    def reanudar(self):
        self.pausado = False

    def avanzar_un_evento(self):
        if not self.pausado or self.terminado:
            return False
        self._acumulado = 0.0
        self._consumir_evento()
        return True

    def cambiar_velocidad(self, factor):
        self.velocidad = min(4.0, max(0.25, self.velocidad * factor))
        return self.velocidad

    def saltar(self):
        while not self.terminado:
            self._consumir_evento()
        self._acumulado = 0.0

    def _consumir_evento(self):
        if self._indice >= len(self.traza):
            self.terminado = True
            return

        evento = self.traza[self._indice]
        self._indice += 1
        self.evento_actual = evento
        self.pila_visible = evento.pila

        if evento.tipo == "apilar":
            self._en_pila.add(evento.casilla)
            self._descartadas.discard(evento.casilla)
            self.apilados += 1
            self.profundidad_maxima = max(self.profundidad_maxima, len(evento.pila))
        elif evento.tipo == "desapilar":
            self._en_pila.discard(evento.casilla)
            self._descartadas.add(evento.casilla)
            self.desapilados += 1
        elif evento.tipo == "encontrado":
            self.encontrado = True
            self.camino_encontrado = evento.pila[1:]

        if self._indice == len(self.traza):
            self.terminado = True
