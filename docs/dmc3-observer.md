# Observador externo DMC3 · solo lectura

Estado 2026-10-16: **acceso real y campos candidatos observados**, con validación
de acciones/menús/transiciones todavía parcial. No hay detector de ataques,
puente de gameplay, reacción GOW2 ni composición visual. `phase2_verified` y
`authentic_attacks_detected` permanecen false. Un código de salida 0 solo indica
acceso correcto o disponibilidad de candidatos, según el modo.

La petición posterior incorporó [análisis temporal offline](dmc3-analisis-offline.md),
sin modificar este lector/perfil. La [investigación fijada](dmc3-campos-investigacion.md)
identifica motionData[0/1] como canales inferior/superior según DDMK; el timer
sigue sin unidades/sentinel validados. Las [fichas y resultados](dmc3-validacion-controlada.md)
conservan la autorización y confirmación exigidas para cada nueva captura.

Actualización de validación controlada: R20 ya se ejecutó con reposo confirmado
por el usuario; ambos motions (grupo 0/índice 3), state=1 y timer=2.0 estables.
Una lectura coherente más el relato permiten asociación contextual, no semántica
universal. Resultado y siguiente ficha E1 en [validación controlada](dmc3-validacion-controlada.md).
E1 ya se ejecutó y el usuario confirmó un espadazo: (3,3)/state65537 por 16
muestras, timer 2.0 constante antes/durante/después. Asociación contextual sin
exclusividad o autenticación independiente; E1-R espera nueva preparación.
No repetir PINE.

## Ejecutar y conservar evidencia

Requiere Windows y Python **x64, 3.10 o posterior**, solo biblioteca estándar.
Debe utilizarse el proyecto completo: observe_dmc3.py importa dmc3_memory.py y
dmc3_profile.py. En esta sesión se utilizó el Python que ya incluye Codex; no se
instaló Python, DDMK ni otro runtime. Desde la raíz, en PowerShell:

```powershell
$observerPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $observerPython .\tools\observe_dmc3.py --access-only
& $observerPython .\tools\observe_dmc3.py --samples 100 --hz 10
```

Cada ejecución crea `D:\logs\dmc3-observe-FECHA-UUID`, con session.json,
events.jsonl y report.json. El modo de muestreo también conserva
candidate-profile.json: metadatos derivados, no bytes del EXE. No sobrescribe
ejecuciones anteriores. Puede fallar con salida 1 y aun así dejar un informe
útil. Un proceso no accesible se conserva como desconocido, no como cerrado.
`--exe` cambia la ruta; una huella distinta no habilita el perfil anterior.

`--access-only` obtiene identidad, base real y cabeceras cargadas sin consultar
raíces de gameplay. El muestreo deriva después el perfil y valida sus guardas
estáticas antes de seguir punteros. Los dos modos revalidan la huella de disco
al terminar. No certifican que toda la memoria del proceso sea original.

Para revisar automáticamente una captura terminada:

```powershell
& $observerPython .\tools\analyze_dmc3_capture.py 'D:\logs\dmc3-observe-FECHA-UUID'
```

Crea candidate-summary.json una sola vez, con hashes, secuencias, sesión,
orden monotónico, contadores, valores rechazados y transiciones. Los hashes
ayudan a detectar cambios respecto a una referencia conservada; no son una
firma digital. Los informes completos y las muestras permanecen fuera de Git.

## Identidad, acceso y presupuesto

Build admitida para candidatos:
`4ae4bb5c83c19a649fc60edc5ca40e7f3ceee6337e4e4275025bfa9caa40c0a0`,
6356432 bytes, PE32+ x64, timestamp 1521798082, SizeOfImage 14336000.
Se calcula SHA-256 del archivo actual; PID, ruta y FILETIME de creación se
descubren nuevamente, sin reutilizar los PID de los documentos históricos.

La identidad usa PROCESS_QUERY_LIMITED_INFORMATION (0x1000). El handle de
memoria pide exactamente **PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
(0x410)**: VirtualQueryEx requiere el primero y ReadProcessMemory el segundo.
No usa acceso completo, privilegio de depuración, elevación automática,
escrituras, inyección, suspensión del juego ni control de ventanas/teclas.
Todos los handles se cierran. GetProcessTimes/GetExitCodeProcess verifican que
se sigue observando el proceso original. EnumProcessModulesEx y
GetModuleInformation proporcionan su base real bajo ASLR; se inspecciona solo
el módulo principal, sin afirmar compatibilidad de los demás módulos.

Se registra por separado la integridad/elevación de ambos tokens mediante
TOKEN_QUERY. En esta sesión, DMC3 elevado (RID 12288) y observador normal
(RID 8192) produjeron **OpenProcess error 5**, sin lectura RAM. El usuario volvió
a abrir directamente el juego sin administrador; ambos quedaron en RID 8192
y el acceso funcionó. El EXE declara asInvoker. No se cambió el manifiesto,
el registro, Steam, permisos ni la configuración del juego desde el agente.
No recomendar elevar el lector como solución automática.

