# Inventario de HD Collection recibido

Se analizó el CSV `dmc-hd-inventario-20261015-225415-069.csv` aportado por el
usuario. Contiene **281 registros**, con columnas `Ruta` y `Bytes`. El análisis
usa únicamente nombres y tamaños; no se recibió el contenido de los juegos.

Se recibieron después las variantes `...225415-541.csv` y `...225415-069.csv`:
son idénticas byte a byte, SHA-256
`c245568f4b9601362963c0d31ac3ef19b5fc400ca09513e57a4528e3f221d80b`.
No faltaban recursos por haber enviado solo una de ellas.

| Archivo relevante | Tamaño en bytes | Observación |
| --- | ---: | --- |
| `dmc3.exe` | 6 356 432 | Ejecutable de DMC3 presente en la instalación |
| `data\dmc3\dmc3-0.nbz` | 960 358 951 | Principal contenedor candidato a investigar |
| `data\dmc3\LOADERICON.dds` | 524 416 | El nombre indica un icono de carga; no identifica el modelo de Dante |

La instalación también contiene `dmc1.exe` y `dmc2.exe`. Se debe mantener la
investigación centrada en los recursos bajo `data\dmc3` para este objetivo.
En esa carpeta hay audio OGG y vídeos WMV, que no son necesarios para el primer
reemplazo visual del personaje.

## Lo que todavía no se sabe

La extensión `.nbz` y el tamaño no confirman por sí solos el formato ni el recurso
de Dante. No se ha abierto ni extraído el contenedor del usuario.

