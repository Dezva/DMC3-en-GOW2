# Diario del proyecto

## R20 real confirmada · señal única preparada para E1

R20 autorizada explícitamente: 25 s preparación, ~20 s / 200 muestras / 10 Hz.
Usuario confirmó después reposo completo y ambas señales, Rebellion/Gunslinger,
misión 7 normal y zona sin enemigos. Lecturas: **198 coherentes, dos de
calentamiento**, ambas parejas motion grupo 0/índice 3, state=1, timer=2.0 constante.
Un bloque/contexto estable; cero errores o ticks omitidos. Cadencia real mediana
99,94 ms, min 63,92/max 147,37. 2.0 no es exclusivo de ataque ni demuestra progreso.
Asociación manual de esta condición, sin clasificador universal de reposo.

Identidad actual redescubierta: PID 10688/inicio 02:38:13.424527Z UTC, base real
0x7FF7C6920000, mismo SHA/PE; ambos tokens medios no elevados. Acceso 0x410 y
guardas correctos; 3405 lecturas/40173 bytes. No PID/base históricos reutilizados,
escrituras, PINE, DLL/hooks o configuración modificada.
Captura dmc3-observe-20261016-234822-3cbbbb1ec2ac49039ef1ab1dd9f985fd;
hash report `9c88411b354360ce976c270ca8f81ddda66c7fd4bd025357be881110f175323b`,
events `63fde113ffebf3e4654263bc3c2abe426fc0701116e50a0d5c62e5da27103178`.
Nota manual e imagen previa privadas conservadas sin alterar fuentes.
Análisis en dmc3-timeline-20261016-235300-a26781cdf9024d9580d05fca7d62a3a4;
hash analysis.json `522d0d71d767c50c8b26306db96bc93072b7d72c1f644be72841e897a73bc666`.

Para E1 se añadió ajuste mínimo opcional --action-cue-seconds: una sola señal
corta 1200 Hz/60 ms durante captura, con begin/end monotónicos y tiempos
previstos/reales, sin inferir acción. Requiere --beep y margen, rechaza modo
access-only/anotación/NaN/fuera de rango. Perfil/punteros/filtros intactos.
Siete tests nuevos de coordinación y 59 regresiones sintéticas correctos, sin
WindowsSelfRead o juegos. Demo acústica sin memoria confirmada audible por usuario;
datos en dmc3-cue-check-20261016-235229-be0b7635cebc48b38748577f893c91a7.
La demo usó tiempo simulado 5/5 del helper, no una captura; eventos monotónicos
conservan su horario real y separación acelerada. No confundir con ejecución.

E1 todavía no iniciada; requiere instrucciones completas y nueva preparación:
25 s para volver, primer pitido reposo, a ~5 s tono corto para una pulsación de
espada, soltar y reposo hasta pitido grave (~20 s totales). Revisar jitter/ticks
por coste de la señal síncrona y límites entre muestras, no precisión por frame.
Detalle en dmc3-validacion-controlada.md. Fase parcial, sin ataques autenticados,
combo completo, impactos ni reacción GOW2. Informes completos fuera de Git.

## Retoma de pruebas controladas · ficha R20 propuesta

Nueva petición autoriza coordinar capturas con el usuario después de revisar
evidencia. Partida main **ee6bde30a38ffa0327755651f8657de0a9fdccd9**, limpio
y coincidente con GitHub, sin avances posteriores al comprobarlo. Se leyeron
instrucciones, continuidad, observador, revisión, investigación y diario.
Reanalizadas seis capturas directamente: 34 archivos históricos coinciden con
los hashes de auditoría. También coinciden dos parejas PINE; no se repitió PINE.

Falta negativo de reposo con equipo/contexto y ejecución explícitamente confirmados.
Propuesta mínima R20: 25 s de preparación, inicio agudo, 20 s quieto, fin grave;
200 muestras/10 Hz y cero acciones voluntarias, con señales existentes. No se
cambia perfil, filtro de -1 o significado del timer. Luego podría contrastarse
un golpe individual en otra captura, mismo equipo, sin activar esa prueba ahora.
Ficha detallada, hipótesis, prohibiciones y límites en dmc3-validacion-controlada.md.
Informe privado: D:\logs\dmc3-validation-preparation-20261016-234354-301d05ffad984276bd31887ade7779ba\preparation.json,
SHA-256 `437489d5b6381d553d5d4bfb3fd68df4f23cddafee53460fde8e1f26acd88e77`.
Contexto aportado después: misión 7 normal al inicio de una partida guardada;
Cerberus/Rebellion y pistolas/escopeta disponibles. Sala desconocida; se pidió
confirmar Rebellion activa, Dante, estilo y entorno sin enemigos. Nota privada
context-user-report.json nueva; respuesta de contexto no equivale a «Listo».

