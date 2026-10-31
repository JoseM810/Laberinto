# Validación: preparación

Entorno inicial: Windows, Python 3.14.7, `.venv` del repositorio. Después se
recreó `.venv` con Python 3.13.17 y pygame 2.6.1 para comprobar la versión objetivo.

## Pruebas existentes antes de implementar

Comando:

```powershell
\.venv\Scripts\python.exe -m pytest -q --basetemp work\pytest-baseline
```

Resultado real: `233 passed in 2.84s`.

Se fija `--basetemp` dentro del repositorio porque la carpeta temporal predeterminada
del entorno está bloqueada por el sandbox de Windows.

## Dependencias de desarrollo

Comando:

```powershell
\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Resultado real: instalación correcta de pytest 8.4.2 y pytest-cov 7.0.0, junto
con sus dependencias.

## Python 3.13 y pygame

Se verificó el runtime portable oficial de Python 3.13.17 porque el instalador
Windows no pudo consultar las claves de instalación del registro en este entorno.
El ejecutable quedó aislado en `work/python313`; `.venv` se creó con ese runtime.

Comandos ejecutados:

```powershell
\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt -r requirements.txt
\.venv\Scripts\python.exe -c "import sys, pygame; pygame.init(); pygame.display.set_mode((1,1)); print(sys.version.split()[0], pygame.version.ver, pygame.display.get_driver()); pygame.quit()"
$env:SDL_VIDEODRIVER = 'dummy'
\.venv\Scripts\python.exe -m pytest tests -q --basetemp work\pytest-py313
```

Resultados reales: instalación de pygame 2.6.1 y herramientas de desarrollo;
pygame abrió una pantalla `dummy` con Python 3.13.17; `233 passed in 1.31s`.

## Búsqueda con traza (Python 3.13.17)

Prueba primero, antes de crear `fantasma_ia.py`:

```powershell
\.venv\Scripts\python.exe -m pytest tests/test_fantasma_ia.py -q --basetemp work\pytest-004-red
```

Resultado real: error de colección `ModuleNotFoundError: No module named 'fantasma_ia'`;
fallo esperado porque la implementación aún no existía.

Después de implementar:

```powershell
\.venv\Scripts\python.exe -m pytest tests/test_fantasma_ia.py -q --basetemp work\pytest-004-green
\.venv\Scripts\python.exe -m pytest tests -q --basetemp work\pytest-004-all
\.venv\Scripts\python.exe -m pytest tests --cov=laberinto --cov=fantasma_ia --cov-report=term-missing --cov-fail-under=80 --basetemp work\pytest-coverage-004
```

Resultados reales: 8 pruebas de búsqueda pasan en 0,06 s; 241 pruebas totales pasan
en 2,00 s; con cobertura pasan 241 en 5,60 s. `fantasma_ia.py` alcanza 100 %
(25/25 sentencias) y `laberinto.py` 100 % (107/107 sentencias).

Comprobación adicional de tiempo y separación gráfica:

```powershell
\.venv\Scripts\python.exe work\bench_004.py
\.venv\Scripts\python.exe -S -c "import sys, fantasma_ia; assert 'pygame' not in sys.modules"
```

Resultado real: en los 225 destinos del laberinto 1, mediana de 0,448 ms y máximo
de 2,178 ms; la importación de `fantasma_ia` sin pygame termina correctamente.
