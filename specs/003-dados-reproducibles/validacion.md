# Validación: dados reproducibles

Entorno: Windows, Python 3.13.17, pygame 2.6.1 instalado desde `requirements.txt`.

## Pruebas primero

Antes de implementar `dado.py`:

```powershell
\.venv\Scripts\python.exe -m pytest tests/test_dado.py -q --basetemp work\pytest-003-red
```

Resultado real: error de colección `ModuleNotFoundError: No module named 'dado'`;
fallo esperado porque el módulo aún no existía.

## Validación tras implementar

```powershell
\.venv\Scripts\python.exe -m pytest tests/test_dado.py -q --basetemp work\pytest-003-green
\.venv\Scripts\python.exe -m pytest tests -q --basetemp work\pytest-003-all
\.venv\Scripts\python.exe -m pytest tests --cov=laberinto --cov=fantasma_ia --cov=dado --cov-report=term-missing --cov-fail-under=80 --basetemp work\pytest-coverage-003
```

Resultados reales: 5 pruebas del dado pasan en 0,04 s; 246 pruebas pasan en 1,89 s;
con cobertura pasan 246 en 11,18 s. `dado.py` alcanza 100 % (32/32 sentencias),
`fantasma_ia.py` 100 % (25/25) y `laberinto.py` 100 % (107/107).

Las pruebas recorren 10 000 tiradas, comprueban que la cara final queda fija,
ignoran tiradas repetidas durante la animación y comparan la secuencia lógica con
avances de 30 y 60 FPS. La comparación integral de dados y aparición, CA-16, queda
pendiente hasta integrar `Partida` y `Aplicacion` en las specs 005/008.