Se pidió personaje/arma/estilo/contexto; esa respuesta no equivale a preparación.
**No hubo muestreo, consulta a procesos, lectura RAM, señal acústica nueva ni
captura real en esta preparación.** Esperar confirmación tras instrucciones.
Actualizados AGENTS, ficha y continuidad para que el límite histórico offline
no bloquee la nueva autorización. Validación documental y relectura de informes;
sin suites nuevas por no cambiar código. Fase parcial, sin detector definitivo,
ataques autenticados, escritura de memoria o reacción GOW2.

## Objetivo y ruta acordados

Dante con movimientos, animaciones, combos y mecánicas originales de DMC3 HD
Collection dentro del mundo de God of War II de PS2, mediante integración entre
motores. El usuario descarta limitarlo a un reemplazo de aspecto. Se conserva
todo el trabajo de recursos/Blender; su conversión queda pausada. Ruta vigente
de Universal Modder: intercambio de estado primero, viabilidad visual después.
No hay mod jugable ni comunicación de gameplay entre los juegos todavía.

Destino: SCUS-97481, NTSC-U, CRC 2F123FD8 según captura; PCSX2 2.8.2.0 según el
usuario. La prueba inicial europea era del primer God of War y no valida este
destino. Pendiente control, guardado y carga del segundo juego.

Preferencia del usuario: los nuevos logs, informes y muestras locales de Windows
van a **D:\logs**. No escribirlos en el escritorio. La nube no accede a su D:.

## Comprobaciones completadas

- Dos inventarios de instalación idénticos: 281 registros.
- Índice NBZ recibido: 4334 entradas; muestra pl000.pac seleccionada.
- Muestra recibida e informe coincidentes: 1335280 bytes, SHA-256
  b73b6e8ee2f2088a088f4215a5a13a50700fb4e4f0bef54dc0bcce11ae7b9c5d.
- PAC leído: 15 posiciones, tres PAC internos y tres DDS DXT5. Texturas abiertas
  y examinadas. Cuerpo y abrigo identificados con código DDMK.
- Lector propio PAC y CLI: 8 pruebas sintéticas nuevas; suite total 15/15.
- Importación de la muestra real en Blender 4.3.2: 26 mallas, 6144 vértices,
  4304 triángulos y dos esqueletos de 24/33 huesos. Ningún vértice importado sin
  peso positivo. GLB exportado con mallas, skins e imágenes; vista estática renderizada.
- Colocación del abrigo en la vista: alineación provisional con pelvis del cuerpo;
  no se reprodujo la física CLT. No es evidencia de animación ni de retargeting.
- Lector PowerShell del índice de God of War II: seis ejecuciones sintéticas
  correctas, incluidos fallos esperados por otra edición, índice ausente e imagen
  inválida o truncada. Repetir no sobrescribe resultados previos.
- Índice real PS2 recibido: 39000 bytes, SHA-256
  9b339a2dfda12827d221e173a2fb806d7be5d6c436bcffcc650e1486604d77b0,
  coincide con informe. SYSTEM.CNF confirma SCUS_974.81 / VER 1.01 / NTSC.
  913 archivos y 1532 ubicaciones, direccionamiento por paquetes DVD9.
- Lector TOC propio: siete nuevas pruebas; suite total actual **22/22**.
- Muestras recibidas 2026-10-16: R_HERO00.WAD (2301856), R_HERO01.WAD (2314640),
  R_PERMA.WAD (3421104 bytes), total 8037600 bytes, copia de PART1.PAK.
  ZIP CRC y hashes coinciden con informe. Conservadas en
  /workspace/dmc3-private/gow-samples. Cabeceras WAD inspeccionadas; no se
  profundiza en conversión por el cambio de prioridad del usuario.
  SHA-256 respectivos:
  41ed2683dfc01d6cbb4328444bba199f56df910cd82a6cd62c92cf5adf4d8a35,
  804934c2fea75d7893ed33b5c7fd3b7e2611ade39a3096a4e79d0137d35447e2,
  1efbec140179820fbfaf4685c8a1a7f7f5cc35eaa0e22e0d74ab6a28ee528760.
- R_HERO00 tiene cinco ubicaciones (3 PART1, 2 PART2). No asumir igualdad entre
  ellas ni que reemplazar una sola valide cambios de nivel.
