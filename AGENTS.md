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
- En la fase actual no escribir memoria desconocida, reemplazar a Kratos,
  instalar DDMK/loaders ni activar hooks gráficos. Explicar cualquier límite
  técnico antes de proponer un cambio de arquitectura.
- Preservar modelos extraídos y avances Blender. Los assets están fuera de Git;
  clonar el repositorio no los traslada desde la nube al PC.

## Trabajo y entregas

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
  **No hay aún puente de gameplay ni prueba real de PCSX2 desde esta sesión.**
  Diferenciar fuentes leídas, tests, datos reales del usuario y pruebas en juego.
- Verificar cambios con checks relevantes; no repetir suites por cambios solo
  documentales. Comandos, precondiciones y resultados en la guía local.
- Mantener MODLOG.md y la guía local al día, con evidencia y siguiente paso.

Rutas de juegos, serial/CRC, hashes, referencias y pasos concretos están en
docs/CONTINUIDAD-LOCAL.md. docs/cloud-start.md contiene instrucciones históricas
del entorno Linux de nube; no ejecutar sus instaladores como setup de Windows.
