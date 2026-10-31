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

La validación de la búsqueda se añadirá aquí después de ejecutar primero las pruebas
nuevas y comprobar su fallo esperado.
