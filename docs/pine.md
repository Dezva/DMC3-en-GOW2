# Prueba PINE de solo lectura

## Qué existe y qué prueba

`tools/Probe-Pine.ps1` es un diagnóstico finito; prepara el canal PCSX2 y el
registro de identidad de DMC3. Antes solo había herramientas de archivos y
Blender. No había otro IPC funcional que conservar o sustituir. Esta fase no
detecta ataques ni provoca reacciones en GOW2.

Lee el nombre del proceso real, su ruta, PID, fecha de arranque y consumo de
memoria observado. El lanzador de HD Collection no cuenta como `dmc3.exe`.
Si MainModule no devuelve ruta, usa QueryFullProcessImageNameW con únicamente
PROCESS_QUERY_LIMITED_INFORMATION; registra `path_source` y conserva el error
del primer método. Una enumeración de módulos vacía se registra como desconocida,
sin afirmar que no hay DLL cargadas. No solicita privilegio de depuración.
Registra SHA-256, tamaño, versión y cabecera PE del ejecutable en disco; también
examina `Mary.dll`/`dinput8.dll` si existen y registra esos módulos si están
cargados. Su presencia no demuestra compatibilidad DDMK. No lee aún estados de
combate de DMC3 ni abre un handle de escritura sobre ningún proceso.

PINE se contrasta con las fuentes oficiales de PCSX2 **v2.8.2**, commit
`fd9d310ccbb6b8b62c976da8886a3c8fd3a10ff3`. El usuario indica 2.8.2.0; el cliente
admite la familia 2.8.2 en la cadena que devuelve PINE. Si difiere, identifica
el juego pero omite RAM hasta revisar esa versión.

