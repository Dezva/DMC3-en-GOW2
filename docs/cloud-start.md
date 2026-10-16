# Inicio reutilizable del entorno de desarrollo

Para la continuidad en el PC Windows del usuario, lee AGENTS.md y
docs/CONTINUIDAD-LOCAL.md. Esta guía de nube contiene rutas específicas Linux;
no trasladar sus instaladores a Windows ni asumir que los assets privados se
descargan al clonar GitHub. El índice completo está en docs/README.md.

Trabaja en `/workspace/DMC3-en-GOW2`, checkout existente. Cada tarea de nube ya
está aislada: no crees un Git worktree salvo petición explícita del usuario.
Lee instrucciones AGENTS.md aplicables, README.md, MODLOG.md, docs/CONTRACT.md,
docs/pine.md y docs/arquitectura.md antes de continuar. Conserva los cambios
locales. El usuario autorizó publicar los scripts y la documentación en
`Dezva/DMC3-en-GOW2` y pide recibir los archivos descargables por ese GitHub,
no mediante enlaces locales del entorno de nube. Entrega enlaces GitHub a los
archivos publicados o al ZIP de main. Conserva esa preferencia en futuras
entregas; no publiques assets de juegos, BIOS ni archivos privados de Blender.
No abras PR ni envíes mensajes a terceros sin una petición específica.

Objetivo vigente: integrar motores y conservar movimientos, animaciones, combos
y mecánicas originales de DMC3 dentro del mundo GOW2. No reducirlo a reemplazar
el aspecto de Kratos. Conversión de recursos pausada; conservar modelos y
Blender. Priorizar PINE de solo lectura y posteriormente estados auténticos
DMC3. No escribir memoria desconocida ni instalar loaders/DDMK en esta fase.
Si una ruta no es viable, explicar la limitación antes de cambiar el enfoque.

Usuario: Windows, i5-4460, GTX 1050 (VRAM desconocida), 8 GB RAM. HD Collection
Steam en `D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection`. Tiene BIOS propia.
PCSX2 2.8.2.0 según el usuario; GOW2 abre. Captura: SCUS-97481 NTSC-U,
CRC 2F123FD8, ISO `D:\Games PS2\God of War II [NTSC]\God of War II.iso`.
La imagen anterior SCES-53133/FB0E6D72 era del primer GOW, no usarla. No volver a
preguntar versión, edición o BIOS. Un mando es válido; teclado opcional.

Todos los nuevos informes/logs/muestras Windows se guardan en `D:\logs`, en
carpetas únicas, nunca escritorio. Esta nube Linux no accede a D:, PCSX2 o
procesos Windows. No hay servicio real que arrancar aquí. Los tests inician y
cierran su propio servidor TCP sintético; no confundirlo con PCSX2. Los tests
no demuestran funcionamiento en partida ni rendimiento real.

## Herramientas y comprobación

`bash tools/setup_cloud_tools.sh` prepara/verifica dependencias fijadas en
`/workspace/.dmc-tools`: Universal Modder 23902ef42e8ea9b077bfbbf6911eb8ea0348e55a,
CLI0.2.0, y deshayu/DMC3HDC-Import-Tools
248dec2a0b7984fbd0c74f85c7de94a09dd81e06 (MIT). Son dependencias, no otros proyectos
del usuario. Python/Pillow/numpy/PyYAML y Blender 4.3.2 proporcionados por la
imagen y comprobados. No recompilar ni reinstalar herramientas válidas sin motivo.
CLI: `UM_NO_UV=1 /workspace/.dmc-tools/universal-modder/bin/um --version`.
Se aplican mod-any-game, mashup-mods y reverse-engineering donde corresponda;
no hay plugin UI instalado. `um win` requiere Windows/WSL; no da acceso al PC
del usuario desde esta nube. No instalar su adaptador pesado para esta prueba.

El setup incluye `tools/setup_pine_test_runtime.sh`: PowerShell 7.4.21 portátil
Linux x86_64 con SHA-256 del paquete y pwsh verificados, instalado en
`/workspace/.dmc-tools/powershell-7.4.21`. No se necesita en el Windows del usuario.
Las pruebas redirigen XDG_CACHE_HOME/XDG_CONFIG_HOME/XDG_DATA_HOME a un temporal
escribible para el proceso hijo; no cambies HOME ni vuelques variables/secretos.
Comando requerido desde el checkout:

```sh
PWSH_BIN=/workspace/.dmc-tools/powershell-7.4.21/pwsh python3 -m unittest discover -s tests -v
```

Sin pwsh se omiten pruebas PINE: no declarar el puente verificado en ese caso.
Los inspectores Python son stdlib; los tests usan ISO/PE/datos sintéticos y un
cliente PowerShell real. No hace falta ejecutar Blender para modificar el puente.
Validaciones, resultados y limitaciones deben quedar en MODLOG.md.

