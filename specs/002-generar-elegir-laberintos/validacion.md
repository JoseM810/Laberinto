# Validación: spec fuera de alcance

Esta funcionalidad no se implementó por decisión explícita del usuario. El juego carga
el laberinto 2 del catálogo, sin generar ni elegir mapas.

Comando para comprobar que el trabajo no altera el material original:

```powershell
git diff --exit-code -- laberinto.py base/
```

Resultado real: código de salida `0`; no hay cambios en `laberinto.py` ni en `base/`.
La interfaz se valida con SDL de prueba en `specs/008-interfaz-ejecucion/validacion.md`.
