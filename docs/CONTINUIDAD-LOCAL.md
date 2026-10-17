# Continuidad para Codex local en Windows

Estado de referencia: 17 de octubre de 2026. Esta guía permite continuar desde
el repositorio sin depender del historial del chat ni del filesystem de nube.
Actualizar al obtener evidencia nueva; los resultados siguientes son históricos,
no pruebas ejecutadas automáticamente al abrir este archivo.

## Diagnóstico timer implementado · JT1 requiere preparación · 2026-10-17

Desde main limpio/local-remoto **bd40b220bf344cbef2e3e4a1cc54978120e66792**.
Usuario autoriza implementar hasta necesitar acción manual/programa. Nuevos
--timer-diagnostic/--profile-only y analizador offline JSON/CSV. Extensión de
perfil estricta con3 guardas disco/cargadas, evento/fase antes/después, speed,
identidad/contexto comprobados aun al rechazar timer. **-1 sigue rechazado**;
intento/calidad aparte, sin promover gameplay. Transiciones no coherentes;
fallos de acceso/parcial/actor/escena/foco/proceso no retienen campos coherentes.
Modo anterior conserva perfil/filtros/lecturas; nuevo22 lecturas/234 bytes,
máximo32. Semántica/unidades de campos nuevos desconocidas.

Profile-only real pasó, sin actor/señales: PID10688/inicio02:38:13.424527Z UTC/
base0x7FF7C6920000 redescubiertos, huella conocida, tokens medios8192/0x410,
8 lecturas/212 bytes, cero errores/muestras. Identidades históricas, no reutilizar.
Campos nuevos del actor aún **sin captura real**.28 tests nuevos y66 regresiones
sintéticas correctos, sin WindowsSelfRead/PINE/cerrar juegos. Detalles/receta:
[diagnóstico timer](dmc3-timer-diagnostic.md).

Perfil privado D:\logs\dmc3-observe-20261017-005434-b15d7e4e93274fb6b98d00b2fb076d69;
report SHA `ac56b4ca0301b85aa0cb1aa6be13f04b6339ea98261f56b252a9c4e771d38f9c`,
events SHA `153024a331e318c0926d6d6c508d906bef0a4cd80063826a7162e4a36ecd5485`,
profile SHA `d914c6b6b842a0a9771a0ed8eac7137e45b20e10fb6802d30edb039c7405e0de`.
Verificación/tests D:\logs\dmc3-timer-diagnostic-check-20261017-005705-58e91be160034bd4b18d369420ea2ac6;
delivery-verification SHA `c83e3b4eeb8c5e8bf8d50b155d31f0d99ae2c548d3be11bbbe86ad13f0825723`.
26 tests iniciales en nota histórica,28 finales en entrega, originales intactos.

Próxima **JT1** necesita usuario: mismo contexto y nuevo «Listo»,25 s preparación,
20 s/200 muestras/10 Hz, pitido largo sin entradas, corto~5 s UN toque de salto
y soltar enseguida, aterrizar/reposo hasta grave. Cero dirección/segundo salto/
espada/disparos/lock-on/menús/equipo/ventanas. Espera automática permitida: reposo
es no tocar controles. No iniciada. Después confirmación manual/análisis/cadencia;
si falta fase/umbral no afirmar causa o frames. Solo DMC3 necesario, ya accesible.
Sin gameplay/PINE nuevo, flags false y fase parcial, sin reacción GOW2.

## Análisis nativo del timer: herramienta y negativo retenido · historial

Desde main local/remoto limpio **3c4d9c045b30b34fa9aab7a65ec724e63e05f1f9**.
Se avanzó sin nuevas capturas/RAM/PINE. Hay herramienta propia de disco finita:
tools/inspect_dmc3_native_timer.py, tests y dependencia opcional aislada. Capstone
wheel oficial5.0.9/SHA fijado,1.273.459 bytes, extraído bajo D:\logs (~9 MB),
sin modificar Python global/juegos. Dist5.0.9/binding5.0.7/API(5,0,1280) registrados.

Build conocida y dos anclas verificadas; 240 referencias candidatas/95 rangos
PE,225 con camino directo local y3 rangos con decode lineal incompleto. No son
240 referencias con actor o ejecución probados. Tabla nativa del selector+3E08
lleva caso5 a1F45E0 (iniciaT=9); caso6 a1F43F0, con valores5/14 y restas de
actor+14 (speed según fuente, unidades desconocidas). En una fase guarda un
resultado negativo, avanza fase y puede retenerlo. Hipótesis comprobable de -1
por resta (ejemplo0−1), no sentinel validado ni causa de J1-R demostrada.
Caso5 es JUMP=5 en fuente fijada; caso6 conserva nombre desconocido. No inferir
que la ruta se ejecutó realmente por el relato o por coincidencia de valores.

**13 tests sintéticos correctos**, ninguno abre juegos. La pasada real de disco
es evidencia distinta, sin ejecución del juego/mod ni alteración del observador.
Detalles, límites, receta y fuentes primarias en
[investigación nativa](dmc3-timer-native.md). No repetir suites sin motivo.
Informe privado: D:\logs\dmc3-native-timer-20261017-004202-c8487fcef47c429897ec31475d3272e8\report.json,
SHA `8221506a31dea8039b4c7a897a1159f8f2fdf94e30753dd363fd31666a936442`.
Decoder/manifiesto/tests/revisión:
D:\logs\dmc3-native-review-20261017-003643-4f0140f82236407da880c1e7f4f5dafa;
native-interpretation.json SHA `543e17720891fbc551f041c87ecf8e190a038e88b983ce8761454e4e69806736`,
review-addendum.json corrige cita speed3007→3008, assert3035 válido;
synthetic-tests.txt SHA `f0d182ca5ce786bfed81b9de7c3793111ed186d22235d628eced0ae59b6930d3`.
Wheel/DLL, ejecutable y desensamblado privado fuera de Git.

Siguiente tarea concreta: mejorar diagnóstico de rechazos con recheck final de
actor/contexto y calidad separada; justificar/comprobar evento+3E08/u32,
fase+3E10/u8 y speed+14/f32. **No implementado o capturado todavía.** Mantener
timer desconocido/rechazado, no ampliar filtros para hacerlo pasar; validar
perfil/guardas/tests antes de una nueva preparación de salto. No reutilizar
PID/base históricos. Luego contraste finito de fases/resta/retención, si permite
distinguir hipótesis; no solicitar combos sin arma/ruta completa. Motion/state
pueden progresar como candidatos sin usar timer/BUSY como ataque. Fase parcial,
phase2_verified=false y authentic_attacks_detected=false, sin reacción GOW2.

## Hipótesis temporal de combos propuesta por el usuario · historial

Después de publicar/verificar **84358f3c0450fef5694d2eda8cb6064c8faabaeb**,
el usuario plantea si el timer puede relacionarse con «golpe, espera, golpe,
golpe». Conservar como hipótesis, sin combo/arma/ruta exactos identificados ni
captura nueva autorizada por esa pregunta. Campo leído continuamente; J1-R
varía5,901–6,293 s y rechaza -1 en6,386–6,685 s desde primera marca de muestra,
tras señal~5 s; espada E1/E1-R permanece2.0. No son horas nativas de input ni
unidades conocidas del valor; variación durante salto no prueba ventana de combo.

Nota privada D:\logs\dmc3-combo-timing-hypothesis-20261017-003232-06e3fd6653504c6b8545ad113f428a4e\hypothesis.json;
SHA `41238296e481b23fc6c82c4935eda3d24cdac80a82bf8a3ed978d41c5f58536b`.
Próximo sigue estudiar rutas nativas. Después, solo si distingue hipótesis,
definir combo completo/alternativa con tiempos de ejecución observados y
frecuencia suficiente; 10 Hz puede perder ventanas breves. No nueva RAM/PINE,
código, filtros o suites. Fase parcial y flags false.

## Timer: dos referencias estáticas verificadas · 2026-10-17

Desde main local/remoto limpio **d883400fd4de4cc191286735f43bc5ffcf638fd5**.
Se siguió el paso técnico anunciado, sin nuevas capturas ni RAM/PINE. Hash
del ejecutable conocido coincide; se comprobaron dos pares de instrucciones
transcritos en DDMK fijado: RVA0x20932C/13 bytes y0x21F69E/16 bytes, dentro
de .text, cargan float desde otra estructura y escriben [rdi+0x3E34]. Los
bloques de fuente los llaman duración de Stinger de Rebellion y Yamato/Force Edge.
No se ejecutó DDMK ni el código estudiado; nombres de fuente, no ataques validados.

