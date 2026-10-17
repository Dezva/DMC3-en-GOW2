# Validación controlada DMC3 · fichas y resultados

La nueva petición autoriza preparar y realizar pruebas con el usuario tras
identificar evidencia faltante. **Ninguna captura nueva se ha iniciado todavía.**
Confirmar contexto y preparación antes de cada ejecución; una respuesta sobre
equipo/personaje no equivale a «Listo». No se necesita repetir PINE. El usuario
controla el juego; no instalar grabadores/hooks ni cambiar sus entradas/ventanas.

## Primera ficha activa: R20, control negativo de reposo

Estado: **propuesta, pendiente de confirmar personaje/arma/estilo/contexto y
preparación**. Se verificaron otra vez 34 archivos históricos y los hashes de
dos parejas PINE. Las primeras capturas permanecen exploratorias; la espada
con pitidos tiene inicio incierto. El baseline 023130 no tiene etiqueta de
reposo confirmado ni contexto de equipo declarado y no sustituye a este control.

Hipótesis: comprobar si el timer 2.0 y/o motions/estados candidatos de espada
pueden aparecer sin ataques voluntarios. Primero un negativo aislado; luego,
si sirve, una captura distinta con un solo golpe y el mismo equipo/contexto.
R20 sola no valida la semántica de un ataque ni del temporizador.

Antes de iniciar, confirmar Dante, arma cuerpo a cuerpo, estilo, misión/sala
si se conoce, en partida sobre suelo llano y sin enemigos/interacciones cerca.
No suponer Rebellion ni un estilo concreto. Mantener equipo/contexto para el
posterior golpe aislado; cualquier cambio se anota, no se oculta.

Procedimiento de **esta ficha únicamente**, con señales ya disponibles:

1. Tras la confirmación de preparación, lanzar una captura finita con 25 s de
   preparación: volver a DMC3, cerrar su pausa y dejar a Dante quieto. No responder
   al chat durante el intervalo. No debe estar atacando al empezar.
2. Primer pitido agudo (880 Hz, 200 ms): comienza el intervalo de muestreo.
   Permanecer quieto **20 segundos**, cero pulsaciones de espada, disparo o salto.
3. Segundo pitido grave (660 Hz, 200 ms): fin. Ya se puede volver al chat.
4. Preguntar después si permaneció quieto entre señales y si hubo menú, enemigo,
   movimiento/ataque accidental o cambio de foco. Registrar la declaración y
   errores como nota posterior, sin tiempos inventados ni reemplazar originales.

Evitar stick/teclas de movimiento, lock-on, cambio de equipo/estilo/devil trigger,
pausa, minimizar, cambiar de sala/ventana. Una animación de reposo espontánea se
conserva: no es error por sí sola ni se reclasifica como acción ofensiva.
Si aparece una interrupción, dejar de actuar, esperar el fin y explicarla después.

Configuración propuesta: 200 muestras a 10 Hz, preparación 25 s y --beep; sin
cambios al código o perfil. Los pitidos existentes ya se usaron en capturas
confirmadas por el usuario; no requieren descarga ni señales intermedias.
Antes de leer gameplay se redescubren PID/ruta/inicio, SHA/PE, base real y guardas
de lectura del observador; error de acceso/build impide continuar, sin elevarlo.
Esto tampoco se ha ejecutado todavía para la nueva ficha.

10 Hz da aproximadamente 100 ms entre muestras, suficiente para contrastar un
tramo de reposo de 20 s, **sin cobertura por frame**. Revisar huecos/ticks omitidos
y tiempos reales al terminar. Para el golpe posterior, los límites solo podrán
acotarse entre muestras; si se pierden transiciones, declarar la limitación antes
de cambiar frecuencia o repetir. No modificar el filtro de -1.0 ni usar 2.0 como
reloj. Guardar rechazos, causas, generaciones y foco; todos los flags semánticos
siguen false hasta evidencia suficiente. R20 no activa automáticamente la prueba E1.

## Diseño posterior, no señales implementadas

Las secciones siguientes conservan propuestas para otras fichas. Los diseños
de cuenta regresiva y pitidos por acción **no están implementados**; no usarlos
como si fuesen la ficha R20 o estuviesen sonando con el CLI actual. Antes de una
prueba con esas señales, explicar el ajuste mínimo, implementarlo y verificarlo.
No pedir al usuario contar entradas de un combo sin completar su ficha exacta.

## Preparación común y señales propuestas

Antes de pedir «Listo», entregar **una sola ficha completa**: objetivo, arma,
estilo, botón real configurado, duración, orden/cantidad de acciones, reposos,
prohibiciones y condición de cancelación. No dar por conocidas teclas o mando.
Confirmar Dante, sala, dificultad/modo, arma/estilo y enemigos presentes; mantener
esos factores entre comparación positiva y negativa. Para acciones básicas,
preferir suelo llano sin enemigos/interacción cercana, sin lock-on ni stick.
Esto separa animación de impacto: **no se intentará medir daño ni aciertos**.