**Resultado local 2026-10-16:** prueba real correcta con Windows PowerShell
5.1 x64, PCSX2 v2.8.2, SCUS-97481/2F123FD8, VM running, instrucción
0x70000C28 en 0x00100008 igual a la ISO, `phase1_verified=true`, sin errores.
También se confirmó dmc3.exe por PID/ruta real y PE/SHA de disco; módulos
desconocidos. Logs, hashes y entorno en
[la continuidad local](CONTINUIDAD-LOCAL.md#primera-prueba-local--2026-10-16).

## Ejecutar en tu PC

Descarga [el ZIP del repositorio](https://github.com/Dezva/DMC3-en-GOW2/archive/refs/heads/main.zip)
y extráelo en Windows. También puedes descargar solo
[Probe-Pine.ps1](https://github.com/Dezva/DMC3-en-GOW2/blob/main/tools/Probe-Pine.ps1)
con **Download raw file** en GitHub. No necesitas acceder a rutas del entorno
en la nube. Si descargaste el archivo suelto, abre PowerShell en su carpeta y
ejecútalo con `.\Probe-Pine.ps1`.

1. En la ventana principal de PCSX2, abre **Herramientas → Mostrar ajustes
   avanzados** (Tools → Show Advanced Settings) si están ocultos y acepta el
   aviso. Después abre **Ajustes → Emulación** y selecciona **Avanzados** en la
   columna izquierda. Desplázate hasta el final del panel: **PINE Settings /
   Ajustes de PINE** está debajo de los ajustes de savestates. Activa **Enable /
   Habilitar** y deja **Slot = 28011**. Cierra la ventana de ajustes. Los textos
   pueden variar con la traducción. El menú que muestra las opciones avanzadas
   es **Herramientas**, no Ajustes; comprobado en MainWindow.ui de v2.8.2.
   La configuración oficial es `[EmuCore] EnablePINE` y `PINESlot`; el script
   no modifica el INI. No necesitas abrir puertos del router.
2. Arranca **God of War II**, entra en una partida y deja el emulador abierto.
   La lectura de código también puede comprobarse en pausa. Cierra otros
   clientes PINE: esta implementación del servidor atiende una conexión a la vez.
3. Con los archivos del proyecto descargados, abre **Windows PowerShell de
   64 bits** en la carpeta del proyecto y ejecuta:

   ```powershell
   .\tools\Probe-Pine.ps1
   ```

   Si la política existente impide ejecutar archivos, puedes abrir el script,
   copiar **todo** su contenido y pegarlo en esa consola, igual que los
   exportadores anteriores. No cambies la política del sistema ni ejecutes como
   administrador para esta prueba. Si falla, la salida puede cerrar la consola
   al devolver código 1; los informes se guardan antes.
4. Busca la carpeta nueva **`D:\logs\pine-probe-...`**. Codex local debe leer
   **`report.json` y `events.jsonl`** directamente, también si indica error. Solo
   hace falta adjuntarlos si el agente no tiene acceso a tu disco. No hacen
   falta ISO, BIOS o EXE.
5. Primero puedes dejar DMC3 cerrado. Después abre **DMC3**, no solamente el
   menú de HD Collection, entra en una partida y repite el mismo script. Las
   ejecuciones crean carpetas distintas. Esta segunda captura confirma el
   proceso y permite comparar su consumo; no mide todavía rendimiento continuo.

Las rutas por defecto son las que ya proporcionaste:

```text
ISO:      D:\Games PS2\God of War II [NTSC]\God of War II.iso
DMC HD:   D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection
Informes: D:\logs
```

Si cambiaste alguna, utiliza `-IsoPath 'ruta'` o `-GameRoot 'carpeta'` al ejecutar
el archivo. Para un Slot personalizado existe `-PinePort`; siempre conecta a
`127.0.0.1`. `-TimeoutMs` controla el plazo de cada respuesta completa, 1500 ms
por defecto. No existe parámetro de dirección arbitraria o de escritura.

## Lectura de memoria con procedencia

Solo tras confirmar **SCUS-97481 / 2F123FD8** y PCSX2 2.8.2, abre la ISO para
lectura, resuelve `SYSTEM.CNF` y el ELF `SCUS_974.81`. Localiza su punto de entrada
en un segmento PT_LOAD ejecutable con cuatro bytes presentes en el archivo.
Comprueba alineación y RAM EE de 32 MiB; admite direcciones físicas y alias
KSEG0/KSEG1, nunca MMIO. Lee **una instrucción de 32 bits** por PINE y compara
con esos bytes. No adivina la dirección de salud, posición o ataques.

Vuelve a consultar identidad antes y después. Esto detecta cambios observados,
pero no es una transacción ni demuestra que no hubiera una recarga del mismo
juego entre consultas. No sirve como snapshot de combate sincronizado por frame.

Si la ISO falta, está comprimida o tiene un ELF no soportado, conserva los
metadatos PINE y omite RAM. Si la instrucción difiere, registra ambos valores y
falla la comprobación: puede requerir estudiar carga, parches o build; nunca
intenta corregirla escribiendo. La comparación de cuatro bytes prueba esta
lectura y no certifica la integridad completa del juego.

## Interpretar el informe

| Campo | Significado |
|---|---|
| `pcsx2_processes` | Procesos candidatos observados por Windows; ruta puede ser desconocida |
| `pine.tcp_connected` | Se abrió TCP; por sí solo no demuestra PINE |
| `pine.responds` | Versión PCSX2 y estado PINE con formato válido |
| `pine.status_name` | `running`, `paused` o `shutdown` |
| `pine.identity` | Título, serial, CRC y versión del disco, no de DMC3 |
| `memory_test.status = verified` | Instrucción coincide con ISO y consultas de identidad válidas |
| `phase1_verified` | Se verificó PINE, identidad y esa lectura; DMC3 puede estar cerrado |
| `dmc3.running = confirmed` | Proceso observado con ejecutable `dmc3.exe`, ruta registrada |
| `unknown_candidate_present` | Hay candidato DMC3, pero no se pudo verificar el ejecutable |
| `dmc3.ddmk_compatibility` | Siempre `unverified` en esta fase |
| `authentic_attacks_detected` / `game_to_game_communication` | Siempre `false` en esta fase |

La lista de procesos y la identidad PINE son observaciones independientes;
todavía no se verifica el PID propietario del listener. Con varios emuladores,
cierra los que no estés probando. Working set y private bytes no son lo mismo,
y sumar working sets puede contar memoria compartida varias veces.

Si no conecta: comprueba PINE activado, Slot, PCSX2 abierto y ausencia de otro
cliente que retenga la conexión. Si dice `shutdown`, carga una partida y repite.
Si hay acceso desconocido a un proceso, no significa que esté cerrado: conserva
el error. Los hashes de disco no garantizan que no se haya modificado memoria
tras cargar la imagen; esto se revalidará al preparar la telemetría real.

## Protocolo verificado y pruebas de desarrollo

Solo Windows usa TCP loopback en PCSX2. En Linux PCSX2 emplea un socket Unix
`$XDG_RUNTIME_DIR/pcsx2.sock` o `/tmp/pcsx2.sock`; este cliente está destinado al
Windows del usuario. Los tests Linux utilizan un **servidor TCP sintético**.

Tramas y opcodes figuran en [CONTRACT.md](CONTRACT.md). El cliente limita cada
respuesta a 16 KiB, lee cabeceras/cuerpos fragmentados, exige longitud/NUL de
cadenas, rechaza IPC_FAIL y tiene plazos. No implementa Write8/16/32/64,
SaveState, LoadState o comandos de mando.

Para probar sin juegos desde la nube Linux x86_64:

```sh
bash tools/setup_pine_test_runtime.sh
PWSH_BIN=/workspace/.dmc-tools/powershell-7.4.21/pwsh python3 -m unittest discover -s tests -v
```

El instalador descarga PowerShell portátil 7.4.21 desde Microsoft/GitHub y
verifica SHA-256 del archivo y del ejecutable. No es requisito en Windows.
Las pruebas invocan el cliente PowerShell real con ISO, PE y servidor de prueba.
Cubren lectura, pausa, edición/versión incorrectas, VM cerrada, cambio de juego,
instrucción distinta, ISO ausente/segmento no ejecutable/MMIO, IPC_FAIL,
fragmentación, truncado, longitud excesiva, cadena inválida, timeout y conexión
rechazada. Comprueban que no cambia ningún archivo fuente y que no se envía
ningún opcode de modificación. Son tests históricos Linux. La prueba real local
Windows PowerShell 5.1 / PCSX2 pasó el 2026-10-16; eso no supone que esta suite
completa se haya repetido en Windows ni valida gameplay entre juegos.

Fuentes oficiales:

- [PINE.cpp de PCSX2 v2.8.2](https://github.com/PCSX2/pcsx2/blob/v2.8.2/pcsx2/PINE.cpp).
- [Ajustes PINE](https://github.com/PCSX2/pcsx2/blob/v2.8.2/pcsx2-qt/Settings/AdvancedSettingsWidget.cpp).
- [Menú avanzado](https://github.com/PCSX2/pcsx2/blob/v2.8.2/pcsx2-qt/MainWindow.ui).