- Export-GowHeroSamples.ps1 probado en seis ejecuciones PowerShell/Linux usando
  el índice y raíz reales con datos WAD sintéticos. Copias, hashes y ZIP CRC
  comprobados, repetición sin sobrescribir, errores de índice/serial/límites/ISO
  ausente registrados. No probado aún en Windows ni con los paquetes reales.

## Herramientas y fuentes

- Universal Modder: 23902ef42e8ea9b077bfbbf6911eb8ea0348e55a; leídas habilidades
  mod-any-game, mashup-mods y reverse-engineering; ejecutada CLI kb search.
  No hay antecedente exacto encontrado para DMC3/PCSX2. No se instaló plugin UI.
- DDMK: 0319ae7132a6a822fd4dede2fb7cad484900169f, inspección de fuentes.
- Importador Blender deshayu/DMC3HDC-Import-Tools:
  248dec2a0b7984fbd0c74f85c7de94a09dd81e06; probado con muestra real.
- God of War Browser: 1bfc55c0172e67c48c8e941c495333f583c721a0;
  solo inspección de código/documentación, sin imagen real ni ejecución.
- Dependencias fijadas preparadas en /workspace/.dmc-tools mediante
  tools/setup_cloud_tools.sh; instalación y repetición verificadas.
  Los clones iniciales de investigación están en /tmp y no deben asumirse persistentes.
  Recursos privados derivados: /workspace/dmc3-private, fuera del checkout Git.

## Fallos y correcciones

El primer render falló por denoising no disponible; se desactivó el denoiser
opcional. Se corrigió el parent de submallas al armature para evitar warnings de
skin durante exportación GLB. Draco no está disponible: GLB sin esa compresión.
El primer render colocaba el abrigo bajo el cuerpo debido a sus orígenes distintos;
se documentó una alineación provisional para inspección estática.

## Próximo paso y criterio de éxito · actualizado

El índice, muestras GOW2, pl000.pac e inventarios ya se recibieron; no pedirlos
de nuevo. PINE ya quedó verificado según las entradas locales posteriores.
Ya hay analizador offline probado sobre las capturas existentes, con hipótesis
sin ataques autenticados. Siguiente paso: resolver campos y preparar validación
según las instrucciones anunciadas por el usuario; no abrir juegos ni pedir
pruebas ahora. Véanse docs/dmc3-analisis-offline.md y continuidad.
Éxito de esta fase: identidad PINE correcta y una instrucción de RAM coincidente
con el ELF; proceso y huella DMC3 registrados independientemente. Eso no prueba
combate ni composición visual. A continuación preparar un perfil DMC3 de lectura
validado antes de detectar una acción auténtica y diseñar una reacción GOW2.

## 2026-10-16 · fase PINE, sin escrituras

Auditoría: no existía IPC con ninguno de los juegos; había inspectores de
archivos y Blender funcionando. No se reemplazó ningún transporte anterior.
Se contrastó PINE con PCSX2 v2.8.2, commit
fd9d310ccbb6b8b62c976da8886a3c8fd3a10ff3. TCP loopback Windows, Slot28011;
Linux usa socket Unix. Se verificaron opcodes, framing, cadenas y estados.

Se añadió tools/Probe-Pine.ps1: cliente finito de solo lectura, límites y timeout,
versión/serial/CRC como requisito previo a Read32, instrucción derivada del ELF
de la ISO en segmento ejecutable/RAM EE y reconsulta de identidad. Errores,
ausencia de DMC3 y discrepancias quedan registrados. Detecta procesos/rutas,
huella SHA-256/PE y módulos Mary/dinput8 observados, sin instalar/inocular DLL.
No hay perfil de combate, entrada manual de prueba ni reenvío de controles.

Se estudió DDMK como referencia para motionData/motionTimer/state. Sus punteros
no están habilitados: falta validar la build real. Memory_Init solicita 1GiB;
no se afirma un consumo residente medido. Se prioriza observador ligero.

Usuario aportó Dezva/Resident-evil-4-en-Minecraft. Se leyó su revisión
e20d988dec258c4ceb3dcd081429003378db02cd (0.4.45), documentación, contrato,
validación y lector. Sirve como antecedente de separación de canales, firmas,
caducidad y pruebas. No se ejecutó ni se copió su DLL/offsets: hooks RE4 D3D9 y
API Fabric no son adaptadores de PCSX2/DMC3. Su combate completo sigue pendiente
según su propia documentación.

