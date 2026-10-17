# Instrucciones para Codex en este repositorio

Lee primero [la continuidad local](docs/CONTINUIDAD-LOCAL.md),
[README.md](README.md), [MODLOG.md](MODLOG.md),
[el contrato](docs/CONTRACT.md) y [la prueba PINE](docs/pine.md).
El [índice de documentación](docs/README.md) enlaza las demás investigaciones.

## Objetivo y prioridad del usuario

- Integrar motores: Dante debe conservar movimientos, animaciones, combos y
  mecánicas originales de DMC3 dentro del mundo de GOW2. No reducir el proyecto
  a sustituir el modelo de Kratos.
- Continuar por fases: PINE de solo lectura, estados auténticos de DMC3,
  reacción comprobable GOW2, espacio/cámara/colisiones y viabilidad visual.
- PINE ya está verificado; la tarea actual es el observador externo DMC3.
  Leer docs/dmc3-observer.md y las evidencias más recientes de continuidad.
  No repetir PINE si los informes íntegros sirven y no hay discrepancias.
- En la fase actual no escribir memoria de los juegos, reemplazar a Kratos,
  instalar DDMK/loaders ni activar hooks gráficos. Explicar cualquier límite
  técnico antes de proponer un cambio de arquitectura.
- Preservar modelos extraídos y avances Blender. Los assets están fuera de Git;
  clonar el repositorio no los traslada desde la nube al PC.

## Trabajo y entregas

- Continuar implementación y verificaciones autónomamente hasta necesitar una
  acción manual del usuario o abrir un programa. Mantener avances en GitHub;
  no detenerse solo en propuestas. Para gameplay sigue siendo necesario explicar
  la ficha y obtener nuevo «Listo» antes de cada captura.
- Usar el checkout existente y conservar cambios del usuario. Detectar primero
  el sistema y las herramientas disponibles; no suponer que una sesión local
  tiene GUI, permisos, PowerShell Windows o acceso a procesos de otra máquina.
- Los nuevos logs, informes y muestras Windows van a **`D:\logs`**, en carpetas
  únicas. No sobrescribir ni usar el escritorio. No volcar secretos.
- Entregar scripts y documentación mediante **Dezva/DMC3-en-GOW2 en GitHub**,
  con enlaces descargables. El usuario autoriza estas publicaciones; no hace
  falta repetir esa autorización para las entregas solicitadas. No publicar
  juegos, BIOS, assets extraídos, informes privados completos ni archivos Blender.
  No abrir PR ni enviar mensajes a terceros sin petición específica.
- Universal Modder sirve como apoyo, no como adaptador ya funcional. Verificar
  herramientas y versiones antes de utilizarlas. No instalar herramientas
  pesadas innecesarias; equipo i5-4460, GTX1050, 8GB RAM.
