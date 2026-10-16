# Ruta de implementación

## Objetivo vigente y fases verificables

El usuario precisa que Dante debe conservar movimientos, animaciones, combos y
mecánicas originales de DMC3. La ruta anterior de conversión del aspecto queda
**pausada**, con sus archivos intactos. Ahora investigamos intercambio de estado
entre los motores; después decidiremos si composición de imagen o transferencia
de geometría es viable. Todavía no hay integración visual ni de combate.

| Fase | Prueba que la cierra | Estado |
|---|---|---|
| 1. Comunicación | PINE identifica SCUS-97481/2F123FD8 y lee código conocido; proceso DMC3 identificado en Windows | Cliente y pruebas sintéticas; ejecución real pendiente |
| 2. Estado auténtico DMC3 | Una acción de Dante reconocida por estado/motion, sin confundirla con pulsar un botón | Investigación de DDMK; sin perfil validado |
| 3. Primer evento | Acción real → reacción pequeña observable en GOW2, con variable/rutina conocida y mecanismo de parada | Sin implementar; no escribir direcciones desconocidas |
| 4. Espacio y cámara | Ejes, escala, proyección y colisiones medidos; latencia y presupuesto comprobados | Sin mediciones |
| 5. Prueba visual | Dante animado, oclusión correcta y coincidencia espacial en un escenario pequeño | Viabilidad pendiente |
| 6. Mecánicas | Daño, combos, cancelaciones, enemigos, carga y cinemáticas coherentes | Objetivo final, sin prueba todavía |

Una reacción de prueba o una animación visible no cierra las fases posteriores.
Si una fase no es viable, se explicará el componente que falta antes de cambiar
el enfoque. No se sustituirá el objetivo por un skin para presentar un éxito.

## Puente PINE y estado actual

Antes de esta revisión solo existían scripts de extracción, inspectores de
archivos e importación Blender. No había comunicación con PCSX2 ni DMC3.
PINE es un canal nuevo y útil, no una sustitución de otro puente funcional.
Se verificó el protocolo contra PCSX2 v2.8.2, commit
fd9d310ccbb6b8b62c976da8886a3c8fd3a10ff3.

`tools/Probe-Pine.ps1` detecta candidatos PCSX2 y DMC3, consulta versión/estado y
datos del disco por TCP local y lee una instrucción obtenida de la ISO. Guarda
JSON y JSONL en carpetas nuevas bajo D:\logs. No modifica memoria, no engancha
teclas y no conecta todavía eventos de ambos juegos. Véanse [la prueba](pine.md)
y [el contrato de propiedad, transporte y ciclo de vida](CONTRACT.md).

PINE puede transportar lecturas de RAM y, en otros clientes, escrituras. No
descubre qué significa una dirección ni expone actores, animaciones, ataques,
mando, matrices o buffers GPU como API de alto nivel. Identificar posiciones y
eventos GOW2 requiere investigación específica de SCUS-97481 / CRC 2F123FD8.
El diagnóstico actual no contiene ni habilita operaciones de escritura.

## Lectura auténtica de DMC3 y DDMK

