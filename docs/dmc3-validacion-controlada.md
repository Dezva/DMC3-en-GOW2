# Validación controlada DMC3 · fichas y resultados

La nueva petición autoriza preparar y realizar pruebas con el usuario tras
identificar evidencia faltante. **R20, E1 y E1-R están completadas y confirmadas;
J1 se conserva exploratoria por pulsación incierta; J1-R tiene toque único y
reposo confirmados por relato posterior, con límites de lectura aún abiertos.**
Confirmar contexto y preparación antes de cada ejecución; una respuesta sobre
equipo/personaje no equivale a «Listo». No se necesita repetir PINE. El usuario
controla el juego; no instalar grabadores/hooks ni cambiar sus entradas/ventanas.

## J1-R registrada · 2026-10-17 · toque único y reposo declarados

Código **39449efbdd14dacc3e4779f1293d84dbafa82290**, main local/remoto limpio
y coincidente. Tras ficha completa y «Mismo contexto; listo para J1-R», lectura
finita con 25 s de preparación y 200 muestras/10 Hz (~20 s), tono a ~5 s.
Usuario confirmó después **un toque de salto al tono corto y reposo como se
indicó**; sugirió que una animación tras permanecer quieto explicase los rechazos.
No aportó tiempos visuales independientes ni confirmó expresamente cada otra
pregunta (tres señales, salto visible único, cada acción prohibida). No informó
incidentes. No ampliar su declaración a una validación completa del protocolo.

**192 coherentes, cuatro rechazos timer=-1.0 y cuatro calentamientos** (dos
iniciales y dos recuperación), dos bloques. Identidad/build/base redescubiertas
coincidentes con capturas anteriores: PID10688/inicio02:38:13.424527Z UTC,
base0x7FF7C6920000, SHA conocido; tokens medios sin elevar y acceso0x410.
3381 lecturas/39821 bytes, sin errores Win32/parciales, foco/contexto/actor
observados o ticks omitidos. No reutilizar esa identidad histórica.

| Tramo | Ambos motions (grupo,índice) | state | Timer aceptado en orden | Muestras |
|---|---|---|---|---|
| Inicial | (0,3) | 1 | 2.0 | 57 |
| Cambio previo a AIR de fuente | (0,4) | 1 | 9.0 | 1 |
| AIR según enum de fuente | (0,4) | 2 | 8.0, 2.0, 11.0, 5.0 | 4 |
| Recuperación tras hueco | (0,0) | 1 | 2.0 | 98 |
| Final | (0,3) | 1 | 2.0 | 32 |

Timer2.0 en 188 coherentes, **incluida una state2/(0,4)**; tampoco identifica
reposo. Secuencia durante (0,4): 9,8,2,11,5; no reloj general monótono.
Cuatro -1: uno conserva bytes [4,0,4,0]/state2 y tres [31,0,31,0]/state1.
Son errores parciales previos al recheck final, no aterrizajes coherentes.
No cambiar filtros, unir huecos, inferir pérdida de actor por generaciones,
reinicio de animación por descenso, unidades o sentinel validado.

Desde primera muestra: entrada (0,4) entre 5,791–5,901 s, state2 entre
5,901–5,991 s; última coherente del episodio6,293 s. Rechazos6,386–6,685 s,
calentamiento6,800–6,901 s, recuperación6,990 s. Fin completo no delimitable.
Marcas tras múltiples lecturas, no fronteras nativas. Mediana100,26 ms,
rango36,03–162,20 ms, sin ticks omitidos. Tono a5,00004 s/coste68,78 ms;
no hora observada de input o latencia. 10 Hz no resuelve frames/contactos.

**Hipótesis de animación de reposo del usuario:** el cambio aceptado posterior
(0,0)→(0,3), state1/timer2, ocurre entre **16,695–16,804 s**, unos diez segundos
después de los rechazos. E1/E1-R también tenían cambios aceptados durante reposo
declarado. Son hechos distintos en estos registros: no todo cambio de motion
es error o ataque. La animación concreta no se identificó visualmente en el
instante del log; no afirmar que los rechazos proceden de esa animación tardía.
«Rechazo» describe una política del lector, no mala ejecución del usuario.

Sin (3,3), BUSY o hipótesis melee/ranged aceptadas en J1-R: contraste contextual
con E1/E1-R, limitado por huecos y muestreo. Patrón similar a J1 exploratoria,
pero J1 no es otra repetición conocida del toque breve. No afirmar repetibilidad
validada de ese input, exclusividad universal, golpes detectados o duración real.
R20 y las dos E1 ya bastan para conservar sus asociaciones contextuales; no
repetirlas por rutina. **No hace falta otra captura ahora** para contrastar la
explicación de reposo tardío. Antes de una regla o nuevas pruebas, revisar uso
nativo estático del timer y las limitaciones del muestreo; tarea aún pendiente.
Combos completos/disparos siguen sin control dedicado y no se solicitan ahora.

