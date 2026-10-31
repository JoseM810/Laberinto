# Validación: tablero y visualizador

Comando ejecutado:

```powershell
$env:SDL_VIDEODRIVER='dummy'; .venv\Scripts\python.exe -m pytest tests/test_aplicacion.py -q --basetemp work\pytest-draw
```

Resultado real final: `7 passed in 0.57s`. También se verificó específicamente el
dibujo de la entrada y salida:

```powershell
$env:SDL_VIDEODRIVER='dummy'; .venv\Scripts\python.exe -m pytest tests/test_aplicacion.py::test_dibujo_respeta_tamano_marcas_y_reutiliza_fuentes -q --basetemp work\pytest-boundary-green2
```

Resultado real: `1 passed in 0.61s`. La suite final vuelve a pasar las 272 pruebas.
Se renderizó y revisó una captura desde una superficie pygame sin ventana. El equipo
de validación es Windows, Python 3.13.17, pygame 2.6.1 y SDL 2.28.4. El objetivo es
60 FPS; no se hizo una medición sostenida de rendimiento.