Se inspeccionó [serpentiem/ddmk](https://github.com/serpentiem/ddmk/tree/0319ae7132a6a822fd4dede2fb7cad484900169f),
commit 0319ae7132a6a822fd4dede2fb7cad484900169f. Su loader selecciona `Mary.dll`
para `dmc3.exe`; eso no verifica el hash o compatibilidad de una instalación.
Su README advierte que determinadas actualizaciones de HD Collection requieren
otra build. No se ha instalado DDMK, copiado DLL ni cambiado la edición de Steam.

Las estructuras de `Mary/Vars.ixx` son una referencia útil: personaje y posición,
`motionData` con grupo/índice, `motionTimer` y `state`. Las direcciones y layouts
son específicos de build. **No se aplican sus punteros a la instalación del usuario
sin validar.** Primero recogeremos SHA-256, cabecera PE, versión, ruta real y
módulos cargados. Después se estudiarán firmas/punteros con lecturas acotadas y
se revalidará la identidad del actor durante transiciones.

El detector posterior deberá distinguir Dante de otros personajes, partida de
menú/carga, inicio de acción de repetición del mismo estado, y ataque de otras
animaciones. Grupo/índice y temporizador deben correlacionarse con acciones
observadas; una tecla o cualquier cambio de pose no prueba un ataque. Los
hitboxes, ventanas de cancelación y confirmación de impacto son problemas
adicionales. No hay perfil de lectura activo ni ataques auténticos detectados.

`Mary/Memory.ixx` solicita una asignación de **1 GiB** en `Memory_Init`. No es una
medida del working set real, pero desaconseja cargar el mod completo sin medir
en un equipo con 8 GB. Se prioriza un observador externo pequeño, de solo
lectura, si puede validarse; un plugin de telemetría sería una alternativa
posterior que requeriría intervención en el proceso. DDMK sirve ahora como
fuente de investigación, no como requisito de instalación.

## Referencia aportada: RE4 × Minecraft

Se inspeccionó [Dezva/Resident-evil-4-en-Minecraft](https://github.com/Dezva/Resident-evil-4-en-Minecraft/tree/e20d988dec258c4ceb3dcd081429003378db02cd),
commit e20d988dec258c4ceb3dcd081429003378db02cd, versión descrita 0.4.45:
README, contrato, validación, lector RE4 y documentación del módulo nativo.
Hay lector externo con firmas PE32/RE4 1.1.0, cliente Fabric, IPC versionado y
hooks de input/cámara/render D3D9, con buffers y geometría local acotados. El
repositorio registra confirmaciones del usuario y pruebas sintéticas por
separado; su combate Minecraft contra ganados sigue pendiente. No se ha
ejecutado ese proyecto ni verificado su gameplay desde esta nube.

Reutilizamos el diseño: observación primero, versión y ruta verificadas,
generaciones/estados caducados, canales acotados y criterios de éxito separados.
No copiamos sus direcciones, DLL, parser PE32 o hooks gráficos: RE4 es nativo,
PCSX2 ejecuta un motor PS2 y DMC3 usa otra build/API. Minecraft tiene interfaces
Fabric que no se han encontrado equivalentes en estos dos juegos. El
antecedente ayuda a organizar el trabajo, sin demostrar viabilidad de esta fusión.

## Viabilidad visual y rendimiento

**PINE por sí solo no permite conservar a Dante renderizado y simulado en el
mundo GOW2.** No se encontró un adaptador listo para esta combinación. La
viabilidad completa en GTX 1050, i5-4460 y 8 GB sigue sin establecerse.

Dos rutas a investigar, después de las fases de estado:

- **Composición de imagen:** capturar a Dante con color y profundidad desde
  DMC3 y combinarlo con el frame de PCSX2. Exige aislar al personaje, sincronizar
  cámara/FOV/proyección, convertir profundidad y resolver oclusión. Una captura
  2D superpuesta no da profundidad ni colisión; PINE no proporciona esos buffers.
- **Geometría en el renderizador de destino:** transferir mallas, materiales,
  poses/esqueleto de DMC3 y dibujarlos con el pase y profundidad apropiados de
  PCSX2. Requiere hooks o cambios específicos al renderizador y al runtime DMC3,
  además de gestionar dispositivos, recursos, pausas y reinicios. Importar un
  GLB en Blender no implementa este canal. El motor PS2 no consume por sí solo
  esqueletos o animaciones de HD Collection.

Ambas rutas necesitan ocultar/coordinar representaciones, mapear posiciones y
transferir colisión del mundo hacia la simulación de Dante; también hitboxes y
daño de vuelta. DMC3 simula su propio escenario: conservar su movimiento real
no basta para que ese movimiento respete automáticamente el escenario GOW2.
No se ha verificado todavía una interfaz para suministrarle esa geometría o
controlar su cámara. Es un límite técnico pendiente de resolver, no una tarea
que PINE resuelva al sincronizar dos números.

Presupuesto inicial **propuesto, no medido**:

1. Comprobar GOW2 solo y DMC3 solo durante unos 60 s en una partida; anotar FPS,
   velocidad de emulación, RAM disponible/comprometida, working set, memoria
   privada y uso GPU/VRAM. La variante de GTX 1050 y su VRAM aún no se conocen.
2. Ejecutarlos juntos solo tras conocer ese margen. Mantener Blender cerrado y
   no añadir Unity, contenedores o runtimes grandes. El i5-4460 tiene cuatro
   núcleos; ambos juegos competirán por CPU y la GPU compartida. Bajar resolución
   puede reducir carga GPU, pero no elimina el coste de emular PS2.
3. Telemetría posterior: empezar por 20–30 Hz, bloques pequeños de direcciones
   verificadas, un worker y snapshots recientes; medir latencia. Evitar escanear
   toda la RAM EE cada frame o consultar/cargar texturas repetidamente.
4. Si hay margen y accesos gráficos válidos, una prueba visual pequeña podría
   empezar a 640×360 y 30 FPS, con máximo tres buffers y descartando frames
   atrasados. No es una promesa de rendimiento ni debe ralentizar la simulación
   nativa de DMC3 para aparentar sincronía.

Solo color RGBA8 + profundidad R32F a 640×360 son 1 843 200 bytes/frame y
55,3 MB/s a 30 FPS por copia completa (5,53 MB para tres buffers). A 1280×720
son 221,2 MB/s por copia. No incluyen assets, backbuffers de los juegos,
conversión, latencia de lectura GPU ni copias adicionales CPU/GPU. Compartir
texturas en GPU podría evitar algunas copias, pero depende de APIs y formatos
compatibles que aún no se han inspeccionado en ejecución.

No se puede dar una cifra fiable de FPS ahora. Si la ejecución simultánea ya
satura CPU/RAM o faltan cámara/profundidad/colisiones accesibles, se documentará
ese resultado antes de proponer otra arquitectura. Esta fase solo añade un
diagnóstico temporal de poco tráfico; no mantiene dos motores extra en segundo plano.

## Universal Modder

Se aplica el flujo de `mod-any-game` y `mashup-mods` de
[rehan-remade/universal-modder](https://github.com/rehan-remade/universal-modder),
revisión examinada **23902ef42e8ea9b077bfbbf6911eb8ea0348e55a**. Se ejecutó su
CLI `um kb search` para buscar antecedentes de DMC3, God of War y PCSX2. Las
búsquedas no localizaron una nota específica que resolviera esta combinación.
Se leyeron las guías de rutas y niveles de evidencia. No se instaló el plugin
en la interfaz de Codex; se utilizaron el código, las habilidades y la CLI del
checkout de investigación.

`tools/setup_cloud_tools.sh` prepara las revisiones fijadas de Universal Modder
y del importador en `/workspace/.dmc-tools`, como dependencias de herramientas.
Se ejecutó desde cero y se repitió correctamente sin sobrescribir cambios.
La imagen de nube utilizada ya proporciona Python, Pillow, numpy, PyYAML y
Blender; el script comprueba esos prerrequisitos y preserva archivos existentes.
Los clones temporales de investigación no son necesarios para ejecutar las
herramientas preparadas allí.

La ruta inicial era conversión de recursos; queda conservada como antecedente.
La ruta vigente se describe arriba y el contrato del puente sigue la guía
`bridge-contracts-ownership-units-and-lifecycle.md` del toolkit. Se volvió a
ejecutar `um --version` y `um win --help`: el CLI funciona, pero su adaptador
Windows necesita Windows/WSL y no da acceso remoto a los procesos del usuario.
No se instaló ese adaptador ni un loader. Universal Modder aporta metodología
y herramientas generales; no resuelve automáticamente los motores ni PINE.

## Importación del origen comprobada

Se utiliza el importador externo
[deshayu/DMC3HDC-Import-Tools](https://github.com/deshayu/DMC3HDC-Import-Tools),
commit **248dec2a0b7984fbd0c74f85c7de94a09dd81e06**, licencia MIT, derivado de las
herramientas originales de igrbn. No se copia su código dentro de este proyecto.
El wrapper propio asigna las tres texturas por índice y prepara la inspección.

Verificado en **Blender 4.3.2, Linux**, con la muestra real del usuario:

- 26 mallas importadas, 6144 vértices y 4304 triángulos de origen.
- Dos armatures con 24 y 33 huesos; no hay vértices sin peso positivo en las mallas
  importadas. No se ha probado su animación ni su adaptación al esqueleto de Kratos.
- Tres texturas DDS asignadas a partir de los índices del modelo.
- Exportación a GLB sin Draco, además de un archivo Blend y vista estática.

El abrigo tiene un origen y esqueleto separados. Para la vista estática se alinea
su `bone_0` con `bone_1` del cuerpo. Es una hipótesis de colocación para inspección,
no una reconstrucción comprobada de la física de tela o del acoplamiento del juego.
Los MOD extraídos permanecen intactos.

El primer render falló por falta de OpenImageDenoise en este Blender. Se desactivó
el denoiser opcional y el render CPU terminó correctamente. El exportador avisa
de que Draco no está disponible; la salida se genera sin compresión Draco.

Para reproducir en la nube con el importador obtenido por separado y fijado a esa
revisión, desde la raíz del proyecto:

```sh
python3 tools/inspect_pac.py /ruta/pl000.pac --manifest /ruta/informe.json --output /workspace/dmc3-private/nueva-extraccion
blender --background --factory-startup --python-exit-code 1 --python tools/import_dante_blender.py -- --addon-root /workspace/.dmc-tools/dmc3-importer --resources /workspace/dmc3-private/nueva-extraccion --output /workspace/dmc3-private/nueva-importacion --render
```

Las carpetas de salida deben ser nuevas. En Windows, utiliza subcarpetas bajo
`D:\logs` para esos informes y resultados locales. Esta importación es material
de trabajo, **no un archivo instalable en God of War II**.

## Investigación del destino PS2

Se examinó [mogaika/god_of_war_browser](https://github.com/mogaika/god_of_war_browser),
commit **1bfc55c0172e67c48c8e941c495333f583c721a0**. Su documentación y código
contemplan PS2, God of War II, índices TOC, paquetes PAK y recursos WAD. Sus
rutinas de lectura no prueban por sí solas que se pueda importar un modelo GLB
arbitrario como malla de God of War II. Esa reinserción todavía debe investigarse
y probarse con los archivos concretos de SCUS-97481 / CRC 2F123FD8.

No se ejecutó esta herramienta sobre la ISO del usuario. Puede abrir imágenes
para escritura y su documentación advierte de la reorganización de paquetes;
cualquier prueba de modificación futura deberá hacerse sobre una copia de trabajo.

El índice y los tres paquetes seleccionados ya se recibieron y verificaron en
`/workspace/dmc3-private/gow-samples`; no se vuelven a pedir. Las muestras quedan
preservadas y se pausa su conversión. Se conservan a continuación los pasos del
índice como referencia histórica; no hace falta repetirlos.

Obtención del índice de archivos mediante
[`tools/Export-GowIndex.ps1`](../tools/Export-GowIndex.ps1):

1. Abre ese script, copia todo su contenido y pégalo en PowerShell.
2. Lee la ruta ISO ya indicada y verifica `SCUS_974.81` en BOOT2.
3. Crea una carpeta nueva bajo **`D:\logs\gow2-indice-...`**.
4. Adjunta `GODOFWAR.TOC` (o `GODOFWAR.BIN` si esa variante existe),
   `raiz-iso.csv` e `informe-gow.json`. Si falla, adjunta `error.txt` y el CSV si
   llegó a crearse. No adjuntes la ISO completa ni los PAK.

El lector abre la imagen para lectura y copia únicamente metadatos pequeños.
Inspecciona la raíz ISO9660 de la primera capa, no UDF ni la segunda capa de un
DVD9; no monta discos y no intenta modificar paquetes. Se probaron seis ejecuciones
con ISOs sintéticas en PowerShell 7.4.21/Linux, incluidos errores y repetición sin
sobrescritura. Queda comprobarlo en Windows con la ISO real.

El índice permitió seleccionar R_HERO00.WAD, R_HERO01.WAD y R_PERMA.WAD para
estudiar los recursos del personaje y posibles dependencias. No se sabe aún qué
recurso concreto habrá que reemplazar ni se puede
prometer una conversión compatible hasta validar el formato de destino.