Captura: `D:\logs\dmc3-observe-20261017-002123-b9067c1c3ea04c5fa64fa30ab76a2e45`;
report SHA `5ed52ca2bbcd3bdb918e8c58265dd19c32369f06b00998c7d2fcde92be75dae7`,
events SHA `f6d9b281f64b6f23ac6a58d78d3a63ef6c09d1072dcf308d0ddb48f22efb13b7`.
Comparación cinco capturas, JSON/CSV y j1r-review.json previo a respuesta:
`D:\logs\dmc3-timeline-20261017-002305-bcecda50b7814cfb98ea0b0d4fe5d904`;
analysis SHA `9bf8f01568ea9b2b2e5efa3892f3829d5c0f20ab2c048312c5da5452fa18d898`.
Nota posterior nueva (complementa la revisión previa sin sobrescribirla):
`D:\logs\dmc3-j1r-confirmation-20261017-002344-1af930c1df94475192ca9bbe23b64c27\manual-review.json`,
SHA `7ae85dfef1c808d40e1b42080aa668ae7df5b9cb1f0525320a5532e3259febb8`.
Cinco parejas report/events verificadas antes/después y nota J1 revalidada;
fuentes intactas. Sin código nuevo, suites repetidas, PINE o escrituras;
phase2_verified=false, authentic_attacks_detected=false, sin impacto/GOW2.

## J1 registrada · 2026-10-17 · relato posterior y límites

Desde main local/remoto limpio **0e7ea97a7c80638590d6b0244c8c57317f528d90**,
tras «Listo para J1» y la ficha completa: 25 s de preparación, 200 muestras/10 Hz,
señal corta a ~5 s y fin tras ~20 s. Esa respuesta autoriza la captura, no
demuestra un salto ejecutado. Después el usuario relató pulsar salto al sonido
corto, soltar estando en el suelo y quedar en reposo hasta el grave. Ante la
pregunta de si lo mantuvo hasta aterrizar o soltó enseguida: **«No recuerdo con
certeza»**. Conservar salto/reposo declarados, duración de pulsación desconocida.
No afirmar toque breve, mantenimiento hasta aterrizar, tres señales o ausencia
de otras acciones expresamente confirmados: el relato no resuelve todo eso.
J1 sirve como asociación exploratoria; no control limpio del protocolo previsto.
Tampoco demuestra que mantener el botón causara los valores o el hueco.

Identidad/build/base redescubiertas y coincidentes con R20/E1/E1-R: SHA conocido,
PID 10688/inicio 2026-10-17T02:38:13.424527Z, base 0x7FF7C6920000. Son datos
históricos de esta ejecución. Ambos tokens medios, sin elevar; acceso 0x410,
3369 lecturas/39645 bytes, sin errores Win32, lecturas parciales, pérdida de
foco ni cambio de contexto observado. Misión 7/sala 127/posición 2/MAIN.

**190 coherentes, seis rechazos por timer=-1.0 y cuatro de calentamiento**
(dos iniciales y dos al recuperar). Dos bloques; no unirlos a través del hueco.
El avance de generación provocado por la política no demuestra pérdida de actor.
Puntero/contexto coinciden antes y después; no hay snapshot atómico o garantía ABA.
Los pares siguientes usan **(grupo, índice)** en ambos canales:

| Tramo del registro | Motion | state | Timer aceptado | Muestras coherentes |
|---|---|---|---|---|
| Inicial | (0,3) | 1 | 2.0 | 60 |
| Cambio previo a AIR de fuente | (0,4) | 1 | 9.0, 9.0 | 2 |
| AIR según enum de fuente | (0,4) | 2 | 0.0, 12.0, 6.0, 0.0 | 4 |
| Después del hueco y calentamiento | (0,0) | 1 | 2.0 | 98 |
| Final | (0,3) | 1 | 2.0 | 26 |

Los seis errores conservan -1.0: tres con bytes motion `[4,0,4,0]`/state2,
tres con `[31,0,31,0]`/state1. Son **campos parciales**: el rechazo ocurre antes
de revalidar contexto al final, por lo que no se autentica (0,31) ni aterrizaje.
Conservarlos íntegros sin ampliar filtros. Las 184 muestras aceptadas restantes
tienen timer2.0. Los descensos 9→0, 12→6→0 no prueban reinicios de animación;
no se validan unidades, progreso, cuenta regresiva ni significado de -1.

Desde primera muestra: entrada registrada a (0,4) entre 6,090–6,195 s;
state2 entre 6,299–6,407 s; última coherente (0,4) a 6,699 s. Rechazos
6,787–7,289 s, calentamiento 7,390–7,502 s y recuperación coherente 7,598 s.
El fin del episodio queda censurado por el hueco; **no medir duración completa
del salto o aterrizaje**. Marcas posteriores a lecturas múltiples, no fronteras
nativas. Cadencia mediana 99,88 ms, rango 44,05–148,40 ms, sin ticks omitidos.
Señal corta a 5,00053 s desde reloj de muestreo, llamada ~64,15 ms; no mide input.
10 Hz alcanza para ver estas muestras, no transiciones por frame ni exclusividad.

No hay (3,3), BUSY ni hipótesis melee/ranged en las muestras aceptadas de J1.
Eso distingue los **registros** de los espadazos E1/E1-R, pero el negativo tiene
duración de pulsación incierta, relato incompleto y un hueco; no demuestra cero falsos
positivos globales. R20/E1/E1-R sí permanecen confirmadas y sin cambios.

