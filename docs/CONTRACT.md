# Contrato del puente · versión 1

Ruta actual: diagnóstico entre procesos, **solo lectura**. La conversión de
recursos anterior se conserva como investigación visual; no define el objetivo
final. Este contrato sigue la guía de puentes de Universal Modder, revisión
23902ef42e8ea9b077bfbbf6911eb8ea0348e55a.

Host previsto: Windows, PCSX2 2.8.2 (usuario: 2.8.2.0), God of War II NTSC-U,
SCUS-97481 / CRC 2F123FD8. Invitado: DMC3 HD Collection de Steam, `dmc3.exe`;
build y compatibilidad DDMK todavía sin verificar. No se carga ningún mod nuevo.

## Propiedad y control

| Sistema | Fase actual | Propuesta posterior, pendiente de validar |
|---|---|---|
| Movimiento, animación y combos de Dante | DMC3, sin intervención | DMC3 conserva su simulación auténtica |
| Posición compartida y física | Cada juego conserva la suya | Requiere resolver colisiones y autoridad antes de sincronizar |
| Cámara | Cada juego conserva la suya | Cámara del mundo GOW2 y proyección compatible para Dante |
| Geometría del mundo, NPC y eventos | GOW2, sin intervención | GOW2 sigue siendo el mundo de destino |
| Colisión mundo → Dante / Dante → mundo | Sin canal | Adaptador por investigar en ambas direcciones |
| Daño, salud e inventario | Independientes, originales | Contrato de daño separado de la conversión de salud |
| Guardado y carga | Cada juego | No se mezclan partidas en esta fase |
| Menús, pausa y cinemáticas | Cada juego | Suspender puente; devolver control nativo al salir del modo compartido |

No se transfiere control ahora; no hay dos programas escribiendo una misma
variable. No existe aún un procedimiento verificado para devolver control tras
una futura integración. Ese procedimiento será requisito previo a activarla.

## Unidades y ejes

No se conocen escalas, ejes, handedness, cámara ni unidades de daño verificadas
de ambos juegos. `host_to_guest` queda **sin definir**, no se presupone identidad
XYZ ni metros. Toda propuesta futura debe aportar mediciones o fuentes.

La única dirección leída en esta fase procede del punto de entrada ELF de la
ISO: una instrucción de código, no una posición, salud ni ataque. Se exige
segmento ejecutable file-backed, dirección alineada dentro de los 32 MiB de RAM
EE y juego/CRC coincidentes antes de enviar Read32. No se interpreta como estado
de combate. Se comprueba otra vez identidad y estado después de leer.

## Canales y formato

| Canal | Dirección | Frecuencia / límite | Si falla o llega tarde |
|---|---|---|---|
| PINE TCP Windows, 127.0.0.1:28011 | Consulta → PCSX2 → respuesta | Una conexión, consultas finitas; respuesta ≤16 KiB | Timeout, cerrar y registrar; no reintentar escrituras |
| Inspección de procesos y PE | Windows → diagnóstico | Una captura; hashes por streaming | Ausente y acceso desconocido se distinguen |
| `events.jsonl` | Diagnóstico → disco | Eventos finitos, esquema v1 | Error visible; no se usa como cola de órdenes |
| `report.json` | Diagnóstico → disco | Un informe por sesión | Directorio único; no sobrescribir anteriores |

PINE: u32 little endian con longitud total; opcode y argumentos; respuesta con
u32 longitud, resultado 0/255 y payload. Cadenas UTF-8 con u32 longitud incluido
NUL. Solo se permiten opcodes 2, 8, 11, 12, 13, 14, 15. No hay opcodes de
escritura, savestates ni entrada de mando en este cliente.

Registros: `protocol="dmc3-gow2-diagnostic"`, `schema_version=1`, UUID por sesión,
secuencia creciente y milisegundos de reloj monotónico, más fecha UTC. Los bytes
PINE son little endian; JSON es UTF-8. Una nueva ejecución crea otra generación.
No hay protocolo compartido de gameplay todavía. Para el futuro: snapshots
reemplazables, colas de eventos acotadas y descarte de estados atrasados; nunca
reproducir ataques pendientes después de reinicio/carga. Tasas y TTL se medirán.

En Windows, si MainModule no devuelve una ruta, se consulta la imagen con
QueryFullProcessImageNameW y un handle PROCESS_QUERY_LIMITED_INFORMATION
(0x1000), cerrado siempre al terminar. No solicita VM_READ/VM_WRITE, acceso
completo ni privilegio de depuración. `path_source` identifica el método;
`main_module_error` conserva el fallo anterior. Enumeración vacía/no accesible
significa `modules_status=unknown`, aunque la ruta permita confirmar dmc3.exe.

## Ciclo de vida y prueba de aceptación

Arrancar PCSX2 con PINE activado; cargar GOW2 y entrar en partida; lanzar el
diagnóstico. DMC3 puede estar cerrado y se registra expresamente. Con PCSX2 sin
VM se conserva versión/estado y se omite memoria. Cambio de identidad durante la
lectura invalida la prueba. Una pausa permite verificar código estático, pero
no cuenta como simulación activa. Carga, muerte y pausa de DMC3 no se detectan
todavía: sus eventos no pueden transmitirse. Desconexión/cierre produce error y
cierra el socket; no se modifican los juegos ni hay nada que restaurar.

Primer éxito real: respuesta PINE válida, identidad correcta e instrucción de
RAM coincidente con ELF. Detectar un proceso o pasar el servidor simulado no lo
demuestra. Segundo éxito, posterior: reconocer una acción auténtica de Dante en
una build identificada y observar una reacción segura y documentada en GOW2.
Eso tampoco probará composición visual, profundidad ni colisiones compartidas.
