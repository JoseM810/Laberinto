# El Laberinto del Fantasma

Se necesita Python 3.13 y pygame 2.

En Windows, desde esta carpeta:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

También se puede fijar la partida con `python main.py --semilla 123`.

Pulsa ENTER para empezar, ESPACIO para tirar, usa las flechas para moverte y ENTER
para terminar el turno. Durante la búsqueda del fantasma: P pausa, N avanza un evento,
S salta la traza y + / - cambia su velocidad. ESC vuelve al menú.