Captura privada:
`D:\logs\dmc3-observe-20261017-000835-e67da5c481c84a9288f7503e9e571c8a`.
report SHA-256 `261d4d6352f1e9ce687097c963c2c87cbd4367dde7ca0cf84f047d4bce90f6fc`;
events SHA-256 `31a17db9503a26272268c635d014228c7b743c28fb58ac3898e463745afab9b9`.
Comparación íntegra R20/E1/E1-R/J1 (JSON/CSV y j1-review.json):
`D:\logs\dmc3-timeline-20261017-001144-2170f5e7ebf24e379924f77eabe275fd`;
analysis SHA-256 `e1602d41a4050f09772c978d7354ca6dd58ae736f936702adc76547951446d9d`.
Las cuatro parejas report/events se comprobaron contra sus hashes publicados,
antes/después del análisis; no se alteraron. j1-review.json conserva el estado
histórico de relato pendiente. Aclaración posterior en nueva carpeta privada:
`D:\logs\dmc3-j1-clarification-20261017-001819-86a6f30dd5d840449e15d5fc9a672f27\manual-review.json`,
SHA-256 `b2a67d37c16d4e61a8639b5c5dbc57b87ea22519ba7baeb1dd8aa98713d017f4`.
Incluye ambas respuestas literales, incógnitas y hashes originales revalidados.
No reescribir análisis previo ni inventar tiempos de acciones.

Siguiente: **J1-R** para obtener un registro con pulsación breve explícita.
La ambigüedad de J1 impide llamarla repetición idéntica; no compara por sí sola
duración mantenida frente a breve. Falta repetibilidad antes de asignar significado
estable a (0,4)/state2. Necesita ficha y nuevo «Listo». No repetir
espada por rutina ni intentar resolver el timer repitiendo acciones sin una
hipótesis distinguible. Investigar referencias nativas estáticas de +0x3E34
antes de cambiar perfil/filtros; sigue sin realizarse. Sin código nuevo, suites
repetidas, PINE, escrituras, impacto o reacción GOW2; fase parcial y flags false.

### Ficha J1-R utilizada: un toque de salto y soltar enseguida

Finalidad: obtener una asociación manual con salto breve sin ambigüedad sobre
mantener el botón; comprobar si reaparecen (0,4)/state2 y rechazos -1. No probar
unidades del timer ni atribuir diferencias a una causa con una sola pareja.
Mismo Dante/Rebellion/Gunslinger, misión 7 normal, mismo lugar y sin enemigos.

1. Tras nuevo «Listo», **25 s** para volver al juego, cerrar pausa y quedar quieto.
2. Pitido largo agudo: inicio de **20 s** de muestreo (200 muestras/10 Hz), reposo.
3. Único pitido corto a ~5 s: **tocar salto una sola vez y soltar de inmediato
   al despegar**; no mantener hasta volver al suelo ni volver a pulsar en el aire.
4. Aterrizar sin entradas y seguir quieto hasta pitido grave final. Se permite
   volver al chat después; nunca responder durante el registro.
5. Prohibido espada, disparos, dirección, segundo salto, lock-on, estilo,
   cambios de equipo, menús, minimizar o cambiar de ventana durante esos 20 s.
6. Después confirmar salto visible único, soltar inmediato, reposos/señales e
   incidentes. Si mantuvo el botón o hubo otra acción, conservar el error y
   reclasificar sin improvisar acciones extra.

Ejecutada después con su propio «Listo»; resultados en la sección superior.
No hubo mejora de sonido o lector, y el hueco por -1 puede
reaparecer: conservar muestras rechazadas y no prometer límites de aterrizaje.

## E1-R confirmada · historial anterior a J1

E1-R se ejecutó desde **449529a50c7c2b1b55487ec6a79406bedbbf683d** tras nueva
preparación explícita. El usuario confirmó una sola pulsación y un espadazo,
reposo antes/después y las tres señales, sin incidentes. Misma configuración,
contexto misión 7/sala 127/posición 2/MAIN e identidad redescubierta coincidente.
198 muestras coherentes, dos de calentamiento; sin errores de acceso/lectura,
foco/actor/contexto o ticks omitidos. Perfil/filtros sin cambios.

Repite la secuencia de ambos motions **(0,3) → (3,3) → (0,0) → (0,3)**, con
16 muestras (3,3), como E1. Diferencia relevante: E1-R conserva state=65537 en
15 de ellas y state=1 en la última; E1 tenía 65537 en las 16. No equiparar BUSY
y duración de motion. Puede reflejar transición nativa o lecturas entre frames:
las guardas de contexto no vuelven atómicos los campos. No atribuir una causa.

Timer=2.0 en las 198 coherentes de E1-R y en las de R20/E1 (594 en conjunto).
No muestra avance del espadazo en estas condiciones. Hay repetibilidad **contextual
asociada al relato**, no exclusividad frente a otras acciones ni ataque autenticado.
No repetir de nuevo E1 por rutina.

Marcas del registro E1-R desde primera muestra: entrada 5,996–6,098 s, salida
7,600–7,694 s; tramo de motion registrado 1,502 s. Son ventanas entre marcas
posteriores a lecturas múltiples, **no fronteras nativas exactas**. Cadencia
mediana 99,77 ms, mínimo 57,71 y máximo 165,46; no cobertura por frame.

