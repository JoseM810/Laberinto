# Especificación: Ver tablero, actores y pila sincronizada

**Identificador**: 007-tablero-visualizador
**Creada**: 2026-10-17
**Estado**: Implementada y validada en la entrega final.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Ver tablero, actores y pila sincronizada (prioridad P1)

Como estudiante quiero ver el laberinto y la pila a la vez para relacionar el camino con la estructura LIFO.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dado un tablero con búsqueda activa, cuando se representa, entonces las marcas quedan debajo de paredes y actores y la cima coincide en tarro y tablero.
2. Dada una pila de más de veinte casillas, cuando se representa, entonces aparecen las diecinueve superiores y un bloque inferior que indica cuántas se ocultan.

### Casos límite

- Pila vacía, veinte y veintiún elementos y profundidad máxima.
- Texto de coordenadas, contadores altos y ausencia de soporte para emoji.
- Actores encima del camino resaltado y animación de retroceso sin tapar paredes.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE mostrar ventana de 920×740, tablero de 15×15 celdas de 40 px, margen 20, paredes de 4 px, panel derecho de 280×640 y HUD de 920×100.
- **RF-02**: Se DEBE respetar la paleta completa de §4.2, la entrada azul clara, meta verde con META y el orden de capas.
- **RF-03**: Se DEBE dibujar jugador azul con ojos y fantasma morado de 30×32 con cabeza semicircular, base ondulada de tres picos y mirada en la última dirección.
- **RF-04**: Se DEBE dibujar tarro, bloques con coordenadas, base/inicio, flecha de cima, contadores y explicación del evento con las medidas de §8.2.
- **RF-05**: Se DEBE mostrar como máximo veinte bloques, incluyendo resumen de desbordamiento; al apilar caer en 0,12 s, al desapilar subir/desvanecer en 0,12 s y al encontrar parpadear dos veces.
- **RF-06**: Se DEBE dibujar únicamente con primitivas y fuente predeterminada; usar inicio si el emoji no está disponible.
- **RF-07**: Se DEBE representar el estado recibido, sin ejecutar búsquedas ni modificar reglas; sincronizar las dos vistas con el mismo evento.

### Entidades

Vista del tablero, actor, tarro, bloque y estado de representación.

### Fuera de alcance

No incluye navegación de pantallas, eventos de teclado ni decisiones de juego; estos pertenecen a 008.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-23 | La ventana mide 920 × 740 px, las paredes se dibujan con 4 px y el tarro muestra como máximo 20 bloques con indicador `… +K más`. **Revisión visual manual** (ver 13.1). |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- [001-modelo-laberintos](../001-modelo-laberintos/spec.md).
- [006-reproducir-traza](../006-reproducir-traza/spec.md).

La apariencia del fantasma se toma de §5.2 y los colores/tiempos de §8. Las dimensiones se revisan manualmente con evidencia. RNF-1 se comprueba en integración con 008, incluida animación.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ### 4.1 Dimensiones (valores fijos, definidos como constantes en `config.py`)
>
> | Constante | Valor | Descripción |
> |---|---|---|
> | `N` | 15 | Casillas por lado |
> | `TAM_CELDA` | 40 px | Lado de cada casilla |
> | `GROSOR_PARED` | 4 px | Grosor de las líneas del laberinto |
> | `MARGEN` | 20 px | Espacio blanco alrededor del laberinto |
> | `ANCHO_PANEL_PILA` | 280 px | Panel derecho del visualizador de backtracking |
> | `ALTO_PANEL` | 100 px | Panel inferior de información (HUD), a todo lo ancho |
> | Área del laberinto | 600 × 600 px | `N × TAM_CELDA`, con origen en `(20, 20)` |
> | Ventana | **920 × 740 px** | ancho `640 + 280`; alto `640 + 100` |
> | `FPS` | 60 | Cuadros por segundo |
>
> Distribución:
> ```
> ┌──────────────────────────────┬──────────────┐
> │                              │  Panel pila  │
> │   Laberinto 600×600          │  (tarro +    │
> │   (+ margen 20 px)           │  contadores) │
> │        640 × 640             │   280 × 640  │
> ├──────────────────────────────┴──────────────┤
> │  HUD: turno, dados, estado      920 × 100   │
> └─────────────────────────────────────────────┘
> ```
>
> Posición en pantalla de la esquina superior izquierda de la casilla `(c, f)`:
> `x = MARGEN + c × TAM_CELDA`, `y = MARGEN + f × TAM_CELDA`.

