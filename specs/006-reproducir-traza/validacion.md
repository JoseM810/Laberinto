# Validación: reproducir y controlar la traza

Comando ejecutado:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_visualizador.py -q --basetemp work\pytest-006-final
```

Resultado real: `9 passed in 0.03s`.

La cobertura conjunta final de la lógica se midió con el comando registrado en
`specs/008-interfaz-ejecucion/validacion.md`: `visualizador.py` obtuvo 95 %.
La clase no importa pygame. La duración aplicada es `max(0.03, 4/eventos)` por
evento; no se impone un máximo al tiempo total.