Captura privada:
`D:\logs\dmc3-observe-20261017-000230-64edd6f4fa7548cca80686e177cb973f`.
report.json SHA-256 `a782b973e728ddd534ddfc2d69247c8b2b0c9ab515f814cdb03814e397e32628`;
events.jsonl SHA-256 `c59cd372e6b8fe38bbcb3c67ae223c798cfa47ae8a32d07d0100efb196e2b199`.
Relato en manual-review.json. Comparación R20/E1/E1-R y e1r-review.json en
`D:\logs\dmc3-timeline-20261017-000501-c0874666be3a46499af6253011f6a04b`;
analysis.json SHA-256 `11910bbcc51f0ba7913cb9b1bb41e2b9408462f15112960560bfe335a2622ace`.
No se alteraron las fuentes originales ni se repitió PINE.

### Ficha J1 utilizada (propuesta histórica)

Hipótesis mínima: comprobar si el patrón (3,3)/BUSY del espadazo aparece en una
acción distinta y contrastar el timer con el contexto donde antes apareció -1.
Las capturas viejas de saltos conservan valor exploratorio; no son un negativo
limpio con equipo/señal/una acción delimitada. No hace falta probar ahora combos
o disparos además de este control. Un J1 limpio tampoco demuestra exclusividad
global; si no reaparece -1, no se declara resuelto su significado.

Mismo lugar/equipo: Dante, Rebellion, Gunslinger, misión 7 normal, sin enemigos,
desde el suelo. **No cambiar arma/estilo ni de sala para preparar la prueba.**

1. Tras un nuevo «Listo para J1», 25 s para volver a DMC3/cerrar pausa y quedar quieto.
2. Pitido agudo largo: inicio de 20 s de registro, seguir quieto.
3. Pitido corto a ~5 s: **una pulsación de salto y soltar**, sin dirección,
   sin espada, disparo, segundo salto en aire o ataque de estilo.
4. Dejar aterrizar y permanecer sin entradas hasta el pitido grave de fin.
5. Después preguntar si hubo un solo salto visible, reposo y las tres señales;
   anotar cualquier incidente sin improvisar repeticiones durante el registro.

No lock-on, movimiento voluntario, equipo, menús, minimizar o cambiar de ventana.
Configuración existente 200 muestras/10 Hz, --lead-in-seconds 25 --beep
--action-cue-seconds 5. No ajuste nuevo de sonido, direcciones o filtros.
J1 se ejecutó después con su propio «Listo»; resultado y relato posterior
en la sección superior. La confirmación posterior E1-R no autorizaba J1.

Conservar rechazos y su causa, incluidos -1: no ampliar rango para aceptarlos.
Si el timer invalida una muestra, sus campos parciales no se presentan como
contexto finalmente revalidado. Revisar cambios de generación/calentamiento,
state y ambos motions sin unir a través de huecos. Los límites por frame y
semántica de sentinel quedan desconocidos si la evidencia no alcanza.

## Resultado R20 y ficha E1, historial de ejecución

R20 se ejecutó tras confirmación explícita de preparación. El usuario confirmó
después reposo completo y haber oído ambas señales. Dante, Rebellion activa y
Gunslinger, misión 7 normal; imagen previa sin enemigos visibles y declaración
de zona sin enemigos. El lector registró misión 7/sala 127; estilo y dificultad
son declaraciones, no campos leídos. Captura con código previo al nuevo pitido.

**200 muestras: 198 coherentes y dos de calentamiento**, un bloque, sin errores
de lectura/acceso, pérdida de foco/actor/contexto o ticks omitidos. Ambos motions
fueron grupo 0/índice 3, state=1, timer=2.0 en todas las coherentes. La asociación
manual permite decir que 2.0 también se registró durante este reposo: no es un
identificador exclusivo de ataque ni valida progreso de animación. No clasificar
todo (0,3) como reposo por una sola prueba ni reinterpretar automáticamente logs viejos.

Intervalos reales entre muestras: mediana 99,94 ms, mínimo 63,92 y máximo 147,37.
10 Hz es nominal, sin precisión por frame. Las dos muestras de calentamiento se
conservaron; no fueron lecturas parciales o fallos del temporizador. Perfil/filtros
intactos; phase2_verified=false y authentic_attacks_detected=false.

Informe privado:
`D:\logs\dmc3-observe-20261016-234822-3cbbbb1ec2ac49039ef1ab1dd9f985fd`.
report.json SHA-256 `9c88411b354360ce976c270ca8f81ddda66c7fd4bd025357be881110f175323b`;
events.jsonl SHA-256 `63fde113ffebf3e4654263bc3c2abe426fc0701116e50a0d5c62e5da27103178`.
manual-review.json conserva relato posterior; context-before-r20.png es imagen
previa, no vídeo de la ejecución. Análisis en
`D:\logs\dmc3-timeline-20261016-235300-a26781cdf9024d9580d05fca7d62a3a4`,
analysis.json SHA-256 `522d0d71d767c50c8b26306db96bc93072b7d72c1f644be72841e897a73bc666`.

