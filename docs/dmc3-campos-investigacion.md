# Campos DMC3: investigación offline · actualización 2026-10-17

Revisión fijada DDMK: `0319ae7132a6a822fd4dede2fb7cad484900169f`.
Se revisaron **30 archivos fuente**: los 28 .ixx/.cpp de Mary, ddmk.js y
Scripts/dmc3_create_data.js. Nueve copias existentes se reutilizaron y 21 se
descargaron como texto; 1.650.199 bytes en total. Todos sus blobs Git SHA-1
coinciden con el árbol fijado conservado en la investigación anterior; también
se registró SHA-256 de cada archivo. Sin compilar, instalar o ejecutar DDMK.
El navegador no recuperó las URLs fijadas; se consultaron las fuentes públicas
raw y se comprobaron sus blobs, sin sustituirlas por main u otra revisión.

Manifiesto privado:
`D:\logs\dmc3-offline-research-20261016-171259-1b3c293254664b488b5ceccf158c5701\source-manifest.json`.
Las fuentes previas siguen en la carpeta dmc3-research-20261016-022124 de continuidad.
En la investigación inicial del 16 no se leyó ejecutable ni RAM. La actualización
del 17 verifica dos referencias desde el ejecutable en disco, sin conexión a
procesos; la compatibilidad en ejecución citada sigue siendo evidencia histórica.

## Layout documentado y límites

