# Revisión de capturas DMC3 · 2026-10-16

Revisión retrospectiva desde main local/remoto
`ec85d8b4eef4968f9788a143dea9da223d1e2c3b`, sin cambios locales previos ni
avances remotos posteriores al comprobarlo. **Sin funciones nuevas, capturas,
consultas a procesos ni repetición de PINE.** Se reutilizaron archivos privados
y el analizador publicado. La fase de estados sigue parcial, sin detector.

## Aclaraciones y alcance

El usuario aclaró que algunas pruebas anteriores mezclaron espadazos, golpes
encadenados/combos y disparos accidentales por instrucciones poco claras.
Confirmó inicialmente que las últimas pruebas con pitidos se realizaron bien.
Después añadió que **una captura con pitido pudo empezar mientras ya golpeaba**:
esperaba tener que descargar algo y la señal le tomó desprevenido. No identificó
inequívocamente cuál ni aportó tiempos de cada acción.

Esta última aclaración limita la certeza sobre el inicio, especialmente al
revisar la espada; no demuestra una causa del motion inicial ni añade disparos
o saltos a esas pruebas. Se conservan las declaraciones anteriores como
históricas. No se reescriben datos ni se inventan etiquetas por frame. Los
pitidos existentes usan Windows `winsound.Beep`; **no requieren descarga**.

## Capturas reutilizables

Identificadores abreviados de las carpetas completas de [continuidad](CONTINUIDAD-LOCAL.md).
«Coherente» significa que pasó las guardas del lector, no acción identificada.

| Captura | Coherentes / total | Uso que sí permite | Límite para la hipótesis |
|---|---|---|---|
| 023130, primera observación | 18 / 20 | Acceso y disponibilidad de candidatos | Sin etiqueta de acción; no prueba de reposo puro |
| 023401, mixta 45 s | 368 / 450 | Explorar motions/estados y rechazos | Secuencia incorrecta/repetida y minimización; posibles mezclas sin tiempos; no separa golpes, combos, disparos o saltos |
| 023634, declarada de saltos | 181 / 200 | Explorar saltos declarados y 13 timers -1.0 | Se conserva la declaración de solo saltos; la aclaración general impide elevarla a negativo decisivo. No afirmar que esta captura concreta incluyó disparos |
| 023832, plan de ataques | 192 / 200 | Datos exploratorios mixtos | Disparo inicial confirmado; no hay ventana observada para aislarlo del resto |
| 024702, espada con pitidos | 198 / 200 | Asociación manual de espada/reposo con candidatos; sin lecturas fallidas | Inicio posiblemente ya activo; no certifica exactamente tres golpes individuales delimitados ni reposo inicial limpio |
| 025054, pausa y puerta con pitidos | 236 / 300 | Invalidación/recuperación durante pausa/transición 127 → 114, con desplazamiento declarado | No es control exclusivo de caminar ni reposo; sin tiempos por acción. La última aclaración no identifica esta captura como afectada |

Las cinco parejas report.json/events.jsonl de las capturas de acciones coinciden
con los hashes de la auditoría anterior. Las seis pasan análisis JSON, sesión,
secuencia, reloj monotónico y contadores. Esto acredita consistencia y ausencia
de cambios respecto a esa referencia, **no ejecución perfecta ni autenticidad
criptográfica de las acciones**. No hay marcas observadas de cada golpe en
annotations.jsonl en estas capturas.

## Qué muestra realmente la espada con pitidos

En 024702 ambos pares de motion coinciden. Hay cuatro intervalos brutos con
grupo/índice `(3,3)`, aproximadamente 0–1,10; 3,70–5,30; 5,80–7,40 y
8,00–9,60 s desde la primera muestra. El primero incluye dos muestras de
calentamiento y ya estaba activo al comenzar. Los tres interiores son
compatibles con la declaración de tres acciones, **sin asignación independiente
uno a uno**. Cuatro intervalos no demuestran cuatro ataques. El jugador pudo
estar golpeando al inicio, pero esa explicación no queda probada por la memoria.
El cambio a `(0,3)` cerca de 19,60 s permanece sin significado establecido.

En las 198 muestras coherentes, el campo candidato motionTimer vale **2.0**,
incluso al cambiar motion/state. Esta captura no valida un reloj de progreso de
animación. Revisar interpretación/procedencia y valores especiales antes de
segmentar golpes o combos. BUSY tampoco prueba ataque, impacto o fin de combo.

