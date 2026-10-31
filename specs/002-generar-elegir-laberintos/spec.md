# Especificación: Generar y elegir un laberinto por partida

**Identificador**: 002-generar-elegir-laberintos
**Creada**: 2026-10-17
**Estado**: Fuera del alcance acordado para esta entrega.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Generar y elegir un laberinto por partida (prioridad P1)

Como jugador quiero elegir entre laberintos nuevos y predefinidos para variar cada partida sin configuraciones adicionales.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dado el modo generado predeterminado, cuando comienza una partida, entonces recibe un tablero perfecto nuevo y una identificación de su semilla.
2. Dado el modo predefinido y una partida anterior, cuando reinicio, entonces recibo otra entrada válida sin repetir inmediatamente la anterior.

### Casos límite

- Catálogo parcialmente válido: elegir solo entradas válidas.
- Con una sola entrada válida no es posible evitar repetición: decisión pendiente antes de planificar.
- La descripción dice recursivo pero el contrato exige pila explícita: se conserva el contrato iterativo.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE generar desde (0,0) con backtracking y pila explícita, eligiendo vecinos no visitados al azar; producir el mismo formato que el catálogo.
- **RF-02**: Se DEBE obtener un laberinto perfecto de 225 casillas, 224 conexiones, entrada izquierda en (0,0) y salida derecha en (14,14).
- **RF-03**: Se DEBE elegir uniformemente entre los cinco predefinidos en la primera selección y entre los elegibles distintos del anterior al reiniciar.
- **RF-04**: Se DEBE usar modo generado por defecto; seleccionar o generar solo al comenzar o reiniciar la partida, conservando el modo.
- **RF-05**: Se DEBE si no hay catálogo válido, desactivar el modo predefinido y ofrecer siempre generación sin cerrar el juego.
- **RF-06**: Se DEBE exponer origen e identificación para el menú y HUD; consumir únicamente la fuente aleatoria lógica de la partida.

### Entidades

Modo, selección, semilla e identidad del laberinto anterior.

### Fuera de alcance

No dibuja el menú ni HUD, no calcula persecución y no implementa la herramienta de exportación de PNG.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-25 | 100 laberintos generados con `generar_backtracking` tienen exactamente 224 pasos abiertos, todas las casillas conectadas y camino de `(0,0)` a `(14,14)`. Cada uno se genera en menos de 50 ms. |
| CA-26 | En modo predefinido, 1 000 elecciones al azar usan los 5 laberintos y nunca repiten dos veces seguidas el mismo. |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- [001-modelo-laberintos](../001-modelo-laberintos/spec.md).

Reutilizar el algoritmo de base/generar_laberintos.py sin alterar los archivos base. El eventual mantenimiento del generador es trabajo técnico asociado, sin introducir dependencias de ejecución.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ### 4.3 Origen del laberinto (al azar en cada partida)
>
> Cada partida usa un laberinto elegido **al azar**. En la pantalla de inicio, la tecla `G` alterna entre dos modos:
>
> | Modo | Comportamiento | Por defecto |
> |---|---|---|
> | **Generado** | Se genera un laberinto nuevo de 15×15 con **backtracking recursivo** (el mismo algoritmo del laberinto #1). Prácticamente nunca se repite. | **Sí** |
> | **Predefinido** | Se elige al azar (uniforme) uno de los 5 laberintos de `laberintos.json`. | No |
>
> - Al reiniciar con `R` se elige **otro** laberinto al azar con el mismo modo. En modo predefinido no se repite el laberinto inmediatamente anterior.
> - El HUD muestra el origen: `Laberinto: generado #<semilla>` o `Laberinto: predefinido 3 (Kruskal)`.
> - **Generación (contrato):** `generar_backtracking(rnd: random.Random) -> Laberinto`. Empieza en `(0,0)`, usa una pila explícita y en cada paso elige un vecino no visitado al azar; si no hay vecinos libres, desapila. Así resultan exactamente `N×N − 1 = 224` pasos abiertos (laberinto perfecto). Debe tardar menos de 50 ms.
> - El código de generación se reutiliza de `generar_laberintos.py` (función `backtracker`), movido a `laberinto.py`. El script generador lo importa desde ahí.
>
> **Respaldo si `laberintos.json` falla:**
> - Al iniciar, el juego valida el archivo. Una entrada es válida si su `grid` tiene 31 filas de 31 caracteres, solo usa `'#'` y `' '`, y forma un laberinto perfecto (224 pasos abiertos y todas las casillas conectadas). Las entradas inválidas se ignoran.
> - Si el archivo no existe, no es JSON válido o no queda ninguna entrada válida:
>   - el modo **predefinido** se desactiva y `G` deja de alternar;
>   - el juego usa siempre el modo **generado**;
>   - la pantalla de inicio muestra en rojo: `"No se pudo leer laberintos.json: se usarán laberintos generados"`.
> - El juego **nunca** se cierra por este motivo.
>
> **Formato de los predefinidos:**
> - El juego **carga** `laberintos.json` (ya existe). Cada entrada tiene `grid`: 31 cadenas de 31 caracteres, `'#'` = pared y `' '` = camino. Un laberinto generado se convierte al mismo formato `grid`, así que el resto del juego no distingue el origen.
> - Correspondencia casilla ↔ grid: la casilla `(c, f)` está en `grid[2f+1][2c+1]`.
> - Hay pared entre dos casillas vecinas `A` y `B` si `grid[fA+fB+1][cA+cB+1] == '#'`.
> - Al dibujar, cada `'#'` que separa dos casillas se pinta como una línea negra de `GROSOR_PARED` px sobre el borde compartido (mismo estilo que las imágenes PNG).
> - Todos los laberintos (predefinidos y generados) son **perfectos**: entre dos casillas cualesquiera existe **un único camino** sin repetir casillas. Esta propiedad es la que hace correcto el algoritmo del fantasma (sección 7).