Nuevo docs/CONTRACT.md define propiedad y ciclo de vida; docs/arquitectura.md
expone límites de PINE, rutas visuales y presupuesto propuesto, sin afirmar FPS.
Se preservaron los inspectores, exportadores y resultados privados de Blender.
Hasta esta fase no se habían publicado archivos, commits, PRs ni mensajes externos.

Validación de esta fase: 22 pruebas anteriores conservadas y correctas; nueve
pruebas nuevas del cliente PowerShell, con 17 ejecuciones de escenarios, todas
correctas y ninguna omitida. Total: **31 pruebas**. Incluyen TCP fragmentado,
versiones/juegos incorrectos, desconexión/timeout/protocolo inválido, código
distinto, cambio de identidad, MMIO/segmento no ejecutable rechazados y alias
KSEG0 normalizado. Fuentes sintéticas sin modificaciones y solo opcodes de
lectura observados. No prueban los procesos o juegos reales de Windows.

PowerShell 7.4.21 Linux x86_64 preparado mediante
tools/setup_pine_test_runtime.sh: paquete Microsoft/GitHub y ejecutable con
SHA-256 verificado. Primera instalación y repetición correctas. Setup completo
tools/setup_cloud_tools.sh repetido con Universal Modder, Blender y runtime
comprobados. Windows PowerShell 5.1 se declara como destino del script y queda
pendiente de ejecución real; no se afirma haberlo probado.

## 2026-10-16 · entrega por GitHub autorizada

El usuario pide que los archivos se entreguen mediante el repositorio vinculado
para poder descargarlos. Se publicó el código propio, tests y documentación en
main de Dezva/DMC3-en-GOW2, commit d8bd78e762792730a4709be4a9a53980e27756c7,
con enlaces al ZIP y al diagnóstico. Se comprobó el ZIP descargado de GitHub,
su CRC y que Probe-Pine.ps1 coincide con el código publicado.
Se conservan fuera de Git los juegos, BIOS, muestras y resultados Blender.
Esta publicación no valida todavía PINE en su Windows ni implica un mod jugable.

## 2026-10-16 · continuidad para Codex local

El usuario va a crear un entorno local para facilitar el acceso a su Windows.
La documentación anterior ya estaba publicada. Se añade AGENTS.md para que
Codex lea automáticamente objetivo/prioridades, y docs/CONTINUIDAD-LOCAL.md con
estado verificado, rutas, limitaciones, primera sesión PINE, fases siguientes,
dependencias fijadas, pruebas y mensaje de inicio. docs/README.md reúne toda la
documentación y README enlaza la guía local.

Se comprobó la conservación de los recursos privados y se generó
docs/recursos-preservados.json con nombres/tamaños/hashes de los grupos elegidos.
No se subieron assets ni se asumió que una clonación los trasladaría al PC. Se
documenta cómo buscar exportaciones locales previas o reproducir una copia
Blender más adelante, sin convertirlo en una dependencia del diagnóstico.

Revisión de consistencia: retiradas referencias obsoletas a muestras todavía
pendientes. Señalada la precondición DMC3 cerrado en el test sintético de
detección negativa. No cambia código del puente ni su protocolo; los 31 tests
anteriores siguen siendo evidencia histórica Linux. No se ejecutaron juegos,
ni hubo nueva verificación de Windows o memoria real en esta entrega documental.
Se comprobaron los enlaces relativos de los 12 documentos Markdown y los hashes
de las 34 entradas del inventario privado; no contienen los recursos binarios.

## 2026-10-16 · persistencia de avances entre nube y local

El usuario pide asegurar que todos los cambios necesarios para progresar queden
en GitHub y aclara que desconoce si Codex local puede acceder a Codex Cloud.
Se establece GitHub como continuidad compartida, sin asumir acceso entre
sesiones. AGENTS.md exige guardar código/tests/documentación/configuración no
secreta, registrar estado y siguiente paso, hacer commit/push y verificar el SHA
remoto. La guía local distingue copia ZIP, cambios locales, commits y publicación.

Se mantiene la separación de recursos privados: sus metadatos y reproducción
están documentados, pero clonar no descarga assets de nube. PINE no depende de
esos modelos. No hay cambios al cliente o nuevas pruebas de juego en esta entrega.

## 2026-10-16 · primera prueba PINE real en Windows

Checkout existente en main, limpio y coincidente con GitHub al iniciar
(`99db3fc31a9da55d56a7fb0757fb9ca0d6a2f89f`); remoto consultado/fetch antes de
editar. Comprobados Windows 10 Pro x64 build 19045, PowerShell 7.6.5 y Windows
PowerShell 5.1.19041.6456 x64. PCSX2 abierto desde Program Files, versión de
archivo/producto 2.8.2.0; dmc3.exe e ISO accesibles en las rutas previstas.

