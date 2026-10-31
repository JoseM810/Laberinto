# Especificación: Iniciar, controlar y reiniciar el juego

**Identificador**: 008-interfaz-ejecucion
**Creada**: 2026-10-17
**Estado**: Implementada y validada en la entrega final.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Iniciar, controlar y reiniciar el juego (prioridad P1)

Como jugador quiero ejecutar el juego, configurar una partida y navegar entre inicio, partida y resultado.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dado el menú, cuando alterno G/V y comienzo con ENTER, entonces se crea la partida con esas opciones y se muestra su origen y estado.
2. Dada una partida finalizada, cuando pulso R, entonces comienza otra en el mismo modo; cuando vuelvo al menú, entonces puedo comenzar una nueva o salir.

### Casos límite

- Cerrar la ventana durante dado, aparición, búsqueda pausada y movimiento.
- Semilla no entera: rechazar el argumento con mensaje claro y sin iniciar una partida.
- ESC en pantallas finales: §6.5 dice salir, pero §10.4 y §11 dicen menú; requiere confirmación antes de implementar esa navegación.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE ofrecer menú con título y textos exactos de §10.1, modo generado y visualizador activado por defecto, sin vista previa.
- **RF-02**: Se DEBE si no hay catálogo válido, impedir alternar G y mostrar en rojo: No se pudo leer laberintos.json: se usarán laberintos generados.
- **RF-03**: Se DEBE interpretar controles según §10.4; ignorar los ajenos al estado, cerrar inmediatamente con X y abandonar al menú con ESC durante partida.
- **RF-04**: Se DEBE mostrar turno, estado, origen del laberinto y últimos dados separados por actor; dado de 60×60, borde de 3 y puntos negros, con animación de 003.
- **RF-05**: Se DEBE mostrar capa negra alfa 160 con ¡HAS GANADO! verde o GAME OVER rojo a 64 px, subtítulo e instrucciones R/M/ESC.
- **RF-06**: Se DEBE aceptar python main.py y opcional --semilla N; ejecutar en Python 3.10+ con pygame 2.x como única dependencia del juego.
- **RF-07**: Se DEBE separar las herramientas de prueba/cobertura de las dependencias necesarias para jugar; comprobar al menos 80 % por módulo de lógica.
- **RF-08**: Se DEBE mantener 60 FPS como objetivo de §14 en macOS, Windows y Linux; registrar equipo y medición de la validación, sin afirmar plataformas no probadas.
- **RF-09**: Se DEBE mantener todo texto propio en español salvo la cadena GAME OVER exigida y nombres obligatorios de herramientas; usar el prototipo HTML solo como referencia.

### Entidades

Pantalla, opciones del menú, entrada de usuario, HUD y salida del proceso.

### Fuera de alcance

Integra funcionalidades anteriores, sin redefinir algoritmos ni añadir sonido, sprites, guardado, multijugador o dificultad.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Menú, controles, mensajes, cierre, ejecución y reinicio se verifican según §10–§14;
  no existe un CA exclusivo para esta integración en la tabla original.

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- [002-generar-elegir-laberintos](../002-generar-elegir-laberintos/spec.md).
- [003-dados-reproducibles](../003-dados-reproducibles/spec.md).
- [005-reglas-partida](../005-reglas-partida/spec.md).
- [006-reproducir-traza](../006-reproducir-traza/spec.md).
- [007-tablero-visualizador](../007-tablero-visualizador/spec.md).

