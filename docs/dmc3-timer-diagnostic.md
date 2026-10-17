# Diagnóstico opcional de timer · implementado, JT1 exploratoria registrada

2026-10-17, desde main limpio/local-remoto
`bd40b220bf344cbef2e3e4a1cc54978120e66792`. El usuario autoriza continuar
implementación hasta necesitar una acción manual/programa. No iniciar gameplay
sin explicar ficha y obtener nuevo «Listo».

## Implementación y procedencia

`observe_dmc3.py --timer-diagnostic` usa `dmc3_timer_diagnostic.py`, solo biblioteca
estándar. El modo anterior permanece sin la opción. Perfil base/protocolo exterior
v1 conservados; extensión opcional versionada timer_diagnostic con campos/guardas
exactos. Sin escrituras, hooks, DDMK instalado o privilegios nuevos.

| Campo | Offset/tipo | Procedencia fijada DDMK y evidencia nativa |
|---|---|---|
| actor_event_u32 | +3E08/u32 | eventData[1].event, Vars.ixx3087/ActorEventData2627; selector1F6F96 |
| phase_u8 | +3E10/u8 | Primer byte var_3E10, Vars.ixx3088; handler1F4440, sin enum universal |
| speed_f32 | +14/f32 | ActorDataBase.speed, Vars.ixx3008/assert3035; resta1F448E, unidades desconocidas |

Revisión `0319ae7132a6a822fd4dede2fb7cad484900169f`, fuentes y flujo en
[análisis nativo](dmc3-timer-native.md). Tres guardas adicionales de esta build
se comprueban en disco y memoria antes de leer al actor:

| RVA | Bytes | SHA-256 |
|---|---|---|
| 1F6F96 | 8 | `4f86986d6e3189f9766658706b522ffa8054f6ff6e978f7cc17811bde7798596` |
| 1F4440 | 7 | `cce4a02dde017c1badcbddb6cf60c0a72a50e66108f42bad5c4a97e38676703b` |
| 1F448E | 24 | `cb9ca6259d4ce40decb3c8f0592a29d6eb8e09050c8bb6b78ce2cb03baa18a12` |

Repite identidad y evento/fase antes/después de campos. Cada par usa9 bytes,
ignorando4 intermedios de lastEvent; no copia estructuras completas. Muestra
estable:22 lecturas/234 bytes, bloque máximo32; modo previo17/200. Guarda ventana
de lectura monotónica, no tiempos nativos de acción. PID/base se redescubren.

## Calidad y rechazo

**Timer finito0..1000000, sin cambios:** -1/no finitos siguen rechazando toda
la muestra, invalidando valores anteriores y exigiendo calentamiento. Generaciones
por política no demuestran actor perdido. Solo tras comprobar contexto/identidad,
vida/foco se conserva el intento rechazado dentro de timer_diagnostic, con calidad
explícita y raw timer; no hay motion/timer aceptados en el nivel exterior.

Evento/fase distintos antes/después producen diagnostic_transition y calidad
transition_observation_only. Fallos de acceso/páginas/parcial/actor/escena/foco/
proceso no conservan intento como contexto revalidado. Speed no finito se guarda
null+repr/calidad desconocida, nunca NaN JSON. Evento/fase son tipos crudos sin
nombre automático; finitud no demuestra unidades. No snapshot atómico: cambios
ABA o entre frames pueden pasar inadvertidos. No unir huecos de capturas anteriores.

`analyze_dmc3_timer_diagnostic.py CAPTURA` valida integridad temporal, build y
extensión/calidades/ventanas, exporta analysis.json y observations.csv a carpeta
nueva. Conserva sample_valid=false en rechazos/transiciones/calentamientos; no
infiere causa de -1, frames, combos o ataques. El analizador anterior conserva
su segmentación de aceptadas. El diagnóstico no necesita Capstone.

## Validación ejecutada

**28 tests nuevos y66 regresiones sintéticas correctos**. Cubren -1/no finitos,
cambios de evento/fase/escena/actor/identidad/foco/proceso, parciales/Win32,
build/perfil/anclas alterados, CLI, JSON finito, presupuesto, calentamiento,
análisis inconsistente y recorrido sintético captura→informe. Regresiones:
25 observador/perfil/logs +34 temporales +7 cues. Sin WindowsSelfRead, PINE o
cierre de juegos. Fixtures sintéticos no son pruebas reales en juego.

**Profile-only real correcto**, sin actor/señales: PID10688, inicio UTC
2026-10-17T02:38:13.424527Z, base0x7FF7C6920000 redescubiertos, huella conocida,
tokens medios8192/no elevados, acceso0x410. Ocho lecturas/212 bytes de cabeceras/
código, cero errores/muestras. Son identidades históricas; no reutilizarlas.
Esto comprobó el perfil antes de JT1; la captura real posterior figura abajo.

