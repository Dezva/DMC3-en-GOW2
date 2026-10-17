# Análisis temporal DMC3 · offline experimental

Implementado el 2026-10-16 desde main local/remoto
`a04276b29c642e1b1ce117ce662835ba5903c235`, limpio y sin avances posteriores al
consultarlo. La nueva petición autoriza implementación offline tras la revisión
de suficiencia. No requiere juegos abiertos, API Windows, PINE ni paquetes externos.
No usa memoria actual: todos los PID/direcciones que aparecen son históricos.

## Ejecutar sin alterar capturas

Desde el checkout completo, con Python 3.10 o posterior:

```powershell
$analysisPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $analysisPython .\tools\analyze_dmc3_timeline.py 'D:\logs\CAPTURA_1' 'D:\logs\CAPTURA_2'
```

Sustituir las rutas por capturas **existentes**; no ejecutar observe_dmc3.py para
obtenerlas durante la ausencia del usuario. Crea una carpeta única
`D:\logs\dmc3-timeline-FECHA-UUID`, sin añadir/sobrescribir archivos en las capturas.
`--output-root` permite otro destino para tests; rechaza destinos dentro de una
captura. Máximo 32 entradas, 6000 muestras por captura, 16 MiB por archivo.

Opciones de evidencia:

- `--integrity-manifest RUTA`: JSON `{"captures":{"NOMBRE_CARPETA":{"report.json":"SHA256","events.jsonl":"SHA256"}}}`.
  Debe cubrir todas las entradas y ambas fuentes; admite también session.json,
  candidate-profile.json, candidate-summary.json, manual-review.json y annotations.jsonl.
  Un hash distinto aborta antes de exportar. Sin manifiesto registra hashes
  actuales y valida estructura, **sin afirmar comparación con una referencia**.
- `--review RUTA`: contexto retrospectivo JSON, repetible; no son features del
  detector. manual-review.json y annotations.jsonl locales se cargan como
  declaraciones no verificadas. Incluir la aclaración posterior junto a la
  revisión original; no usar notas antiguas de «limpia» omitiendo la corrección.

`analyze_dmc3_capture.py` anterior queda intacto; su CLI crea un resumen dentro
de la captura. El nuevo CLI exporta todo fuera de ella y permite repetir análisis
sin reescribir candidate-summary.json. No cambia Probe-Pine.ps1 ni el perfil/lector.

## Cronología, incertidumbre y API

`tools/dmc3_temporal.py` expone:

- `load_capture(ruta, expected_hashes=None, reviews=())`: solo archivos.
- `analyze_records(report, events, name='capture', associations=())`: API pura,
  determinista; las entradas no se modifican.
- `detect_candidates(upper_runs, compatible_profile=...)`: consume los runs ya
  validados por analyze_records, no snapshots arbitrarios ni una cola de gameplay.
- `compare_captures(resultados)`: firmas de ambos motions/state, firmas superiores
  y motivos exactos de dos/tres motions dentro de un bloque; separa builds.

Rechaza captura incompleta, secuencias duplicadas/faltantes/fuera de orden,
mezcla de sesión, reloj regresivo, tiempo duplicado entre muestras, contadores
inconsistentes, JSON ambiguo/nonfinite y cadencia desconocida. **No ordena o deduplica
la entrada para hacerla pasar**. Los errores de lectura de archivos se informan;
el CLI sale 1. Un archivo de captura malformado impide exportar todo el conjunto.

Cada muestra marcada válida vuelve a comprobar campos esenciales: actor/id/
personaje, contexto Dante MAIN, dos MotionData, state u32 y timer finito dentro
de la política. Una muestra incompleta/inválida se conserva como rechazada, sin
usar valores anteriores. Esto valida el registro, **no relee páginas ni RAM**.
Rechazos originales, calentamiento, generación/actor/contexto, nuevo evento de
identidad de proceso, sampling.skipped y huecos >2,5 periodos cortan bloques.
Muestras a menos de 1/4 de periodo se rechazan; no garantizamos distinguir un
replay con reloj/contadores falsificados de valores genuinamente estables.

Segmentos estables usan ambos motions y state. Los runs superiores mantienen
una sola pareja superior aunque varíe el inferior/state: preservan state_values
y lower_motion_values; sus campos state/motion iniciales no describen todo el run.
Una bajada de timer con motion constante se registra como observación; no
certifica reinicio. Ninguna secuencia se enlaza a través de una invalidación.

Los tiempos exactos son **marcas del registro posteriores a la lectura múltiple**.
Las ventanas entre observaciones contiguas no garantizan fronteras nativas:
los campos se leen en instantes distintos y pueden cruzar frames aun pasando
las guardas de contexto. No convertir time_bracket_ns en una hora precisa de
inicio/final de acción ni en garantía matemática sobre sus frames.
observed_span_seconds mide el
tramo observado, no duración total de acción. left_censored/right_censored
indican que el límite se desconoce (captura, pérdida, pausa, hueco o cierre).
No inventar un tiempo cero de ataque al primer sample. El baseline inicial era
5 Hz; las otras cinco capturas 10 Hz, con transiciones breves posiblemente ausentes.

Cuatro niveles separados:

| Nivel | Representación | Lo que acredita |
|---|---|---|
| Observación de memoria registrada | timeline, segments, transitions, boundaries | Valores que el lector histórico registró, con validez/guardas conocidas |
| Declaración del usuario | manual_capture_intent, manual_associations, cues | Intención, relato o señal; nunca acción automática por frame |
| Hipótesis de movimiento | candidate_events, hypotheses y motivos comparados | Regla explícita, secuencias fuente, contexto, incertidumbre y alternativas |
| Ataque autenticado independientemente | authenticated_actions=[] | No hay evidencia suficiente; no se genera en esta versión |