| Campo | Evidencia de fuente fijada | Qué sabemos y qué falta |
|---|---|---|
| MotionData | [Vars.ixx:2633](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L2633): index u8 seguido de group u8 | Se interpreta en ese orden, no group/index en los bytes crudos |
| Dos MotionData | [Vars.ixx:117](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L117), [layout:3071](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3071): LOWER_BODY=0, UPPER_BODY=1, actor+0x39B0 | Canales inferior/superior según DDMK, no actual/anterior. Coinciden en las 1.193 muestras aceptadas históricas; no demuestra que sean redundantes |
| Mirrors | motionDataMirror[3] en +0x39B4 | No leídos ni necesarios para el análisis actual; no suponer que representan historia temporal |
| motionTimer | float32 +0x3E34, [Vars.ixx:3090 y static_assert:3261](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3090), [generador:205](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Scripts/dmc3_create_data.js#L205) | El lector usa exactamente el offset/tipo publicados. La semántica nativa y las unidades no quedan probadas |
| state | byte32 +0x3E64, lastState +0x3E68; [enum:943](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L943) | Fuente nombra floor=1, air=2, busy=0x10000. Registrar bits restantes sin bautizarlos; BUSY no es ataque |
| Actor | [ActorDataBase:3003](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3003): status u8 +8, personaje/enemigo union u32 +0x78; id u8 +0x118, isClone bool32 +0x11C | El perfil histórico comprueba personaje/id/clone y punteros; status no se capturó. Una dirección reutilizada no conserva identidad tras una carga |
| Sesión/contexto | [ddmk.js:2689](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/ddmk.js#L2689), [EventData:2179](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L2179) | Misión/personaje/sala/posición/evento/subevento/pantallas se registraron. La ruta de raíces y guardas estáticas siguen en dmc3-observer.md; no son un catálogo exhaustivo de escenas |

Vars.ixx y su generador son representaciones relacionadas del mismo layout:
su coincidencia **no es una segunda validación independiente**. Los static_assert
prueban coherencia de la estructura compilada DDMK, no la semántica del juego
nativo. El hash/PE, las guardas históricas y los valores coherentes respaldan
compatibilidad candidata; no garantizan que todo campo tenga el significado sugerido.

El enum EVENT de la fuente nombra 1 MAIN, 2 TELEPORT, 3 PAUSE y 11 DELETE.
Son nombres de fuente: el 11 observado anteriormente sigue sin validación
semántica independiente. No reinterpretar retrospectivamente una muestra de
transición como borrado de partida ni modificar la política MAIN del lector.

## Dos referencias nativas verificadas desde disco · 2026-10-17

Desde main local/remoto limpio **d883400fd4de4cc191286735f43bc5ffcf638fd5**.
Se revalidaron SHA-256 y blobs Git de los 30 archivos fijados. La búsqueda por
el identificador literal `motionTimer` había omitido comentarios con direcciones
numéricas/desensamblado. **Se corrige esa limitación**, sin cambiar de revisión:

| Procedencia fijada | RVA de carga → escritura | Operación transcrita en fuente y bytes comprobados |
|---|---|---|
| [Actor.ixx:14969](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L14969), bloque «Get Rebellion Stinger Duration» | 0x20932C → 0x209331 | Carga float desde [rax+0x28] a xmm1 y guarda en [rdi+0x3E34]; 13 bytes |
| [Actor.ixx:15165](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L15165), «Get Yamato & Force Edge Stinger Duration» | 0x21F69E → 0x21F6A6 | Carga float desde [rax+0x9C] a xmm1 y guarda en [rdi+0x3E34]; 16 bytes |

El SHA del ejecutable en disco coincide con la build conocida. Los dos rangos
caen dentro de .text ejecutable respaldada por archivo y coinciden exactamente
con la transcripción de fuente. Se leyó en modo rb: hash por bloques de 64 KiB,
cabeceras PE acotadas y **29 bytes de código** en esas ubicaciones, sin volcar
ejecutable/RAM, escanear procesos, ejecutar instrucciones o instalar DDMK.
Metadatos de archivo estables antes/después. No utilizar RVA como dirección absoluta.

Los helpers del mod [GetRebellionStingerDuration:11967](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L11967)
y [GetYamatoForceEdgeStingerDuration:11987](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L11987)
seleccionan stingerDuration/airStingerDuration por IN_AIR y el índice devil.
Solo se estudiaron como texto; la configuración del mod no es una medición nativa.

**Alcance:** dos caminos estáticos cargan un escalar de otra estructura y lo
guardan en ese offset; el mod los asocia con duración de Stinger. Esto respalda
un uso dependiente de acción y desaconseja asumir un reloj universal de animación.
No resuelve las unidades, identidad/procedencia completa de RDI/RAX, lectores,
otros escritores, actualización por frame, rutas del salto o significado de -1.
No demuestra que se ejecutaran esos caminos en las capturas anteriores ni que
los espadazos observados fueran Stinger. No se cambia offset, perfil o filtros.

Informe privado: `D:\logs\dmc3-timer-static-20261017-003000-8ba641ace1c94e80b3474d3261b1ef8a\report.json`,
SHA-256 `db723c5349c5451920221d1867c19eba48995d4610cfa44d894b2418ced721e3`.
Hashes de los rangos: 13 bytes `ecbcdfe1b67c21cb406351b5646398513c4fc2f0be3a3c9cf4fcc259fe13b16f`;
16 bytes `4abfb7c8c4a44c0e649fd5cdfc35505252185827d5f6f98bab99f1567680e6ad`.
Sin código nuevo/tests sintéticos ni conexión real nueva/PINE. Fase parcial/flags false.

Reproducción desde la raíz, usando el Python x64 existente (solo disco). Esta
receta reutiliza inspect_pe, que carga un PE de tamaño acotado ≤64 MiB para
validarlo; la comprobación real anterior usó hash streaming y lecturas puntuales:

```powershell
@'
import sys, hashlib
sys.path.insert(0, 'tools')
from dmc3_profile import inspect_pe, BUILD_SHA256
meta, data = inspect_pe(r'D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection\dmc3.exe')
assert meta['sha256'] == BUILD_SHA256, 'Build distinta: no aplicar RVA'
for rva, size, expected in [
    (0x20932C, 13, 'ecbcdfe1b67c21cb406351b5646398513c4fc2f0be3a3c9cf4fcc259fe13b16f'),
    (0x21F69E, 16, '4abfb7c8c4a44c0e649fd5cdfc35505252185827d5f6f98bab99f1567680e6ad')]:
    s = next(s for s in meta['sections'] if s['flags'] & 0x20000000
             and s['rva'] <= rva and rva + size <= s['rva'] + s['raw_size'])
    offset = s['raw_offset'] + rva - s['rva']
    assert hashlib.sha256(data[offset:offset+size]).hexdigest() == expected
    print(hex(rva), size, 'coincidente; semántica general no validada')
'@ | & "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -
```

Siguiente comprobación: delimitar funciones/instrucciones x64 y seguir lectores/
escritores de +0x3E34, especialmente inicialización, salto y valores negativos.
No había decoder general disponible en los módulos Python, PATH y rutas conocidas
consultados (capstone/iced_x86/distorm3/objdump/llvm-objdump/dumpbin); no se instaló
otro. Una continuación puede usar un decoder ligero aislado para análisis estático,
sin alterar el lector o los juegos. No interpretar coincidencias de bytes sin
fronteras de instrucciones como referencias válidas. No pedir otra captura hasta
obtener de esa investigación una hipótesis que la prueba pueda distinguir.

## Qué podemos concluir sobre el temporizador

Validación posterior R20/E1/E1-R: reposo y dos espadazos aislados, confirmados
por el usuario con Rebellion/Gunslinger, mantienen **2.0 en las 198 muestras
coherentes de cada captura**, aun cambiando motion/state. No muestra
progreso de ese espadazo, sin decidir unidad/sentinel o incompatibilidad nativa.
El episodio (3,3)/state65537 tiene asociación manual contextual; no es todavía
un ataque identificado independientemente. Detalles y hashes en
[validación controlada](dmc3-validacion-controlada.md).

J1 posterior se registró tras preparación; usuario declaró salto al tono corto
y reposo posterior, pero no recuerda cuánto mantuvo el botón. Es exploratoria
para el protocolo de pulsación breve; no atribuir el timer a mantener el botón.
Seis muestras coherentes (0,4) muestran timer **9,9,0,12,6,0**,
con state=1 en dos y state=2 en cuatro. Otras 184 coherentes mantienen 2.0; seis
rechazos conservan -1.0 con campos parciales anteriores al recheck final.
El campo sí varía en este registro, pero no muestra un progreso monótono
general ni resuelve unidades/cuenta regresiva/sentinel. Los descensos no prueban
reinicios. El hueco impide delimitar el episodio entero; no cambiar offset o
filtros por conveniencia. Falta estudiar referencias nativas estáticas acotadas.

J1-R posterior: usuario confirmó toque único y reposo. Timer9,8,2,11,5 en cinco
coherentes(0,4), una state1/cuatro state2; 188 timer2 incluyen una state2. Cuatro
-1 rechazados, campos parciales previos al recheck. No monotonicidad general,
no reposo identificado por2.0. El cambio posterior(0,0)→(0,3), state1/timer2,
fue aceptado~16,8 s, distinto de rechazos~6,4–6,7 s. Esto no respalda atribuir
los rechazos a la animación tardía de reposo sugerida por el usuario; la causa
de -1 sigue desconocida. No hace falta otra captura para comparar esos tiempos.

El identificador literal motionTimer aparece en declaración/static_assert y
el generador reproduce el campo. La búsqueda numérica posterior encontró las
dos escrituras anteriores; la conclusión inicial que omitía todo uso queda
corregida. Aún no se explica cómo se actualiza en salto o se trata -1: las
fuentes del mod no contienen la implementación completa del juego. No hay base
para cambiar automáticamente de offset, tipo o política de lectura.

Resultados históricos reanalizados:

- Espada con pitidos: 198/198 muestras aceptadas valen **2.0**, con cambios de
  motion/state. No sirve aquí como reloj de progreso, ni prueba que el juego
  estuviera detenido. No se segmentan golpes con ese valor.
- Saltos declarados: 13 rechazos preservan -1.0; siete conservan state=2 y seis
  state=1, con motion bruto `[4,0,4,0]` o `[31,0,31,0]` (index/group).
- Prueba mixta con disparo inicial: cuatro rechazos -1.0, uno con state=2 y
  tres con state=1. No es evidencia de un valor exclusivo de salto o de aire.
- Mixta 45 s: 60 rechazos del timer **sin valor registrado** en esa versión;
  no convertirlos retrospectivamente en -1.0.

Las muestras rechazadas por timer fallan **antes** de la revalidación final del
contexto. Los valores de error son observaciones parciales conservadas, no
snapshots coherentes. -1 podría ser un sentinel nativo, transición entre frames
o semántica/layout incompletamente comprendidos; ninguna explicación está validada.
Las bajadas positivas del timer en un motion constante son observaciones de
descenso, no prueba automática de reinicio de animación, repetición o combo.

## Hipótesis del usuario: ventanas de combos con pausa

El usuario propone relacionar +0x3E34 con una secuencia «golpe, esperar un poco,
golpe, golpe». Es una hipótesis útil sobre duración de acción/encadenamiento,
**no significado validado del campo** ni combo exacto identificado. El campo se
lee durante toda la captura, no aparece únicamente al rechazar una muestra.
En J1-R cambió a 9,8,2,11,5 entre 5,901–6,293 s desde primera marca de muestra;
los -1 rechazados están en 6,386–6,685 s, recuperación coherente a 6,990 s.
Son marcas tras lecturas, no hora visual del salto/input, y la unidad del valor
no se conoce. Los dos espadazos aislados conservaron 2.0 antes/durante/después.

La variación sin combo declarado y las referencias de duración de Stinger no
identifican una ventana de combo general; tampoco excluyen usos distintos por
acción. Antes de probarla, seguir lectores/escritores nativos, identificar arma,
estilo y ruta completa exacta, y definir comparación temporal que distinga
explicaciones. 10 Hz puede omitir ventanas breves: no medirlas como frames.
No se inicia ni se programa otra captura por esta pregunta. Filtros intactos.

Nota literal privada: `D:\logs\dmc3-combo-timing-hypothesis-20261017-003232-06e3fd6653504c6b8545ad113f428a4e\hypothesis.json`,
SHA `41238296e481b23fc6c82c4935eda3d24cdac80a82bf8a3ed978d41c5f58536b`.

## Campos complementarios para una validación posterior

| Campo de fuente | Lugar/tipo | Comprobación necesaria; no realizado ahora |
|---|---|---|
| idleTimer | actor+0x3E38, float32 | [Actor.ixx:615](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L615) asigna 600.0 en lógica del mod: no acredita unidades ni comportamiento nativo. Comparar reposo/acción/pausa sin asumir contador ascendente |
| motionSpeed / multiplier | +0x3894 / +0x3898, float32 | Son factores según nombres/uso de fuente, no temporizadores; falta lectura/compatibilidad/correlación nativa |
| frameCount de MissionData | +0xA8, u32 dentro de otra estructura | Contador de misión documentado, no fase de animación. Resolver su propia raíz, probar pausa/escena y wrap; no aplicar +0xA8 al actor |
| action / lastAction / bufferedAction | +0x3FA4 / +0x3FA5 / +0x3FA8, u8 | Layout fuente; no están en logs. [ACTION_DANTE:487](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L487) nombra partes de combos, pero no podemos mapear ese enum a un motion index |
| chainCount | +0x3FAC, u8 | Nombre candidato para secuencias; unidad, reinicio y relación con combos/impactos sin validar |
| weaponTimers[5] | +0x64F4, float32[5] | No leídos, no presumir reloj de animación. No usar newWeaponTimers de estructuras extendidas DDMK en un proceso sin mod |

Estos campos son una lista de investigación, **no se añadieron al observador**.
Primero harían falta comprobaciones nativas acotadas del uso del campo (referencias
de lectura/escritura estudiadas estáticamente, sin ejecutarlas), y luego una
captura pequeña autorizada con guardas/páginas y observación temporal independiente.
Una animación completa/interrumpida y controles de reposo/salto/pausa permiten
contrastar progreso, countdown y sentinel; la mera coincidencia con un botón no.

## Regla experimental de familias

[IsWeaponActive en Actor.ixx:2109](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L2109)
consulta UPPER_BODY y familias de [MOTION_GROUP_DANTE:411](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L411).
El nuevo analizador deriva una heurística explícita: grupos 3–7/13–17, index>0,
como candidatos de motion de familia cuerpo a cuerpo; 8–12/18–22 como familia
de arma a distancia. Excluye grupo 8 índices 2/4/5 según ese helper. Añade index>0
también a familias de estilo como filtro conservador, sin fingir ser el helper exacto.

Ni el helper ni nuestra derivación certifican un ataque: pueden incluir manejo,
recuperación y otras animaciones. No se asignan nombres de golpes a índices.
El tipo ranged tampoco demuestra disparo. La regla ni siquiera produce un
candidato ranged en la prueba que el usuario dijo empezar con un disparo:
**cobertura incompleta**, sin métricas de precisión/recall ni validación negativa.
Detalles de cronología y resultados en [análisis offline](dmc3-analisis-offline.md).
