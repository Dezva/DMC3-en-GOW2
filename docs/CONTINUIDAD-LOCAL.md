# Continuidad para Codex local en Windows

Estado de referencia: 16 de octubre de 2026. Esta guía permite continuar desde
el repositorio sin depender del historial del chat ni del filesystem de nube.
Actualizar al obtener evidencia nueva; los resultados siguientes son históricos,
no pruebas ejecutadas automáticamente al abrir este archivo.

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
> No abras ni controles juegos ni hagas capturas durante mi ausencia. Espera mis
> instrucciones anunciadas antes de pruebas en juego. El protocolo futuro no
> está ejecutado y las señales intermedias no están implementadas. Las primeras
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