> ### 4.2 Colores
>
> | Elemento | Color (RGB) |
> |---|---|
> | Fondo | Blanco `(255, 255, 255)` |
> | Paredes | Negro `(0, 0, 0)` |
> | Entrada (relleno de casilla) | Azul claro `(210, 225, 255)` |
> | Meta (relleno de casilla) | Verde claro `(200, 240, 200)` con texto "META" |
> | Personaje | Azul `(30, 90, 220)` |
> | Fantasma | Morado `(140, 60, 200)` |
> | Casilla **en la pila** (camino que se explora) | Naranja `(255, 190, 90)` |
> | Casilla **descartada** (se retrocedió desde ella) | Gris rosado `(230, 200, 200)` |
> | Casilla que **se explora ahora** (cima de la pila) | Borde naranja oscuro `(220, 110, 0)`, 3 px |
> | Camino **encontrado** | Naranja intenso `(255, 150, 30)` |
> | Tarro (contorno) | Gris `(120, 120, 120)`, 3 px |
> | Texto | Negro |

> ### 5.1 Personaje (jugador)
> - **Forma:** círculo azul de radio 14 px, centrado en su casilla, con dos ojos blancos (radio 3 px) y pupilas negras.
> - **Posición inicial:** la entrada `(0,0)`.
> - **Control:** flechas del teclado ↑ ↓ ← →.

> ### 8.2 El tarro (panel derecho, x = 640..920)
>
> | Elemento | Especificación |
> |---|---|
> | Título | "Pila del backtracking" en y = 20, centrado en el panel |
> | Tarro | Contorno gris de 3 px, 160 px de ancho × 460 px de alto, centrado en el panel, de y = 60 a y = 520. Lados y fondo con esquinas inferiores redondeadas (radio 16 px) y boca abierta arriba con un borde ligeramente más ancho (180 px). |
> | Bloques | Rectángulos de 140 × 20 px con 2 px de separación, apilados **de abajo hacia arriba**. Texto centrado `(c,f)`. Caben **20 bloques** visibles. |
> | Base de la pila | El primer bloque (la casilla del fantasma) lleva el texto `(c,f) 👻` o la etiqueta "inicio". |
> | Cima | Borde naranja oscuro de 3 px y una flecha `← cima` a la derecha del tarro. |
> | Desbordamiento | Si la pila tiene más de 20 elementos, se dibujan los 19 de arriba y el bloque inferior muestra `… +K más` en gris. |
> | Animación apilar | El bloque nuevo aparece arriba de la boca del tarro y **cae** a su posición en 0.12 s. |
> | Animación desapilar | El bloque de la cima se pone rojo claro y **sube** fuera del tarro, desvaneciéndose en 0.12 s. |
> | Encontrado | Todos los bloques del tarro se pintan de naranja intenso y parpadean 2 veces. |
>
> Debajo del tarro (y = 530..640), contadores y mensaje:
> - `Apilados: A`  `Desapilados (retrocesos): R`
> - `Profundidad actual: P`  `Máxima: M`
> - Mensaje del último evento, por ejemplo:
>   - `Apilar (4,2): avanzo a un vecino libre`
>   - `Desapilar (6,3): callejón sin salida, retrocedo`
>   - `¡Encontrado! Camino de L pasos`
>
> Cuando no hay búsqueda en curso (turno del jugador antes de que aparezca el fantasma), el panel muestra el tarro vacío y el texto "Esperando al fantasma…".
