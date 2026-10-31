"""Dibujo de la interfaz con primitivas de pygame."""

import pygame

import config


class Dibujante:
    def __init__(self):
        self.fuentes = {}

    def fuente(self, tamano):
        if tamano not in self.fuentes:
            self.fuentes[tamano] = pygame.font.Font(None, tamano)
        return self.fuentes[tamano]

    def texto(self, superficie, mensaje, posicion, tamano=22, color=config.NEGRO, centro=False):
        imagen = self.fuente(tamano).render(str(mensaje), True, color)
        rectangulo = imagen.get_rect()
        if centro:
            rectangulo.center = posicion
        else:
            rectangulo.topleft = posicion
        superficie.blit(imagen, rectangulo)

    def dibujar(self, superficie, app):
        superficie.fill(config.BLANCO)
        if app.pantalla == "MENU":
            self.texto(superficie, "El Laberinto del Fantasma", (460, 250), 48, centro=True)
            self.texto(superficie, "Mapa fijo: laberinto 2", (460, 330), 28, centro=True)
            self.texto(superficie, f"V: visualizador {'ACTIVADO' if app.mostrar_traza else 'DESACTIVADO'}", (460, 390), 24, centro=True)
            self.texto(superficie, "ENTER para comenzar · ESC para salir", (460, 455), 24, centro=True)
            return

        partida = app.partida
        if partida is None:
            return
        self._tablero(superficie, partida, app.reproductor)
        self._panel(superficie, partida, app.reproductor)
        pygame.draw.rect(superficie, config.BLANCO, (0, 640, 920, 100))
        self.texto(superficie, f"Turno: {partida.turno}", (20, 665), 25)
        self.texto(superficie, f"Dado jugador: {partida.dado_jugador.valor or '-'}", (190, 665), 25)
        self.texto(superficie, f"Dado fantasma: {partida.dado_fantasma.valor or '-'}", (400, 665), 25)
        self.texto(superficie, app.mensaje, (20, 705), 20)
        if partida.estado in (partida.VICTORIA, partida.DERROTA):
            capa = pygame.Surface((640, 640), pygame.SRCALPHA)
            capa.fill((0, 0, 0, 160))
            superficie.blit(capa, (0, 0))
            gano = partida.estado == partida.VICTORIA
            self.texto(superficie, "¡HAS GANADO!" if gano else "GAME OVER", (320, 280), 64,
                       (80, 240, 100) if gano else (255, 80, 80), True)
            self.texto(superficie, f"Turnos: {partida.turno} · R reiniciar · M/ESC menú", (320, 350), 25, config.BLANCO, True)

    def _tablero(self, superficie, partida, reproductor):
        marcas = reproductor if reproductor else None
        camino = set(partida.camino_fantasma)
        for fila in range(15):
            for columna in range(15):
                casilla = (columna, fila)
                x, y = 20 + columna * 40, 20 + fila * 40
                color = config.ENTRADA if casilla == (0, 0) else config.META if casilla == (14, 14) else None
                if marcas and marcas.estado_casilla(casilla) == "en_pila":
                    color = config.NARANJA
                elif marcas and marcas.estado_casilla(casilla) == "descartada":
                    color = config.DESCARTADA
                if casilla in camino:
                    color = config.CAMINO
                if color:
                    pygame.draw.rect(superficie, color, (x, y, 40, 40))
                if casilla == (14, 14):
                    self.texto(superficie, "META", (x + 2, y + 12), 16)
                paredes = ((0, -1, x, y, x + 40, y), (1, 0, x + 40, y, x + 40, y + 40),
                           (0, 1, x, y + 40, x + 40, y + 40), (-1, 0, x, y, x, y + 40))
                for dc, df, x1, y1, x2, y2 in paredes:
                    if (casilla == (0, 0) and (dc, df) == (-1, 0)
                            or casilla == (14, 14) and (dc, df) == (1, 0)):
                        continue
                    vecino = (columna + dc, fila + df)
                    cerrado = not (0 <= vecino[0] < 15 and 0 <= vecino[1] < 15)
                    if not cerrado:
                        cerrado = vecino not in partida.laberinto.vecinos_accesibles(casilla)
                    if cerrado:
                        pygame.draw.line(superficie, config.NEGRO, (x1, y1), (x2, y2), 4)
        if marcas and marcas.cima:
            x, y = marcas.cima
            pygame.draw.rect(superficie, config.BORDE_CIMA, (20 + x * 40, 20 + y * 40, 40, 40), 3)
        self._actor(superficie, partida.jugador, config.AZUL)
        if partida.fantasma:
            self._fantasma(superficie, partida.fantasma, partida.direccion_fantasma)

    def _actor(self, superficie, casilla, color):
        x, y = 40 + casilla[0] * 40, 40 + casilla[1] * 40
        pygame.draw.circle(superficie, color, (x, y), 14)
        pygame.draw.circle(superficie, config.BLANCO, (x - 5, y - 3), 3)
        pygame.draw.circle(superficie, config.BLANCO, (x + 5, y - 3), 3)
        pygame.draw.circle(superficie, config.NEGRO, (x - 5, y - 3), 1)
        pygame.draw.circle(superficie, config.NEGRO, (x + 5, y - 3), 1)

    def _fantasma(self, superficie, casilla, direccion):
        x, y = 40 + casilla[0] * 40, 40 + casilla[1] * 40
        pygame.draw.rect(superficie, config.MORADO, (x - 15, y - 3, 30, 18))
        pygame.draw.circle(superficie, config.MORADO, (x, y - 3), 15)
        pygame.draw.polygon(superficie, config.MORADO, (
            (x - 15, y + 13), (x - 5, y + 8), (x, y + 13),
            (x + 5, y + 8), (x + 15, y + 13), (x + 15, y + 16), (x - 15, y + 16),
        ))
        dx, dy = direccion or (1, 0)
        for ojo in (-5, 5):
            ex, ey = x + ojo, y - 4
            pygame.draw.circle(superficie, config.BLANCO, (ex, ey), 4)
            pygame.draw.circle(superficie, config.NEGRO, (ex + dx, ey + dy), 2)

    def _panel(self, superficie, partida, reproductor):
        pygame.draw.rect(superficie, config.GRIS, (680, 60, 160, 460), 3, border_radius=16)
        pygame.draw.line(superficie, config.GRIS, (670, 60), (850, 60), 4)
        self.texto(superficie, "Pila del backtracking", (780, 25), 23, centro=True)
        pila = list(reproductor.pila_visible) if reproductor else []
        visibles = pila[-20:]
        evento = reproductor.evento_actual if reproductor else None
        animar_apilado = (
            evento is not None and evento.tipo == "apilar"
            and reproductor.tiempo_evento < reproductor.duracion_evento
        )
        for indice, casilla in enumerate(visibles):
            if animar_apilado and indice == len(visibles) - 1:
                continue
            y = 490 - indice * 22
            if len(pila) > 20 and indice == 0:
                etiqueta = f"… +{len(pila) - 19} más"
                color = config.DESCARTADA
            else:
                etiqueta = f"{casilla}"
                color = config.CAMINO if reproductor and reproductor.encontrado else config.NARANJA
            pygame.draw.rect(superficie, color, (690, y, 140, 20))
            self.texto(superficie, etiqueta, (760, y + 2), 16, centro=True)
        if animar_apilado:
            progreso = reproductor.tiempo_evento / reproductor.duracion_evento
            y_final = 490 - (len(visibles) - 1) * 22
            y = round(35 + (y_final - 35) * progreso)
            pygame.draw.rect(superficie, config.NARANJA, (690, y, 140, 20))
            self.texto(superficie, str(evento.casilla), (760, y + 2), 16, centro=True)
        elif (evento is not None and evento.tipo == "desapilar"
              and reproductor.tiempo_evento < reproductor.duracion_evento):
            progreso = reproductor.tiempo_evento / reproductor.duracion_evento
            y_inicio = 490 - min(len(evento.pila), 19) * 22
            y = round(y_inicio - 55 * progreso)
            pygame.draw.rect(superficie, (255, 140, 140), (690, y, 140, 20))
            self.texto(superficie, str(evento.casilla), (760, y + 2), 16, centro=True)
        self.texto(superficie, f"Apilados: {reproductor.apilados if reproductor else 0}", (660, 535), 18)
        self.texto(superficie, f"Retrocesos: {reproductor.desapilados if reproductor else 0}", (660, 560), 18)
        self.texto(superficie, app_estado(partida.estado), (660, 590), 17)


def app_estado(estado):
    return estado.replace("_", " ").title()