Evidencia privada:

- `D:\logs\dmc3-observe-20261017-005434-b15d7e4e93274fb6b98d00b2fb076d69`;
  report SHA `ac56b4ca0301b85aa0cb1aa6be13f04b6339ea98261f56b252a9c4e771d38f9c`,
  events SHA `153024a331e318c0926d6d6c508d906bef0a4cd80063826a7162e4a36ecd5485`,
  profile SHA `d914c6b6b842a0a9771a0ed8eac7137e45b20e10fb6802d30edb039c7405e0de`.
- `D:\logs\dmc3-timer-diagnostic-check-20261017-005705-58e91be160034bd4b18d369420ea2ac6`;
  delivery-verification SHA `c83e3b4eeb8c5e8bf8d50b155d31f0d99ae2c548d3be11bbbe86ad13f0825723`,
  diagnostic-tests-delivery SHA `245fb86189cb8d6f12536d66225a6d881633da84ddf7c005202a63aee6337554`,
  regression-tests SHA `32ad073810a9c1f01e4335d68a3112f5a027e4d0aa73bc0f4947edc98d8553ed`.

verification.json conserva26 tests iniciales; delivery-verification lo complementa
con28 finales sin sobrescribir. Informes completos fuera de Git. Fase parcial.

## JT1 real · dos saltos declarados y negativo con contexto revalidado

Capturada con código **cda57168baf2e2fdf037a1a979066d29f19b0216**, tras ficha y
«Mismo contexto; listo para JT1». Dante/Rebellion/Gunslinger, misión7 normal,
mismo lugar sin enemigos declarados.25 s preparación,200 muestras/10 Hz y
señal corta a5,00026 s. Usuario informó después que saltó por confusión al
primer pitido largo, descansó y saltó otra vez al corto. **Exploratoria: no es
un control limpio de reposo→un salto.** No confirmó duraciones exactas de
pulsaciones, tiempos visuales independientes ni todas las prohibiciones.

**179 muestras coherentes y21 no aceptadas:**8 timer=-1,3 transiciones durante
lecturas,10 calentamientos; cuatro bloques aceptados.200 intentos conservan
diagnóstico tras recheck final. Actor/contexto constantes observados, speed1
en200 intentos. Cero fallos Win32, parciales o pérdida observada de foco/actor/
contexto/proceso. Huella/identidad/base redescubiertas: PID10688, inicio UTC
02:38:13.424527, base0x7FF7C6920000; tokens medios8192/0x410 sin elevar.
4408 lecturas/47012 bytes incluyendo perfil; máximo32 bytes por bloque.
Identidad histórica, nunca usar como parámetros de una ejecución futura.

Tiempos desde primera marca de muestra, **no horas de input ni frames nativos**:

| Episodio observado | Evento/fase | Timer en orden | Tiempos aproximados (s) |
|---|---|---|---|
| Inicial, salto accidental declarado | 6/3 | 14,8,2 | 0,588–0,788 |
| Inicial, negativo | 6/4 | -1 | 0,895 |
| Inicial, negativo persistente | 8/0 | -1,-1,-1 | 0,989–1,200 |
| Tras corto, salto declarado | 6/3 | 8,1 | 5,988–6,110 |
| Tras corto, negativo | 6/4 | -1 | 6,195 |
| Tras corto, negativo persistente | 8/0 | -1,-1,-1 | 6,292–6,488 |

Algunas filas de la tabla son calentamientos y **todos los -1 son rechazados**.
No unirlas como segmento aceptado. Evento5/fase1/timer9 aparece antes del segundo
episodio; en el primero se observó5→6 dentro de una lectura. La transición2→3
del segundo conserva14 pero se rechaza como transición. Dos episodios en una
sesión no equivalen a dos repeticiones controladas independientes.

Cadencia entre marcas: mediana99,66 ms, mínimo28,14/máximo191,69; ventana de
lecturas mediana25,21 ms,19,70–54,50 ms. Ningún tick omitido registrado; la señal
corta ocupa75,74 ms y el jitter limita resolución. Fase0/2, cruce por cero y
restas individuales pueden perderse. La secuencia es **compatible con negativo
retenido tras resta y fase4**, reforzada por flujo estático, pero no prueba
causa aritmética exacta, unidades, sentinel universal ni tiempo de combos.
La permanencia del negativo en evento8 no demuestra un temporizador activo.
Cambio posterior1/fase0→1/fase1/motion(0,0)→(0,3), timer2, es un hecho distinto.