Antes de cada lectura se exige dirección de usuario, tamaño acotado y páginas
MEM_COMMIT legibles, sin PAGE_GUARD/NOACCESS. Un ReadProcessMemory incompleto
rechaza toda la muestra; conserva dirección/tamaño solicitado, bytes recibidos
y error Win32. No se usa el fragmento como si fuera completo.

Presupuesto: 1–20 Hz, máximo 6000 muestras y 300 segundos de muestreo por
ejecución. Preparación opcional de hasta 30 s. El perfil actual lee **200 bytes
de gameplay por intento completo**, en bloques de hasta 32 bytes; una lectura
individual del backend nunca supera 4096 bytes. Ticks atrasados se descartan,
sin ráfagas para ponerse al día. No hay escaneo continuo, volcados de RAM,
tráfico PINE ni proceso permanente. No se han medido FPS/CPU/GPU del observador.

## Procedencia y resolución del perfil candidato

Se investigó DDMK **0319ae7132a6a822fd4dede2fb7cad484900169f**, sin ejecutarlo.
Las expresiones se usan como hipótesis de lectura, no se copian sus hooks.

| Dato | Cadena/RVA respecto a la base real | Procedencia |
|---|---|---|
| Actor principal | `pool = u64(base + 0xC90E28)`; `actor = u64(pool + 3*8)` | [ddmk.js, IntroduceMainActorData](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/ddmk.js#L2389) |
| EventData | `pool = u64(base + 0xC90E10)`; `event = u64(pool + 8*8)` | [ddmk.js, IntroduceEventData](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/ddmk.js#L2786) |
| Sesión | Estructura inline en `base + 0xC8F250`; misión u32 en +0, personaje u8 en +0x14 | [ddmk.js](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/ddmk.js#L2689), [Vars.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L2220) |
| Contexto de evento | Seis u32 desde event+0x18: room, position, event, subevent, screen, nextScreen | [Vars.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L2179) |
| Personaje del actor | actor+0x78, u32; candidato Dante=0 | [ActorDataBase](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3003) |
| Identidad auxiliar | actor+0x118, u8 id; actor+0x11C, u32 isClone | [PlayerActorDataBase](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3050) |
| Motion | actor+0x39B0, cuatro u8: **index, group**, repetidos para dos MotionData | [MotionData](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L2633), [layout](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3071) |
| motionTimer | actor+0x3E34, float32; unidad/valores especiales sin validar | [Vars.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3090) |
| state | actor+0x3E64, u32, conservado sin clasificar acciones | [Vars.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3094) |

Tamaños de referencia: puntero x64 8, MotionData 2, ActorDataBase 200,
PlayerActorDataBase 0x7540, Dante 0xB8C0, EventData 48, SessionData 304 bytes.
El lector **no copia esas estructuras completas**. DDMK comprueba sus offsets
con static_assert; eso no constituye una prueba de su significado en nuestro
proceso. El enum STATE de DDMK nombra 1=ON_FLOOR, 2=IN_AIR y 0x10000=BUSY;
BUSY no equivale a atacar.

Guardas estáticas de esta build:

- Hash de archivo exacto, sección PE escribible que contiene cada raíz y
  cabeceras cargadas coincidentes con máquina/timestamp/tamaño del archivo.
- Búsqueda **finita en disco**, en secciones ejecutables, de codificaciones MOV
  RIP-relative hacia la raíz del actor. La primera coincidencia actual está en
  RVA **0x3D570**, 7 bytes, SHA-256
  `9bbc486e5fbecf1c2057c83a5dbc88f082bc80659287ad8a95741386858a5f7c`.
  Se comprueban bytes hash y destino relativo también en memoria. Es un
  reconocedor acotado de codificaciones candidatas, no un desensamblador general.
- Dos secuencias comentadas en [Mary/Global.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Global.ixx#L185):
  RVA 0x23918A (5 bytes) y 0x238CCA (9 bytes), comprobadas en disco y memoria.
  Son guardas de compatibilidad; no se ejecutan ni alteran esos saltos.

No apareció una referencia MOV RIP-relative directa a la raíz del evento en
ese reconocedor. Evento y sesión conservan evidencia **fuente DDMK + sección
PE**, más comprobaciones pequeñas de páginas/punteros/contexto en ejecución;
no se presentan como firmas semánticas independientes. No se inventaron RVA
alternativos ni se aplicaron direcciones virtuales absolutas de otra sesión.

## Validez, desconocidos y etiquetas

El lector exige personaje candidato Dante en sesión y actor, id conservador
0–3, isClone=0, grupo motion menor que 34 (motionArchives[34]), temporizador
finito entre 0 y 1000000. Los índices u8 se registran sin atribuirles una acción.
state queda como u32 sin convertir BUSY o cambio de motion en ataque. Los
rangos de contexto (misión 0–20 y valores de evento/room acotados) son filtros
conservadores de esta investigación, no catálogo completo de todos los modos.

Se leen raíces/contexto antes y después de los campos. Cualquier cambio
observado de proceso, actor, punteros, misión/sala/evento, pérdida del foco,
lectura parcial, página inválida o fallo de rango descarta la muestra y limpia
el estado anterior. Tres muestras del mismo contexto son necesarias para salir
del calentamiento, sin reutilizar valores anteriores a la pérdida del actor.
No hay snapshot atómico: puede haber transiciones de frame entre lecturas, y
una salida y retorno al mismo contexto entre ticks (ABA) puede no observarse.

`g_scene` en DDMK es estado de su propio mod y no se usa como dirección del juego.
**Tener foco o EventData MAIN no demuestra que todo menú esté cerrado.** Las
pruebas de otros menús/cargas siguen pendientes; ya hay evidencia de una pausa
y cambio de sala específicos, sin cobertura general. El control
de foco solo consulta a qué PID pertenece la ventana activa; no mueve ventanas.

En capturas reales se observó **motionTimer=-1.0** durante el control de saltos.
Su significado sigue desconocido; esas muestras se rechazan y se registra el
valor. No se amplió el rango para hacer pasar la captura ni se interpretó -1
como ataque, fin de animación o prueba de puntero inválido. La primera captura
mixta no conservaba el valor rechazado: queda expresamente diferenciada.

## Capturas manuales sin cambiar de ventana

El usuario confirmó que DMC3 abre la pausa al recuperar el foco. No exigir que
la partida permanezca activa mientras responde al chat. Se adaptó la captura:

```powershell
& $observerPython .\tools\observe_dmc3.py --samples 200 --hz 10 --lead-in-seconds 15 --beep --label 'plan-reposo-tres-espada-reposo-sin-validar'
```

El siguiente procedimiento es el plan histórico, **no una captura solicitada
ahora**. Leer primero la [revisión de suficiencia](revision-capturas-dmc3.md):
la espada con pitidos tiene inicio incierto según la última aclaración, y las
primeras pruebas son exploratorias. Los pitidos usan Windows, sin descargar nada.

Para una prueba autorizada de una sola acción, ahora existe **una señal adicional
opcional**: --action-cue-seconds 5 junto a --beep. Requiere muestreo (no access-only
ni annotate) y un segundo de margen al inicio/final. Tono 1200 Hz, 60 ms, una vez;
eventos sampling.action_cue.begin/end con reloj monotónico y cue_only. El horario
real puede diferir del previsto; una señal no demuestra ejecución. El bloqueo
breve puede ensanchar un intervalo: revisar cadencia y descartes. Sin esta opción
se mantienen las señales anteriores. Cuenta regresiva/múltiples señales aún no
implementadas. Demo sin memoria y tests descritos en la ficha E1.

Responder al chat, volver al juego y cerrar su pausa durante los 15 segundos
iniciales. Al primer pitido comienza el intervalo de 20 s; permanecer quieto
3 s, realizar tres ataques de espada separados y terminar en reposo. Segundo
pitido: fin. Los pitidos solo coordinan al operador: **no son acciones detectadas**.
Los controles futuros deberán decidirse por la hipótesis y la evidencia ausente;
no repetir por rutina pausa/puerta ya observadas. No minimizar entre señales.
Ventana o pantalla completa pueden
usarse; el lector descarta las muestras cuando otro proceso tiene el foco.

`--label` conserva la **intención de la captura**, no su cumplimiento. Para un
operador independiente que vea una acción durante la captura, existe:

```powershell
& $observerPython .\tools\observe_dmc3.py --annotate 'D:\logs\dmc3-observe-FECHA-UUID' --action 'salto observado por operador'
```

La anotación lleva reloj monotónico compartido, sesión y procedencia
manual_report_unverified; no se admite después del cierre. Una declaración
posterior del jugador se conserva como nota de revisión, sin inventar tiempos
de acciones. No generar etiquetas observadas a partir del horario previsto.

Antes de afirmar detección auténtica faltan repeticiones limpias, controles
negativos y correspondencia temporal comprobable. Disparo, salto, cualquier
cambio de animación y etiqueta manual no sustituyen ese requisito.

Antes de cada petición de captura especificar duración, orden, cantidad de
acciones, reposos y prohibiciones. Separar golpe individual, combo completo,
disparo, salto, desplazamiento y reposo. Estudiar los combos como secuencias
propias; múltiples cambios de motion no certifican una cadena completa. Señales
por acción serían una mejora futura, no implementada en esta revisión. Las
actuales solo marcan inicio/fin del muestreo, sin tiempos observados de golpes.

## Tests y límites de la entrega

`python -m unittest discover -s tests -p test_dmc3_observer.py -v` comprueba fallos
de acceso, permisos pedidos, perfil incompatible, guardas estáticas, punteros,
páginas, lecturas parciales, pérdida de actor/proceso/foco, contexto, timers,
etiquetas y análisis de logs. La prueba Windows de lectura usa un buffer del
propio proceso Python; las restantes usan fixtures sintéticos. No cierran juegos
ni usan el PCSX2 del usuario. La suite PINE y los inspectores sin cambios no
necesitan repetirse para esta entrega. Evidencias reales y pendientes en
[CONTINUIDAD-LOCAL.md](CONTINUIDAD-LOCAL.md).

Referencias de permisos y lectura: [VirtualQueryEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualqueryex)
y [ReadProcessMemory](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory).