Primer Probe-Pine.ps1, salida 1 por timeout TCP, conservado en
`D:\logs\pine-probe-20261016-015652-620-7d8b36ba84784c25ad8cfbf14e2f12fa`.
El usuario necesitó ayuda para localizar PINE. La UI oficial v2.8.2 mostró un
error en nuestra guía: Mostrar ajustes avanzados pertenece a **Herramientas**,
no Ajustes. Corregido en pine.md y continuidad; después Ajustes → Emulación →
Avanzados, bajar al final hasta PINE. El usuario confirmó activación Slot 28011
y GOW2 en partida. No se editó automáticamente el INI.

Segunda ejecución con Windows PowerShell 5.1, **salida 0, phase1_verified=true,
sin errores**. PINE respondió PCSX2 v2.8.2, running, God of War II,
SCUS-97481, CRC 2f123fd8, disco 1.01. Read32 en **0x00100008** devolvió
**0x70000C28**, igual a la ISO; identidad/estado válidos antes/después.
Se leyeron report.json y los 21 eventos JSONL: 17 respuestas de lectura y una
sola lectura RAM de cuatro bytes. Carpeta:
`D:\logs\pine-probe-20261016-020052-357-1ccbaefbfac345fdb51c9c7a88e794d6`.
No equivale a observar gameplay visualmente ni a detectar ataques o salud.

inspect_ps2.py leyó la ISO real sin cambios y devolvió SCUS-97481, GODOFWAR2,
entrada ELF 0x00100008 y SHA-256, salida 0. Informe nuevo en
`D:\logs\disc-check-20261016-015829-827-566439793e184a69a736d1357d78d9af`.
Huella PE/SHA de dmc3.exe registrada, pero DMC3 no observado ejecutándose.
Metadatos y reproducción en la guía local; informes privados fuera de Git.
No se modificaron originales de juegos ni memoria ni se instalaron DLL/hooks.
El usuario después confirmó DMC3 en partida, con PCSX2 abierto. Una captura
adicional confirmó PINE pero dejó el proceso DMC3 desconocido por MainModule
nulo y módulos inaccesibles, incluso fuera del sandbox. Una consulta mínima
QueryFullProcessImageNameW sí devolvió la ruta. Se añadió esa alternativa a
Probe-Pine.ps1, usando solo PROCESS_QUERY_LIMITED_INFORMATION (0x1000), con
cierre de handle, path_source y conservación del error MainModule. Una lista
vacía de módulos se registra unknown; no se solicitan VM_READ/VM_WRITE ni
debug privilege. No se amplía la lectura de memoria de juegos.

**Captura final correcta con cliente actualizado**, salida 0:
`D:\logs\pine-probe-20261016-020627-849-cef3b6e1780b4f7b8406ad4f86528806`.
PINE/identidad/instrucción correctos y **dmc3.running=confirmed**, PID 23396,
ruta real de la instalación esperada, misma huella PE/SHA de disco. Módulos
DMC3 siguen desconocidos, expresamente registrado. Report.json y los 21 eventos
JSONL revisados; hashes en continuidad. Se cumple la aceptación inicial de
PINE y proceso DMC3 independiente, con la limitación de módulos desconocidos.

Validación Windows PowerShell 5.1: dos nuevos tests de ruta con permisos mínimos
(proceso propio/PID inválido) y ocho tests PINE anteriores correctos. Excluido
explícitamente el test que exige DMC3 cerrado; no se cerró el juego del usuario.
No se repitieron los 22 tests de inspectores. Logs de los diez tests en
`D:\logs\pine-validation-20261016-020524-384-a87616c80d8447c19a12e533ea27d6ae`;
sin fallos en la selección ejecutada. Las 31 pruebas Linux anteriores siguen
siendo evidencia histórica, no una suite completa repetida en Windows.

Siguiente fase: estudiar esta build DMC3 y comprobar acceso de lectura a
firmas/actor antes de correlacionar reposo, ataque, salto, pausa y cambio de
escena. No pedir esas acciones como si ya hubiese detector ni presentar el
consumo puntual como medición de rendimiento. Sin puente de gameplay, reacción
GOW2 ni composición visual; juegos, BIOS, informes completos y assets fuera de Git.

## 2026-10-16 · observador externo DMC3, validación parcial