Ese tiempo cero es la primera muestra, unos 20 ms después de sampling.begin.
Este evento se escribe después del pitido inicial de 200 ms; sampling.end se
escribe antes del pitido final. Las marcas delimitan el muestreo, no cuándo el
usuario oyó la señal o actuó. A 10 Hz no hay cobertura por frame ni garantía de
registrar transiciones cortas. No se convierten horarios previstos en acciones.

## Suficiencia por acción y repeticiones que podrían hacer falta

| Hipótesis | Qué sirve ahora | Qué falta antes de afirmarla |
|---|---|---|
| Golpe individual de espada | Asociación con acciones declaradas | Inicio/reposo delimitados, comprobar motion y repetir acciones individuales con negativos; pulsaciones no prueban animaciones ni impactos |
| Combo completo | Mezclas como exploración de posibles cadenas | No hay combo concreto ni límites confirmados. Identificar arma, combo/ruta y secuencia completa observada; repetir separadamente de golpes individuales y cadenas interrumpidas |
| Disparo | Accidente declarado en 023832 | Control exclusivo; ningún intervalo actual queda identificado como disparo por memoria |
| Salto | Prueba declarada y timers rechazados | Negativo delimitado, repetición y revisión de -1; no convertir `(0,3)` o state=2 por sí solos en detector |
| Desplazamiento | Acercamiento declarado a puerta | Control exclusivo con inicio/fin observados; aquí se mezcla con pausa/transición |
| Reposo | Intervalos candidatos y reposo declarado dentro de pruebas | Control dedicado; no etiquetar automáticamente todo `(0,0)` como reposo real |
| Pausa/cambio de sala | Esa pausa, pérdida de actor/contexto y recuperación | No repetir la misma secuencia ahora; falta cobertura de otros menús/cargas para un perfil general |

Los combos son objeto de estudio propio del combate original: secuencia,
ramificaciones, interrupciones, recuperación y vuelta a reposo. No reducirlos a
varios eventos genéricos de ataque. `(3,6)` aparece solo en la mixta 023401 y no
basta para nombrar un combo ni certificar su finalización. Tampoco se conoce
aquí el arma/estilo/ruta exactos de cada prueba. Revisar esos significados antes
de pedir repeticiones que el lector todavía no puede distinguir; no se
implementa ese trabajo ahora.

## Condiciones para una futura captura, todavía no solicitada

Antes de pedir «Listo», dar una ficha explícita: hipótesis, preparación fuera
del muestreo, duración entre señales, orden, número de acciones, reposo entre
ellas y acciones prohibidas. Separar pulsación, animación de un golpe, combo
completo e impacto contra un enemigo. Para combos fijar primero arma, estilo
y combo/ruta; no inventar ahora golpes/temporización. Registrar equipo y contexto.

Se propone para una futura mejora, **sin implementarla ahora**, una señal de
preparación y señales por acción con tiempos monotónicos, explicadas antes de
empezar. Los pitidos seguirían siendo instrucciones, no ejecución observada.
La anotación monotónica manual ya disponible requiere otro operador durante la
captura; cambiar al chat alteraría foco/pausa. Una declaración posterior no
aporta tiempos precisos; no existe vídeo u observación independiente sincronizada.

Primero reutilizar pruebas y revisar campos/segmentación. Si hace falta un
control ausente, explicar el defecto concreto y proponer solo ese control con
instrucciones completas. **No se solicita otra captura ahora.**
phase2_verified=false; sin detector auténtico, reacción GOW2 o integración visual.

## Auditoría privada y reproducción

Carpeta nueva, sin sobrescribir capturas ni notas:
`D:\logs\dmc3-capture-review-20261016-031930-aa7413b5cd734d6890ea2dc42e13e5c6`.
capture-review.json incluye hashes, resúmenes y transiciones; SHA-256
`105ef1b5c57d9eec613b00b759311c3eed5d15344cb6f108964d446840a00843`.
clarification-after-review.json añade la aclaración posterior; SHA-256
`003453e2fc73d45ec62f434212ce2d6badd77fa622384c78ce2950b1f3788394`.
**Leer ambos**: el segundo limita la clasificación inicialmente confirmada
de espada, sin cambiar datos ni resultados de integridad del primero.

Para reproducir sin sobrescribir candidate-summary.json, importar `analyze` de
`tools/analyze_dmc3_capture.py` y llamar `analyze(ruta_de_captura)`; solo lee.
La CLI crea un resumen exclusivo y no reescribe uno existente. Los informes
completos quedan fuera de Git. Validación documental: diff, enlaces y
consistencia; no se repiten suites por estos cambios.