- El diagnóstico PINE está implementado y probado con datos sintéticos.
  **PINE real verificado en Windows/PCSX2 2.8.2; no hay puente de gameplay.**
  DMC3 identificado por ruta/PE/SHA; módulos desconocidos. Consultar la continuidad.
  Ya hay lecturas reales de campos candidatos DMC3; no equivalen a un detector.
  Si DMC3 está elevado y el lector no, registrar acceso denegado sin elevarlo.
  Para capturas manuales usar preparación y pitidos: el usuario reportó pausa
  automática al cambiar de ventana. No exigir partida activa mientras responde.
  Leer docs/revision-capturas-dmc3.md antes de pedir nuevas pruebas: las antiguas
  son exploratorias y una con pitidos tiene inicio incierto. Reutilizar evidencia.
  Explicar duración, acciones, orden, cantidad, reposos y prohibiciones antes de
  cada captura. Distinguir golpes individuales, combos completos, disparos,
  saltos, desplazamiento y reposo; estudiar los combos como acciones propias.
  La suficiencia ya se revisó; la petición posterior autoriza herramientas y
  detector experimental exclusivamente offline. Leer docs/dmc3-analisis-offline.md
  y docs/dmc3-campos-investigacion.md. La petición posterior ya autoriza preparar
  y coordinar pruebas controladas con el usuario, una por una, empezando por
  reposo y golpe individual. No iniciar muestreo hasta explicar la ficha y recibir
  confirmación de preparación; confirmar personaje/arma/estilo/contexto primero.
  docs/dmc3-validacion-controlada.md conserva R20/E1/E1-R confirmadas y J1 registrada
  (salto declarado, duración de pulsación incierta; seis timer=-1 rechazados,
  no ampliar filtros). J1-R ya tiene toque único y reposo declarados, cuatro -1
  rechazados; no confundir el cambio tardío en reposo con esos rechazos.
  Revisar suficiencia/timer antes de pedir más capturas por rutina;
  docs/dmc3-timer-native.md añade análisis estático: negativo retenido por resta
  es una hipótesis, no causa real probada. Diagnóstico opcional de contexto/
  evento/fase/speed ya implementado: docs/dmc3-timer-diagnostic.md. Perfil real
  comprobado sin actor,28 tests nuevos/66 regresiones sintéticas correctos.
  JT1 requiere nueva preparación; campos nuevos aún sin captura real. Mantener
  filtros y flags falsos. Animación automática de espera no invalida reposo.
  el combo sigue por concretar. No controlar entradas o ventanas de los juegos.
  Las hipótesis offline no son ataques autenticados: mantener phase2_verified
  y authentic_attacks_detected false, sin reacción GOW2 ni eventos de impacto.
  Diferenciar fuentes leídas, tests, datos reales del usuario y pruebas en juego.
- Verificar cambios con checks relevantes; no repetir suites por cambios solo
  documentales. Comandos, precondiciones y resultados en la guía local.
- Mantener MODLOG.md y la guía local al día, con evidencia y siguiente paso.

## Persistencia obligatoria de los avances

El usuario pide que **todos los cambios necesarios para progresar** queden
guardados en GitHub, tanto si se trabaja en nube como en local. No depender de
que Codex local pueda acceder a Codex Cloud o al historial del chat.

- Al iniciar una sesión, leer el estado Git y consultar el remoto antes de
  continuar. Conservar cambios locales y avances de otras sesiones; no hacer
  reset destructivo ni force push para actualizar el proyecto.
- Por cada avance relevante, guardar código, tests, documentación, configuración
  no secreta y pasos de reproducción. Actualizar MODLOG.md con qué cambió,
  evidencia, limitaciones y siguiente acción; mantener la guía de continuidad
  sincronizada cuando cambie el estado o el plan.
- Hacer commit y push al repositorio autorizado; la entrega actual usa main.
  Verificar que el commit está en la rama remota y entregar su enlace. Un
  archivo local o un commit sin push **no es una copia en GitHub**.
- Si se guarda trabajo parcial, identificarlo expresamente y registrar qué falta
  y qué pruebas no pasaron/no se ejecutaron. No presentarlo como una fase cerrada.
- Si el push falla por acceso, red o conflicto, conservar el trabajo y comunicar
  qué commit sigue pendiente de publicar; no declarar completada la copia remota.
- Los recursos privados siguen fuera de Git. Publicar metadatos/hashes, recetas
  y conclusiones técnicas necesarias para continuar; no afirmar que los assets
  privados o el filesystem de nube se transfieren al clonar el repositorio.

El procedimiento entre equipos se explica en
[la guía de continuidad](docs/CONTINUIDAD-LOCAL.md#guardar-y-sincronizar-los-avances).

Rutas de juegos, serial/CRC, hashes, referencias y pasos concretos están en
docs/CONTINUIDAD-LOCAL.md. docs/cloud-start.md contiene instrucciones históricas
del entorno Linux de nube; no ejecutar sus instaladores como setup de Windows.
