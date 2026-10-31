from fantasma_ia import Evento
from visualizador import ReproductorTraza


def traza_con_retroceso():
    inicio = (0, 0)
    callejon = (1, 0)
    destino = (1, 1)
    return [
        Evento("apilar", inicio, (inicio,)),
        Evento("apilar", callejon, (inicio, callejon)),
        Evento("desapilar", callejon, (inicio,)),
        Evento("apilar", destino, (inicio, destino)),
        Evento("encontrado", destino, (inicio, destino)),
    ]


def test_actualizar_reproduce_eventos_y_contadores_en_orden():
    reproductor = ReproductorTraza(traza_con_retroceso())

    reproductor.actualizar(0.79)
    assert reproductor.evento_actual is None
    reproductor.actualizar(0.01)
    assert reproductor.evento_actual.tipo == "apilar"
    assert reproductor.pila_visible == ((0, 0),)
    assert reproductor.apilados == 1
    assert reproductor.profundidad_maxima == 1

    reproductor.actualizar(reproductor.intervalo)
    assert reproductor.pila_visible == ((0, 0), (1, 0))
    assert reproductor.apilados == 2
    reproductor.actualizar(reproductor.intervalo)
    assert reproductor.pila_visible == ((0, 0),)
    assert reproductor.desapilados == 1


def test_marca_casillas_en_pila_y_descartadas():
    reproductor = ReproductorTraza(traza_con_retroceso())
    reproductor.saltar()

    assert reproductor.estado_casilla((0, 0)) == "en_pila"
    assert reproductor.estado_casilla((1, 0)) == "descartada"
    assert reproductor.estado_casilla((1, 1)) == "en_pila"
    assert reproductor.cima == (1, 1)
    assert reproductor.camino_encontrado == ((1, 1),)


def test_pausa_bloquea_tiempo_y_paso_avanza_un_solo_evento():
    reproductor = ReproductorTraza(traza_con_retroceso())
    reproductor.pausar()
    reproductor.actualizar(100)
    assert reproductor.evento_actual is None

    assert reproductor.avanzar_un_evento()
    assert reproductor.evento_actual.tipo == "apilar"
    assert reproductor.apilados == 1
    assert reproductor.avanzar_un_evento()
    assert reproductor.evento_actual.casilla == (1, 0)
    assert reproductor.apilados == 2


def test_saltar_termina_la_traza_incluso_durante_pausa():
    reproductor = ReproductorTraza(traza_con_retroceso())
    reproductor.pausar()

    reproductor.saltar()

    assert reproductor.terminado
    assert reproductor.encontrado
    assert reproductor.evento_actual.tipo == "encontrado"
    assert reproductor.pila_visible == ((0, 0), (1, 1))
    assert reproductor.apilados == 3
    assert reproductor.desapilados == 1


def test_velocidad_se_duplica_y_se_limita():
    reproductor = ReproductorTraza(traza_con_retroceso())
    for _ in range(5):
        reproductor.cambiar_velocidad(2)
    assert reproductor.velocidad == 4

    for _ in range(5):
        reproductor.cambiar_velocidad(0.5)
    assert reproductor.velocidad == 0.25


def test_visualizador_desactivado_consumo_la_traza_sin_animacion():
    reproductor = ReproductorTraza(traza_con_retroceso(), mostrar=False)

    assert reproductor.terminado
    assert reproductor.evento_actual.tipo == "encontrado"
    assert reproductor.pila_visible == ((0, 0), (1, 1))


def test_intervalo_respeta_minimo_y_no_impone_duracion_total():
    reproductor = ReproductorTraza(traza_con_retroceso())
    assert reproductor.intervalo == 0.8

    muchos_eventos = [Evento("apilar", (0, 0), ((0, 0),))] * 200
    largo = ReproductorTraza(muchos_eventos)
    assert largo.intervalo == 0.03


def test_animacion_de_evento_nunca_dura_mas_que_su_intervalo():
    reproductor = ReproductorTraza(traza_con_retroceso())
    assert reproductor.duracion_evento == 0.12
    reproductor.actualizar(0.4)
    assert reproductor.tiempo_evento == 0.4
    reproductor.actualizar(0.4)
    assert reproductor.evento_actual.tipo == "apilar"
    assert reproductor.tiempo_evento == 0

    muchos = ReproductorTraza([Evento("apilar", (0, 0), ((0, 0),))] * 200)
    assert muchos.duracion_evento == 0.03


def test_origen_igual_a_destino_y_traza_vacia():
    casilla = (4, 4)
    reproductor = ReproductorTraza([
        Evento("apilar", casilla, (casilla,)),
        Evento("encontrado", casilla, (casilla,)),
    ])
    reproductor.saltar()
    assert reproductor.camino_encontrado == ()
    assert reproductor.pila_visible == (casilla,)

    vacio = ReproductorTraza([])
    assert vacio.terminado
    assert vacio.evento_actual is None
    assert vacio.pila_visible == ()
