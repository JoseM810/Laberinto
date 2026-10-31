"""Aplicación pygame del laberinto del fantasma."""

import argparse
from pathlib import Path
import random

import pygame

import config
from dibujo import Dibujante
from juego import Partida
from laberinto import cargar_catalogo
from visualizador import ReproductorTraza


class Aplicacion:
    def __init__(self, semilla=None, fps=60, superficie=None):
        pygame.init()
        self.superficie = superficie or pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
        pygame.display.set_caption("El Laberinto del Fantasma")
        self.fps = fps
        self.reloj = pygame.time.Clock()
        self.dibujante = Dibujante()
        self.semilla = semilla
        self.azar_logico = random.Random(semilla)
        self.azar_visual = random.Random()
        self.entradas = cargar_catalogo(Path(__file__).parent / "base" / "laberintos.json").entradas
        self.laberinto = self.entradas[1].laberinto
        self.pantalla = "MENU"
        self.mostrar_traza = True
        self.partida = None
        self.reproductor = None
        self.saliendo = False
        self.mensaje = "Vuelve al menú con ESC"
        self._tiempo = 0.0

    def comenzar(self):
        self.partida = Partida(self.laberinto, azar_logico=self.azar_logico, azar_visual=self.azar_visual)
        self.reproductor = None
        self.pantalla = "JUEGO"
        self.mensaje = "Tu turno: pulsa ESPACIO para tirar"

    def manejar_tecla(self, tecla):
        if self.pantalla == "MENU":
            if tecla == pygame.K_RETURN:
                self.comenzar()
            elif tecla == pygame.K_v:
                self.mostrar_traza = not self.mostrar_traza
            elif tecla == pygame.K_ESCAPE:
                self.saliendo = True
            return
        p = self.partida
        if tecla == pygame.K_ESCAPE:
            self.pantalla, self.partida, self.reproductor = "MENU", None, None
            return
        if p.estado in (p.VICTORIA, p.DERROTA):
            if tecla == pygame.K_r:
                p.reiniciar()
                self.reproductor = None
            elif tecla == pygame.K_m:
                self.pantalla, self.partida = "MENU", None
            return
        if p.estado == p.JUGADOR_TIRAR and tecla == pygame.K_SPACE:
            p.tirar_jugador()
            self.mensaje = "Se está tirando el dado"
        elif p.estado == p.JUGADOR_MOVER:
            direcciones = {pygame.K_UP: (0, -1), pygame.K_RIGHT: (1, 0), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0)}
            if tecla in direcciones:
                p.mover_jugador(direcciones[tecla])
                self.mensaje = f"Mueve con las flechas: quedan {p.pasos_restantes} pasos · ENTER para terminar"
            elif tecla == pygame.K_RETURN:
                p.terminar_turno_jugador()
        elif p.estado == p.FANTASMA_BUSCA and self.reproductor:
            if tecla == pygame.K_p:
                self.reproductor.reanudar() if self.reproductor.pausado else self.reproductor.pausar()
            elif tecla == pygame.K_n:
                self.reproductor.avanzar_un_evento()
            elif tecla == pygame.K_s:
                self.reproductor.saltar()
            elif tecla in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                self.reproductor.cambiar_velocidad(2)
            elif tecla in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.reproductor.cambiar_velocidad(0.5)

    def manejar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.saliendo = True
        elif evento.type == pygame.KEYDOWN:
            self.manejar_tecla(evento.key)

    def actualizar(self, delta):
        if self.pantalla != "JUEGO":
            return
        p = self.partida
        delta = max(0.0, delta)
        if p.estado == p.DADO_JUGADOR:
            if p.dado_jugador.actualizar(delta):
                p.terminar_dado_jugador()
                self.mensaje = f"Mueve con las flechas: quedan {p.pasos_restantes} pasos · ENTER para terminar"
        elif p.estado == p.APARECE_FANTASMA:
            self._tiempo += delta
            self.mensaje = "¡Apareció el fantasma!"
            if self._tiempo >= 1:
                self._tiempo = 0
                p.terminar_aparicion_fantasma()
        elif p.estado == p.FANTASMA_TIRAR:
            p.tirar_fantasma()
        elif p.estado == p.DADO_FANTASMA:
            if p.dado_fantasma.actualizar(delta):
                p.terminar_dado_fantasma()
                self.reproductor = ReproductorTraza(p.traza_fantasma, mostrar=self.mostrar_traza)
                self.mensaje = "El fantasma busca tu rastro…  (P pausa · N paso · S saltar · +/- velocidad)"
        elif p.estado == p.FANTASMA_BUSCA:
            if self.reproductor:
                self.reproductor.actualizar(delta)
                if self.reproductor.terminado:
                    p.terminar_busqueda_fantasma()
        elif p.estado == p.FANTASMA_MOVER:
            self._tiempo += delta
            while self._tiempo >= 0.25 and p.estado == p.FANTASMA_MOVER:
                self._tiempo -= 0.25
                p.mover_fantasma_paso()
            self.mensaje = "El fantasma avanza…"
        elif p.estado == p.JUGADOR_TIRAR:
            self.mensaje = "Tu turno: pulsa ESPACIO para tirar"
        elif p.estado == p.VICTORIA:
            self.mensaje = "Llegaste a la meta"
        elif p.estado == p.DERROTA:
            self.mensaje = "El fantasma te atrapó"

    def dibujar(self):
        self.dibujante.dibujar(self.superficie, self)

    def ejecutar(self):
        while not self.saliendo:
            delta = self.reloj.tick(self.fps) / 1000
            for evento in pygame.event.get():
                self.manejar_evento(evento)
            self.actualizar(delta)
            self.dibujar()
            pygame.display.flip()
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="El Laberinto del Fantasma")
    parser.add_argument("--semilla", type=int, default=None)
    Aplicacion(semilla=parser.parse_args().semilla).ejecutar()


if __name__ == "__main__":
    main()
