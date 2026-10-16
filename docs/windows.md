# Primer paso en Windows: Dante en God of War II

## Alcance

El objetivo vigente es integrar ambos motores conservando los movimientos,
animaciones y mecánicas de DMC3. La fase actual es [la prueba PINE de solo
lectura](pine.md): comienza allí. El inventario y las muestras ya se recibieron;
los pasos siguientes se conservan como referencia y no necesitan repetirse.
La ruta de HD Collection está en tu PC; la nube no tiene acceso a esa unidad.
La presencia de `steam_api` no permite identificar por sí sola el archivo del
modelo ni su formato. No es necesario modificar esa DLL.

Se preservan la extracción y los avances Blender. Un reemplazo de texturas o
de malla no conservaría por sí solo las mecánicas originales de Dante. La
conversión visual queda pausada hasta estudiar la viabilidad del puente y del
renderizado, documentada en [arquitectura.md](arquitectura.md).

## Inventario de HD Collection sin instalar herramientas

El inventario de esta instalación ya se recibió; no es necesario repetirlo.
Para futuros informes y muestras se utiliza **`D:\logs`**, por petición del
usuario. Los bloques siguientes crean esa carpeta si no existe.

Abre PowerShell en Windows y pega el bloque completo:

```powershell
$ErrorActionPreference = 'Stop'
$game = (Get-Item -LiteralPath 'D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection').FullName.TrimEnd('\')
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$logRoot = 'D:\logs'
[System.IO.Directory]::CreateDirectory($logRoot) | Out-Null
$report = Join-Path $logRoot "dmc-hd-inventario-$stamp.csv"
$files = @(Get-ChildItem -LiteralPath $game -Recurse -File -ErrorAction Stop)
if ($files.Count -eq 0) { throw 'No se encontraron archivos en esa carpeta.' }
$files | ForEach-Object {
    [PSCustomObject]@{
        Ruta = $_.FullName.Substring($game.Length).TrimStart('\')
        Bytes = $_.Length
    }
} | Export-Csv -LiteralPath $report -NoTypeInformation -Encoding UTF8 -NoClobber
Write-Host "Inventario creado: $report"
```

El bloque enumera archivos y tamaños; no lee su contenido ni modifica la
instalación. Crea un CSV con rutas relativas en `D:\logs`, con un nombre
fechado para evitar sobrescrituras. Si aparece un error, comparte el mensaje;
no uses un informe parcial. Adjunta el CSV en el chat para localizar los
candidatos a contenedores y recursos. No hace falta enviar toda la instalación.

Este bloque se entrega como instrucciones para tu Windows: no se ha ejecutado
en tu máquina ni validado con PowerShell desde el entorno de nube.

## Preparar God of War II en PCSX2

1. Si aún no tienes el emulador, obtén la versión estable de Windows desde
   [el sitio oficial de PCSX2](https://pcsx2.net/). Anota su versión.
2. En el asistente de configuración, selecciona la carpeta de tu BIOS de PS2 y
   elige la BIOS detectada. La BIOS se queda en tu PC: no hace falta compartirla.
3. Prepara una imagen ISO de tu disco de God of War II y añádela a la biblioteca
   del emulador. No se instala como un juego de PC. Este flujo utiliza una ISO
   sin comprimir para poder inspeccionarla con la herramienta del proyecto.
4. Mantén los valores predeterminados de emulación, configura el mando y una
   tarjeta de memoria. Empieza con resolución interna nativa y renderizador
   automático; no actives trucos, parches ni reemplazos de texturas en esta prueba.
5. Arranca God of War II, inicia una partida, llega a un momento en que puedas
   controlar a Kratos y comprueba imagen, sonido y controles. Comprueba también
   un guardado y su carga cuando el juego lo permita. Si falla, registra el error
   antes de cambiar ajustes; la configuración concreta depende de tu hardware.
6. Los datos ya se proporcionaron: PCSX2 2.8.2.0, SCUS-97481 / CRC 2F123FD8.
   No hace falta volver a enviarlos ni reinstalar un juego que ya abre.

No se han probado estos pasos en tu PC. No hay todavía ajustes especiales
justificados para un mod de Dante ni un archivo PNACH que instalar.

## Qué aportó el inventario

- El inventario permite localizar qué archivos de HD Collection investigar para
  encontrar el Dante de DMC3, sin confundirlo con los recursos de DMC1 o DMC2.
- La edición de PS2 y una ejecución de referencia permiten investigar el recurso
  de Kratos y comprobar cambios contra una versión concreta que ya funciona.
- El inventario no contiene los modelos. Una vez localizados los candidatos,
  será necesario acceder a los archivos pertinentes para analizar el formato;
  no se puede construir el reemplazo solo con sus nombres.

El criterio actual es PINE con identidad correcta y lectura de código conocida.
Después se validará una acción real de Dante y una reacción GOW2; la composición
visual y las mecánicas requieren fases adicionales, no se dan por resueltas.

## Teclado en PCSX2

El destino confirmado por captura es God of War II NTSC-U, SCUS-97481, CRC
2F123FD8. La imagen europea anterior correspondía al primer God of War. No se
deben aplicar direcciones de memoria o parches de otra edición como si fueran
iguales. El teclado es opcional: un mando compatible con Windows puede utilizarse
en el puerto 1 con tipo DualShock 2 y asignación automática, revisando ambos sticks.

Con el juego detenido o pausado, abre **Ajustes / Configuración → Mandos /
Controladores** (`Settings → Controllers`). Selecciona **Puerto 1** (`Controller
Port 1`) y tipo **DualShock 2**. Los nombres exactos varían por idioma y versión.
En las asignaciones, pulsa cada casilla y después la tecla correspondiente:

| Entrada de PS2 | Tecla sugerida |
| --- | --- |
| Stick izquierdo arriba / izquierda / abajo / derecha | W / A / S / D |
| Stick derecho arriba / izquierda / abajo / derecha | I / J / K / L |
| Cruz (X) | Espacio |
| Cuadrado | F |
| Triángulo | R |
| Círculo | E |
| L1 / L2 | Q / 1 |
| R1 / R2 | C / 3 |
| L3 / R3, pulsación de sticks | Z / X |
| Cruceta arriba / izquierda / abajo / derecha | Flechas correspondientes |
| Start / Select | Enter / Retroceso |

Es una propuesta de distribución, no un perfil instalado automáticamente.
**WASD debe asignarse al stick izquierdo**, no solo a la cruceta. El stick derecho
sirve para esquivar en este juego; no lo dejes sin configurar. Si una tecla activa
también una función del emulador, resuelve el conflicto en **Atajos / Hotkeys**.
Guarda un perfil si tu versión lo permite.

Al volver al juego, comprueba movimiento con WASD, salto con Espacio, ataques
con F/R, bloqueo con Q y esquiva con IJKL. Completa después la prueba de guardado
y carga. Esto valida los controles del juego base; aún no prueba un mod.