La cadena GAME OVER se conserva como requisito explícito. El historial menciona §19 pero el archivo termina en §18; la definición verificable de terminado se toma de la constitución. El criterio manual no se sustituye por pytest.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ## 10. Interfaz y pantallas
>
> ### 10.1 Pantalla de inicio
> - Título "El Laberinto del Fantasma".
> - Texto "G: laberinto [GENERADO / PREDEFINIDO AL AZAR]" (por defecto GENERADO).
> - Texto "V: visualizador de backtracking [ACTIVADO/DESACTIVADO]".
> - Texto "ENTER para comenzar".
> - Sin vista previa: el laberinto es sorpresa y se elige al pulsar ENTER.
>
> ### 10.2 Pantalla de juego
> - Laberinto, entrada, meta, marcas de la búsqueda, personaje y (si ya apareció) fantasma.
> - Panel derecho: visualizador (sección 8).
> - **Panel inferior (HUD)**, de izquierda a derecha:
>   - `Turno: N`
>   - Dado del jugador y dado del fantasma (última tirada).
>   - Estado:
>     - `"Tu turno: pulsa ESPACIO para tirar"`
>     - `"Mueve con las flechas: quedan X pasos · ENTER para terminar"`
>     - `"¡Apareció el fantasma!"` (1 s)
>     - `"El fantasma busca tu rastro…  (P pausa · N paso · S saltar · +/- velocidad)"`
>     - `"El fantasma avanza…"`
>
> ### 10.3 Pantallas finales
> - Capa semitransparente sobre el tablero (negro con alfa 160) y mensaje centrado:
>   - Victoria: **"¡HAS GANADO!"** en verde, fuente de 64 px.
>   - Derrota: **"GAME OVER"** en rojo, fuente de 64 px.
> - Subtítulo con la cantidad de turnos y las instrucciones `R / M / ESC`.
>
> ### 10.4 Controles
>
> | Tecla | Acción | Activa en |
> |---|---|---|
> | `G` | Alternar origen del laberinto (generado / predefinido al azar) | Inicio |
> | `V` | Activar/desactivar visualizador | Inicio |
> | `ENTER` | Comenzar partida | Inicio |
> | `ESPACIO` | Tirar el dado | Turno del jugador (antes de tirar) |
> | `↑ ↓ ← →` | Mover un paso | Turno del jugador (con pasos restantes) |
> | `ENTER` | Terminar el turno antes de tiempo | Turno del jugador (después de tirar) |
> | `P` / `N` / `S` / `+` / `-` | Controles del visualizador (8.4) | Búsqueda del fantasma |
> | `R` | Reiniciar | Fin de partida |
> | `M` | Volver al menú | Fin de partida |
> | `ESC` | Volver al menú (la partida en curso se abandona sin confirmar) | Partida y pantallas finales |
> | `ESC` | Salir del juego | Inicio |
> | Cerrar ventana (X) | Salir de inmediato, sin confirmar (no hay nada que guardar) | Siempre |
>
> Las teclas que no correspondan al estado actual se ignoran (por ejemplo, flechas mientras se mueve el fantasma).

> ## 12. Arquitectura (archivos)
>
> ```
> Laberinto/
> ├── SPEC.md                  # este documento
> ├── generar_laberintos.py    # ya existe: genera laberintos.json y PNG
> ├── laberintos.json          # ya existe: datos de los 5 laberintos
> ├── config.py                # constantes de las secciones 4.1, 4.2 y 8
> ├── laberinto.py             # clase Laberinto: carga JSON, generar_backtracking(), elegir_al_azar(), hay_pared(), vecinos_accesibles(), distancias_desde()
> ├── simulacion.html          # prototipo visual de referencia (sección 18), no es parte del juego Python
> ├── fantasma_ia.py           # buscar_camino_con_traza() / buscar_camino() (sección 7)
> ├── visualizador.py          # ReproductorTraza: reproduce la traza en el tiempo (sección 8.5)
> ├── dado.py                  # clase Dado: tirar(), estado de animación
> ├── juego.py                 # lógica pura: estado, turnos, reglas, aparición del fantasma
> ├── dibujo.py                # todo el render con pygame (tablero, tarro, HUD, pantallas)
> ├── main.py                  # bucle principal, eventos de teclado, argumento --semilla
> ├── requirements.txt         # pygame, pytest, pytest-cov
> └── tests/
>     ├── test_laberinto.py
>     ├── test_fantasma_ia.py
>     ├── test_visualizador.py
>     ├── test_dado.py
>     └── test_juego.py
> ```
>
> **Regla de diseño:** `juego.py`, `laberinto.py`, `fantasma_ia.py`, `visualizador.py` y `dado.py` **no importan pygame**, así que se pueden probar con `pytest` sin abrir ventana. Solo `dibujo.py` y `main.py` usan pygame.
>
> **Ejecución (única forma de distribución):**
> ```
> pip install -r requirements.txt
> python main.py [--semilla N]
> ```
> No se empaqueta como ejecutable.
>
> **Pruebas:**
> ```
> pytest --cov=laberinto --cov=fantasma_ia --cov=visualizador --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80
> ```

> ## 14. Requisitos no funcionales
> - **RNF-1** El juego corre a 60 FPS en un portátil normal (macOS, Windows o Linux), también durante la animación del tarro.
> - **RNF-2** El código, los textos de la interfaz y los comentarios están en español.
> - **RNF-3** Sin recursos externos (imágenes, sonidos ni fuentes descargadas): fuente por defecto de pygame. Si el emoji 👻 no se ve con la fuente por defecto, se usa la etiqueta "inicio".
> - **RNF-4** `buscar_camino_con_traza` responde en menos de 10 ms en un laberinto de 15×15.

> ## 18. Simulación de referencia
> `simulacion.html` es un prototipo jugable en el navegador. Implementa esta spec (tablero, dado, fantasma, captura, tarro y marcas en el tablero) para validar la experiencia **antes** de escribir el código Python. No es el entregable: si la simulación y esta spec no coinciden, **manda la spec**. Cualquier cambio que surja al probar la simulación se registra primero aquí (nueva versión) y después se aplica.