### E1 ejecutada y confirmada

Se lanzó desde **476130021a7edd6ce47bbe22eb1c4b39f83be564** después de «Listo
para E1». El usuario confirmó después una sola pulsación y un espadazo visible,
reposo antes/después y tres señales oídas, sin incidentes declarados.

200 muestras, 198 coherentes y dos de calentamiento; mismo contexto misión 7/
sala 127/posición 2/MAIN, un bloque, sin pérdida de actor/foco/contexto, errores
de lectura o ticks omitidos. Identidad/build/base se redescubrieron y coincidían
con R20; lector/juego medios y no elevados, 3405 lecturas/40173 bytes.

| Tramo observado | Ambas parejas (grupo, índice) | state | Muestras coherentes |
|---|---|---|---|
| Reposo previo declarado | (0,3) | 1 | 59 |
| Único episodio de familia melee | (3,3) | 65537 | 16 |
| Reposo posterior declarado, primer patrón | (0,0) | 1 | 100 |
| Reposo posterior declarado, segundo patrón | (0,3) | 1 | 23 |

Timer=2.0 en las **198 coherentes**, sin reinicios observados; no se rechazó
ningún timer. Por tanto este campo no muestra progreso del espadazo en esta
captura; su semántica continúa desconocida. (0,0) y (0,3) aparecen durante
reposo declarado: el cambio entre ellos no es otro ataque. Una sola E1 no prueba
exclusividad de (3,3)/65537 ni convierte BUSY en ataque.

Origen temporal: **primera muestra**, distinto del comienzo de pitido/muestreo.
Entrada al episodio acotada entre **5,995–6,098 s**, salida entre
**7,604–7,701 s**; tramo observado 1,506 s, no duración completa certificada de
la animación. La primera muestra (3,3) aparece ~1,164 s después del inicio de
la señal corta: no se conoce la hora de pulsación y esto no mide latencia de input.
Sin vídeo/observador independiente, se conserva asociación manual contextual.

Cadencia real: mediana 100,11 ms, mínimo 62,14 y máximo **156,40 ms** (intervalo
que abarca la señal); llamada de sonido acotada por eventos durante 62,97 ms.
Se conservaron todas las muestras y no hubo ticks omitidos. Basta para observar
este tramo de 16 muestras y acotar sus límites; no resuelve partes por frame,
ventanas de cancelación, contacto o hitboxes. No aumentar frecuencia por rutina.

Captura privada:
`D:\logs\dmc3-observe-20261016-235733-2960ab20ee8f4c6287ca42eeb511567f`.
report.json SHA-256 `f3057e8493f7173807e83b7d434b1f95fd6a1ed2ac2f56cf75de4fdeed4406de`;
events.jsonl SHA-256 `d2cceb19c179a4df936c8005061e5d4c1ce80e46ab82a1e73aedba7e6fcd8684`.
Relato en manual-review.json, sin tiempos de acción inventados. Comparación R20/E1:
`D:\logs\dmc3-timeline-20261016-235923-4a113a6765a148b2b5370291d66bec8b`,
analysis.json SHA-256 `d0b7d4dedacd37073b69a7ba19bed1dda555cf8aebeaec00121c5cbaae136856`;
e1-review.json conserva límites y cadencia. Fuentes originales sin modificar.

### Siguiente: E1-R, una única repetición idéntica propuesta

Propuesta histórica, **ya completada según el resultado anterior**.

Objetivo: comprobar repetibilidad del episodio y del timer constante, no
corregir un error de E1 (el usuario la confirmó limpia). Misma ficha de abajo,
25 s preparación, 20 s/10 Hz, tono corto a ~5 s para **una** pulsación de espada;
misma Rebellion/Gunslinger/lugar, reposo antes/después, sin otras acciones.
Requiere otro «Listo»; no se lanzó automáticamente con el relato posterior.
Después comparar y decidir el negativo distinto mínimo que falte antes de
proponer regla; no pedir combo, salto y disparo juntos. Sin detector definitivo,
phase2_verified=false y authentic_attacks_detected=false.

### Procedimiento y señal utilizados en E1

Objetivo: contrastar R20 con **una sola pulsación de espada**, conservando Dante,
Rebellion, Gunslinger y el mismo lugar, sin enemigos. Comprobar si cambian ambos
motions/state, si vuelven al patrón previo y si el timer sigue fijo. La señal y
la pulsación no certifican una animación/impacto; preguntar después qué ocurrió.

Se añadió el ajuste mínimo opcional `--action-cue-seconds 5`, con --beep: un
único tono corto de 1200 Hz/60 ms a partir de t=5 s, sin tocar punteros/filtros.
Registra sampling.action_cue.begin/end, horario previsto, tiempo real de llamada,
resultado del sonido y cue_only/actual_action_unknown. No afirma cuándo se oyó
o actuó. La llamada síncrona puede ensanchar un intervalo de muestreo; revisar
la cadencia real y ticks omitidos, sin ocultar ese coste o afirmar límites por frame.