Se investigó el código fuente de [DDMK, `Mary/File.ixx`, commit
0319ae7132a6a822fd4dede2fb7cad484900169f](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/File.ixx#L109-L209).
Su función `ExtractFile` abre `data\\dmc3\\dmc3-0.nbz` mediante `zip_open`
(libzip) y lee entradas `GData.afs/<nombre>` mediante `zip_fopen`.
Esto respalda probar un lector ZIP directamente sobre el NBZ, sin renombrarlo.
No demuestra aún que el NBZ concreto del usuario sea compatible o esté íntegro.
Solo se inspeccionó el código fuente externo: no se instaló ni ejecutó DDMK.

No es necesario modificar `steam_api` ni ejecutar programas de la instalación
para enumerar estos recursos.

## Resultado del listado interno recibido

El usuario ejecutó el lector ZIP y adjuntó `dmc3-nbz-20261015-235339-251.csv`.
Contiene **4334 entradas** (4333 archivos y el directorio `GData.afs/`), con
**2257001989 bytes** de contenido descomprimido declarado. Incluye 3725 archivos
`.pac`; no es necesario extraerlos todos.

La entrada **`GData.afs/pl000.pac`** mide **1335280 bytes** descomprimidos y
**651475 bytes** comprimidos. DDMK vincula `pl000` con Dante en
[`fileDataHelperDante`, Mary/Actor.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Actor.ixx#L2893-L2912),
y con `obj\\pl000.pac` en
[`cacheFileHelpers`, Mary/Vars.ixx](https://github.com/serpentiem/ddmk/blob/0319ae7132a6a822fd4dede2fb7cad484900169f/Mary/Vars.ixx#L1329-L1344).
Es la muestra inicial seleccionada para investigar los recursos de Dante.
La muestra ya se recibió y se inspeccionó. La conversión al formato de PS2 destino
todavía no se ha implementado.

## Resultado del análisis de pl000.pac

Tamaño recibido: **1335280 bytes**. SHA-256 calculado:
`b73b6e8ee2f2088a088f4215a5a13a50700fb4e4f0bef54dc0bcce11ae7b9c5d`.
Coincide con `informe.json`; esto confirma la correspondencia con la muestra
exportada, no su identidad contra una huella oficial del juego.

El PAC contiene 15 posiciones en su tabla de bloques. Los offsets son little-endian
y relativos al inicio de cada PAC; se validaron también tres PAC internos.

| Recurso | Posición PAC | Offset en el archivo | Resultado |
| --- | ---: | ---: | --- |
| Texturas | 0 | `0x50` | Tres DDS DXT5 con mipmaps |
| Modelo principal | 1 | `0x96850` | MOD, 17 objetos, 24 huesos |
| Modelo del abrigo | 12 | `0x13A070` | MOD, 6 objetos, 33 huesos |
| Configuración de tela | 13 | `0x142BE0` | Texto CLT, no simulado |

Los roles principal/abrigo coinciden con el uso de `file[1]`, `file[0]`, `file[12]`
y `file[13]` en `UpdateModel` de DDMK, `Mary/Actor.ixx`.

| DDS | Offset | Dimensiones | Mipmaps | Bytes extraídos |
| --- | ---: | --- | ---: | ---: |
| `texture_000.dds` | `0x8C0` | 512 × 512 | 10 | 349680 |
| `texture_001.dds` | `0x560C0` | 256 × 512 | 10 | 174928 |
| `texture_002.dds` | `0x810C0` | 256 × 256 | 9 | 87536 |

Se abrieron y examinaron visualmente las tres texturas: rostro y abrigo rojo;
pantalones, botas y accesorios; pelo. Los DDS se copiaron sin recodificar.
La longitud de sus mipmaps se calcula a partir de dimensiones y bloques DXT;
el campo de tamaño lineal del encabezado original no siempre coincide con ella
y se conserva tal como está.

`tools/inspect_pac.py` reproduce el análisis y la copia selectiva. Rechaza tablas
inválidas, offsets duplicados, imágenes DDS truncadas y sobrescritura de carpetas:

```sh
python3 tools/inspect_pac.py /ruta/pl000.pac --manifest /ruta/informe.json --output /ruta/nueva/carpeta
```

La importación 3D adicional se describe en [arquitectura.md](arquitectura.md).
Los recursos de juego y vistas derivadas permanecen fuera del checkout Git.

## Copiar la muestra de Dante

**Completado por el usuario.** Se conservan estos pasos como referencia; no hay
que volver a enviar `pl000.pac` ni su informe.

El script [Export-DanteSample.ps1](../tools/Export-DanteSample.ps1) abre el NBZ
para lectura, selecciona únicamente `GData.afs/pl000.pac` y comprueba que su
tamaño descomprimido coincida con el inventario recibido. Crea un subdirectorio nuevo bajo
**`D:\logs`** para evitar sobrescribir resultados de ejecuciones anteriores.

Copia el contenido del script y pégalo completo en PowerShell. Sus valores
predeterminados corresponden a la instalación indicada por el usuario. También
puede ejecutarse desde el repositorio en Windows, si la política local permite
scripts:

```powershell
.\tools\Export-DanteSample.ps1
```

Adjunta **`pl000.pac`** y **`informe.json`** de la carpeta que indique el comando.
Si falla, adjunta **`error.txt`** de esa ejecución en su lugar. No modifica el NBZ,
no instala nada en el juego y no extrae otros recursos. No cambies la política
de ejecución de PowerShell para este paso; puedes usar el contenido pegado.

Se validaron seis ejecuciones funcionales en PowerShell 7.4.21 sobre Linux con
ZIP sintéticos: copia y hash del contenido exacto, repetición sin sobrescribir,
entrada ausente, nombre duplicado, tamaño incorrecto y NBZ ausente. Los originales
permanecieron sin cambios. No se ha ejecutado en Windows ni con el NBZ del usuario.

El informe incluye tamaño y SHA-256 de la muestra. Esa huella identifica lo
copiado: no es una comparación con una huella oficial ni el CRC de PCSX2. El
script no verifica el CRC de la entrada ZIP de origen. La comprobación del tamaño
no sustituye una prueba de integridad del archivo.

## Listar el interior del NBZ en Windows (referencia)

Este paso ya se completó. Se conserva para reproducir el análisis; los próximos
informes van a `D:\logs`, no al escritorio.

Este bloque utiliza el lector ZIP incluido en .NET/PowerShell y crea un CSV en
`D:\logs`. Abre el NBZ para lectura: no lo modifica ni extrae sus entradas.
Ejecuta el bloque completo en PowerShell y adjunta el nuevo CSV:

```powershell
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$nbz = 'D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection\data\dmc3\dmc3-0.nbz'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$logRoot = 'D:\logs'
[System.IO.Directory]::CreateDirectory($logRoot) | Out-Null
$report = Join-Path $logRoot "dmc3-nbz-$stamp.csv"
$zip = [System.IO.Compression.ZipFile]::OpenRead($nbz)
try {
    $rows = @($zip.Entries | Select-Object FullName, Length, CompressedLength)
    if ($rows.Count -eq 0) { throw 'El archivo no contiene entradas ZIP.' }
    $rows | Export-Csv -LiteralPath $report -NoTypeInformation -Encoding UTF8 -NoClobber
    Write-Host "Listado creado: $report"
} finally {
    $zip.Dispose()
}
```

La lectura del índice ZIP no comprueba el CRC ni descomprime el contenido de cada
entrada. Si el lector produce un error, comparte ese mensaje; no renombres el
original ni uses un informe parcial. El usuario ya aportó el listado real; esta
instancia no tiene acceso al NBZ para repetir esa lectura.

El listado permitirá escoger archivos concretos para analizar; no confirma por
sí solo qué entrada contiene a Dante. La conversión del modelo y la investigación
del formato de God of War II siguen pendientes.

## Estado del destino PS2

La nueva captura identifica **God of War II NTSC-U**, **SCUS-97481**, **CRC
2F123FD8**. El usuario indica PCSX2 **2.8.2.0**, en Windows. Ruta de la ISO:
`D:\Games PS2\God of War II [NTSC]\God of War II.iso`.

Corrección de la identificación anterior: el juego europeo que había arrancado
era **God of War**, SCES-53133 / FB0E6D72, y no God of War II. Su configuración
o sus parches no son intercambiables con los del destino confirmado.

Pendientes: prueba de control del personaje, guardado y carga del segundo juego;
acceso e investigación de sus WAD. El [índice PS2 ya se recibió y analizó](indice-gow2.md).
La etiqueta de
compatibilidad de la biblioteca no sustituye una prueba funcional.
