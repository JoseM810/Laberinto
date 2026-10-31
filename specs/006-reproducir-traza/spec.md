# Especificación: Reproducir y controlar la explicación

**Identificador**: 006-reproducir-traza
**Creada**: 2026-10-17
**Estado**: Implementada y validada en la entrega final.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Reproducir y controlar la explicación (prioridad P1)

Como docente quiero pausar, avanzar y saltar una búsqueda para explicar cada operación de la pila.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dada una traza y un reloj controlado, cuando avanza el tiempo, entonces la pila, marcas y contadores corresponden al último evento consumido.
2. Dada una reproducción pausada, cuando solicito un paso, entonces se procesa un único evento; cuando salto, entonces se alcanza exactamente el estado final.

### Casos límite

- Salto desde pausa, salto al final, pasos repetidos al terminar y cambio de velocidad durante pausa.
- Traza de origen igual a destino y pila de profundidad 225.
- Hay una contradicción temporal pendiente: mínimo de 30 ms por evento y duración máxima aproximada de cuatro segundos no son compatibles con trazas largas.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE consumir eventos en orden y exponer evento actual, pila, cima, descartadas, camino final y contadores de apilados, retrocesos, profundidad y máximo.
- **RF-02**: Se DEBE actualizar conjuntamente la representación de pila y tablero con cada evento.
- **RF-03**: Se DEBE permitir pausa/reanudación, avance de un evento solo en pausa, salto al final y velocidad duplicada o reducida a la mitad entre ×0,25 y ×4.
- **RF-04**: Se DEBE con visualizador desactivado consumir la traza al estado final directamente y notificar finalización sin animación.
- **RF-05**: Se DEBE conservar camino y descartadas mientras camina el fantasma; borrar las marcas al tirar el jugador en su turno siguiente.
- **RF-06**: Se DEBE antes de la primera aparición exponer pila vacía y estado de espera; no dibujar ni importar pygame.

### Entidades

Reproductor, tiempo, velocidad, pausa, marcas y contadores.

### Fuera de alcance

No busca caminos ni decide la persecución; no dibuja el tarro ni sus transiciones gráficas.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-21 | `ReproductorTraza` en el instante `t` expone una `pila_visible` igual a la pila del último evento reproducido hasta `t`, y contadores coherentes con esos eventos. |
| CA-22 | `ReproductorTraza.saltar()` deja el estado igual al del último evento de la traza. |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- [004-busqueda-con-traza](../004-busqueda-con-traza/spec.md).

Bloqueo de planificación temporal: para 449 eventos, el mínimo original exige 13,47 s. Se debe aprobar si prevalece el mínimo, el límite o el agrupamiento de eventos; no se modifica la fórmula sin aprobación.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ### 8.1 Concepto
> Se usan **dos vistas sincronizadas** de la misma traza:
> 1. **El tarro (panel derecho):** la pila dibujada como un frasco vertical de vidrio. Cada casilla apilada cae al tarro como un bloque con su coordenada. Al retroceder, el bloque de la cima sale por arriba.
> 2. **El tablero:** cada casilla se colorea según su estado en la búsqueda (en la pila, descartada, explorándose ahora). Así se ve **dónde** está cada elemento de la pila.
>
> Los dos se animan con el mismo reloj: cada evento de la traza actualiza el tarro y el tablero a la vez.

> ### 8.3 Marcas sobre el tablero
> Durante la animación, en cada evento:
> - Casillas **en la pila** → relleno naranja.
> - Casillas **desapiladas** → relleno gris rosado (zona descartada).
> - **Cima** → borde naranja oscuro.
> - Al terminar: el camino encontrado queda en naranja intenso mientras el fantasma camina por él. Las casillas descartadas siguen visibles.
> - Las marcas se **borran** cuando el jugador tira el dado en su siguiente turno.
> - Las marcas se dibujan **debajo** de las paredes, el jugador y el fantasma (no tapan nada).

> ### 8.4 Velocidad y controles del visualizador
> Una búsqueda puede tener cientos de eventos, así que la velocidad se adapta:
> - Intervalo entre eventos: `max(0.03 s, 4.0 s / número_de_eventos)`, con un **tope de ~4 s** por búsqueda en velocidad normal y un mínimo de 30 ms por evento para que se alcance a ver.
> - Teclas, activas solo durante la animación de la búsqueda:
>
> | Tecla | Acción |
> |---|---|
> | `+` / `-` | Duplicar / reducir a la mitad la velocidad (×0.25 … ×4) |
> | `P` | Pausar / reanudar |
> | `N` | Con la animación pausada: avanzar **un** evento (modo paso a paso para explicar en clase) |
> | `S` | Saltar la animación (mostrar el resultado final de inmediato) |
>
> - Opción en la pantalla de inicio: `V` activa/desactiva el visualizador (por defecto **activado**). Desactivado, el panel sigue visible pero la búsqueda no se anima: muestra directamente el estado final.

> ### 8.5 Separación de responsabilidades
> - `fantasma_ia.py` genera la traza (lógica pura, sin pygame, se prueba con pytest).
> - `visualizador.py` tiene la clase `ReproductorTraza`: recibe la traza y, según el tiempo transcurrido, expone `evento_actual`, `pila_visible`, el estado de cada casilla (`"en_pila" | "descartada" | None`) y los contadores. No dibuja; se puede probar sin ventana.
> - `dibujo.py` solo pinta lo que expone `ReproductorTraza`.