La cuenta regresiva y señales por acción siguientes son un **diseño pendiente**;
la herramienta actual solo tiene preparación y pitidos de inicio/fin. No indicar
al usuario que ya oirá las señales intermedias con el CLI publicado. Cuando se
implemente esa coordinación, usará audio Windows sin descargar nada. Antes de
la primera captura explicar y demostrar las señales fuera del registro, para
que un pitido inesperado no encuentre al jugador atacando.

Horario propuesto, t=0 inicio del muestreo:

| Momento | Señal/instrucción |
|---|---|
| t=-25 s | Aviso de preparación. Volver a DMC3, cerrar la pausa automática y dejar a Dante quieto. No atacar durante la preparación |
| t=-3, -2, -1 s | Tres pitidos cortos iguales (440 Hz, 80 ms), cuenta regresiva 3–2–1; seguir quieto |
| t=0 | Un pitido agudo largo (880 Hz, 200 ms), inicio; **todavía no actuar** |
| t=5 s y otros tiempos de la ficha | Un pitido corto diferente (1000 Hz, 80 ms), ejecutar solo la acción indicada |
| t=T | Un pitido grave largo (660 Hz, 500 ms), fin; ya se puede volver al chat |

Permanecer en el juego hasta la señal final, sin Alt-Tab, minimizar ni responder
al chat. Si aparece un menú o sucede un accidente, detener las acciones, esperar
el final y describirlo después; no improvisar una repetición dentro de la misma
captura. No hay obligación de dejar el juego activo mientras se contesta al chat:
los 25 s sirven precisamente para volver y cerrar su pausa.

## Fichas de acciones básicas

T=30 s de muestreo, aparte de 25 s de preparación. Cada pulsación debe soltarse;
no mantener ni machacar botones. Los horarios son **órdenes previstas**, no
etiquetas de acciones observadas ni tiempos exactos de reacción humana.
La prohibición de moverse se refiere a entradas voluntarias de stick/teclas;
el desplazamiento propio de una animación no invalida por sí solo su registro.

| Ficha | Acciones y cantidad | Reposos | Acciones prohibidas durante los 30 s |
|---|---|---|---|
| R: reposo | Cero acciones; pitidos de control a 5, 13 y 21 s que se deben ignorar | Quieto de 0 a 30 s | Espada, disparos, salto, movimiento, lock-on, estilo/devil trigger, cambio de arma, menú/ventana |
| E1: golpe aislado | Una pulsación del botón de espada a 5 s; soltar y no continuar la cadena | 0–5 s y desde terminar la animación hasta 30 s | Segunda pulsación de espada, combo, disparo, salto, movimiento, lock-on, cambio de equipo/estilo, menú/ventana |
| E3: tres separados | Una pulsación de espada a 5, 13 y 21 s, tres en total | Ocho segundos entre inicios previstos; después de cada pulsación dejar concluir y volver a reposo. Quieto 0–5 s y tras el tercero hasta 30 s | Encadenar una segunda pulsación antes de la siguiente señal; disparar, saltar, moverse, lock-on, equipo/estilo, menú/ventana |
| D3: disparo | Una pulsación de disparo a 5, 13 y 21 s, tres pulsaciones; soltar cada una | 0–5 s y reposo entre señales/final | Espada, salto, movimiento, lock-on, mantener disparo, cambio de arma/estilo, menú/ventana |
| J3: salto | Una pulsación de salto a 5, 13 y 21 s; tres saltos previstos desde suelo | Aterrizar y quedar quieto antes de cada siguiente señal; 0–5 s y final en reposo | Espada, disparo, stick, segundo salto en aire, lock-on, equipo/estilo, menú/ventana |

E3 no son tres combos ni tres impactos contra un enemigo. D3 cuenta pulsaciones,
no balas ni impactos: un botón podría generar varias animaciones/proyectiles.
Si una acción no terminó antes de su siguiente señal, **no pulsar para cumplir
el horario**; la ficha no quedó correctamente ejecutada y se conserva como
exploratoria. No modificar datos para simular recuperación o ausencia de menú.

## Combo completo y cadena interrumpida: fichas aún incompletas

No conocemos arma/estilo/ruta ni entradas exactas de las capturas históricas.
El enum DDMK distingue partes de REBELLION_COMBO_1, pero eso no basta para elegir
controles o mapear motion IDs a partes. Antes de estas dos pruebas completar
una ficha C con **nombre tal como aparece en el juego, arma, estilo, N entradas,
orden, ritmo/pausas de cada entrada y final visible esperado**. Consultar la lista
de movimientos en el juego antes de empezar, fuera de la captura; el usuario
podrá aportar sus instrucciones cuando vuelva. Sin esa ficha no se pide «Listo».

