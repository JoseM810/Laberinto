import random

from dado import Dado


class AzarFijo:
    def __init__(self, valores):
        self.valores = iter(valores)
        self.llamadas = 0

    def randint(self, minimo, maximo):
        assert (minimo, maximo) == (1, 6)
        self.llamadas += 1
        return next(self.valores)


def test_diez_mil_tiradas_son_validas_y_muestran_todas_las_caras():
    dado = Dado(random.Random(1234), random.Random(5678))
    resultados = set()

    for _ in range(10_000):
        resultados.add(dado.tirar())
        dado.actualizar(0.6)

    assert resultados == {1, 2, 3, 4, 5, 6}


def test_animacion_cambia_cara_cada_60_ms_y_fija_el_resultado_a_600_ms():
    azar_logico = AzarFijo([5])
    azar_visual = AzarFijo([1, 2])
    dado = Dado(azar_logico, azar_visual)

    assert dado.tirar() == 5
    assert dado.cara == 1
    assert not dado.actualizar(0.059)
    assert dado.cara == 1
    assert not dado.actualizar(0.001)
    assert dado.cara == 2
    assert dado.actualizar(0.54)
    assert not dado.animando
    assert dado.cara == 5


def test_tiradas_repetidas_durante_animacion_no_consumen_azar_logico():
    azar_logico = AzarFijo([4, 6])
    dado = Dado(azar_logico, AzarFijo([2]))

    assert dado.tirar() == 4
    assert dado.tirar() is None
    assert azar_logico.llamadas == 1


def test_cara_final_permanece_fija_despues_de_la_animacion():
    azar_logico = AzarFijo([3])
    azar_visual = AzarFijo([1])
    dado = Dado(azar_logico, azar_visual)

    dado.tirar()
    assert dado.actualizar(0.6)
    assert dado.cara == 3
    assert not dado.actualizar(1.0)
    assert dado.cara == 3
    assert azar_visual.llamadas == 1


def test_las_tiradas_logicas_no_cambian_entre_30_y_60_fps():
    def tirar_varias(fotogramas_por_segundo):
        azar_logico = random.Random(2468)
        azar_visual = random.Random(1357)
        dados = [Dado(azar_logico, azar_visual), Dado(azar_logico, azar_visual)]
        resultados = []
        intervalo = 1 / fotogramas_por_segundo

        for indice in range(12):
            dado = dados[indice % 2]
            resultados.append(dado.tirar())
            while dado.animando:
                dado.actualizar(intervalo)

        return resultados

    assert tirar_varias(30) == tirar_varias(60)
