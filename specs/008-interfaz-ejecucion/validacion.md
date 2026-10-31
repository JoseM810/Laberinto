# Validación: interfaz y ejecución

Entorno: Windows, Python 3.13.17, pygame 2.6.1, SDL 2.28.4.

Comando de integración:

```powershell
$env:SDL_VIDEODRIVER='dummy'; .venv\Scripts\python.exe -m pytest tests/test_visualizador.py tests/test_aplicacion.py -q --basetemp work\pytest-spec-final
```

Resultado real: `16 passed in 0.53s`. Incluye semilla idéntica a 30 y 60 FPS a través
de varias rondas, controles de menú, dibujo SDL y cierre.

Comando final de pruebas y cobertura:

```powershell
$env:SDL_VIDEODRIVER='dummy'; .venv\Scripts\python.exe -m pytest tests --cov=laberinto --cov=fantasma_ia --cov=visualizador --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80 -q --basetemp work\pytest-final5
```

Resultado real: `272 passed in 7.53s`; cobertura total 95.95 %. Cobertura por módulo:
`laberinto.py` 100 %, `fantasma_ia.py` 100 %, `visualizador.py` 95 %, `dado.py` 100 %
y `juego.py` 91 %.

`python main.py --help` se ejecutó correctamente y presenta `--semilla`. Las pruebas
usan `SDL_VIDEODRIVER=dummy`; la ventana y el bucle se prueban en esta máquina, no se
declara rendimiento medido en otros sistemas. Se usa el mapa fijo 2 por decisión del
usuario; no se implementan generación ni selección de mapas de la spec 002.
