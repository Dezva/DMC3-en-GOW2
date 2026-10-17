# Campos DMC3: investigación offline · 2026-10-16

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
No se leyó el ejecutable original ni la RAM en esta sesión. La compatibilidad
en ejecución indicada abajo es **evidencia histórica**, no una nueva conexión.

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

## Qué podemos concluir sobre el temporizador

En las fuentes Mary revisadas, motionTimer solo aparece en declaración y
static_assert; el generador reproduce el campo. No encontramos un uso que
explique cómo se incrementa, reinicia o trata -1. **Eso no significa que el
juego nativo no lo use**: las fuentes de un mod no contienen su implementación.
No hay base para cambiar automáticamente de offset, tipo o política de lectura.

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