Integridad: JSON/esquema/relojes/calidades/perfil verificados por el loader
temporal y el analizador diagnóstico;
hashes de los cuatro originales iguales antes/después del análisis. Eso acredita
consistencia de archivos, no autenticación independiente de las acciones.

Evidencia privada completa (no publicada):

- Captura `D:\logs\dmc3-observe-20261017-010459-45d2ef79d54e428fbc907de5c0f91485`;
  report SHA `133623bc0e999165ba03e39129fb7ea4b7976f3abded91cba903e0dfe5ef7fa5`,
  events SHA `106569551f47a49eeacfa5ad9674d3b2413d463d4f11f5efe80024ef7799afd8`,
  session SHA `9adb3d5bdf59d1d8fba85218e05ed87226ead08524e20e94c3fc013db0058ff3`;
  candidate-profile SHA igual al perfil de005434 anterior.
- Análisis JSON/CSV `D:\logs\dmc3-timer-review-20261017-010835-49917b1ddfdb434a88bf0d02fa154dfc`;
  analysis SHA `106322bd443821535e3e3d8a5592cd29eb8d828a8e5a81eaae6a0b4a5b72a776`.
- Aclaración literal y revisión `D:\logs\dmc3-jt1-review-20261017-010930-f060b875ddd0421b8ae471c6149c214e\manual-review.json`;
  SHA `b953a9cb4d37bfc7f0c3495c73798a112de3036a456ba64ff0bb2e4f9cbd272e`.

Sin código/perfil/filtro nuevo tras JT1 ni suites repetidas por documentación.
La comprobación real del nuevo diagnóstico complementa los28/66 tests previos;
no convierte fixtures sintéticos en pruebas del juego. PINE no se repitió.

## Decisión sobre repetición y procedimiento futuro

**No repetir ahora por rutina.** JT1 no prueba un salto exclusivo, pero los dos
episodios declarados permiten estudiar los campos y la persistencia. El salto
inicial invalida la hipótesis de reposo inicial limpio, no el acceso/perfil o
toda la evidencia. No ocultarlo ni sobrescribir la captura. Primero investigar
qué condición termina el evento8; [seguimiento estático](dmc3-timer-native.md#seguimiento-del-evento8-tras-jt1)
ya acota dos funciones, con callees aún desconocidos. Solo pedir otra prueba
si distingue una hipótesis que los datos existentes no resuelvan.

El usuario pide **15 s de preparación** en futuras capturas. La configuración
de25 s usada en JT1 es histórica. Para una eventual repetición de salto, todavía
no solicitada/iniciada, conservar esta ficha adaptada y nuevo «Listo»:

Objetivo: observar evento/fase/speed con el rechazo y contrastar el negativo
retenido.10 Hz puede omitir fases/umbral; no demuestra cada resta nativa ni su
unidad. No es repetición idéntica de J1: cambió el lector. Si falta cobertura,
declararla sin inferir causa o inventar muestras.

Confirmar Dante, Rebellion activa, Gunslinger, mismo lugar misión7 normal/sin
enemigos. **Reposo significa no tocar controles:** animaciones automáticas de
espera permitidas, no errores de ejecución.

1. Tras nuevo «Listo»,15 s para volver a DMC3/cerrar pausa.
2. Pitido largo agudo: inicio20 s/200 muestras/10 Hz, permanecer sin entradas.
3. Pitido corto a~5 s: UN toque de salto, soltar enseguida al despegar.
4. Aterrizar sin dirección y reposo hasta pitido grave final.
5. Cero espada/disparos/segundo salto/dirección/lock-on/estilo/equipo/menús/
   cambios de ventana durante registro. Volver al chat solo al terminar.
6. Preguntar después por salto/toque/reposo/señales/incidentes. Pitidos y relato
   no son detector independiente; conservar cualquier desviación.

**No hay otra captura iniciada.** Solo se necesita DMC3 para esta fase.
No abrir PCSX2 ni repetir PINE para esta fase.

```powershell
$timerPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
# Verifica código/perfil, sin leer actor ni exigir foco/partida:
& $timerPython .\tools\observe_dmc3.py --profile-only --timer-diagnostic
# Solo tras nueva preparación explícita:
& $timerPython .\tools\observe_dmc3.py --timer-diagnostic --samples 200 --hz 10 --lead-in-seconds 15 --beep --action-cue-seconds 5 --label 'future-plan-one-brief-jump-action-unverified'
# Usar la ruta de captura devuelta por el observador:
& $timerPython .\tools\analyze_dmc3_timer_diagnostic.py 'D:\logs\RUTA_NUEVA_DE_CAPTURA'
& $timerPython -m unittest discover -s tests -p test_dmc3_timer_diagnostic.py -v
```

phase2_verified=false y authentic_attacks_detected=false. Sin impactos/reacción GOW2.
