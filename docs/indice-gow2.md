# Índice real de God of War II

**Actualización 2026-10-16:** el índice y las muestras R_HERO00.WAD,
R_HERO01.WAD y R_PERMA.WAD ya se recibieron. Se verificaron tamaños, CRC ZIP y
SHA-256 contra el informe; están preservadas fuera de Git en
`/workspace/dmc3-private/gow-samples`. No hace falta repetir las exportaciones
siguientes. La conversión visual queda pausada durante [la fase PINE](pine.md).

Se recibieron `GODOFWAR.TOC`, `raiz-iso.csv`, `SYSTEM.CNF` e `informe-gow.json`.
Los originales se conservan fuera de Git en `/workspace/dmc3-private/gow-index`.
No hace falta volver a enviarlos.

## Verificación y estructura

- `SYSTEM.CNF` identifica `SCUS_974.81`, versión declarada 1.01, vídeo NTSC.
- TOC: **39000 bytes**, SHA-256
  `9b339a2dfda12827d221e173a2fb806d7be5d6c436bcffcc650e1486604d77b0`.
  Tamaño y hash coinciden con el informe del usuario.
- **913 archivos**, **1532 ubicaciones**, sin posiciones sin usar en la tabla.
- Tipos: 293 WAD, 343 VPK, 194 VAG, 43 PSS, 39 PSW y un TXT.
- La raíz ISO9660 recibida sitúa `PART1.PAK` en sector 1654, con 4264382464 bytes.
  El listado solo cubre esa raíz, no la segunda capa.

La correspondencia con el informe verifica el archivo recibido, no su identidad
contra un hash oficial. El CRC `2F123FD8` sigue siendo el informado por PCSX2 en
la captura; no se recalculó al leer el TOC.

El lector propio `tools/inspect_gow_toc.py` interpreta un contador uint32
little-endian, registros de 36 bytes (nombre de 24 bytes, tamaño, cantidad e
inicio de ubicaciones), y una tabla de ubicaciones uint32. Se contrastó con
`drivers/toc/gow2.go` y `encounter.go` de God of War Browser, revisión
1bfc55c0172e67c48c8e941c495333f583c721a0.

La tabla usa direccionamiento por paquetes: valores desde 10000000 señalan
`PART2.PAK`; no son sectores absolutos de la ISO. El lector deja sin resolver
los offsets físicos de un PAK que no aparezca en el listado de raíz, en vez de
inventarlos. Los candidatos seleccionados tienen copias disponibles en PART1.

## Muestras seleccionadas

| Archivo | Bytes | Offset relativo a PART1.PAK | Offset absoluto ISO |
| --- | ---: | ---: | ---: |
| `R_HERO00.WAD` | 2301856 | 250535936 | 253923328 |
| `R_HERO01.WAD` | 2314640 | 3540992 | 6928384 |
| `R_PERMA.WAD` | 3421104 | 118784 | 3506176 |

Total: **8037600 bytes**, antes de comprimir. Los nombres HERO son candidatos
para estudiar variantes del personaje; no confirman aún el contenido de las
mallas. PERMA se incluye como candidato a recursos comunes por si los primeros
referencian recursos externos. No se ha identificado todavía cuál corresponde
a Kratos normal o a otras apariencias.

`R_HERO00.WAD` tiene cinco ubicaciones: tres en PART1 y dos en PART2. La recogida
selecciona una copia de PART1 para analizarla. No demuestra que las cinco copias
sean idénticas. Un futuro reemplazo debe considerar todas las ubicaciones que
el juego utilice; modificar solo una no prueba compatibilidad en otros escenarios.

## Copiar solo estas muestras en Windows

1. Abre [Export-GowHeroSamples.ps1](../tools/Export-GowHeroSamples.ps1), copia todo
   su contenido y pégalo en PowerShell. También puede ejecutarse desde un checkout
   local si tu política ya lo permite; no hay que cambiarla.
2. Lee la ISO de la ruta ya indicada, verifica BOOT2 y que el TOC coincida por
   SHA-256 con el recibido. Calcula las ubicaciones desde el índice y la raíz
   leídos de nuevo en la ISO, sin usar offsets físicos fijos.
3. Crea una carpeta nueva y un archivo **`D:\logs\gow2-muestras-...zip`**.
4. Adjunta ese ZIP: contiene los tres WAD e `informe-muestras.json` con tamaños,
   offsets y SHA-256. Si falla, adjunta `error.txt` de la carpeta de esa ejecución.

No modifica la ISO, no copia todo el PAK y no instala un parche. Limita cada
muestra a 16 MiB y el conjunto a 32 MiB. La comprobación de SHA-256 del TOC
detecta que se esté usando otro índice; no verifica la integridad completa de
la ISO ni compara los WAD con huellas oficiales. Los hashes de muestras son
huellas de los bytes copiados.

Verificado en PowerShell 7.4.21/Linux con la tabla y raíz reales del usuario,
pero con contenidos de paquetes sintéticos colocados en imágenes de prueba:
dos recogidas correctas sin sobrescribir, tres archivos exactos, hashes y CRC de
los ZIP comprobados; rechazo de TOC distinto, otro BOOT2, límites de PAK
inválidos e ISO ausente. **Seis ejecuciones**. Posteriormente se recibió el ZIP
real del usuario y sus hashes coinciden; no se ha validado un mod en PCSX2.

El lector TOC añade siete pruebas a la suite Python, que termina con **22/22**.
No contiene ni necesita archivos de juego para sus pruebas unitarias.
