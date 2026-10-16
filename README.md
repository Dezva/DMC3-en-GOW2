# DMC3 en God of War II · PS2 / PCSX2

## Descargar los archivos

Descarga [el proyecto completo en ZIP desde GitHub](https://github.com/Dezva/DMC3-en-GOW2/archive/refs/heads/main.zip)
y utiliza **Extraer todo** en Windows. El diagnóstico está en
[`tools/Probe-Pine.ps1`](https://github.com/Dezva/DMC3-en-GOW2/blob/main/tools/Probe-Pine.ps1);
puedes descargarlo desde su página con **Download raw file**.
Las instrucciones están en [docs/pine.md](docs/pine.md).

**Para continuar en Codex local:** abre la raíz de este proyecto y utiliza
[la guía de continuidad](docs/CONTINUIDAD-LOCAL.md). Incluye el estado comprobado,
la próxima prueba, las fases posteriores y un mensaje listo para iniciar la
sesión. [AGENTS.md](AGENTS.md) conserva las instrucciones para Codex y el
[índice de documentación](docs/README.md) reúne la investigación disponible.

Los scripts y la documentación se entregan mediante este repositorio, según
la preferencia del usuario. El ZIP no incluye juegos, BIOS, modelos extraídos
ni archivos privados de Blender; esos recursos se conservan por separado.

Proyecto para investigar una **integración entre motores**: Dante conserva los
movimientos, animaciones y mecánicas auténticos de **DMC3 HD Collection** dentro
del mundo de **God of War II de PS2**. No se limita a sustituir un modelo.

**Fase actual:** observador externo DMC3 de solo lectura, con PINE ya verificado.
Hay lecturas reales de campos candidatos; la validación de acciones y ciclo de
vida sigue parcial. Véase [el observador DMC3](docs/dmc3-observer.md).
El usuario utiliza Windows y tiene HD Collection
para PC en `D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection`. Ya dispone de
una BIOS de PS2 y PCSX2 **2.8.2.0**, versión indicada por el usuario. La captura
de propiedades identifica ahora **God of War II NTSC-U**, **SCUS-97481**,
**CRC 2F123FD8**, ubicado en
`D:\Games PS2\God of War II [NTSC]\God of War II.iso`.
La primera prueba local de solo lectura confirmó PCSX2 v2.8.2, esa identidad
de GOW2 y una instrucción RAM coincidente con la ISO; detalles en la guía local.

La imagen europea anterior era del **primer God of War**, SCES-53133 / FB0E6D72;
no debe utilizarse como destino de este proyecto.

Los inventarios y las muestras ya se recibieron; [la preparación en Windows](docs/windows.md)
se conserva como referencia de los pasos anteriores y de los controles.
El [análisis de DMC3](docs/inventario-dmc3.md) registra los inventarios y recursos
identificados. La [ruta de implementación](docs/arquitectura.md) explica cómo se
utiliza Universal Modder en este proyecto.

La muestra `GData.afs/pl000.pac` ya se recibió y verificó contra su informe.
Se extrajeron tres DDS y se importaron cuerpo y abrigo en Blender: **26 mallas,
6144 vértices y 4304 triángulos**, con esqueletos de 24 y 33 huesos. Se conservan
los modelos, las texturas, el Blend y el GLB. Su conversión para reemplazar a
Kratos queda pausada. Las tres muestras WAD de GOW2 ya se recibieron y verificaron.
Los próximos informes y muestras locales de Windows se guardarán bajo
**`D:\logs`**, según la preferencia del usuario.

**Estado:** extracción e importación 3D verificadas y diagnóstico PINE implementado.
Cliente probado con datos sintéticos y **PINE real verificado en Windows
PowerShell 5.1**: SCUS-97481/2F123FD8, lectura 0x70000C28 en 0x00100008 igual a
la ISO, phase1_verified=true. Segunda captura con DMC3 ejecutándose confirmada
por PID/ruta y huella PE/SHA; sus módulos no pudieron inspeccionarse.
No hay comunicación de gameplay entre juegos, detector de
ataques, composición visual ni mod jugable. Consulta [la prueba PINE](docs/pine.md),
el [contrato](docs/CONTRACT.md) y [los límites y fases](docs/arquitectura.md).

## Siguiente prueba en Windows: observación DMC3

La evidencia PINE íntegra ya sirve; no hay que repetirla por cada captura DMC3.
El observador usa Python x64 y biblioteca estándar, identifica nuevamente el
proceso, comprueba huella/base real/páginas y lee bloques pequeños. No usa PINE,
DDMK instalado ni una DLL dentro del juego. En esta sesión se utilizó el Python
que ya incluye Codex. Comandos y perfil en [docs/dmc3-observer.md](docs/dmc3-observer.md).

Para capturas manuales hay 15 s de preparación y pitidos al inicio/fin, porque
DMC3 abre la pausa al cambiar de ventana. No se interpreta una etiqueta manual,
BUSY ni cualquier cambio de motion como un ataque. `phase2_verified` sigue false;
motionTimer=-1.0 se registra como desconocido y descarta esas muestras.

## Repetir PINE solo si hace falta investigar

En PCSX2 activa Herramientas → Mostrar ajustes avanzados; después abre Ajustes
→ Emulación → Avanzados y baja hasta PINE (Enable, Slot 28011). Carga GOW2 y ejecuta
desde la raíz del proyecto, en PowerShell de 64 bits:

```powershell
.\tools\Probe-Pine.ps1
```

Utiliza las rutas de ambos juegos ya indicadas. Crea una carpeta nueva
`D:\logs\pine-probe-...` con `report.json` y `events.jsonl`. Identifica el juego,
compara una instrucción de RAM con el ELF de la ISO y registra procesos y huellas
PE de DMC3. No instala DLL ni escribe en memoria. DMC3 puede estar cerrado;
para comprobar su proceso real, ejecuta otra vez con DMC3 abierto en una partida.
Instrucciones y diagnóstico de errores en [docs/pine.md](docs/pine.md).

## Preparación

El diagnóstico Windows utiliza PowerShell 5.1 o posterior y .NET, sin Python ni
Universal Modder instalado en el PC. Los inspectores Python requieren Python 3.10 o posterior, sin dependencias
externas. La importación 3D opcional requiere Blender y el importador externo
indicado en [la documentación](docs/arquitectura.md). PCSX2 se configura en la máquina donde se vaya a jugar,
con una BIOS de PS2 y una imagen del juego aportadas por el usuario. Los formatos
concretos de los modelos de ambos juegos todavía requieren investigación.

Conserva imágenes, BIOS y recursos extraídos fuera del repositorio. En la nube se
utiliza `/workspace/dmc3-private`; en Windows, los informes y muestras van bajo
`D:\logs`. `local/` permanece ignorado por Git para proteger salidas antiguas.
Conserva los originales y utiliza archivos de trabajo separados.

## Identificar la edición de PS2

Desde la raíz del repositorio:

```sh
python3 tools/inspect_ps2.py /ruta/a/God-of-War-II.iso
```

Lee una ISO9660 sin comprimir de sectores de 2048 bytes, localiza `SYSTEM.CNF`,
resuelve su ejecutable `BOOT2` y devuelve JSON con el código de disco, dirección
de entrada y SHA-256 del ELF. Abre la imagen únicamente para lectura. No extrae
recursos, no parchea el juego y no acepta CHD/CSO ni imágenes raw de 2352 bytes.
Rechaza extensiones ISO9660 no soportadas en lugar de interpretarlas parcialmente.
La huella SHA-256 **no es el CRC usado por los archivos PNACH de PCSX2**.

Para guardar un informe en Windows desde PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path 'D:\logs' | Out-Null
$discReport = Join-Path 'D:\logs' ('disc-report-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '.json')
py tools/inspect_ps2.py 'D:\Games PS2\God of War II [NTSC]\God of War II.iso' | Out-File -LiteralPath $discReport -Encoding utf8 -NoClobber
```

Solo conserva el informe si el comando termina correctamente. La herramienta
identifica el ejecutable; no certifica la integridad de toda la imagen ni confirma
por sí sola que corresponda a God of War II.

## Validación de las herramientas

```sh
python3 -m unittest discover -s tests -v
```

Las pruebas construyen imágenes sintéticas sin contenido de juegos. Validan la
lectura y los errores de las herramientas; no sustituyen las pruebas en PCSX2.
Los tests del cliente necesitan PowerShell; en la nube:

```sh
bash tools/setup_pine_test_runtime.sh
PWSH_BIN=/workspace/.dmc-tools/powershell-7.4.21/pwsh python3 -m unittest discover -s tests -v
```

Sin PowerShell se omiten explícitamente las pruebas sintéticas PINE; eso no
borra la evidencia real local ya conservada. El servidor TCP de los tests no es
un emulador, y PINE verificado no significa puente de gameplay implementado.
