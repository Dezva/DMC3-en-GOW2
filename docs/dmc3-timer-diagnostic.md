# Diagnóstico opcional de timer · implementado, captura de actor pendiente

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
Los campos nuevos del actor **todavía no tienen captura real**.

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

## Próxima prueba manual JT1: un solo salto

Objetivo: observar evento/fase/speed con el rechazo y contrastar el negativo
retenido.10 Hz puede omitir fases/umbral; no demuestra cada resta nativa ni su
unidad. No es repetición idéntica de J1: cambió el lector. Si falta cobertura,
declararla sin inferir causa o inventar muestras.

Confirmar Dante, Rebellion activa, Gunslinger, mismo lugar misión7 normal/sin
enemigos. **Reposo significa no tocar controles:** animaciones automáticas de
espera permitidas, no errores de ejecución.

1. Tras nuevo «Listo para JT1»,25 s para volver a DMC3/cerrar pausa.
2. Pitido largo agudo: inicio20 s/200 muestras/10 Hz, permanecer sin entradas.
3. Pitido corto a~5 s: UN toque de salto, soltar enseguida al despegar.
4. Aterrizar sin dirección y reposo hasta pitido grave final.
5. Cero espada/disparos/segundo salto/dirección/lock-on/estilo/equipo/menús/
   cambios de ventana durante registro. Volver al chat solo al terminar.
6. Preguntar después por salto/toque/reposo/señales/incidentes. Pitidos y relato
   no son detector independiente; conservar cualquier desviación.

**No iniciada.** DMC3 estaba abierto y accesible; solo se necesita ese juego.
No abrir PCSX2 ni repetir PINE para esta fase.

```powershell
$timerPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
# Verifica código/perfil, sin leer actor ni exigir foco/partida:
& $timerPython .\tools\observe_dmc3.py --profile-only --timer-diagnostic
# Solo tras nueva preparación explícita:
& $timerPython .\tools\observe_dmc3.py --timer-diagnostic --samples 200 --hz 10 --lead-in-seconds 25 --beep --action-cue-seconds 5 --label 'JT1-plan-one-brief-jump-action-unverified'
# Usar la ruta de captura devuelta por el observador:
& $timerPython .\tools\analyze_dmc3_timer_diagnostic.py 'D:\logs\RUTA_NUEVA_DE_CAPTURA'
& $timerPython -m unittest discover -s tests -p test_dmc3_timer_diagnostic.py -v
```

phase2_verified=false y authentic_attacks_detected=false. Sin impactos/reacción GOW2.