Verificado antes de usar: **7 tests sintéticos de coordinación + 59 regresiones
sintéticas** (25 observador/perfil/logs y 34 temporales), todos correctos, sin
WindowsSelfRead ni acceso a juegos. Demo acústica real sin memoria: tres tonos,
con separación acelerada de dos segundos; el usuario confirmó distinguirlos.
No fue una captura: los parámetros 5/5 del helper eran valores de fixture de
la demostración, no sus tiempos de acción ni un muestreo de cinco segundos.
Evidencia privada: D:\logs\dmc3-cue-check-20261016-235229-be0b7635cebc48b38748577f893c91a7.

Ficha E1 que debe explicarse antes de pedir «Listo»:

1. Preparación **25 s** para volver al juego/cerrar pausa; quieto, sin atacar.
2. Pitido agudo largo: comienza la captura de **20 s**; seguir quieto.
3. Aproximadamente **5 s después**, pitido corto más agudo: pulsar **una vez**
   el botón de espada y soltar; no repetir ni continuar combo. Dejar concluir la
   animación y permanecer sin entradas hasta el fin (unos 15 s restantes).
4. Pitido grave: fin; ya se puede volver al chat y confirmar ejecución/errores.

Prohibido disparar, saltar, mover stick/teclas voluntariamente, usar lock-on,
cambiar arma/estilo, abrir menú, minimizar o cambiar de ventana. El movimiento
propio del espadazo se conserva. Si se equivoca, no intentar corregir/repetir
dentro de la captura; describirlo después. Una única pulsación es intención,
no etiqueta de ataque observada. No iniciar E1 con la confirmación anterior R20
ni con la confirmación de sonido: requiere **nueva preparación explícita**.

Configuración: 200 muestras/10 Hz, --lead-in-seconds 25 --beep
--action-cue-seconds 5. Toda identidad/build/base/página se revalida por ejecución.
Solo después se decidirá si hace falta una repetición o control negativo distinto.

## Primera ficha activa: R20, control negativo de reposo

Estado de esta propuesta histórica: **ejecutada y confirmada**, resultado arriba.
Se verificaron otra vez 34 archivos históricos y los hashes de
dos parejas PINE. Las primeras capturas permanecen exploratorias; la espada
con pitidos tiene inicio incierto. El baseline 023130 no tiene etiqueta de
reposo confirmado ni contexto de equipo declarado y no sustituye a este control.

Hipótesis: comprobar si el timer 2.0 y/o motions/estados candidatos de espada
pueden aparecer sin ataques voluntarios. Primero un negativo aislado; luego,
si sirve, una captura distinta con un solo golpe y el mismo equipo/contexto.
R20 sola no valida la semántica de un ataque ni del temporizador.

Antes de iniciar, confirmar Dante, arma cuerpo a cuerpo, estilo, misión/sala
si se conoce, en partida sobre suelo llano y sin enemigos/interacciones cerca.
No suponer Rebellion ni un estilo concreto. Mantener equipo/contexto para el
posterior golpe aislado; cualquier cambio se anota, no se oculta.

Procedimiento de **esta ficha únicamente**, con señales ya disponibles:

1. Tras la confirmación de preparación, lanzar una captura finita con 25 s de
   preparación: volver a DMC3, cerrar su pausa y dejar a Dante quieto. No responder
   al chat durante el intervalo. No debe estar atacando al empezar.
2. Primer pitido agudo (880 Hz, 200 ms): comienza el intervalo de muestreo.
   Permanecer quieto **20 segundos**, cero pulsaciones de espada, disparo o salto.
3. Segundo pitido grave (660 Hz, 200 ms): fin. Ya se puede volver al chat.
4. Preguntar después si permaneció quieto entre señales y si hubo menú, enemigo,
   movimiento/ataque accidental o cambio de foco. Registrar la declaración y
   errores como nota posterior, sin tiempos inventados ni reemplazar originales.

Evitar stick/teclas de movimiento, lock-on, cambio de equipo/estilo/devil trigger,
pausa, minimizar, cambiar de sala/ventana. Una animación de reposo espontánea se
conserva: no es error por sí sola ni se reclasifica como acción ofensiva.
Si aparece una interrupción, dejar de actuar, esperar el fin y explicarla después.

Configuración propuesta: 200 muestras a 10 Hz, preparación 25 s y --beep; sin
cambios al código o perfil. Los pitidos existentes ya se usaron en capturas
confirmadas por el usuario; no requieren descarga ni señales intermedias.
Antes de leer gameplay se redescubren PID/ruta/inicio, SHA/PE, base real y guardas
de lectura del observador; error de acceso/build impide continuar, sin elevarlo.
Estas comprobaciones se ejecutaron para R20; su identidad histórica está en continuidad.

10 Hz da aproximadamente 100 ms entre muestras, suficiente para contrastar un
tramo de reposo de 20 s, **sin cobertura por frame**. Revisar huecos/ticks omitidos
y tiempos reales al terminar. Para el golpe posterior, los límites solo podrán
acotarse entre muestras; si se pierden transiciones, declarar la limitación antes
de cambiar frecuencia o repetir. No modificar el filtro de -1.0 ni usar 2.0 como
reloj. Guardar rechazos, causas, generaciones y foco; todos los flags semánticos
siguen false hasta evidencia suficiente. R20 no activa automáticamente la prueba E1.