## Fase actual y siguiente prueba real

`tools/Probe-Pine.ps1` es finito y de solo lectura, sin Python para el usuario.
Consulta PINE TCP Windows 127.0.0.1:28011, verifica versión 2.8.2, serial/CRC,
deriva una instrucción del ELF ejecutable en la ISO y hace un solo Read32 en
RAM EE alineada. Reconsulta identidad y estado; discrepancia implica fallo,
nunca corrección automática. Lista procesos PCSX2/DMC3, huellas SHA-256/PE,
versiones, working set/private bytes y módulos Mary/dinput8 observados. No
detecta ataques ni transmite gameplay. DMC3/DDMK compatibilidad sin verificar.

Siguiente paso: usuario activa PINE (avanzados, Enable, Slot28011), carga GOW2
y ejecuta el script conforme a la política existente; después repite con DMC3
en partida para identificar el proceso real. Adjunta report.json y events.jsonl
de la carpeta D:\logs\pine-probe-...; no pedir ISO, BIOS o ejecutables completos.
Ver docs/pine.md para errores/campos. No afirmar que se probó la conexión Windows.
Tras esos datos, validar un perfil DMC3 antes de leer estados auténticos; solo
entonces planear una reacción pequeña GOW2 por una dirección/rutina conocida.

Fuentes inspeccionadas: PCSX2 v2.8.2
fd9d310ccbb6b8b62c976da8886a3c8fd3a10ff3 (PINE.cpp, UI/bindings). Windows TCP,
Linux socket Unix. PINE no expone GPU/depth ni API de ataques. DDMK
0319ae7132a6a822fd4dede2fb7cad484900169f: Mary para dmc3.exe, motionData/timer/state
como candidatos de investigación, no offsets aplicables a cualquier build.
Memory_Init solicita 1 GiB, no una medición de RAM residente. No se ejecutó.
Referencia del usuario Dezva/Resident-evil-4-en-Minecraft, commit
e20d988dec258c4ceb3dcd081429003378db02cd /0.4.45: se leyeron contrato, documentación,
validación y lector; no se ejecutó. Sus hooks RE4 D3D9/PE32 y API Fabric no son
reutilizables directamente. Adoptar separación de canales, caducidad, generaciones
y pruebas verificables. No dar por probado combate pendiente según ese proyecto.

## Recursos recibidos y preservados fuera de Git

Inventarios HD 281 entradas (-541/-069 idénticos), NBZ 4334; no repetir. PAC y
informe en `/workspace/dmc3-private/source-sample`; pl000.pac 1335280 bytes,
SHA256 b73b6e8ee2f2088a088f4215a5a13a50700fb4e4f0bef54dc0bcce11ae7b9c5d.
Extracción en pl000-extracted: 15 slots, tres DDS DXT5, cuerpo/abrigo slots1/12.
Blender final `/workspace/dmc3-private/dante-source-blender-v4`: Blend, GLB, PNG,
informe. 26 mallas,6144 vértices,4304 triángulos, skins24/33 huesos, sin vértices
sin peso positivo. Abrigo alineado provisionalmente bone0 a bodybone1, sin
validar física CLT o retarget. GLB sin Draco; denoiser opcional desactivado por
falta de OpenImageDenoise. No regenerar ni borrar salidas sin motivo.

Índice real en `/workspace/dmc3-private/gow-index`: TOC39000 bytes, SHA256
9b339a2dfda12827d221e173a2fb806d7be5d6c436bcffcc650e1486604d77b0,
913 archivos/1532 ubicaciones. BOOT2 SCUS_974.81 /VER1.01/NTSC. PART1 sector1654,
4264382464 bytes; ubicaciones de PART2 requieren metadatos de segunda capa,
no interpretar índices >=10000000 como sectores ISO físicos. HERO00 tiene cinco
ubicaciones (3PART1/2PART2): no asumir igualdad.

ZIP de tres WAD ya recibido y verificado (tamaños, CRC ZIP y SHA contra informe)
en `/workspace/dmc3-private/gow-samples`: R_HERO00.WAD2301856 bytes,
R_HERO01.WAD2314640, R_PERMA.WAD3421104. Hashes en MODLOG.md. No volver a pedirlos.
No se profundizó en su conversión por la prioridad PINE. Conservar originales
y assets fuera de Git. God of War Browser commit
1bfc55c0172e67c48c8e941c495333f583c721a0 solo se inspeccionó, no se ejecutó.
Su apertura RW por defecto desaconseja usarlo sobre originales.

Los clones /tmp de investigación pueden desaparecer; recrear solo si necesario,
desde commits documentados. No publicar assets ni usar generación pagada.
No hay benchmarks de GTX1050/i5-4460/8GB: analizar viabilidad y medir antes de
renderizar/componer ambos juegos. Plan y límites están en docs/arquitectura.md.
