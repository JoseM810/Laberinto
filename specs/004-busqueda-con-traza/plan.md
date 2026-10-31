# Plan: búsqueda con traza

## Objetivo

Implementar la búsqueda del fantasma de la sección 7 de `base/SPEC.md` en
`fantasma_ia.py`, sin importar pygame. La función usará una pila explícita y
explorará vecinos en el orden arriba, derecha, abajo e izquierda.

## Diseño

- `Evento` será una tupla nombrada inmutable con tipo, casilla y copia de la pila.
- `buscar_camino_con_traza` devolverá el camino sin el origen y una traza completa.
- `buscar_camino` reutilizará esa búsqueda y devolverá solo el camino.
- Las pruebas usarán los mapas del catálogo y un tablero con ramas sin salida.
- No se cambiarán `laberinto.py` ni los archivos de `base/`.

## Validación

Primero se agregan y ejecutan las pruebas para observar que fallan por faltar
`fantasma_ia.py`. Después se implementa lo mínimo y se comprueban los criterios
CA-03, CA-04, CA-05 y CA-17 a CA-20, el límite de 225 casillas, el tiempo de
búsqueda menor de 10 ms y la cobertura individual del 80 % o más.

Comando previsto para esta fase:

```powershell
\.venv\Scripts\python.exe -m pytest -q --basetemp work\pytest-004
```