## Diseño posterior, no señales implementadas

Las secciones siguientes conservan propuestas para otras fichas. La cuenta
regresiva y secuencias de varias señales **no están implementadas**; no usarlas
como si fuesen la ficha R20 o estuviesen sonando con el CLI actual. Antes de una
prueba con esas señales, explicar el ajuste mínimo, implementarlo y verificarlo.
La excepción es la única señal intermedia opcional recién verificada para E1.
No pedir al usuario contar entradas de un combo sin completar su ficha exacta.

## Preparación común y señales propuestas

Antes de pedir «Listo», entregar **una sola ficha completa**: objetivo, arma,
estilo, botón real configurado, duración, orden/cantidad de acciones, reposos,
prohibiciones y condición de cancelación. No dar por conocidas teclas o mando.
Confirmar Dante, sala, dificultad/modo, arma/estilo y enemigos presentes; mantener
esos factores entre comparación positiva y negativa. Para acciones básicas,
preferir suelo llano sin enemigos/interacción cercana, sin lock-on ni stick.
Esto separa animación de impacto: **no se intentará medir daño ni aciertos**.

La cuenta regresiva y señales por acción siguientes son un **diseño pendiente**;
la herramienta actual tiene preparación, inicio/fin y una señal intermedia
opcional para E1. No indicar al usuario que ya oirá toda la secuencia de la tabla.
Cuando se
implemente esa coordinación, usará audio Windows sin descargar nada. Antes de
la primera captura explicar y demostrar las señales fuera del registro, para
que un pitido inesperado no encuentre al jugador atacando.

Horario propuesto, t=0 inicio del muestreo:

| Momento | Señal/instrucción |
|---|---|
| t=-25 s | Aviso de preparación. Volver a DMC3, cerrar la pausa automática y dejar a Dante quieto. No atacar durante la preparación |
| t=-3, -2, -1 s | Tres pitidos cortos iguales (440 Hz, 80 ms), cuenta regresiva 3–2–1; seguir quieto |
| t=0 | Un pitido agudo largo (880 Hz, 200 ms), inicio; **todavía no actuar** |
| t=5 s y otros tiempos de la ficha | Un pitido corto diferente (1000 Hz, 80 ms), ejecutar solo la acción indicada |
| t=T | Un pitido grave largo (660 Hz, 500 ms), fin; ya se puede volver al chat |

Permanecer en el juego hasta la señal final, sin Alt-Tab, minimizar ni responder
al chat. Si aparece un menú o sucede un accidente, detener las acciones, esperar
el final y describirlo después; no improvisar una repetición dentro de la misma
captura. No hay obligación de dejar el juego activo mientras se contesta al chat:
los 25 s sirven precisamente para volver y cerrar su pausa.

## Fichas de acciones básicas

T=30 s de muestreo, aparte de 25 s de preparación. Cada pulsación debe soltarse;
no mantener ni machacar botones. Los horarios son **órdenes previstas**, no
etiquetas de acciones observadas ni tiempos exactos de reacción humana.
La prohibición de moverse se refiere a entradas voluntarias de stick/teclas;
el desplazamiento propio de una animación no invalida por sí solo su registro.

| Ficha | Acciones y cantidad | Reposos | Acciones prohibidas durante los 30 s |
|---|---|---|---|
| R: reposo | Cero acciones; pitidos de control a 5, 13 y 21 s que se deben ignorar | Quieto de 0 a 30 s | Espada, disparos, salto, movimiento, lock-on, estilo/devil trigger, cambio de arma, menú/ventana |
| E1: golpe aislado | Una pulsación del botón de espada a 5 s; soltar y no continuar la cadena | 0–5 s y desde terminar la animación hasta 30 s | Segunda pulsación de espada, combo, disparo, salto, movimiento, lock-on, cambio de equipo/estilo, menú/ventana |
| E3: tres separados | Una pulsación de espada a 5, 13 y 21 s, tres en total | Ocho segundos entre inicios previstos; después de cada pulsación dejar concluir y volver a reposo. Quieto 0–5 s y tras el tercero hasta 30 s | Encadenar una segunda pulsación antes de la siguiente señal; disparar, saltar, moverse, lock-on, equipo/estilo, menú/ventana |
| D3: disparo | Una pulsación de disparo a 5, 13 y 21 s, tres pulsaciones; soltar cada una | 0–5 s y reposo entre señales/final | Espada, salto, movimiento, lock-on, mantener disparo, cambio de arma/estilo, menú/ventana |
| J3: salto | Una pulsación de salto a 5, 13 y 21 s; tres saltos previstos desde suelo | Aterrizar y quedar quieto antes de cada siguiente señal; 0–5 s y final en reposo | Espada, disparo, stick, segundo salto en aire, lock-on, equipo/estilo, menú/ventana |

E3 no son tres combos ni tres impactos contra un enemigo. D3 cuenta pulsaciones,
no balas ni impactos: un botón podría generar varias animaciones/proyectiles.
Si una acción no terminó antes de su siguiente señal, **no pulsar para cumplir
el horario**; la ficha no quedó correctamente ejecutada y se conserva como
exploratoria. No modificar datos para simular recuperación o ausencia de menú.

