# Continuidad para Codex local en Windows

Estado de referencia: 16 de octubre de 2026. Esta guía permite continuar desde
el repositorio sin depender del historial del chat ni del filesystem de nube.
Actualizar al obtener evidencia nueva; los resultados siguientes son históricos,
no pruebas ejecutadas automáticamente al abrir este archivo.

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

La fase PINE actual puede continuar con el repositorio y las instalaciones de
juegos del usuario: no requiere los recursos Blender de nube. Su siguiente
comprobación real está en [la primera sesión](#la-primera-sesión-cerrar-la-prueba-pine).

## Objetivo que debe conservarse

Integrar **DMC3 HD Collection de Steam** con **God of War II de PS2 ejecutado por
PCSX2** para mantener los movimientos, animaciones, ataques, combos y mecánicas
auténticos de Dante dentro del mundo GOW2. El usuario precisó que un reemplazo
de aspecto no cumple el objetivo. La ruta inicial de conversión visual quedó
pausada; sus recursos y herramientas siguen conservados.

Prioridad actual: comunicación entre procesos mediante **PINE en solo lectura**;
después, detectar estados reales de DMC3. No avanzar a composición visual sin
analizar acceso a cámara, profundidad, poses, colisiones y presupuesto del equipo.
Si un componente no resulta viable, explicar la limitación antes de cambiar de
enfoque. No hay una fusión completa ya implementada que baste con activar.

## Equipo y datos ya proporcionados

| Dato | Valor / evidencia |
|---|---|
| Sistema del usuario | Windows; edición/build de Windows aún no recogidas |
| CPU / RAM | Intel i5-4460 / 8 GB |
| GPU | NVIDIA GTX 1050; VRAM y driver exactos por verificar |
| PCSX2 | Usuario indica 2.8.2.0; protocolo investigado en fuentes v2.8.2 |
| Destino | God of War II NTSC-U, SCUS-97481, CRC 2F123FD8, según captura |
| ISO | `D:\Games PS2\God of War II [NTSC]\God of War II.iso` |
| DMC HD | `D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection` |
| Ejecutable esperado | `dmc3.exe`; hay que confirmar el proceso real y su huella |
| PINE Windows | TCP local `127.0.0.1:28011`; desactivado de fábrica, activación real por verificar |
| Logs / informes / muestras nuevos | `D:\logs`, subcarpetas únicas |
| BIOS y controles | Usuario tiene BIOS preparada; mando válido, teclado opcional |

GOW2 abre según el usuario. Control completo, guardado/carga, rendimiento y
conexión PINE no se comprobaron desde la nube. La primera descarga europea era
**God of War I**, SCES-53133 / FB0E6D72: no es el destino ni un perfil compatible.
No volver a pedir los datos ya confirmados; verificar localmente si han cambiado.

## Qué existe y qué falta

| Componente | Estado comprobado | Límite |
|---|---|---|
| `tools/Probe-Pine.ps1` | Cliente real PowerShell, probado contra TCP sintético | Pendiente ejecutarlo con PCSX2/Windows reales |
| Identidad y lectura PINE | Versión/estado/título/serial/CRC; Read32 de instrucción derivada del ELF | No posiciones, salud, ataques ni cámara |
| Diagnóstico DMC3 | Inspección de proceso, ruta, PE/SHA, módulos Mary/dinput8 y memoria observada | No perfil de telemetría de combate; DDMK sin validar |
| `inspect_ps2.py` | ISO9660/ELF de solo lectura; siete tests | No CHD/CSO ni CRC PNACH recalculado |
| `inspect_pac.py` | PAC/DDS, ocho tests y extracción real de muestra | No conversión PS2 |
| `inspect_gow_toc.py` | TOC, siete tests e índice real recibido | Segunda capa DVD9 no resuelta sin metadatos adicionales |
| Exportadores PowerShell | Scripts de muestras/índice conservados; pruebas sintéticas previas | No hace falta repetir exportaciones recibidas |
| Blender | Importación real cuerpo/abrigo, Blend/GLB y vista estática | Sin animación runtime, física de abrigo o integración GOW2 |
| Gameplay entre motores | Sin implementar | No detección auténtica de ataques ni reacción GOW2 |
| Composición visual | Investigación y requisitos documentados | Sin hooks, renderer compartido o prueba de rendimiento |

Última validación: **31 tests correctos**, sin omitidos, combinando 22 tests de
inspectores y nueve de PINE con 17 escenarios. Ejecutados en Linux/Python 3.12 y
PowerShell 7.4.21. No equivalen a validar Windows PowerShell 5.1 o una partida.

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

## La primera sesión: cerrar la prueba PINE

1. Leer el estado del checkout y los informes `pine-probe-*` existentes bajo
   D:\logs, si los hay. Elegir informes por fecha/contenido, no asumir que el
   último directorio contiene una ejecución terminada. No volver a escanear
   toda la instalación ni pedir inventarios que ya se analizaron.
2. Verificar rutas de ISO y `dmc3.exe`. Detectar PCSX2 y si hay partida cargada.
   En la GUI PCSX2: Ajustes → Mostrar ajustes avanzados → Avanzados → PINE,
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

Windows PowerShell 5.1 no se probó en la nube. Si una prueba falla en Windows,
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
> War II, conservando las mecánicas y animaciones reales de Dante. Primero revisa
> los informes locales existentes y ejecuta el diagnóstico PINE de solo lectura
> en mi Windows cuando PCSX2 tenga GOW2 cargado. Confirma SCUS-97481/2F123FD8,
> compara la instrucción de prueba con mi ISO y verifica el proceso real y la
> huella de dmc3.exe. Guarda los nuevos informes en D:\logs. No escribas memoria
> desconocida ni instales DDMK o hooks gráficos. Después explica qué falta para
> detectar una acción auténtica de Dante. Conserva Blender/modelos y publica los
> scripts y la documentación que me entregues en el GitHub del proyecto.
> Guarda también los demás cambios de código, tests, documentación y pasos de
> reproducción necesarios para continuar. Haz commit y push y verifica que
> quedaron publicados; no dependas de acceso a Codex Cloud para recuperar avances.
