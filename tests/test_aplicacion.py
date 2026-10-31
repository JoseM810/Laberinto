import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

import config
from main import Aplicacion
from fantasma_ia import Evento
from visualizador import ReproductorTraza


def nueva_aplicacion(fps):
    pygame.init()
    pantalla = pygame.Surface((920, 740))
    return Aplicacion(semilla=781, fps=fps, superficie=pantalla)


def simular(fps):
    app = nueva_aplicacion(fps)
    app.manejar_tecla(pygame.K_RETURN)
    app.manejar_tecla(pygame.K_SPACE)
    for _ in range(fps):
        app.actualizar(1 / fps)
    app.manejar_tecla(pygame.K_RETURN)
    app.actualizar(1)
    return app.partida.dado_jugador.valor, app.partida.fantasma


def test_aplicacion_inicia_con_mapa_fijo_y_puede_dibujar():
    app = nueva_aplicacion(60)
    assert app.pantalla == "MENU"
    app.dibujar()
    app.manejar_tecla(pygame.K_RETURN)
    assert app.pantalla == "JUEGO"
    assert app.partida.laberinto is not None


def test_dibujo_respeta_tamano_marcas_y_reutiliza_fuentes():
    app = nueva_aplicacion(60)
    app.comenzar()
    app.reproductor = ReproductorTraza(())
    app.dibujar()
    assert app.superficie.get_size() == (config.ANCHO_VENTANA, config.ALTO_VENTANA)
    assert app.superficie.get_at((55, 50))[:3] == config.ENTRADA
    assert app.superficie.get_at((20, 40))[:3] == config.ENTRADA
    assert app.superficie.get_at((619, 600))[:3] == config.META
    dibujante = app.dibujante
    assert dibujante.fuente(24) is dibujante.fuente(24)


def test_tarrito_muestra_pila_larga_sin_fallar():
    app = nueva_aplicacion(60)
    app.comenzar()
    celdas = tuple((i % 15, i // 15) for i in range(225))
    traza = [Evento("apilar", celda, celdas[:i + 1]) for i, celda in enumerate(celdas)]
    app.reproductor = ReproductorTraza(traza, mostrar=False)
    app.dibujar()


def test_misma_semilla_da_mismo_dado_y_aparicion_a_30_y_60_fps():
    assert simular(30) == simular(60)


def test_esc_en_partida_regresa_al_menu_y_en_menu_solicita_salida():
    app = nueva_aplicacion(60)
    app.manejar_tecla(pygame.K_RETURN)
    app.manejar_tecla(pygame.K_ESCAPE)
    assert app.pantalla == "MENU"
    app.manejar_tecla(pygame.K_ESCAPE)
    assert app.saliendo


def test_cerrar_ventana_solicita_salida():
    app = nueva_aplicacion(60)
    app.manejar_evento(pygame.event.Event(pygame.QUIT))
    assert app.saliendo


def simular_rondas(fps):
    app = nueva_aplicacion(fps)
    app.manejar_tecla(pygame.K_RETURN)
    tiradas = []
    apariciones = []
    app.manejar_tecla(pygame.K_SPACE)
    presiono_fin = False
    for _ in range(fps * 80):
        app.actualizar(1 / fps)
        p = app.partida
        if p.estado == p.JUGADOR_MOVER and not presiono_fin:
            tiradas.append(p.dado_jugador.valor)
            app.manejar_tecla(pygame.K_RETURN)
            presiono_fin = True
        if p.estado == p.APARECE_FANTASMA and not apariciones:
            apariciones.append(p.fantasma)
        if p.estado == p.JUGADOR_TIRAR and presiono_fin:
            if len(tiradas) >= 3:
                break
            app.manejar_tecla(pygame.K_SPACE)
            presiono_fin = False
        if p.estado in (p.VICTORIA, p.DERROTA):
            break
    return tiradas, apariciones


def test_semilla_repite_tiradas_y_apariciones_durante_varias_rondas_a_30_y_60_fps():
    resultado = simular_rondas(30)
    assert resultado == simular_rondas(60)
    assert len(resultado[0]) >= 2
    assert len(resultado[1]) == 1