Se comenzó desde main limpio/local-remoto **4c93af92984d1efe842ae68f6913bee735701e9b**,
sin avances posteriores al iniciar. Se leyeron los documentos requeridos y se
comprobaron los dos informes PINE con hashes publicados: JSON, SHA-256, 21 eventos
y secuencias coincidentes. No se repitió PINE ni se cambió Probe-Pine.ps1.
La huella dmc3.exe sigue siendo 4ae4bb5c83c19a649fc60edc5ca40e7f3ceee6337e4e4275025bfa9caa40c0a0.

Implementados observe_dmc3.py, dmc3_memory.py, dmc3_profile.py y
analyze_dmc3_capture.py con Python 3.12.14 x64 ya disponible. Solo consultas y
ReadProcessMemory: handle 0x410 (QUERY_INFORMATION | VM_READ), VirtualQueryEx,
lecturas completas y páginas legibles, identidad PID/ruta/inicio y base real
bajo ASLR. Modo access-only independiente del perfil de gameplay. Capturas
finitas, límites de frecuencia/tamaño y descarte de ticks atrasados. Sin API de
escritura, debug privilege, elevación automática, DLL, DDMK instalado ni hooks.

Primero, PID actual 21132 elevado/RID 12288: OpenProcess devolvió error 5 y no
se leyó RAM, aunque funcionaba consultar la ruta. Se comprobó manifiesto asInvoker.
Tras reapertura manual directa sin administrador, PID 12156/RID 8192 como el
lector, inicio 05:29:18.123767Z. Base real 0x7FF749D60000, SizeOfImage 14336000;
se leyeron cabeceras y guardas de código. Módulos adicionales no inventariados.

Investigadas fuentes DDMK 0319ae7132a6a822fd4dede2fb7cad484900169f sin ejecutarlas.
Perfil candidato: pool actor RVA C90E28 → slot 3; pool evento C90E10 → slot 8;
sesión inline C8F250. Campos personaje, id/clone, motion index/group, timer y
state. Hash/PE exactos, raíces en sección escribible, referencia MOV RIP-relative
de actor en RVA 3D570 y dos secuencias de Mary/Global verificadas también en RAM.
Evento/sesión conservan evidencia de fuente/contexto, no una firma semántica
independiente. Procedencia, tipos, tamaños y limitaciones en dmc3-observer.md.

Resultados reales:

- Acceso y primer muestreo: 20 muestras, 18 candidatas coherentes, 2 de
  calentamiento, 4173 bytes totales. Contexto y punteros se vuelven a consultar;
  no se leen estructuras enteras ni se escanea la RAM.
- La mixta de 45 s y el primer plan de espada no son controles limpios: el
  usuario informó secuencia inicial incorrecta/repetida/minimización y un
  disparo accidental en la prueba posterior. Se conservan como tales.
- Control de saltos confirmado: 200 muestras, 181 coherentes, 13 timers **-1.0**
  rechazados más 6 calentamientos. El significado de -1 permanece desconocido;
  no se relajó el rango para forzar éxito.
- DMC3 abre pausa al cambiar de ventana, según usuario. Se adaptó el observador
  con 15 s de preparación y pitidos inicial/final. También se descartan muestras
  cuando el PID del juego pierde el foco; tener foco no demuestra que no haya
  menús. Los primeros logs anteriores al filtro conservan esa limitación.
- Espada con pitidos: el usuario confirmó tres ataques separados y reposo,
  sin salto/disparo. **200 muestras, 198 coherentes, 2 calentamientos**, sin
  lecturas fallidas ni timers rechazados; 40173 bytes.
- Pausa/puerta con pitidos: **300 muestras, 236 coherentes y 64 inválidas**:
  48 evento pausa, 7 evento 2, 1 valor 11 sin interpretar, 2 sin actor y 6
  calentamientos. Sala **127 → 114**, misión 7; dirección de actor reutilizada
  pero muestras anteriores invalidadas y calentamiento nuevo. El usuario
  confirmó pausa, desplazamiento para colocarse ante puerta y cruce. 53661 bytes.
- Modo final access-only: 2 lecturas/152 bytes de cabeceras, sin raíces de actor.

Las etiquetas de captura representan intención y los reportes del usuario son
anotaciones manuales sin tiempos precisos por golpe. No se presentan como
acciones detectadas; BUSY o cualquier cambio de motion no basta. Los registros
tienen UTC/monotónico, sesión, secuencia/generación e invalidaciones; el analizador
valida su consistencia y guarda hashes. No son un snapshot atómico ni detectan
todas las recargas ABA del mismo contexto. Ningún dato se envía a GOW2.