Revalidación de los30 fuentes por SHA-256/blob Git. Corrección: la búsqueda
inicial por el nombre motionTimer omitió referencias numéricas de Actor.ixx:
14969–14970 y15165–15166, helpers11967/11987. Detalles, enlaces fijados y receta
reproducible en [investigación de campos](dmc3-campos-investigacion.md#dos-referencias-nativas-verificadas-desde-disco--2026-10-17).
Eso respalda uso dependiente de acción, no prueba tiempo general/progreso,
unidad, ruta de salto, origen de -1 o ejecución de esos caminos durante E1.
Conservar perfil/filtros y muestras rechazadas; fase parcial y flags false.

Informe privado nuevo: D:\logs\dmc3-timer-static-20261017-003000-8ba641ace1c94e80b3474d3261b1ef8a\report.json;
SHA `db723c5349c5451920221d1867c19eba48995d4610cfa44d894b2418ced721e3`.
Solo lectura rb: hash streaming64KiB, cabeceras acotadas y29 bytes puntuales,
sin dump/scan de RAM o modificaciones. Archivo estable antes/después. Sin código
nuevo ni suites por documentación; receta verificada contra el ejecutable real.

Próximo paso concreto: decoder x64 ligero aislado para delimitar instrucciones/
funciones y seguir lectores/escritores de +0x3E34 en inicialización/salto/negativos.
No disponible en Python/PATH/rutas conocidas consultadas; no instalado ahora.
No usar coincidencias crudas como instrucciones ni pedir más capturas sin una
hipótesis diferenciable. Usuario no necesita actuar dentro del juego por ahora.

## J1-R: variantes de reposo descritas por el usuario · historial

Desde main publicado/verificado **ab094fc5d79bc54fa398fb3f54b4bd176b63043d**,
el usuario añadió: inició en animación de reposo, saltó como se indicó, quedó
en quietud habitual y luego regresó a la animación. Compatible en orden con
(0,3)→(0,4)→hueco→(0,0)→(0,3). Conservar como hipótesis manual contextual:
(0,3) espera prolongada/animada; (0,0) quietud habitual. Ambas aceptadas state1/
timer2.0, no ataques ni semántica universal. Sin tiempos visuales independientes;
esta aclaración no identifica la causa de -1 ni elimina el hueco.

Nota literal nueva privada y hashes originales revalidados:
D:\logs\dmc3-j1r-idle-note-20261017-002604-7dfcb4d0494a4692baf44125809d5fe0\manual-review.json;
SHA `e1a28a7ba02e092ff89dae61920d5ffbeb4402c52aec3e27aac56ddf4e9ce6f4`.
No nueva captura/RAM/PINE, código, filtros o suites. Siguiente sigue investigar
uso nativo del timer antes de pedir más pruebas; fase parcial y flags false.

## J1-R: toque único/reposo declarados · datos y revisión anterior

Partida main **39449efbdd14dacc3e4779f1293d84dbafa82290**, local/remoto limpio
y coincidente. Captura única tras ficha y «Mismo contexto; listo para J1-R»:
25 s preparación, 200 muestras/10 Hz. Usuario confirmó toque único al corto
y reposo como se indicó; propuso animación de reposo como causa de rechazos.
No inventar tiempos visuales ni confirmar por él cada otra pregunta no resuelta.

192 coherentes, cuatro rechazos -1 y cuatro calentamientos, dos bloques.
Ambos motions (0,3)→(0,4)/state1 (1 muestra)→(0,4)/state2 (4)→hueco→
(0,0)/state1→(0,3)/state1. Timer de cinco (0,4):9,8,2,11,5; 188 coherentes
valen2.0, incluida una state2: no identifica reposo/progreso. Errores parciales
-1: uno bytes[4,0,4,0]/state2, tres[31,0,31,0]/state1, antes del recheck final.
Conservar filtros/huecos, semántica desconocida, generaciones no son actor perdido.
Sin (3,3)/BUSY/candidatos melee/ranged aceptados; contraste contextual con espada,
sin exclusividad/ataque autenticado. J1 sigue exploratoria por duración incierta.

Rechazos entre6,386–6,685 s desde primera muestra; cambio durante reposo declarado
(0,0)→(0,3) aceptado entre16,695–16,804 s. No son el mismo hecho; el cambio
tardío no explica por sí solo -1. Rechazo es política, no error del usuario.
Mediana100,26 ms/rango36,03–162,20; sin ticks omitidos, fin del episodio no
delimitable por hueco. Identidad/build/base redescubiertas coincidentes, tokens
medios, acceso0x410,3381 lecturas/39821 bytes; sin errores Win32/parciales ni
cambio de foco/contexto observado. No reutilizar PID/base históricos.

Captura D:\logs\dmc3-observe-20261017-002123-b9067c1c3ea04c5fa64fa30ab76a2e45;
report SHA `5ed52ca2bbcd3bdb918e8c58265dd19c32369f06b00998c7d2fcde92be75dae7`,
events SHA `f6d9b281f64b6f23ac6a58d78d3a63ef6c09d1072dcf308d0ddb48f22efb13b7`.
Comparación cinco capturas/j1r-review.json previo a respuesta:
D:\logs\dmc3-timeline-20261017-002305-bcecda50b7814cfb98ea0b0d4fe5d904;
analysis SHA `9bf8f01568ea9b2b2e5efa3892f3829d5c0f20ab2c048312c5da5452fa18d898`.
Nota posterior complementaria nueva con respuesta literal e hipótesis:
D:\logs\dmc3-j1r-confirmation-20261017-002344-1af930c1df94475192ca9bbe23b64c27\manual-review.json;
SHA `7ae85dfef1c808d40e1b42080aa668ae7df5b9cb1f0525320a5532e3259febb8`.
Cinco parejas revalidadas antes/después; originales y notas históricas intactos.

Siguiente: no pedir otra captura por rutina. Ya se puede separar cambio tardío
en reposo/rechazos con lo existente. Revisar referencias nativas estáticas de
+0x3E34 y límites por huecos antes de proponer regla o nueva hipótesis comprobable;
no realizado. Ficha/detalle en dmc3-validacion-controlada.md. Sin código/tests
nuevos, suites repetidas o PINE; lectura solamente, fase parcial/flags false.

## J1: relato posterior con pulsación incierta (historial)

Desde main local/remoto limpio **154e41b10c3ebc02a8b31bfbc25ac7702c088a03**.
El usuario relató pulsar salto al sonido corto, soltar estando en el suelo y
reposo hasta el grave. Preguntado si mantuvo hasta aterrizar o soltó enseguida:
**«No recuerdo con certeza»**. Salto/reposo declarados; duración de pulsación
desconocida, sin confirmar expresamente todos los otros controles preguntados.
J1 queda exploratoria para el protocolo breve, sin desechar sus datos ni
atribuir los valores del timer a mantener el botón.

Nota posterior nueva con ambas respuestas literales, incógnitas y hashes:
D:\logs\dmc3-j1-clarification-20261017-001819-86a6f30dd5d840449e15d5fc9a672f27\manual-review.json;
SHA-256 `b2a67d37c16d4e61a8639b5c5dbc57b87ea22519ba7baeb1dd8aa98713d017f4`.
report/events J1 y analysis.json anterior revalidados e intactos; la revisión
anterior de «pendiente» sigue como historia, esta nota la complementa.

Siguiente mínima propuesta **J1-R**, mismo equipo/contexto, 25 s preparación,
20 s/10 Hz; quieto al tono largo, a ~5 s **una pulsación de salto y soltar
enseguida al despegar**, sin esperar al suelo; aterrizar/reposo hasta grave.
Sin ninguna otra acción/menú/ventana. Ficha completa en validación controlada;
exige nuevo «Listo» y no se ha iniciado. Resolver pulsación breve no establece
por sí solo significado del timer ni compara causalmente una retención conocida.
Sin nueva RAM/PINE, código, filtros o tests; solo notas y comprobaciones de
integridad/enlaces. Fase parcial, flags false. Historial numérico debajo.

## J1 registrada · estado anterior al relato posterior

Partida main **0e7ea97a7c80638590d6b0244c8c57317f528d90**, local/remoto limpio
y coincidente. Tras ficha completa y «Listo para J1», captura única finita:
25 s preparación, 200 muestras/10 Hz, señal a ~5 s. **Todavía falta respuesta
posterior** sobre salto único visible/reposo/señales/incidentes; se preguntó al
terminar. No convertir preparación/pitidos en prueba de ejecución correcta.

190 coherentes; seis rechazos timer=-1.0 y cuatro calentamientos (dos iniciales,
dos recuperación). Dos bloques separados por el hueco, nunca unidos. Sin errores
Win32/lecturas parciales, pérdida de foco, ticks omitidos o cambio de contexto
observado. Build/base/PID/inicio se redescubrieron y coincidían con R20/E1/E1-R;
tokens medios sin elevar, 0x410, 3369 lecturas/39645 bytes. No reutilizar PID/base.

Ambos motions (grupo,índice): (0,3)/state1 → (0,4)/state1 (2 muestras) →
(0,4)/state2 (4) → hueco → (0,0)/state1 → (0,3)/state1. Timer durante las seis
(0,4) aceptadas: 9,9,0,12,6,0; restantes 184 aceptadas=2.0. Seis rechazos -1:
tres con bytes [4,0,4,0]/state2 y tres [31,0,31,0]/state1. Esos campos parciales
se guardan antes del recheck final, no son snapshots coherentes. Generaciones
por invalidación no prueban pérdida del actor. Filtros conservados, semántica
de timer/progreso/cuenta regresiva/sentinel desconocida. No inferir reinicios.

Sin (3,3), BUSY o hipótesis melee/ranged aceptados en J1, contraste preliminar
con E1/E1-R, aún no negativo limpio confirmado. Hueco/recalentamiento impiden
delimitar fin completo del episodio. 10 Hz nominal; mediana 99,88 ms, rango
44,05–148,40, sin precisión por frame. Ficha, secuencia y límites en
[validación controlada](dmc3-validacion-controlada.md#j1-registrada--2026-10-17--relato-posterior-y-límites).

Captura: D:\logs\dmc3-observe-20261017-000835-e67da5c481c84a9288f7503e9e571c8a.
report SHA-256 `261d4d6352f1e9ce687097c963c2c87cbd4367dde7ca0cf84f047d4bce90f6fc`;
events `31a17db9503a26272268c635d014228c7b743c28fb58ac3898e463745afab9b9`.
Comparación R20/E1/E1-R/J1 y j1-review.json (confirmación pendiente):
D:\logs\dmc3-timeline-20261017-001144-2170f5e7ebf24e379924f77eabe275fd;
analysis SHA-256 `e1602d41a4050f09772c978d7354ca6dd58ae736f936702adc76547951446d9d`.
Cuatro parejas report/events verificadas antes/después; originales intactos.

Próximo paso: guardar respuesta posterior y valorar una sola repetición J1-R
si confirma ejecución limpia y se necesita repetibilidad, con nueva preparación.
No hay otra captura autorizada por «Listo para J1». Antes de modificar timer,
falta estudiar referencias nativas estáticas acotadas de +0x3E34; no realizado.
Sin código/tests nuevos, suites repetidas o PINE; lectura exclusivamente, fase
parcial, phase2_verified=false y authentic_attacks_detected=false. Sin GOW2.
Las secciones inferiores conservan el historial; el estado superior prevalece.

## E1-R confirmada · J1 propuesta (historial)

Partida **449529a50c7c2b1b55487ec6a79406bedbbf683d**, main local/remoto limpio
y coincidente. Tras «Listo para E1-R» se ejecutó la única repetición prevista:
25 s preparación, ~20 s/200 muestras/10 Hz, señal a ~5 s. Usuario confirmó un
solo espadazo/pulsación, reposo antes/después, tres tonos y ningún incidente.

198 coherentes y dos de calentamiento, contexto e identidad redescubiertos
coincidentes con R20/E1: misión 7/sala 127/posición 2/MAIN, PID 10688, mismo
inicio/base/build; ambos tokens medios sin elevar. 3405 lecturas/40173 bytes,
sin errores, pérdidas de actor/foco/contexto o ticks omitidos. No reutilizar
PID/base históricos en la siguiente ejecución.

Ambos motions repiten (0,3) → **(3,3), 16 muestras** → (0,0) → (0,3).
En E1-R, 15 de las 16 tienen state65537 y la última state1; E1 tenía 65537
en todas. No equiparar límites BUSY/motion ni resolver si es fase nativa o
lectura entre frames. El evento se registra después de lecturas múltiples:
las ventanas temporales son de marcas de registro, no fronteras nativas exactas.
Timer=2.0 en las 198, como en R20/E1 (594 coherentes entre las tres).
Repetibilidad contextual con asociación manual, sin exclusividad/auth detector.

E1-R: entrada registrada 5,996–6,098 s, salida 7,600–7,694 s desde primera
muestra; tramo 1,502 s. Cadencia mediana 99,77 ms (57,71–165,46); no por frame.
Captura: D:\logs\dmc3-observe-20261017-000230-64edd6f4fa7548cca80686e177cb973f.
report SHA-256 `a782b973e728ddd534ddfc2d69247c8b2b0c9ab515f814cdb03814e397e32628`;
events `c59cd372e6b8fe38bbcb3c67ae223c798cfa47ae8a32d07d0100efb196e2b199`.
Nota manual nueva, fuentes intactas. Comparación R20/E1/E1-R y e1r-review.json:
D:\logs\dmc3-timeline-20261017-000501-c0874666be3a46499af6253011f6a04b;
analysis SHA-256 `11910bbcc51f0ba7913cb9b1bb41e2b9408462f15112960560bfe335a2622ace`.

Siguiente mínima **J1: un solo salto**, como negativo del espadazo y contraste
del timer antes visto -1 en saltos. Misma Rebellion/Gunslinger/lugar: 25 s
preparación, 20 s registro, quieto al pitido largo, una pulsación de salto al
corto (~5 s), soltar, aterrizar y reposo hasta grave. Nada de espada, disparo,
segundo salto, dirección, lock-on, equipo, menús o ventana. Ficha completa en
dmc3-validacion-controlada.md; requiere nuevo «Listo», **no iniciada**.
No repetir E1 por rutina ni mezclar pruebas de todas las acciones. No cambiar
filtros para -1; preservar rechazos y campos parciales como tales. Si no se
reproduce -1 no darlo por resuelto. Sin cambios de código/tests repetidos o PINE;
phase2_verified=false y authentic_attacks_detected=false. No impactos/reacción GOW2.

## E1 ejecutada y confirmada · repetición propuesta

Desde main local/remoto limpio **476130021a7edd6ce47bbe22eb1c4b39f83be564**.
Usuario confirmó «Listo para E1» después de conocer toda la ficha; se ejecutaron
25 s preparación + 200 muestras/10 Hz (~20 s) y señal única a ~5 s. Después
confirmó una pulsación y un espadazo visible, reposo antes/después y tres tonos
oídos, sin incidentes. No transformar ese relato en tiempos de acción observados.

**198 coherentes y dos de calentamiento**, mismo contexto que R20 (misión 7,
sala 127, posición 2, MAIN), un bloque, sin errores de lectura, foco/actor/contexto
o ticks omitidos. PID 10688/inicio/base/build redescubiertos y coincidentes;
ambos tokens medios no elevados, 0x410, 3405 lecturas/40173 bytes. No reutilizar
estas identidades históricas para próximas ejecuciones.

Ambas parejas motion: (0,3)/state1 → **(3,3)/state65537** (16 muestras) →
(0,0)/state1 → (0,3)/state1. Timer=2.0 en las 198 coherentes, cero rechazos/reset.
Una asociación manual limpia y contraste R20; todavía no prueba repetibilidad,
exclusividad de motion/BUSY, impactos ni semántica universal. El cambio de los
dos patrones posteriores ocurrió durante reposo declarado, no otro golpe.

Límites del episodio desde primera muestra: inicio 5,995–6,098 s y fin
7,604–7,701 s; tramo observado 1,506 s. Primera (3,3) ~1,164 s tras señal corta,
sin conocer hora de pulsación: no es medida de latencia. Cadencia mediana
100,11 ms (62,14–156,40), mayor hueco alrededor del sonido; evento de emisión
duró ~62,97 ms, sin ticks omitidos. No precisión por frame o ventanas de combate.

Captura privada: D:\logs\dmc3-observe-20261016-235733-2960ab20ee8f4c6287ca42eeb511567f.
report.json SHA-256 `f3057e8493f7173807e83b7d434b1f95fd6a1ed2ac2f56cf75de4fdeed4406de`;
events.jsonl SHA-256 `d2cceb19c179a4df936c8005061e5d4c1ce80e46ab82a1e73aedba7e6fcd8684`.
Nota posterior manual-review.json nueva, sin alterar esas fuentes. Comparación:
D:\logs\dmc3-timeline-20261016-235923-4a113a6765a148b2b5370291d66bec8b;
analysis.json SHA-256 `d0b7d4dedacd37073b69a7ba19bed1dda555cf8aebeaec00121c5cbaae136856`.

Siguiente propuesta **E1-R**, solo una repetición idéntica para comprobar
repetibilidad, misma Rebellion/Gunslinger/lugar, 25 s preparación y ~20 s,
reposo → señal corta a ~5 s para una pulsación → reposo. Necesita nueva
confirmación; no iniciada. Ficha completa en dmc3-validacion-controlada.md.
Después decidir el negativo distinto mínimo antes de reglas, sin probar todo
a la vez. Código/perfil/filtros sin cambios; no suites nuevas por esta entrega
documental. No se repitió PINE. Fase parcial y flags semánticos false.

## R20 ejecutada y confirmada · E1 propuesta

Desde main local/remoto limpio **0da01d353cc0b9a9f0eea19b59f1db44a4c7ee09**.
Usuario confirmó Rebellion activa y «Listo para R20» tras conocer instrucciones.
Se ejecutó captura de lectura: 25 s preparación + 200 muestras/10 Hz (~20 s),
pitidos inicial/final. Después confirmó reposo completo y ambas señales.
Dante por imagen previa/personaje candidato; Rebellion/Gunslinger, misión 7
normal declarados, zona sin enemigos. Sala cruda 127, posición 2, evento MAIN.

Nuevo PID **10688**, inicio **2026-10-17T02:38:13.424527Z** (UTC, no hora local),
base real **0x7FF7C6920000**, build SHA conocido coincidente. Lector y juego sin
elevación, integridad media 8192; handle 0x410, guardas de perfil y cabeceras
correctas. PID/base son históricos de R20, no reutilizar como parámetros.
**198 muestras coherentes y dos de calentamiento**, un bloque, sin errores de
lectura/contexto/foco/actor ni ticks omitidos; 3405 lecturas / 40173 bytes.
Ambos motions grupo 0/índice 3, state=1 y timer=2.0 en todas las coherentes.
Cadencia: mediana 99,94 ms, rango 63,92–147,37 ms; no precisión por frame.
2.0 aparece también durante reposo declarado: no identifica ataque ni valida
tiempo transcurrido de animación. No convertir (0,3) en reposo universal.

Captura privada: D:\logs\dmc3-observe-20261016-234822-3cbbbb1ec2ac49039ef1ab1dd9f985fd.
report.json SHA-256 `9c88411b354360ce976c270ca8f81ddda66c7fd4bd025357be881110f175323b`;
events.jsonl SHA-256 `63fde113ffebf3e4654263bc3c2abe426fc0701116e50a0d5c62e5da27103178`.
manual-review.json y context-before-r20.png guardan relato e imagen **previa**,
sin modificar report/events. Análisis JSON/CSV en
D:\logs\dmc3-timeline-20261016-235300-a26781cdf9024d9580d05fca7d62a3a4;
analysis.json SHA-256 `522d0d71d767c50c8b26306db96bc93072b7d72c1f644be72841e897a73bc666`.

Siguiente ficha **E1, un solo espadazo**, no iniciada: mismo equipo/contexto,
25 s preparación, 20 s muestreo, reposo inicial, señal corta a ~5 s para una
pulsación de espada y reposo hasta fin. Requiere nuevo «Listo», no reutilizar R20.
Se añadió únicamente --action-cue-seconds 5 opcional con --beep: tono 1200 Hz/
60 ms, eventos begin/end con tiempos previstos/reales y acción desconocida.
Sin la opción se conserva coordinación anterior; memoria/perfil/filtros intactos.
La llamada síncrona puede ensanchar un intervalo: revisar cadencia real después.
No hay cuenta regresiva/múltiples señales implementadas ni detector definitivo.

Verificación previa al uso: siete tests de cues y 59 regresiones sintéticas
(25 observador/perfil/logs + 34 temporales), todos correctos. Se excluyó
WindowsSelfRead y PINE; no se cerraron juegos. Demo real de tres tonos sin
lectura RAM; el usuario confirmó distinguirlos. Evidencia en
D:\logs\dmc3-cue-check-20261016-235229-be0b7635cebc48b38748577f893c91a7.
Los parámetros 5/5 usados en la demo eran de fixture, no tiempos de acciones;
el reloj monotónico registra la demo acelerada con separaciones de dos segundos.
Ficha completa en [validación controlada](dmc3-validacion-controlada.md).
phase2_verified=false, sin ataques autenticados o envío a GOW2; no se repitió PINE.
Las secciones siguientes conservan la preparación e informes históricos.

## Retoma de validación con el usuario · propuesta R20

Nueva petición explícita: **ya autoriza coordinar pruebas controladas**, una
por una, tras revisar evidencia. El límite anterior de no pedir capturas era
histórico. No muestrear hasta explicar instrucciones y recibir preparación.
Partida **ee6bde30a38ffa0327755651f8657de0a9fdccd9**, main local/remoto limpio
y sin avances posteriores al consultar GitHub. No se sobrescribieron cambios.

Revisadas directamente seis capturas con el analizador y hashes de la auditoría:
34 archivos originales coinciden; las dos parejas report/events PINE también.
PINE no se repitió. Se reutilizan espada/pausa y las exploratorias con sus límites.
La investigación fijada no resuelve significado de motionTimer; no cambiar offset,
tipo o filtros para aceptar -1.0. Los 198 valores 2.0 de espada siguen sin probar
progreso de animación. El baseline antiguo carece de reposo/equipo confirmados.

Primera prueba propuesta: **R20, solo reposo**, 25 s de preparación para volver
al juego/cerrar pausa, pitido agudo de inicio, 20 s quieto, pitido grave final.
200 muestras/10 Hz, señales existentes; cero espada/disparo/salto/movimiento
voluntario/lock-on/equipo/menú/ventana. Confirmar personaje, arma, estilo y
contexto primero; pregunta enviada, **aún no es confirmación de preparación**.
Ficha completa y criterios en [validación controlada](dmc3-validacion-controlada.md).
Preparación privada: D:\logs\dmc3-validation-preparation-20261016-234354-301d05ffad984276bd31887ade7779ba\preparation.json,
SHA-256 `437489d5b6381d553d5d4bfb3fd68df4f23cddafee53460fde8e1f26acd88e77`.
Respuesta de contexto posterior: misión 7 normal, inicio desde partida guardada;
dispone de Cerberus/Rebellion y pistolas/escopeta, sala desconocida. Se pidió
Rebellion activa, Dante, estilo y suelo sin enemigos; aún pendientes. Nota nueva
context-user-report.json en la misma carpeta. No hay «Listo» ni captura iniciada.

Hipótesis mínima: separar qué valores aparecen en reposo de la asociación
histórica con espada; luego contrastar un golpe aislado en otra captura con el
mismo equipo. R20 no ejecuta E1 automáticamente. A 10 Hz se estudia estabilidad,
sin fases por frame. No hay implementación nueva, modificación de lector/perfil,
test de juego, consulta de procesos o lectura RAM nueva en esta preparación.
Persistir notas posteriores y errores en carpetas únicas D:\logs, fuera de Git;
fase parcial, sin ataques autenticados o envío a GOW2. Las secciones siguientes
son históricas y sus prohibiciones de capturas no anulan la nueva autorización.

## Análisis automatizado offline · 2026-10-16 · fase parcial

Partida local/remota **a04276b29c642e1b1ce117ce662835ba5903c235**, checkout
limpio y sin commits posteriores al consultar main. La petición adjunta posterior
autoriza trabajar autónomamente con archivos, investigación y fixtures mientras
el usuario está en la facultad. Luego anunció que dará instrucciones antes de
pruebas en juego. **No abrir/controlar juegos ni solicitar capturas ahora.**
La restricción anterior de no implementar pertenecía a la revisión retrospectiva;
ahora se implementaron exclusivamente herramientas offline autorizadas.

Lectura necesaria: [análisis offline](dmc3-analisis-offline.md),
[investigación de campos](dmc3-campos-investigacion.md) y
[protocolo futuro sin ejecutar](dmc3-validacion-controlada.md). Las aclaraciones
de revision-capturas-dmc3.md permanecen: antiguas exploratorias, inicio de una
con pitidos incierto, relatos/manualidad sin tiempos inventados.

### Qué quedó implementado y probado

- `tools/dmc3_temporal.py`: API offline determinista para validar registros,
  reconstruir ambos motions/state/contextos, segmentos/runs y generaciones,
  pérdidas, huecos, descenso de timer y comparar firmas/motivos entre capturas.
- `tools/analyze_dmc3_timeline.py`: CLI con manifiesto de hashes/revisiones;
  exporta JSON, cinco CSV y resumen Markdown a una carpeta única D:\logs.
  Nunca escribe en la captura histórica. Sin backend Windows, procesos o IPC.
- Detector experimental: hipótesis de familias de arma según MotionData superior
  y fuente DDMK; cadenas de motions adyacentes sin declarar combo completo.
  No usa BUSY/pitidos/etiquetas/timer como ataque. Build desconocida no habilita
  esas reglas. Sin nombres de ataques, impactos, daño o reacción GOW2.
- **34 tests sintéticos correctos**, en tests/test_dmc3_temporal.py y fixtures
  explícitamente sintéticos. Actor/foco/pausa/sala/generación, dos canales,
  timer desconocido/negativo, muestras atrasadas/duplicadas/incompletas/desorden,
  JSON/overflow, build, procedencia, hashes y exportación reproducible.
  No se repitieron suites Windows/PINE/inspectores sin cambios.
- Se reanalizaron **seis capturas / 1.370 muestras**, 1.193 aceptadas, 177
  rechazadas, 21 bloques, 80 segmentos y 63 runs superiores. Nueve firmas de
  ambos motions/state, siete superiores, ocho motivos repetidos; sin semántica
  autenticada. Los **34 archivos originales** conservan hashes antes/después.
- La espada devuelve cuatro hipótesis de familia melee, la primera con límite
  inicial desconocido; no cuatro ataques. La mixta 45 s devuelve una cadena
  candidata `(3,3) → (3,6)` sin identificar combo. La captura con disparo
  accidental no da candidato ranged: cobertura insuficiente, no ausencia de disparo.

### Investigación y lo que no quedó resuelto

DDMK **0319ae7132a6a822fd4dede2fb7cad484900169f**: 30 archivos fuente,
1.650.199 bytes, nueve copias previas reutilizadas y 21 textos públicos nuevos;
blobs Git coincidentes con el árbol fijado y SHA-256 conservados. No se ejecutó
el mod. Fuentes/manifiesto en
`D:\logs\dmc3-offline-research-20261016-171259-1b3c293254664b488b5ceccf158c5701`.

MotionData[0/1] son inferior/superior según fuente; coinciden en las 1.193
aceptadas, sin probar redundancia. Offset float32 +0x3E34 coincide con Vars y
generador (representaciones relacionadas, no pruebas independientes). No se
halló en Mary lógica que explique actualización/unidades/sentinel de motionTimer.
En espada las 198 aceptadas valen 2.0; en saltos/mixta posterior hay 17 rechazos
-1.0 con state crudo 1 o 2, antes de revalidar contexto. No certifica reloj de
animación, valor exclusivo de salto ni fallo de puntero. Mantener desconocido.
Otros campos/timers/action/chainCount están documentados como investigación;
**no se cambiaron dmc3_profile.py, el lector ni sus rangos**.

### Informes y reproducción

Salida final:
`D:\logs\dmc3-timeline-20261016-231402-e35c3bbc301c4da5a0b81813aaa4f9bf`.
analysis.json SHA-256
`ab20e0f3d717ed098a506b1c8e098873cf4e70162155eceac5dec62e779e3886`.
synthetic-tests-delivery.txt SHA-256
`4929de99ce643112afdea035e5153b62977f68e0c8fcb45639606016d91c8a85`.
Manifiesto esperado/invocación en
`D:\logs\dmc3-offline-validation-20261016-231219-b4cca074d33c45b6972ed3af9c74c594`.
La salida 231219 y test logs anteriores son checkpoints preservados. CLI,
API, presupuestos, criterios y comandos en dmc3-analisis-offline.md. Los CSV
se comprobaron contra filas JSON; informes completos y fuentes no van a Git.

**No hubo captura nueva, lectura de procesos, PINE, elevación de lector,
instaladores/hooks, escrituras ni acceso a juegos/ISO/BIOS/partidas.**
Blender y extracciones se preservan. phase2_verified=false y
authentic_attacks_detected=false. El protocolo futuro propone cuenta regresiva
y señales por acción, **todavía no implementadas**; la herramienta actual solo
emite inicio/fin. Fichas de combo requieren arma/ruta/entradas/ritmo confirmados.
Esperar las instrucciones del usuario para capturas; no ejecutar el diseño ahora.
Lo que sigue conserva el historial de revisión e implementación anterior.

## Revisión posterior de capturas · 2026-10-16

Punto de partida local/remoto: **ec85d8b4eef4968f9788a143dea9da223d1e2c3b**,
main limpio y sin avances remotos posteriores al comprobarlo. El usuario aclaró
que algunas capturas anteriores mezclaron golpes, combos y disparos por falta
de claridad. Inicialmente confirmó las últimas con pitidos; después advirtió
que una pudo empezar mientras ya golpeaba porque esperaba descargar algo para
la señal. No indicó inequívocamente cuál ni tiempos de acción. Los pitidos ya
usan Windows y no requieren descarga.

**Leer [la revisión por hipótesis](revision-capturas-dmc3.md) antes de continuar.**
Reutiliza seis capturas existentes; cinco parejas report/events conservan los
hashes de la auditoría anterior y las seis pasan secuencia/reloj/contadores.
Las primeras son exploratorias; la declarada de saltos no es negativo decisivo.
La espada con pitidos conserva asociación manual útil, pero inicio incierto y
cuatro intervalos brutos (3,3), uno ya activo al comenzar: no son cuatro ataques
detectados ni prueba de tres golpes delimitados. Su timer vale 2.0 en todas las
198 muestras coherentes, sin validar progreso de animación. La pausa/puerta
sigue sirviendo para esa invalidación y recuperación, con movimiento declarado.
No hay combo concreto completo identificado ni control aislado de disparos.

Auditoría privada nueva:
`D:\logs\dmc3-capture-review-20261016-031930-aa7413b5cd734d6890ea2dc42e13e5c6`.
Leer capture-review.json y **clarification-after-review.json**, que añade la
última aclaración sin alterar la primera revisión ni los originales. Hashes y
detalle en revision-capturas-dmc3.md. Las notas antiguas siguen siendo históricas.

Por petición del usuario, esta revisión solo analiza suficiencia: **sin funciones
nuevas, capturas, consulta a procesos ni PINE**. Próximo trabajo: revisar campos
y límites semánticos con lo existente antes de implementar o pedir pruebas.
Si después falta un control concreto, explicar por qué y dar duración, orden,
cantidad, reposos y prohibiciones antes de «Listo». Diferenciar golpe individual,
combo completo, disparo, salto, desplazamiento y reposo; estudiar combos como
acciones propias del combate original. No se piden repeticiones ahora.
Cambios documentales verificados por diff/enlaces; suites anteriores no repetidas.
phase2_verified sigue false. Lo que sigue conserva el informe histórico de
implementación; sus confirmaciones manuales se leen con esta revisión posterior.

## Observación DMC3 · 2026-10-16 · avance parcial

Referencia inicial y remoto comprobados: **4c93af92984d1efe842ae68f6913bee735701e9b**,
main limpio, sin avances posteriores al iniciar. Se leyeron los documentos
requeridos y los dos informes PINE con hashes publicados (020052 y 020627):
contenido, SHA-256, 21 eventos y secuencias correctos. **No se repitió PINE**.
La huella actual de dmc3.exe coincide con la documentada. La fase siguiente usa
[el observador DMC3](dmc3-observer.md), independiente del diagnóstico PINE finito.

### Qué se implementó y qué se comprobó

- `tools/observe_dmc3.py`: captura finita Windows x64 con Python estándar;
  `dmc3_memory.py`: APIs de consulta/lectura; `dmc3_profile.py`: guardas estáticas
  y campos candidatos; `analyze_dmc3_capture.py`: revisión automática de logs.
- Python local **3.12.14 x64** ya incluido en Codex. No se instaló otro runtime.
  El PID se descubrió nuevamente: primero **21132**, iniciado 05:21:36.6928085Z,
  con integridad alta/elevado. OpenProcess(0x410) devolvió **Win32 5**, cero
  lecturas RAM. La consulta de ruta sí funcionaba: no demuestra acceso de lectura.
- Se verificó el manifiesto asInvoker sin modificarlo. El usuario reabrió
  directamente dmc3.exe sin administrador. Nuevo PID **12156**, iniciado
  **05:29:18.123767Z**; lector y juego en integridad media/RID 8192, no elevados.
  Se obtuvo base real ASLR **0x7FF749D60000** y tamaño 14336000. Las direcciones
  son evidencia histórica de esta ejecución, **no parámetros para reutilizar**.
- Perfil candidato derivado de DDMK **0319ae7132a6a822fd4dede2fb7cad484900169f**,
  sin instalarlo. Hash/PE, una referencia RIP-relative al pool del actor y dos
  secuencias de código de las fuentes coinciden en archivo y memoria. Evento y
  sesión tienen evidencia de fuente/contexto; el detalle de esa diferencia,
  offsets, tamaños, punteros y política de rangos está en dmc3-observer.md.
- Se leyeron personaje, id/isClone, dos MotionData, motionTimer y state con
  páginas y lecturas completas verificadas. El intento completo usa 200 bytes
  de gameplay, no un volcado de estructuras. Hay datos reales de actor/motion;
  **no son aún un detector de ataques ni validación semántica completa**.
- Se descartan muestras por pérdida de foco, contexto/actor/proceso, página o
  lectura inválida. Contexto antes/después, generaciones y tres muestras de
  calentamiento impiden arrastrar valores antiguos. No es una transacción ni
  detecta necesariamente una recarga ABA entre ticks. Tener foco no certifica
  que un menú esté cerrado. g_scene de DDMK es estado del mod, no del juego.
- Se adaptó el procedimiento al usuario: DMC3 abre pausa al cambiar de ventana.
  Preparación **15 s**, pitido inicial, captura sin cambiar de ventana y pitido
  final. No exigir partida activa mientras el usuario responde en el chat.
  El usuario confirmó que los pitidos hacen más entendible la captura.

### Evidencia privada en D:\logs

Las carpetas siguientes son ejecuciones distintas; no asumir que la última
contiene una captura terminada. Cada informe conserva su versión real del
lector. Los resúmenes analizan secuencias, reloj y contadores sin detectar ataques.

| Carpeta (bajo D:\logs) | Resultado |
|---|---|
| `dmc3-research-20261016-022124-767-087b22554c664bb48a2f4628c1e6cc98` | Índice y fuentes públicas DDMK fijadas, solo investigación |
| `dmc3-access-20261016-022502-73c09498ed6d4aff817e9025a078cfd8` | Proceso elevado, error 5 al abrir 0x410; cero lecturas RAM |
| `dmc3-access-20261016-023005-f794fde5038a4b12b070f43b38062860` | Proceso reabierto sin elevar; base real y MZ leídos, 64 bytes |
| `dmc3-observe-20261016-023130-2bb2824f285c4ccea1a5ff3ba4834656` | Primeros candidatos reales: 20 muestras, 18 coherentes, 2 de calentamiento; 4173 bytes totales |
| `dmc3-observe-20261016-023401-74c4bea167e343d48364121f70c8a0fe` | Mixta 45 s: 450 muestras, 368 coherentes, 82 inválidas; 84893 bytes; no control limpio |
| `dmc3-observe-20261016-023634-aea8f72386cc417a8d477577486b01ed` | Saltos declarados originalmente: 200 muestras, 181 coherentes, 19 inválidas; 13 timers -1.0. Tras aclaración general, exploratoria y no negativo decisivo |
| `dmc3-observe-20261016-023832-3c0bdbfb62a147439b8c6693ea109c48` | Plan de espada **no limpio**: usuario informó disparo inicial; no usar como control de reposo/espada |
| `dmc3-observe-20261016-024702-93b5c31ffa994db1956f2c050369acde` | Espada con pitidos: inicialmente tres ataques/reposo declarados, sin disparo/salto; posible inicio ya activo aclarado después, no tres acciones delimitadas. 200 muestras, 198 coherentes, 2 calentamientos; 40173 bytes, sin lecturas fallidas/timers rechazados |
| `dmc3-observe-20261016-025054-9b073fab99fb467b88783a6e7fd6ff9b` | Pausa y puerta con pitidos: 300 muestras, 236 coherentes, 64 inválidas; 53661 bytes; usuario confirmó pausa, movimiento para situarse ante puerta y cruce |
| `dmc3-observe-20261016-025259-252d8deb23ac4afd97650143201514a4` | Modo final access-only correcto: 2 lecturas, 152 bytes de cabeceras; sin RVA/actor |
| `dmc3-tests-20261016-025204-787-aa78e9173c93413c98a55b3f5aee204b` | **26 tests correctos**: 25 sintéticos y una lectura Windows de buffer/imagen del propio Python; sin cerrar juegos |
| `dmc3-session-review-20261016-025629-a9af75698b0045cd92fe722939d9dded` | Auditoría de dos informes PINE reutilizados y cinco capturas DMC3; hashes de fuentes y notas manuales separadas |

session-review.json tiene SHA-256
`64c7a4fb4d22b6e2ff4582c273672e783df9cd1c552a999886c57aa29a278142`.
Cada una de esas cinco capturas conserva manual-review.json, con declaración
posterior del usuario y sin inventar tiempos de acción. El control con pitidos
de espada y el de pausa/puerta tienen confirmación manual explícita.

La primera mixta tuvo una secuencia errónea al principio, luego repetida y
finalmente juego minimizado, según el usuario. Las primeras capturas todavía
no tenían el filtro de foco final. No inventar tiempos de acciones a partir
del plan. Las etiquetas de las carpetas son intención; las confirmaciones del
jugador son evidencia manual separada de la memoria. No hubo marcas de un
operador independiente para cada golpe. El lector dispone de anotaciones
monotónicas manuales, siempre unverified, que no activan ataques.

Pausa/puerta: 48 muestras descartadas con evento 3 (~4,8 s), siete con evento 2,
una con valor 11 conservado sin interpretarlo, dos sin actor y seis de
calentamiento. Sala **127 → 114**, misión 7; se volvió a calentar aunque la
dirección del actor se reutilizó. No hubo error de acceso/lectura. Las
transiciones que vieron los logs y la confirmación del jugador son evidencia
real de esa ejecución, no cobertura de todos los menús/cargas.

Hashes de los dos informes con pitidos, para futuras comprobaciones:

- Espada report.json:
  `b554f65cd69fbd44c9eee2b60fb7ea042f316b26b6fd5ee14f9bb9c5f432f371`;
  events.jsonl:
  `40afe030e8aeaac5210d43a95c18e03b2100b5be0c8ac1f19136052093907174`.
- Pausa/puerta report.json:
  `ccff1dc96646c73254125136803495070adc5b6a406c28b30d4f28849cccd50e`;
  events.jsonl:
  `453c1c5fa54ce7d999c907b01ce2e45679304f744c3b7a8bb4e23a1925acbf88`.

### Qué queda pendiente

**Avance parcial de estados DMC3.** Acceso y observación candidata sí funcionan;
`phase2_verified=false`, `actor_semantics_verified=false` y ataques detectados
false. El timer **-1.0** aparece en control de saltos y su significado sigue
sin validar: se rechaza, no se amplía el rango para forzar éxito. Estado BUSY o
un cambio de motion no prueban un ataque. Se registraron valores de state fuera
de los tres bits nombrados en la referencia DDMK y se conservaron como u32.

Siguiente acción: revisar esos timers y correspondencia de motions con las
capturas existentes según revision-capturas-dmc3.md, antes de implementar más
o pedir controles. La captura de espada aporta acciones declaradas, con inicio
ahora incierto; no tres ventanas de acción marcadas independientemente.
Verificar más menús/transiciones antes de considerar un perfil robusto. No
volver a pedir la prueba PINE ni elevar el lector; guardar cualquier error de
acceso futuro con la nueva identidad de proceso. No avanzar a reacciones GOW2,
escrituras, DDMK instalado ni hooks gráficos en esta entrega.

## Primera prueba local · 2026-10-16

**PINE real verificado:** ejecución de Probe-Pine.ps1 con salida 0,
`phase1_verified=true`, sin errores. PCSX2 respondió `PCSX2 v2.8.2`, estado
`running` antes/después, God of War II, **SCUS-97481 / CRC 2F123FD8**, versión
de disco 1.01. Read32 en **0x00100008** devolvió **0x70000C28**, igual al ELF
de la ISO (offset 4104). Se revisaron report.json y los 21 eventos JSONL;
17 respuestas, únicamente opcodes 2,8,11,12,13,14,15 y una lectura RAM de 4 bytes.
No se verificó visualmente el gameplay desde el agente: el usuario informó
haber cargado partida, y PINE observó la VM en ejecución.

Informes privados, fuera de Git:

- Primer intento con salida 1, timeout TCP y ninguna lectura RAM:
  `D:\logs\pine-probe-20261016-015652-620-7d8b36ba84784c25ad8cfbf14e2f12fa`.
- Prueba correcta, salida 0:
  `D:\logs\pine-probe-20261016-020052-357-1ccbaefbfac345fdb51c9c7a88e794d6`.
  SHA-256 report.json
  `261985250867c198f28246425e78b5f1d0d5a8607626c3c85d733deef4b75cab`;
  events.jsonl
  `7adf8afb737a3ee340afd1c6cdb3e9ef49d45737063324fc81ed50b03deedcf6`.
- Captura con DMC3 abierto, cliente anterior: PINE correcto pero
  `dmc3.running=unknown_candidate_present`, MainModule/módulos no accesibles:
  `D:\logs\pine-probe-20261016-020327-264-6f85f9cd2a734b5d8a2ab6b04a7bbedc`.
- **Captura final con cliente corregido y ambos juegos abiertos**, salida 0,
  `phase1_verified=true`, `dmc3.running=confirmed`, sin errores globales:
  `D:\logs\pine-probe-20261016-020627-849-cef3b6e1780b4f7b8406ad4f86528806`.
  SHA-256 report.json
  `9a3c0eaf6de1bc574f0a5945aec73a9d9274f6da59ce09bd2af4ccdc436ded25`;
  events.jsonl
  `f662e6b83db7bce8d9fa47067409f55c7bc8bb6ff974e84a14d5d1810cbb2f76`.
  También 21 eventos, secuencias 1–21, 17 respuestas, un Read32 y los mismos
  opcodes permitidos, instrucción e identidad; estado running antes/después.
- Lectura independiente con inspect_ps2.py, salida 0:
  `D:\logs\disc-check-20261016-015829-827-566439793e184a69a736d1357d78d9af\disc-report.json`.
  ISO GODOFWAR2, 8533671936 bytes; ELF SCUS_974.81, 2125688 bytes,
  entrada 0x00100008, SHA-256
  `fd403603be46dea70d130695820d28b3f31de6d7e48484a5f006398a605f7dd6`.
  No se recalculó el CRC PCSX2 ni se certificó toda la imagen.

Comando real, desde la raíz, sin cambiar políticas de ejecución:

```powershell
& 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -NoProfile -File .\tools\Probe-Pine.ps1
```

Entorno comprobado: Windows 10 Pro x64 build 19045, Windows PowerShell
5.1.19041.6456 de 64 bits (diagnóstico) y PowerShell 7.6.5 (shell de trabajo).
PCSX2 desde `C:\Program Files\PCSX2\pcsx2-qt.exe`, versión de archivo/producto
2.8.2.0. El primer intento falló antes de que el usuario activara PINE y cargara
GOW2; el segundo pasó tras esos pasos. Se corrigió la ruta de la guía usando
MainWindow.ui y AdvancedSettingsWidget.ui oficiales v2.8.2: **Herramientas →
Mostrar ajustes avanzados**, después Ajustes → Emulación → Avanzados, al final
PINE Settings, Enable y Slot 28011. No se editó el INI desde el agente.

DMC3 no observado en las primeras dos capturas; después el usuario confirmó
haber entrado en partida con Dante y mantuvo PCSX2 abierto. **PID 23396 y ruta
real confirmados** en la captura final, coincidente con
`D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection\dmc3.exe`. Archivo dmc3.exe
accesible, 6356432 bytes, PE x64 (`0x8664`), timestamp PE 1521798082,
SizeOfImage 14336000, sin versión de archivo/producto declarada, SHA-256
`4ae4bb5c83c19a649fc60edc5ca40e7f3ceee6337e4e4275025bfa9caa40c0a0`.
Mary.dll y dinput8.dll ausentes en la raíz consultada; no se afirma ausencia
global de mods ni compatibilidad DDMK. MainModule devolvía nulo y la enumeración
de módulos no era accesible, incluso fuera del sandbox. Se comprobó que
QueryFullProcessImageNameW con PROCESS_QUERY_LIMITED_INFORMATION (0x1000)
sí podía devolver la ruta; se añadió como alternativa en Probe-Pine.ps1,
conservando el fallo anterior en main_module_error y registrando path_source.
No se solicita VM_READ/VM_WRITE ni debug privilege. Los módulos vacíos se
registran expresamente **unknown**, sin afirmar ausencia de DLL cargadas.

**Aceptación inicial cumplida:** PINE/identidad/instrucción verificados y DMC3
identificado independientemente por proceso/ruta/huella. Límite: módulos DMC3
desconocidos, sin lectura de actor ni acciones auténticas. No se midió FPS,
latencia ni consumo continuo de ambos juegos; las cifras del informe son una
captura puntual. Siguiente fase: estudiar esta build DMC3 y la posibilidad de
leer firmas/actor con permisos de lectura, antes de pedir correlaciones manuales
de reposo → ataque → reposo, salto, pausa y cambio de escena. Aún no hay detector
de ataques, reacción GOW2 ni integración visual. No hace falta repetir acciones
para este cliente: solo identifica proceso y una instrucción estática GOW2.

Git local/remoto coincidían en `99db3fc31a9da55d56a7fb0757fb9ca0d6a2f89f`,
main limpio al iniciar; se consultó/fetch del remoto. Para Git HTTPS se usa
`C:\Program Files\Git\cmd\git.exe`: el Git del runtime no encontró remote-https.
En este sandbox escribir D:\logs y acceder a GitHub requirió ejecución fuera
del sandbox; eso no significa ejecutar PINE como administrador. No se cambiaron
originales de los juegos ni se instalaron loaders/hooks.

Validación tras cambiar el cliente: **dos nuevos tests Windows correctos**
(ruta del proceso propio y PID inválido rechazado) y **ocho tests PINE anteriores
correctos** con Windows PowerShell 5.1. El test
test_fragmented_protocol_and_verified_code_read no se ejecutó porque exige
DMC3 cerrado; no se cerró el juego del usuario. No se repitieron los 22 tests
de inspectores sin cambios. Resultados en
`D:\logs\pine-validation-20261016-020524-384-a87616c80d8447c19a12e533ea27d6ae`
(process-image-tests.txt y pine-regression-tests.txt). Esto no son 33 tests
ejecutados: fueron diez tests seleccionados y después la captura real final.
Para reproducir la selección en PowerShell, usar Python disponible, PWSH_BIN
apuntando a Windows PowerShell 5.1, PYTHONPATH=tests y:

```python
import unittest
from test_pine_probe import PineProbeTests
names = unittest.defaultTestLoader.getTestCaseNames(PineProbeTests)
suite = unittest.TestSuite(PineProbeTests(name) for name in names
    if name != 'test_fragmented_protocol_and_verified_code_read')
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
```

Los nuevos tests se ejecutan con `python -m unittest test_process_image_path -v`
con ese PYTHONPATH; se omiten explícitamente fuera de Windows. Para guardar
salidas, crear una carpeta única en D:\logs y dirigir TMP/TEMP y el log de
la consola a ella durante esa ejecución, sin cambiar variables globales.

## Guardar y sincronizar los avances

**GitHub es el punto compartido de continuidad del proyecto.** Codex local no
debe asumir acceso al filesystem, los procesos, las sesiones o el historial de
Codex Cloud. Abrir este repositorio localmente proporciona los archivos que
estén publicados en GitHub, no el entorno de nube completo. Un ZIP es una copia
de un momento concreto; no recibe automáticamente cambios posteriores.

El usuario autoriza guardar en Dezva/DMC3-en-GOW2 todos los avances de código,
tests y documentación necesarios para continuar. El agente debe completar esta
sincronización sin pedir de nuevo autorización para cada entrega solicitada:

1. **Antes de trabajar:** comprobar estado local, rama y commits remotos. Si el
   usuario alterna local/nube, incorporar los avances publicados por la otra
   sesión preservando cambios existentes. No asumir que ambos checkouts están
   actualizados ni trabajar a la vez sobre la misma fase sin comprobarlo.
2. **Durante el trabajo:** guardar implementación, tests relevantes, versiones y
   configuración no secreta. Registrar en MODLOG.md resultados, errores,
   decisiones y el siguiente paso. Actualizar esta guía y el contrato si cambian
   arquitectura, requisitos, protocolo o criterios de aceptación.
3. **Al cerrar un avance:** revisar los archivos que se publicarán, hacer commit
   y push a la rama acordada (actualmente main) y verificar el SHA remoto.
   Entregar un enlace GitHub al commit o a los archivos, no rutas exclusivas del
   workspace local/nube. El usuario no necesita encargarse de esos pasos Git
   cuando el agente tiene herramientas y acceso para completarlos.
4. **Si queda incompleto o bloqueado:** guardar el punto alcanzado con su estado
   explícito. Distinguir archivo guardado, commit local y commit publicado. Un
   fallo de push requiere informar qué falta; nunca afirmar que GitHub contiene
   un avance que solo existe en el equipo actual.

Los informes completos permanecen bajo D:\logs y los recursos privados fuera
de Git. Sus conclusiones reproducibles y metadatos útiles sí deben incorporarse
a la documentación publicada. El manifiesto de recursos indica qué existe en
la nube; no es una copia de los modelos o de Blender. Si algo imprescindible
para una fase solo está fuera de Git, documentar cómo obtenerlo o reproducirlo
localmente antes de depender de ello. No publicar credenciales o binarios de
los juegos para intentar sincronizar los equipos.

La observación DMC3 actual puede continuar con el repositorio y las instalaciones
del usuario: no requiere los recursos Blender de nube. PINE ya está verificado;
el procedimiento histórico se conserva abajo para diagnosticar discrepancias.

## Objetivo que debe conservarse

Integrar **DMC3 HD Collection de Steam** con **God of War II de PS2 ejecutado por
PCSX2** para mantener los movimientos, animaciones, ataques, combos y mecánicas
auténticos de Dante dentro del mundo GOW2. El usuario precisó que un reemplazo
de aspecto no cumple el objetivo. La ruta inicial de conversión visual quedó
pausada; sus recursos y herramientas siguen conservados.

Prioridad actual: **observador DMC3 de solo lectura**, tras PINE verificado.
Completar la validación de estados reales antes de detectar acciones. No avanzar a composición visual sin
analizar acceso a cámara, profundidad, poses, colisiones y presupuesto del equipo.
Si un componente no resulta viable, explicar la limitación antes de cambiar de
enfoque. No hay una fusión completa ya implementada que baste con activar.

## Equipo y datos ya proporcionados

| Dato | Valor / evidencia |
|---|---|
| Sistema del usuario | Windows 10 Pro x64, build 19045; consulta local 2026-10-16 |
| CPU / RAM | Intel i5-4460 / 8 GB |
| GPU | NVIDIA GTX 1050; VRAM y driver exactos por verificar |
| PCSX2 | Archivo/producto 2.8.2.0 y respuesta PINE PCSX2 v2.8.2 comprobados localmente |
| Destino | God of War II NTSC-U, SCUS-97481, CRC 2F123FD8, según captura |
| ISO | `D:\Games PS2\God of War II [NTSC]\God of War II.iso` |
| DMC HD | `D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection` |
| Ejecutable esperado | `dmc3.exe`, PID/ruta real y huella PE/SHA confirmados; módulos desconocidos |
| PINE Windows | TCP local `127.0.0.1:28011`, identidad y Read32 real verificados 2026-10-16 |
| Logs / informes / muestras nuevos | `D:\logs`, subcarpetas únicas |
| BIOS y controles | Usuario tiene BIOS preparada; mando válido, teclado opcional |

GOW2 abre según el usuario; PINE quedó verificado localmente en esta sesión.
Control completo, guardado/carga y rendimiento siguen sin medir. La primera descarga europea era
**God of War I**, SCES-53133 / FB0E6D72: no es el destino ni un perfil compatible.
No volver a pedir los datos ya confirmados; verificar localmente si han cambiado.

## Qué existe y qué falta

| Componente | Estado comprobado | Límite |
|---|---|---|
| `tools/Probe-Pine.ps1` | TCP sintético y prueba real Windows 5.1 / PCSX2 2.8.2 correctos | No telemetría de gameplay |
| Identidad y lectura PINE | Prueba real: SCUS-97481/2F123FD8, Read32 0x70000C28 en 0x00100008 coincide con ISO | No posiciones, salud, ataques ni cámara |
| Observación DMC3 | Acceso x64/ASLR real, campos candidatos, espada/pausa/puerta observadas con confirmación manual | Perfil semántico parcial, timer -1 desconocido, sin detector ni compatibilidad DDMK |
| `inspect_ps2.py` | ISO9660/ELF de solo lectura; siete tests | No CHD/CSO ni CRC PNACH recalculado |
| `inspect_pac.py` | PAC/DDS, ocho tests y extracción real de muestra | No conversión PS2 |
| `inspect_gow_toc.py` | TOC, siete tests e índice real recibido | Segunda capa DVD9 no resuelta sin metadatos adicionales |
| Exportadores PowerShell | Scripts de muestras/índice conservados; pruebas sintéticas previas | No hace falta repetir exportaciones recibidas |
| Blender | Importación real cuerpo/abrigo, Blend/GLB y vista estática | Sin animación runtime, física de abrigo o integración GOW2 |
| Gameplay entre motores | Sin implementar | No detección auténtica de ataques ni reacción GOW2 |
| Composición visual | Investigación y requisitos documentados | Sin hooks, renderer compartido o prueba de rendimiento |

Última suite sintética: **31 tests correctos**, sin omitidos, combinando 22 tests de
inspectores y nueve de PINE con 17 escenarios. Ejecutados en Linux/Python 3.12 y
PowerShell 7.4.21. No equivalen a una partida. La prueba real Windows 5.1 de
esta sesión figura arriba y valida solamente el diagnóstico PINE y la huella de disco.

El cliente permite únicamente opcodes PINE 2,8,11,12,13,14,15, con respuesta
máxima 16 KiB y timeout. Exige PCSX2 2.8.2 y serial/CRC correctos antes de Read32.
Abre la ISO para lectura, encuentra la entrada ELF en segmento ejecutable y
comprueba dirección alineada en RAM EE; lee cuatro bytes y compara. No hay
opcodes de escritura, guardado/carga de savestate ni control de mando.

## Abrir el proyecto en Codex local

1. Descargar [el ZIP de main](https://github.com/Dezva/DMC3-en-GOW2/archive/refs/heads/main.zip)
   y extraerlo, o clonar el repositorio si ya hay Git. Una carpeta posible es
   `D:\Proyectos\DMC3-en-GOW2`; es una sugerencia, no una ruta comprobada.
   Para una clonación nueva en una ubicación libre:

   ```powershell
   git clone https://github.com/Dezva/DMC3-en-GOW2.git 'D:\Proyectos\DMC3-en-GOW2'
   ```

2. Abrir **la raíz del proyecto** en Codex local para que lea `AGENTS.md`.
   Si ya hay un checkout, revisar `git status` y preservar cambios antes de
   actualizar. No borrar ni reinicializar una carpeta existente para clonar.
3. Comprobar qué entorno ejecuta realmente las herramientas. Codex local puede
   usar Windows, WSL o un contenedor: no todos comparten red, permisos o procesos.
   Para esta primera prueba, el script debe ejecutarse en **PowerShell Windows
   de 64 bits junto al emulador**. WSL/Linux tienen distinta vista de procesos y
   no debe suponerse que su `127.0.0.1` llega al PINE TCP de Windows. Si se usa
   interoperabilidad, verificar el mecanismo y las rutas antes de ejecutar.
4. No instalar todo el setup Linux ni Blender/DDMK para probar PINE. En Windows
   el script utiliza PowerShell 5.1 o posterior y .NET. Las utilidades Python y
   Blender se necesitan solo al trabajar en sus respectivas partes.

Una sesión local podrá utilizar solo las capacidades y rutas que tenga
efectivamente disponibles. Detectarlas primero; no asumir control de la GUI o
acceso a todos los procesos por el hecho de ser local.

## Procedimiento histórico de la primera prueba PINE

1. Leer el estado del checkout y los informes `pine-probe-*` existentes bajo
   D:\logs, si los hay. Elegir informes por fecha/contenido, no asumir que el
   último directorio contiene una ejecución terminada. No volver a escanear
   toda la instalación ni pedir inventarios que ya se analizaron.
2. Verificar rutas de ISO y `dmc3.exe`. Detectar PCSX2 y si hay partida cargada.
   En la ventana principal PCSX2: **Herramientas → Mostrar ajustes avanzados**;
   después **Ajustes → Emulación → Avanzados**, bajar al final hasta **PINE**,
   habilitado, Slot28011. El agente no debe editar automáticamente otros ajustes.
3. Con GOW2 en una partida, ejecutar desde la raíz:

   ```powershell
   .\tools\Probe-Pine.ps1
   ```

   Si la política existente impide ejecutar el archivo, seguir la alternativa
   de copiar su contenido a la consola descrita en [pine.md](pine.md). No
   cambiar la política global ni asumir que hace falta elevar permisos.
4. Leer `report.json` y `events.jsonl` del nuevo directorio D:\logs\pine-probe-...
   **incluso si el comando termina con código 1**. El código 0 exige que la
   instrucción coincida con ISO; un puerto abierto no demuestra PINE funcional.
   DMC3 puede estar cerrado en esta primera ejecución.
5. Si versión/juego difieren, no relajar el filtro para forzar éxito: investigar
   la nueva identidad. Si el valor difiere, conservar esperado/real, consultar
   parches/estado de carga y estudiar la discrepancia sin escribirlo de vuelta.
   Error de acceso a proceso significa desconocido, no cerrado.
6. Después, con DMC3 abierto en partida, repetir y confirmar `dmc3.running`,
   ruta real, SHA/PE y módulos. Registrar si hay dos instalaciones o un proceso
   distinto del esperado. La compatibilidad DDMK sigue sin demostrarse por su
   presencia. El listener PINE y la lista de procesos se observan por separado;
   el cliente aún no verifica el PID dueño del puerto.
7. Actualizar el diario con SO/runtime, comandos, directorio de resultados,
   identidad, comparación de memoria y errores. Publicar el resumen técnico y
   cambios de código en GitHub; conservar informes completos en D:\logs. Con
   acceso local no es necesario que el usuario adjunte de nuevo cada informe.

Aceptación: `phase1_verified=true`, identidad correcta y memoria coincidente;
DMC3 identificado independientemente en la segunda captura. En pausa puede
validarse código estático; no prueba simulación activa. La reconsulta de
identidad no es una transacción ni detecta toda recarga del mismo juego.

## Qué hacer después y qué evidencia exigir

| Fase | Acción siguiente | Prueba necesaria antes de avanzar |
|---|---|---|
| Perfil DMC3 | Identificar la build y estudiar punteros/firmas y estructura actor | Cadena/rangos/identidad válidos en lecturas pequeñas y cambios de escena |
| Acción auténtica | Correlacionar personaje Dante, grupo/índice motion, timer y estado | Acción observada, transición correcta, sin falsos eventos en menús/carga |
| Primer evento GOW2 | Investigar una reacción pequeña con dirección/rutina y significado verificados | Reacción visible y registro causal; mecanismo de parada y ciclo de vida |
| Espacio compartido | Medir ejes, escala, cámara, proyección y colisiones en ambas direcciones | Correspondencia reproducible; nada de copiar XYZ sin medir |
| Viabilidad visual | Estudiar acceso a poses/color/depth y hooks compatibles | Oclusión, alineación, latencia, consumo y estabilidad en escenario pequeño |
| Mecánicas completas | Integrar hitboxes, daño, combos, cancelaciones, enemigos y transiciones | Casos reales de combate, muerte, pausas, carga y escenas |

Un evento manual solo puede ser un fixture temporal expresamente etiquetado;
no es un ataque auténtico. La fase actual no incluye ese generador ni una
reacción de escritura. No introducir escrituras exploratorias por avanzar
antes: primero identificar y documentar las variables.

PINE no exporta animaciones, color/depth GPU, mando o colisiones como API de
alto nivel. El motor DMC3 simula su propio escenario; mantener sus ataques no
le aporta automáticamente la colisión GOW2. Composición de imagen y dibujo de
geometría en PCSX2 son rutas todavía sin validar. DDMK tampoco es un adaptador
universal de motores. Más detalle en [arquitectura.md](arquitectura.md).

Para el i5-4460/GTX1050/8GB: medir cada juego solo, luego ambos si hay margen;
anotar FPS/velocidad emulada, RAM disponible/comprometida, memoria privada y
GPU/VRAM. Mantener Blender cerrado al jugar. No hay cifras de FPS medidas en
este equipo. Una futura telemetría de 20–30 Hz y prueba visual a 640×360/30 FPS son
presupuestos propuestos, no resultados ni motivos para ralentizar DMC3.

## Herramientas y fuentes ya investigadas

| Referencia | Revisión | Uso comprobado |
|---|---|---|
| [Universal Modder](https://github.com/rehan-remade/universal-modder) | `23902ef42e8ea9b077bfbbf6911eb8ea0348e55a` | CLI 0.2.0, búsquedas y guías de ruta/contrato; sin plugin UI ni adaptador de esta combinación |
| [PCSX2](https://github.com/PCSX2/pcsx2/tree/v2.8.2) | `fd9d310ccbb6b8b62c976da8886a3c8fd3a10ff3` | PINE.cpp y configuración/UI leídos; no emulador ejecutado aquí |
| [DDMK](https://github.com/serpentiem/ddmk) | `0319ae7132a6a822fd4dede2fb7cad484900169f` | Código Mary/DMC3 y estructuras leídos; sin instalación o perfil validado |
| [Importador DMC3](https://github.com/deshayu/DMC3HDC-Import-Tools) | `248dec2a0b7984fbd0c74f85c7de94a09dd81e06` | Importación real Blender 4.3.2; MIT, derivado de igrbn |
| [God of War Browser](https://github.com/mogaika/god_of_war_browser) | `1bfc55c0172e67c48c8e941c495333f583c721a0` | Fuentes/formato leídos; no ejecutar su apertura RW sobre originales |
| [RE4 × Minecraft del usuario](https://github.com/Dezva/Resident-evil-4-en-Minecraft) | `e20d988dec258c4ceb3dcd081429003378db02cd` | Contrato, lector y docs 0.4.45 leídos; no ejecutado desde esta nube |

Universal Modder aporta método y herramientas verificadas, no una fusión lista.
DDMK selecciona Mary para `dmc3.exe`, pero requiere comprobar la build y su
README advierte sobre actualizaciones. Sus direcciones no son perfiles listos
para la instalación del usuario. Memory_Init solicita 1 GiB; no es una medición
de working set. No instalarlo ni degradar Steam automáticamente para esta fase.

Del antecedente RE4/Minecraft son útiles firmas, propiedad de estado, canales
acotados y descarte de datos viejos. Sus hooks RE4/PE32/D3D9 y API Fabric no se
pueden aplicar directamente a estos dos motores. Su documentación también
mantiene pendientes de combate y validación Windows; no supone prueba aquí.

## Recursos y avances que no se trasladan con GitHub

El repositorio contiene código propio y documentación, **no los archivos
privados derivados de los juegos**. La ruta `/workspace/dmc3-private` pertenece
a esta nube, no es una carpeta de Windows ni se restaura al clonar. Se comprobó
su conservación durante la preparación de esta guía. El inventario
[recursos-preservados.json](recursos-preservados.json) registra nombres, tamaños
y SHA-256; no contiene los recursos ni los descarga.

| Carpeta privada en nube | Contenido conservado |
|---|---|
| `source-sample` | pl000.pac e informe; PAC 1335280 bytes, SHA `b73b6e8ee2f2088a088f4215a5a13a50700fb4e4f0bef54dc0bcce11ae7b9c5d` |
| `pl000-extracted` | Extracción de 15 slots y tres DDS; cuerpo/abrigo slots1/12 |
| `dante-source-blender-v4` | Blend, GLB, PNG e informe finales |
| `gow-index` | TOC, SYSTEM.CNF, CSV e informes de índice |
| `gow-samples` | R_HERO00/R_HERO01/R_PERMA.WAD e informe, hashes verificados |

Resultado Blender: 26 mallas, 6144 vértices, 4304 triángulos, esqueletos 24/33 huesos,
sin vértices sin peso positivo. Abrigo alineado provisionalmente coatbone0 a
bodybone1, no física CLT validada. GLB sin Draco; denoiser opcional desactivado.
Los modelos no son instalables en GOW2 ni contienen un puente de animaciones.

Inventarios ya recibidos: 281 archivos HD (-541/-069 idénticos),4334 entradas
NBZ. TOC 39000 bytes, 913 archivos / 1532 ubicaciones. WAD recibidos: 2301856,
2314640 y 3421104 bytes. No pedirlos ni repetir extracción para el diagnóstico.

Si una prueba visual posterior requiere estos recursos localmente, buscar
primero las carpetas de exportación originales bajo D:\logs. Si falta el Blend
final, conservar el de nube y reproducir una copia de trabajo desde el PAC local
con inspect_pac.py, import_dante_blender.py y el importador fijado, usando nuevas
carpetas D:\logs. El procedimiento exacto y las restricciones están en
[arquitectura.md](arquitectura.md). No se ejecuta esa reproducción ahora; el
trabajo PINE no depende de ella. No afirmar que el hash de un Blend regenerado
será idéntico entre rutas/versiones diferentes. No subir assets a GitHub.

## Validación para desarrollo

En Windows, con Python instalado, desde la raíz:

```powershell
py -3 -m unittest discover -s tests -v
```

Los tests encuentran `pwsh` o `powershell` en PATH; `PWSH_BIN` admite la ruta de
un ejecutable alternativo. Sin PowerShell se omiten los nueve tests PINE: no
declarar 31 verificaciones en ese caso. Son pruebas sintéticas con puertos
temporales; no intentan conectarse al emulador real para validar gameplay.
**La suite PINE espera DMC3 cerrado en el caso de detección negativa**; ejecutarla
antes de las pruebas con ambos juegos, o reconocer esa precondición si falla.
No cerrar procesos del usuario automáticamente para satisfacer un test.

Windows PowerShell 5.1 no se probó en la nube; localmente pasó la prueba real
PINE descrita arriba, sin ejecutar la suite sintética completa. Si una prueba falla en Windows,
guardar la causa y diferenciar portabilidad, precondiciones y defecto real;
no modificar expectativas para aparentar éxito. Los instaladores `setup_* .sh`
del repositorio contienen rutas y runtime Linux; no son necesarios en Windows.
En la nube el comando usado fue:

```sh
PWSH_BIN=/workspace/.dmc-tools/powershell-7.4.21/pwsh python3 -m unittest discover -s tests -v
```

Para cambios solo documentales: revisar enlaces/consistencia y diff; no hace
falta ejecutar de nuevo juegos o las31 pruebas. Después de cambios al cliente,
verificar protocolo/errores relevantes y registrar los resultados reales.

## Mensaje para iniciar la siguiente sesión local

Puedes pegar este texto al abrir el proyecto en Codex:

> Lee AGENTS.md y docs/CONTINUIDAD-LOCAL.md de este repositorio y continúa desde
> su estado actual. Quiero integrar los motores de DMC3 HD Collection y God of
> War II, conservando las mecánicas y animaciones reales de Dante. Comprueba el
> estado local/remoto e incorpora avances posteriores preservando cambios.
> Revisa integridad y contenido de los informes existentes de D:\logs. PINE ya
> está verificado; no lo repitas salvo evidencia ausente, cambio o discrepancia.
> Continúa el observador externo DMC3 exclusivamente de lectura desde su estado
> actual: hash/build, PID nuevo, inicio, base real, derechos mínimos y páginas.
> Lee docs/revision-capturas-dmc3.md, docs/dmc3-analisis-offline.md y
> docs/dmc3-campos-investigacion.md. Ya hay analizador offline y pruebas sintéticas;
> reutiliza los informes finales y hashes, sin confundir hipótesis con ataques.
> No abras ni controles juegos ni hagas capturas durante mi ausencia. Las pruebas
> controladas están autorizadas una por una tras ficha completa y un nuevo «Listo».
> R20/E1/E1-R están confirmadas; J1 es exploratoria por duración de pulsación
> incierta. J1-R ya tiene toque único y reposo declarados; sus cuatro -1 siguen
> rechazados. No repetir capturas por rutina: revisar suficiencia y timer primero.
> Lee docs/dmc3-validacion-controlada.md para el estado más reciente. La señal
> intermedia única --action-cue-seconds ya está implementada, probada y utilizada.
> No hay cuenta regresiva ni múltiples señales de acción. Las primeras
> capturas son exploratorias y una con pitidos tiene inicio incierto.
> Distingue golpes individuales, combos completos, disparos, saltos, movimiento
> y reposo. No certifiques acciones por etiquetas manuales o cambios de motion.
> Si después hace falta una prueba concreta, explica por qué y da duración,
> orden, número de acciones, reposos y prohibiciones; no pidas repetir por rutina.
> Investiga el timer -1.0 y valida semántica/motions sin transformar una etiqueta
> manual o cambio de animación en ataque. Usa preparación y pitidos para las
> capturas: DMC3 vuelve a pausa al cambiar de ventana. No reutilices PID/base
> históricos, no eleves permisos, no escribas memoria ni instales DDMK/loaders
> o hooks gráficos. Conserva desconocidos y diferencia tests, lecturas reales y
> declaraciones del usuario. No declares la fase cerrada si falta validación.
> Conserva Blender/modelos y publica los
> scripts y la documentación que me entregues en el GitHub del proyecto.
> Guarda también los demás cambios de código, tests, documentación y pasos de
> reproducción necesarios para continuar. Haz commit y push y verifica que
> quedaron publicados; no dependas de acceso a Codex Cloud para recuperar avances.