## Combo completo y cadena interrumpida: fichas aún incompletas

No conocemos arma/estilo/ruta ni entradas exactas de las capturas históricas.
El enum DDMK distingue partes de REBELLION_COMBO_1, pero eso no basta para elegir
controles o mapear motion IDs a partes. Antes de estas dos pruebas completar
una ficha C con **nombre tal como aparece en el juego, arma, estilo, N entradas,
orden, ritmo/pausas de cada entrada y final visible esperado**. Consultar la lista
de movimientos en el juego antes de empezar, fuera de la captura; el usuario
podrá aportar sus instrucciones cuando vuelva. Sin esa ficha no se pide «Listo».

Diseño común: T=40 s, preparación 25 s, señal de comienzo de secuencia a 5 y
22 s, **dos intentos**. Reposo inicial 5 s; tras cada intento, soltar controles
hasta la siguiente señal o fin. Solo ejecutar si la ficha C termina con margen
antes de 22 s y de 40 s; de lo contrario, ajustar y explicar toda la duración
antes de empezar, dentro del presupuesto finito del lector.

- C-completo: en cada señal ejecutar exactamente las N entradas y pausas de C,
  sin agregar movimientos. Observar la secuencia final y recuperación; pulsar
  N veces no acredita que haya salido el combo completo.
- C-prefijo: misma C, misma arma/estilo y ritmo, pero **omitir su última entrada**
  (N-1 en cada intento), soltar y dejar recuperar. Si C tuviera tres entradas
  confirmadas serían dos por intento; este número no se impone sin completar C.
  Es cadena truncada por no continuar, no una cancelación mediante salto/estilo.

Prohibido en ambas: disparar, saltar, desplazarse voluntariamente, lock-on si no
forma parte explícita de C, cambiar arma/estilo, devil trigger, menú o ventana.
Si una técnica exige dirección/lock-on, incorporarlos exactamente a C y a su
control; no cambiar la regla a mitad del registro. Estudiar después cancelaciones
auténticas requiere otra hipótesis, sin mezclarla con el prefijo incompleto.

## Campos y sincronización que se contrastarán

Campos ya disponibles: identidad histórica del actor, generación, personaje/id,
misión/sala/evento, ambos MotionData, state y timer crudo, estado de validez,
foco/errores, secuencia y reloj monotónico. Mantener -1 como desconocido y romper
continuidad. Analizar por separado inferior y superior, cambios y tramos estables.
No usar BUSY, timer o cantidad de pitidos para certificar un golpe.

Campos de investigación adicionales (action/lastAction/bufferedAction/chainCount,
idleTimer y otros) **no están implementados ni validados**. Resolver primero
su compatibilidad y significado; no hacer volcados o escaneos para llenar huecos.
Un aumento de frecuencia hasta el límite ya existente de 20 Hz sería una decisión
posterior con coste medido, no garantiza cobertura por frame ni arregla etiquetas.

La futura coordinación debería registrar reloj monotónico antes/después de emitir
cada señal y su horario objetivo. Si una señal llega tarde, conservar el retraso
sin emitir una ráfaga para recuperar el horario. Describir latencia acústica y
reacción humana como incertidumbre. Conservar separadamente:

1. Horario previsto y señal realmente emitida.
2. Muestras/intervalos de motion/state del lector.
3. Relato posterior del jugador (incluidos accidentes, sin tiempos inventados).
4. Inicio/final de acción observado independientemente, con incertidumbre.

Para el punto 4, si se dispone y autoriza después, una cámara externa que capte
pantalla y pitidos puede dar alineación audiovisual sin DLL/hooks ni carga de
grabación en el juego. Revisarla contra el registro de señales; no hay grabación
de ese tipo ahora. Otra persona podría anotar con reloj compartido sin alterar
el foco; un jugador solo no debe cambiar a una ventana de anotaciones durante
la prueba. Sin observación independiente, conservar el resultado como asociación
declarada, aunque la ejecución haya sido correcta.

## Aceptación y qué repetir

Antes de proponer detector auténtico: al menos dos capturas limpias separadas por
condición, acciones observadas y límites temporales, negativos R/D3/J3, y otro
conjunto independiente del usado para formular la regla. Reportar resultados por
captura, falsas alarmas y acciones omitidas; no elegir umbrales con todos los datos
y presentar esos mismos datos como validación. No hay aún métricas de precisión.

Si empieza con acción ya activa, ese primer intervalo queda censurado; el resto
puede servir para otras hipótesis. Si hay disparo en E3, no usarlo como control
exclusivo de espada. Si hay un combo donde se esperaba E1, conservar como cadena
exploratoria sin nombrarla. Si hay pausa/pérdida de actor/sala, invalidar bloques
y no unir secuencias; la evidencia puede servir para ciclo de vida. Explicar
qué hipótesis perdió soporte antes de repetir únicamente la condición faltante.

La prueba de pausa/puerta existente se reutiliza; no se pide de nuevo por rutina.
Estas fichas no permiten afirmar impactos, hitboxes, daño o integración GOW2.
La observación futura seguirá de solo lectura y la fase permanecerá parcial
hasta aportar evidencia independiente, repeticiones y controles suficientes.