Validación final: **26 pruebas correctas** (25 sintéticas y una de lectura de
imagen/buffer del propio proceso Python en Windows). Incluyen permisos/denegación,
build incompatible, guardas, punteros/páginas, lecturas parciales, pérdida de
actor/proceso/foco, pausa/contexto, timers desconocidos, etiquetas e integridad
de logs. No se cerraron juegos ni se repitieron PINE/inspectores sin cambios.
Log: D:\logs\dmc3-tests-20261016-025204-787-aa78e9173c93413c98a55b3f5aee204b.
Carpetas, hashes y reproducción de capturas reales en la continuidad.

Actualizados AGENTS, README, índice, contrato de observación v2, arquitectura,
guía del observador y continuidad, incluido el prompt obsoleto de repetir PINE.
Informe parcial: **phase2_verified=false**, semántica de actor sin certificar y
sin detector. Próximo paso: investigar timer -1 y completar mapeo temporal de
acciones con repeticiones/controles. No se declara cerrada la fase de estados.
Originales de juegos, configuración, Blender y extracciones preservados; fuentes
de investigación e informes completos quedan en D:\logs, fuera de Git.

## 2026-10-16 · revisión retrospectiva y aclaración de capturas

Partida desde **ec85d8b4eef4968f9788a143dea9da223d1e2c3b**, main local/remoto
coincidentes y limpio, sin avances posteriores al consultar el remoto. El
usuario aclaró que algunas pruebas antiguas mezclaron golpes, combos y disparos
por falta de claridad; se conservan como exploratorias. La antigua declaración
de solo saltos permanece, sin usarla como negativo decisivo tras esa aclaración.

Las últimas con pitidos fueron inicialmente confirmadas, pero el usuario añadió
después que una pudo comenzar mientras ya golpeaba: esperaba descargar algo y
la señal le sorprendió. No identificó con certeza cuál ni tiempos por acción.
No se atribuye una causa probada al intervalo inicial de espada ni se inventan
disparos/saltos nuevos. Los pitidos ya usan winsound.Beep, sin descarga.

Reanalizadas seis capturas existentes con la función de solo lectura publicada:
JSON, sesión, secuencia, reloj y contadores consistentes. Cinco parejas report/
events coinciden con hashes de la auditoría anterior, también comprobada. La
espada conserva 198/200 muestras coherentes y asociación manual útil, pero no
tres golpes delimitados: hay cuatro intervalos brutos (3,3), uno ya activo al
inicio, que no equivalen a cuatro ataques. Timer=2.0 en todas las 198; no valida
progreso de animación. La pausa/puerta conserva evidencia de invalidación y
recuperación sala 127 → 114, con desplazamiento manual declarado.

Nueva docs/revision-capturas-dmc3.md: suficiencia y carencias para golpe
individual, combo completo, disparo, salto, desplazamiento, reposo y ciclo de
vida. Los combos se estudiarán como secuencias propias, sin inferir completitud
de cambios de motion o BUSY. Faltan identidad de combo/arma/ruta, límites y
negativos aislados. Primero revisar significados con lo existente, sin pedir
al jugador una secuencia que aún no sabemos distinguir. Próximas peticiones
deberán explicar hipótesis, duración, orden, cantidad, reposos y prohibiciones.
Posibles señales por acción quedan propuestas; no se implementaron.

Auditoría privada nueva en
`D:\logs\dmc3-capture-review-20261016-031930-aa7413b5cd734d6890ea2dc42e13e5c6`.
capture-review.json SHA-256
`105ef1b5c57d9eec613b00b759311c3eed5d15344cb6f108964d446840a00843`;
clarification-after-review.json SHA-256
`003453e2fc73d45ec62f434212ce2d6badd77fa622384c78ce2950b1f3788394`.
Leer ambos: el segundo limita las clasificaciones manuales del primero. No se
sobrescribieron archivos originales ni notas históricas. Informes completos
permanecen privados; solo conclusiones/metadatos se guardan en GitHub.

Actualizados instrucciones, README, índice, arquitectura, guía del observador
y continuidad/prompt. Sin implementación, nueva captura, acceso a procesos,
escritura en juegos ni repetición PINE. Validación de esta entrega documental:
análisis de logs, hashes, diff y enlaces; no se repitieron suites sin cambios.
**phase2_verified=false**; sin detector, reacción GOW2 o composición visual.

## 2026-10-16 · análisis temporal offline y detector experimental de hipótesis

La nueva petición autoriza avanzar offline durante la ausencia del usuario;
supersede el límite de implementación de la revisión anterior, sin autorizar
juegos/pruebas manuales. Partida **a04276b29c642e1b1ce117ce662835ba5903c235**,
main local/remoto limpio y sin avances posteriores al comprobarlo. Se leyeron
instrucciones, continuidad, diario, contrato, revisión y herramientas actuales.