Diseño común: T=40 s, preparación 25 s, señal de comienzo de secuencia a 5 y
22 s, **dos intentos**. Reposo inicial 5 s; tras cada intento, soltar controles
hasta la siguiente señal o fin. Solo ejecutar si la ficha C termina con margen
antes de 22 s y de 40 s; de lo contrario, ajustar y explicar toda la duración
antes de empezar, dentro del presupuesto finito del lector.

- C-completo: en cada señal ejecutar exactamente las N entradas y pausas de C,
  sin agregar movimientos. Observar la secuencia final y recuperación; pulsar
  N veces no acredita que haya salido el combo completo.
- C-prefijo: misma C, misma arma/estilo y ritmo, pero **omitir su última entrada**
  (N-1 en cada intento), soltar y dejar recuperar. Si C tuviera tres entradas
  confirmadas serían dos por intento; este número no se impone sin completar C.
  Es cadena truncada por no continuar, no una cancelación mediante salto/estilo.

Prohibido en ambas: disparar, saltar, desplazarse voluntariamente, lock-on si no
forma parte explícita de C, cambiar arma/estilo, devil trigger, menú o ventana.
Si una técnica exige dirección/lock-on, incorporarlos exactamente a C y a su
control; no cambiar la regla a mitad del registro. Estudiar después cancelaciones
auténticas requiere otra hipótesis, sin mezclarla con el prefijo incompleto.

## Campos y sincronización que se contrastarán

Campos ya disponibles: identidad histórica del actor, generación, personaje/id,
misión/sala/evento, ambos MotionData, state y timer crudo, estado de validez,
foco/errores, secuencia y reloj monotónico. Mantener -1 como desconocido y romper
continuidad. Analizar por separado inferior y superior, cambios y tramos estables.
No usar BUSY, timer o cantidad de pitidos para certificar un golpe.

Campos de investigación adicionales (action/lastAction/bufferedAction/chainCount,
idleTimer y otros) **no están implementados ni validados**. Resolver primero
su compatibilidad y significado; no hacer volcados o escaneos para llenar huecos.
Un aumento de frecuencia hasta el límite ya existente de 20 Hz sería una decisión
posterior con coste medido, no garantiza cobertura por frame ni arregla etiquetas.

La futura coordinación debería registrar reloj monotónico antes/después de emitir
cada señal y su horario objetivo. Si una señal llega tarde, conservar el retraso
sin emitir una ráfaga para recuperar el horario. Describir latencia acústica y
reacción humana como incertidumbre. Conservar separadamente:

1. Horario previsto y señal realmente emitida.
2. Muestras/intervalos de motion/state del lector.
3. Relato posterior del jugador (incluidos accidentes, sin tiempos inventados).
4. Inicio/final de acción observado independientemente, con incertidumbre.

Para el punto 4, si se dispone y autoriza después, una cámara externa que capte
pantalla y pitidos puede dar alineación audiovisual sin DLL/hooks ni carga de
grabación en el juego. Revisarla contra el registro de señales; no hay grabación
de ese tipo ahora. Otra persona podría anotar con reloj compartido sin alterar
el foco; un jugador solo no debe cambiar a una ventana de anotaciones durante
la prueba. Sin observación independiente, conservar el resultado como asociación
declarada, aunque la ejecución haya sido correcta.

## Aceptación y qué repetir

Antes de proponer detector auténtico: al menos dos capturas limpias separadas por
condición, acciones observadas y límites temporales, negativos R/D3/J3, y otro
conjunto independiente del usado para formular la regla. Reportar resultados por
captura, falsas alarmas y acciones omitidas; no elegir umbrales con todos los datos
y presentar esos mismos datos como validación. No hay aún métricas de precisión.

Si empieza con acción ya activa, ese primer intervalo queda censurado; el resto
puede servir para otras hipótesis. Si hay disparo en E3, no usarlo como control
exclusivo de espada. Si hay un combo donde se esperaba E1, conservar como cadena
exploratoria sin nombrarla. Si hay pausa/pérdida de actor/sala, invalidar bloques
y no unir secuencias; la evidencia puede servir para ciclo de vida. Explicar
qué hipótesis perdió soporte antes de repetir únicamente la condición faltante.

La prueba de pausa/puerta existente se reutiliza; no se pide de nuevo por rutina.
Estas fichas no permiten afirmar impactos, hitboxes, daño o integración GOW2.
La observación futura seguirá de solo lectura y la fase permanecerá parcial
hasta aportar evidencia independiente, repeticiones y controles suficientes.
