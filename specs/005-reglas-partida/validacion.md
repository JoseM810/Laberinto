# Validación: reglas de partida

Entorno: Windows, Python 3.13.17, pygame 2.6.1 instalado. `juego.py` no importa pygame.

## Pruebas primero

Antes de implementar `juego.py`:

```powershell
\.venv\Scripts\python.exe -m pytest tests/test_juego.py -q --basetemp work\pytest-005-red
```

Resultado real: error de colección `ModuleNotFoundError: No module named 'juego'`;
fallo esperado porque el módulo aún no existía.

## Validación tras implementar

```powershell
\.venv\Scripts\python.exe -m pytest tests/test_juego.py -q --basetemp work\pytest-005-green
\.venv\Scripts\python.exe -m pytest tests -q --basetemp work\pytest-005-all
\.venv\Scripts\python.exe -m pytest tests --cov=laberinto --cov=fantasma_ia --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80 --basetemp work\pytest-coverage-005
\.venv\Scripts\python.exe -S -c "import sys, juego; assert 'pygame' not in sys.modules"
```

Resultados reales: 10 pruebas de partida pasan en 0,39 s; 256 pruebas pasan en 2,29 s;
en la última corrida con cobertura pasan 256 en 6,90 s. `juego.py` alcanza 91 % (114/125 sentencias),
`dado.py` 100 % (32/32), `fantasma_ia.py` 100 % (25/25) y `laberinto.py` 100 %
(107/107). La importación sin pygame termina correctamente.

Las pruebas cubren 10 000 apariciones en posiciones aleatorias, la distancia mínima,
la meta excluida, el primer turno sin fantasma, tres rondas sucesivas, el recálculo de
la ruta desde las posiciones actuales, los dados separados por actor y la captura
después de cada paso. La IA prepara el camino en `FANTASMA_BUSCA`; los movimientos del
fantasma ocurren después, un paso por orden, hasta `min(dado, longitud del camino)`.

Como se decidió usar un único mapa fijo y excluir la spec 002, reiniciar restaura la
partida sobre el mismo mapa. La comparación integral CA-16 a 30/60 FPS queda pendiente
hasta integrar la aplicación en 008.