Investigación: 30 fuentes DDMK fijadas, 1.650.199 bytes; nueve copias existentes,
21 textos públicos descargados y todos los blobs comprobados contra árbol fijado.
MotionData[0/1] corresponden a inferior/superior según la fuente. El timer float32
+0x3E34 coincide con Vars/generador, pero no hay lógica explicativa de su uso
en las fuentes Mary revisadas. No se resolvió unidad, sentinel -1 ni motivo de
2.0 constante en espada. Las declaraciones/generador no son pruebas semánticas
independientes. Documentados campos complementarios; **perfil y lector intactos**.

Implementados tools/dmc3_temporal.py y tools/analyze_dmc3_timeline.py: validación
estricta sin ordenar/deduplicar entradas, cronologías, ambos motions/state,
bloques por contexto/actor/generación y pérdidas, segmentos estables, descenso
de timer, comparaciones de firmas/motivos y exportación JSON/CSV/Markdown a
carpetas únicas fuera de los históricos. API pura y determinista sin backend
Windows. Edges censurados y transiciones acotadas entre muestras; no tiempos
de acción inventados. Separadas memoria registrada, declaración, hipótesis y
acciones autenticadas (vacías).

Regla experimental de familia superior derivada de DDMK con guardas de build:
eventos melee/ranged de motion y cadenas adyacentes candidatas. No son ataques,
combo completo o impacto; sin nombres inventados ni BUSY/timer/pitidos como
prueba de ataque. No se usa el texto manual como feature. Perfil desconocido
conserva datos brutos sin reglas de familia; error de integridad aborta exportación.

Reanalizadas seis capturas históricas, **1.370 muestras**: 1.193 aceptadas, 177
rechazadas, 21 bloques, 80 segmentos, 63 runs superiores. Los 34 archivos
originales conservan hashes antes/después. Trece episodios hipotéticos de
familia cuerpo a cuerpo y una cadena `(3,3) → (3,6)` en la mixta; **no son trece
golpes ni un combo validado**. Espada: cuatro hipótesis, primera ya activa;
sin tres ventanas independientes. Cero ranged incluso en la captura con disparo
declarado: cobertura insuficiente, no negativo autenticado. Nueve firmas de
motion/state, siete superiores y ocho motivos repetidos sin nombre de acción.

**34 tests sintéticos correctos**: separados/cadenas, reposo/movimientos no
ofensivos, actor/foco/pausa/sala/generación, canales, timer desconocido/negativo,
duplicados/incompletos/retrasados/desorden, JSON ambiguo/nonfinite/overflow,
build, etiquetas/cues, hashes, CSV y reproducibilidad. CSV reales cotejados
contra JSON. No se ejecutaron tests que lean juegos ni se repitieron PINE/Windows.

Salida final:
`D:\logs\dmc3-timeline-20261016-231402-e35c3bbc301c4da5a0b81813aaa4f9bf`.
analysis.json SHA-256
`ab20e0f3d717ed098a506b1c8e098873cf4e70162155eceac5dec62e779e3886`;
synthetic-tests-delivery.txt SHA-256
`4929de99ce643112afdea035e5153b62977f68e0c8fcb45639606016d91c8a85`.
Invocación/manifiesto en dmc3-offline-validation-20261016-231219; fuentes en
dmc3-offline-research-20261016-171259; rutas completas en continuidad. Checkpoints
intermedios preservados. Informes/fuentes completos privados fuera de Git.

Documentados API/resultados, investigación y protocolo futuro por acción, con
preparación, cuenta regresiva, señales, orden, cantidades, reposos/prohibiciones,
controles y sincronización independiente propuesta. No ejecutado; señales por
acción aún sin implementar y ficha de combo pendiente de ruta/entradas exactas.
Usuario anunció instrucciones antes de pruebas: **esperar, no solicitar capturas**.
Actualizados AGENTS/README/índice, arquitectura, contrato, observador y continuidad.

Sin abrir/controlar juegos, consultar RAM/procesos, repetir PINE, elevar lector,
instalar mod/hooks, tocar originales/partidas/ISO/BIOS ni reacción/composición GOW2.
Blender/extracciones preservados. Avance parcial verificable; **phase2_verified=false,
authentic_attacks_detected=false**. Pendientes significado del timer/otros campos,
observación independiente, controles aislados, repeticiones y validación fuera
del conjunto exploratorio antes de afirmar reconocimiento auténtico.
