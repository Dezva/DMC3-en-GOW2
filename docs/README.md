# Documentación del proyecto

Punto de entrada para retomar el trabajo en Codex local:
**[CONTINUIDAD-LOCAL.md](CONTINUIDAD-LOCAL.md)**. Las instrucciones que Codex debe
leer automáticamente están en [AGENTS.md](../AGENTS.md), en la raíz.

| Documento | Contenido |
|---|---|
| [README principal](../README.md) | Objetivo, descarga y ejecución inicial |
| [Continuidad local](CONTINUIDAD-LOCAL.md) | Estado real, Windows, siguiente sesión, fases y recursos que no viajan con Git |
| [Contrato](CONTRACT.md) | Propiedad de estado, canales, formato y ciclo de vida |
| [PINE](pine.md) | Activación en PCSX2, diagnóstico, campos y errores |
| [Observador DMC3](dmc3-observer.md) | Lecturas externas, perfil candidato, permisos, validación y capturas con pitidos |
| [Revisión de capturas DMC3](revision-capturas-dmc3.md) | Aclaraciones del jugador, evidencia reutilizable, límites por acción y controles ausentes |
| [Análisis offline DMC3](dmc3-analisis-offline.md) | API/CLI temporal, JSON/CSV, hipótesis, pruebas sintéticas y resultados históricos |
| [Investigación de campos](dmc3-campos-investigacion.md) | DDMK fijado, dos escrituras nativas del timer verificadas en disco, anomalías y límites |
| [Timer: análisis nativo](dmc3-timer-native.md) | Herramienta estática x64, 13 tests, rutas de resta/fases y siguiente diagnóstico |
| [Timer: diagnóstico opcional](dmc3-timer-diagnostic.md) | Implementación,28 tests/66 regresiones, perfil real sin actor y ficha JT1 pendiente |
| [Validación controlada](dmc3-validacion-controlada.md) | R20/E1/E1-R confirmadas, J1 exploratoria, J1-R con toque/reposo declarados y límites |
| [Arquitectura](arquitectura.md) | Integración entre motores, DDMK, antecedente RE4/Minecraft y viabilidad visual/rendimiento |
| [Diario](../MODLOG.md) | Evidencias, pruebas, decisiones y cambios de prioridad |
| [Inventario DMC3](inventario-dmc3.md) | Inventarios recibidos, PAC, DDS e investigación del origen |
| [Índice GOW2](indice-gow2.md) | TOC, DVD9, muestras WAD recibidas y exportación histórica |
| [Recursos preservados](recursos-preservados.json) | Metadatos: nombres, tamaños y SHA-256 de archivos privados de la nube |
| [Preparación Windows](windows.md) | Referencia de controles e inventarios ya completados |
| [Inicio de nube](cloud-start.md) | Setup reproducible Linux; no es el setup de Windows |

La fase vigente es observación DMC3 de solo lectura; PINE ya quedó verificado.
Los documentos de inventario/exportación
conservan procedimientos anteriores: no implican que haya que repetirlos ni
retomar la conversión de aspecto. Los recursos extraídos y Blender se conservan
fuera del repositorio. El inventario JSON solo registra metadatos; no los descarga.

La documentación del proyecto disponible está publicada en este repositorio.
El historial completo del chat, los binarios privados y los logs originales de
trabajo no forman parte de una clonación. Su contexto técnico útil queda resumido
en la guía de continuidad, el diario y los documentos enlazados.