La [regla de familia superior](dmc3-campos-investigacion.md#regla-experimental-de-familias)
solo se aplica al SHA conocido con guardas históricas de perfil aprobadas.
Build desconocida conserva cronología bruta sin esas hipótesis. Un perfil lateral
con identidad contradictoria se rechaza. BUSY, timer, pitidos y textos manuales
no son disparadores de ataques. Las cadenas exigen motions superiores distintos,
adyacentes de la misma familia y bloque (máximo 32 miembros); su combo_completed
es null, nunca completitud inferida. Un mismo motion sostenido o descenso de
timer no inventa golpes adicionales. La lista derivada se ordena por tiempo,
sin alterar la entrada. No hay eventos de impacto, daño o reacción GOW2.

## Archivos de salida

- analysis.json: fuentes/hashes, cronologías, segmentos, límites, cambios,
  cues/declaraciones, hipótesis y comparación entre capturas; flags false.
- timeline.csv: una fila por muestra, también las rechazadas; campos desconocidos
  vacíos, no ceros. Los valores parciales rechazados completos quedan en JSON.
- segments.csv, transitions.csv, candidate_events.csv y boundaries.csv:
  observaciones/hipótesis separadas; tiempos ns y/o segundos relativos indicados.
- transitions.md: resumen legible de cambios, contadores y timers.

CSV UTF-8 BOM; listas/objetos como JSON en una celda, texto peligroso para
fórmulas escapado. No importar niveles de hipótesis como órdenes de un puente.
Los informes completos siguen privados. La salida del análisis es reproducible
en contenido para iguales entradas/configuración; solo cambia la carpeta UUID.

## Resultados reales reutilizados, no capturas nuevas

**1.370 muestras**, 1.193 aceptadas y 177 rechazadas; 21 bloques, 80 segmentos
de motion/state y 63 runs superiores. Los 34 archivos históricos conservan hashes
de la auditoría previa. Nueve firmas de ambos motions/state, siete firmas superiores
y ocho motivos repetidos de dos/tres motions (sin interpretación de combo).

| Captura abreviada | Aceptadas/total | Bloques | Segmentos | Hipótesis de familia cuerpo a cuerpo / cadenas |
|---|---|---|---|---|
| 023130, baseline sin acción etiquetada | 18/20 | 1 | 1 | 0 / 0 |
| 023401, mixta exploratoria | 368/450 | 11 | 45 | 6 / 1 |
| 023634, saltos declarados exploratorios | 181/200 | 3 | 7 | 0 / 0 |
| 023832, plan espada con disparo accidental | 192/200 | 2 | 11 | 3 / 0 |
| 024702, espada con inicio incierto | 198/200 | 1 | 10 | 4 / 0 |
| 025054, pausa/movimiento/puerta | 236/300 | 3 | 6 | 0 / 0 |

Estos son contadores de hipótesis, **no golpes, combos reales, aciertos o controles
negativos certificados**. Las aclaraciones de [revisión de capturas](revision-capturas-dmc3.md)
siguen vigentes. En la mixta se estudia una adyacencia `(3,3) → (3,6)`; no se
nombra ataque ni combo. La espada conserva el primer episodio sin inicio conocido
y tres interiores compatibles con el relato, sin marcas independientes.
El cero de saltos/puerta no demuestra ausencia de falsos positivos generales.
No hay candidato ranged pese al disparo declarado en la mixta posterior.

Salida final:
`D:\logs\dmc3-timeline-20261016-231402-e35c3bbc301c4da5a0b81813aaa4f9bf`.
analysis.json SHA-256
`ab20e0f3d717ed098a506b1c8e098873cf4e70162155eceac5dec62e779e3886`.
La salida 231219 anterior precede a comparar firmas completas de segmentos;
se conserva como intermedia, no se sobrescribió. Invocación y manifiesto de
referencia están en
`D:\logs\dmc3-offline-validation-20261016-231219-b4cca074d33c45b6972ed3af9c74c594`.
Reutilizar invocation.json de esa carpeta para generar otra salida única.

## Validación y siguiente paso

```powershell
& $analysisPython -m unittest discover -s tests -p test_dmc3_temporal.py -v
```

**34 tests sintéticos correctos**, fixtures explícitamente sintéticos. Cubren
separados/cadenas, reposo/salto/no ofensivos, dos canales, actor/foco/pausa/sala/
generación, timers, retrasos/duplicados/incompletos/desorden, build incompatible,
etiquetas/pitidos, hashes, exportación intacta y reproducibilidad. Los CSV reales
se contaron contra JSON y los 34 archivos originales se rehashearon al terminar.
Log final synthetic-tests-delivery.txt en la salida final, SHA-256
`4929de99ce643112afdea035e5153b62977f68e0c8fcb45639606016d91c8a85`.
synthetic-tests.txt y synthetic-tests-final.txt permanecen como checkpoints;
el mismo caso de parser ahora comprueba overflow JSON (1e309) y captura vacía
con anotaciones, rechazadas antes de consultar sus límites.
La suite Windows/PINE anterior no se repitió: no se cambió lector, perfil o IPC.

Acceso a procesos: ninguno. Juegos/archivos originales, partidas, ISO/BIOS,
Blender y recursos preservados. Sin instaladores, hooks, elevación de lector ni
escrituras. **phase2_verified=false, authentic_attacks_detected=false**.
El [protocolo futuro](dmc3-validacion-controlada.md) es diseño sin ejecutar;
esperar las instrucciones anunciadas por el usuario antes de pruebas en juego.
