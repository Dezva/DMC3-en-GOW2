# Temporizador DMC3: investigación estática parcial · 2026-10-17

Se continuó desde main local/remoto limpio
`3c4d9c045b30b34fa9aab7a65ec724e63e05f1f9`. No hubo nueva captura, conexión
a procesos, PINE, escritura en juegos o instalación/ejecución de DDMK. La build
de disco sigue siendo SHA-256 `4ae4bb5c83c19a649fc60edc5ca40e7f3ceee6337e4e4275025bfa9caa40c0a0`.

## Método y herramienta

`tools/inspect_dmc3_native_timer.py` reutiliza la inspección PE acotada existente,
exige build conocida y las dos anclas de fuente verificadas anteriormente. Hace
una pasada finita de secciones ejecutables **en disco** buscando el desplazamiento
3E34, selecciona rangos de la tabla de excepciones PE y decodifica desde sus
inicios. No inicia un debugger, instala breakpoints ni ejecuta código del juego.

La tabla RUNTIME_FUNCTION contiene RVA de inicio/fin/unwind según
[Microsoft](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64).
Sus entradas pueden ser fragmentos, y las funciones hoja pueden no figurar.
No confundir esos límites con una función fuente completa o con alcance dinámico.

Se obtuvo una rueda oficial PyPI Capstone **5.0.9**, 1.273.459 bytes, SHA-256
`732cedbbb56d42e723f14d7af6387f1454194a820b4b96b56d1e53f865ef85d0`, extraída
en carpeta única privada (~9 MB), sin cambiar el Python global ni los juegos.
La metadata de distribución dice5.0.9, el binding informa5.0.7 y cs_version()
devuelve(5,0,1280): conservar las tres cosas, no inventar una versión uniforme.
La [API oficial](https://www.capstone-engine.org/lang_python.html) permite
decodificar x64 y consultar operandos; esto no valida la semántica del juego.

Resultado: **240 referencias candidatas en95 rangos**, todas las ocurrencias
crudas dentro de rangos de excepción. 225 referencias tienen un camino directo
local desde el inicio del rango. Tres rangos dejan decodificación lineal incompleta,
conservada como limitación. Los otros15 no se llaman «inaccesibles»: saltos
indirectos, fragmentos y caminos externos no se resuelven automáticamente.
No todas las referencias al mismo desplazamiento tienen identidad de actor probada.

Presupuestos: PE≤64 MiB; hasta1024 ocurrencias/512 rangos seleccionados, rango
individual≤64 KiB y total seleccionado≤2 MiB. Conserva anchos de operandos,
hashes, contexto mínimo, decodificación incompleta y alcanzabilidad local.
Una coincidencia dentro de un inmediato no se convierte en referencia a memoria.
No cubre accesos vía bases ajustadas ni constituye un grafo completo de control.

## Evidencia nueva e hipótesis de negativo retenido

La revisión manual acotada de1705 bytes añade estas relaciones estáticas:

| Sitio/RVA | Evidencia | Alcance |
|---|---|---|
| 1F6F96 / tabla1F7234 | Selector desde actor+3E08, menos1; caso5 llama1F45E0 y caso6 llama1F43F0 | Campo que la fuente sitúa en eventData[1].event; no leído en capturas |
| 1F476F | Caso5 inicializa +3E34 con9.0 | La fuente fija ACTOR_EVENT::JUMP=5; asociación estática, no trazado real |
| 1F4639 → 1E09D0 | Caso5 puede pasar6 al setter; mapa589FA0 índice6 contiene6; se escribe+3E08 y reinicia+3E10 | Enlace candidato de inicialización a continuación |
| 1F4598 / 1F450A | El handler del caso6 puede asignar5.0 o14.0 según fase/condiciones | No son segundos ni umbrales de combo validados |
| 1F4519–1F4531 | CargaT, resta actor+14, guardaT y contrasta con cero | En una fase espera mientrasT>0 |
| 1F448E–1F44D8 | Resta actor+14, guarda incluso resultado negativo; cambia de fase al ser negativo, sin clamp en ese camino | Puede conservar un resultado negativo después |
| 1E011D | Escribe2.0 en otra ruta que también limpia campos de acción | Evidencia local; el rango se decodifica incompleto más adelante |

La fuente [Vars.ixx:759](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L759)
fija JUMP=5. El caso6 sigue teniendo nombre desconocido en esa fuente: no
rebautizarlo como acción universal validada. +3E08 pertenece a eventData[1]
según [layout:3087](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3087).
+3E10 es un byte dentro de var_3E10, sin enum semántico validado. +14 es
[speed:3008](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L3008),
con assert3035; no asumir tiempo en segundos o frames.

En el handler candidato: fase0 prueba una máscara de botones y puede ponerT=5;
fase1 decrementa; fase2 depende de una condición vertical y poneT=14; fase3
decrementa hasta negativo y avanza a fase4 sin borrarlo. La identidad exacta
de la máscara de entrada no se resolvió; el campo no mide necesariamente el
tiempo que se mantiene un botón. También hay usos de suma y otros valores
en otras rutas: no llamarlo contador exclusivo de salto o de combos.

**Hipótesis comprobable:** siT=0 y speed=1, la resta produce-1; al cambiar de
fase puede quedar retenido hasta otra transición. Es un ejemplo aritmético,
no una medición de speed ni demostración de la causa de J1/J1-R. No se encontró
store inmediato0xBF800000 entre las240 referencias candidatas, lo que no excluye
escrituras vía registros/indirectas u otros caminos. No declarar un sentinel
documentado ni un fallo del juego. Esta explicación es más concreta que asociar
el negativo a una animación de reposo tardía o a un combo nunca ejecutado.

## Siguiente avance, sin cambiar el filtro para aceptar -1

Preparar una revisión del diagnóstico que termine de comprobar actor/contexto
incluso cuando rechace el timer y pueda conservar calidades separadas. Justificar
y comprobar lecturas pequeñas de eventData[1].event(+3E08/u32), fase(+3E10/u8)
y speed(+14/f32), además de los campos actuales. **No implementado ni capturado
en esta entrega**; exige perfil/guardas/tests y evitar nuevos usos de PID/base antiguos.

El timer seguirá desconocido/rechazado bajo la política actual. No mezclar
«contexto verificado» con «semántica del timer aceptada» ni unir huecos anteriores.
Después de validar ese diagnóstico, una sola captura finita de salto con preparación
podrá contrastar el orden de fases, la resta y la retención. Pedir nueva preparación,
no lanzar nada por estas preguntas. 10 Hz puede perder umbrales; medir cobertura
antes de afirmar la causa. Un combo requiere arma/ruta completa/alternativa exactas.

Esto permite progresar con motion/state e identidad/calidad sin fabricar ataques
a partir de BUSY o del timer. La fase DMC3 sigue parcial y no se activa GOW2.

## Reproducir y comprobar

El observador mantiene su dependencia exclusiva de biblioteca estándar. Capstone
es opcional solo para investigación estática. Si se prepara en otro equipo, usar
el Python x64 existente y un directorio privado **nuevo** como --target, con
`--only-binary=:all: --no-deps --require-hashes -r tools/requirements-native-analysis-windows.txt`.
No instalarlo en carpetas de juegos ni activar mods.

En este equipo ya está aislado en:
`D:\logs\dmc3-native-review-20261017-003643-4f0140f82236407da880c1e7f4f5dafa\decoder`.
No hace falta descargarlo de nuevo. Desde la raíz en PowerShell:

```powershell
$nativePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$nativeDecoder = 'D:\logs\dmc3-native-review-20261017-003643-4f0140f82236407da880c1e7f4f5dafa\decoder'
& $nativePython .\tools\inspect_dmc3_native_timer.py --exe 'D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection\dmc3.exe' --decoder-path $nativeDecoder
$env:DMC3_STATIC_DECODER_PATH = $nativeDecoder
& $nativePython -m unittest discover -s tests -p test_dmc3_native_timer.py -v
```

**13 pruebas sintéticas correctas**, separadas del ejecutable real: build
incompatible, ancla distinta, mapeos ambiguos/no ejecutables, cola virtual,
lectura parcial, tabla de excepción inválida, falso positivo en inmediato,
código sin camino local, decode incompleto, negativo preservado y ancho64.
Sin Capstone se omiten cinco tests del decoder; no confundir skip con ejecución.
No se repitieron suites de juegos/PINE u observador sin cambios.

Evidencia privada completa:

- `D:\logs\dmc3-native-timer-20261017-004202-c8487fcef47c429897ec31475d3272e8\report.json`,
  SHA `8221506a31dea8039b4c7a897a1159f8f2fdf94e30753dd363fd31666a936442`.
- `D:\logs\dmc3-native-review-20261017-003643-4f0140f82236407da880c1e7f4f5dafa\native-interpretation.json`,
  SHA `543e17720891fbc551f041c87ecf8e190a038e88b983ce8761454e4e69806736`;
  `review-addendum.json` corrige la cita de declaración speed3007→3008, sin cambiar
  offset/tipo ni el assert3035. El manifiesto del decoder registra procedencia y hashes.
- Misma carpeta, `synthetic-tests.txt`, SHA
  `f0d182ca5ce786bfed81b9de7c3793111ed186d22235d628eced0ae59b6930d3`.

Solo código propio, fixtures sintéticos, receta/metadatos y conclusiones se
publican. Wheel/DLL del decoder, desensamblado privado y ejecutable quedan fuera
de Git. `phase2_verified=false`, `authentic_attacks_detected=false`.
