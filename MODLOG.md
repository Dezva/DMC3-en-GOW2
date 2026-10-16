# Diario del proyecto

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

## Próximo paso y criterio de éxito

El índice, muestras GOW2, pl000.pac e inventarios ya se recibieron; no pedirlos
de nuevo. El siguiente paso real es activar PINE en PCSX2 y ejecutar
tools/Probe-Pine.ps1 en Windows: primero GOW2 y después con DMC3 abierto.
Adjuntar report.json y events.jsonl de D:\logs\pine-probe-...; véase docs/pine.md.
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
