# Instrucciones para generar el Manual de Programación

Cuando el usuario pida generar el manual de programación, debes:
1. Crear un archivo HTML temporal con la estructura definida abajo.
2. Convertirlo a **PDF** y **DOCX**.
3. **Eliminar el HTML** — el entregable final es solo el PDF y el DOCX.

---

## Datos fijos (siempre iguales)

- **Autor:** Didier Eduardo Coa  
- **Materia:** Lenguaje Programacion II  
- **Universidad:** Universidad de la salle  
- **Git user:** Eduardo-Coa  

---

## Estructura del documento

### PÁGINA 1 — Portada (página completa, todo centrado)

```
[Título de la actividad] → bold, ej: "Actividad 6."
[Nombre del autor]       → bold: "Didier Eduardo Coa"
[Materia]                → normal: "Lenguaje Programacion II"
[Universidad]            → bold: "Universidad de la salle"
[Fecha]                  → italic bold: formato D/M/AAAA
```

---

### PÁGINA 2+ — Cuerpo del manual

#### Encabezado
```
Manual de Programación   ← h1
Autor: Eduardo Coa
Repositorio: Eduardo-Coa/[nombre-repo]
Rama principal de trabajo: [rama-git]
```

---

#### Sección 1 — Descripción General

- Párrafo introductorio describiendo qué implementa el proyecto, en qué lenguaje y la fuente bibliográfica si aplica.
- **Tabla:** `Sistema | Descripción` (una fila por sistema/módulo principal).
- Párrafo resumiendo el patrón o concepto central del proyecto.

---

#### Sección 2 — Estructura del Proyecto

- Bloque de código (fondo oscuro) con el árbol de carpetas y archivos del proyecto.

```
NombreProyecto/
├── Clases/
│   ├── Clase1.java
│   └── Clase2.java
├── Interfaces/
│   └── Interfaz1.java
├── test/
│   ├── Clase1Test.java
│   └── Clase2Test.java
└── AppPrincipal.java
```

---

#### Sección 3 — Sistema [NombreSistema]

**3.1 Diagrama UML**
- Envolver la imagen en un `<div class="figure">` que incluye el título `<h3>` y el `<img>`.
- NUNCA separar el título del diagrama de la imagen — deben ir juntos en la misma página.

**3.2 Descripción de Clases**
- **Tabla:** `Clase | Responsabilidad`
- Una fila por cada clase e interfaz del proyecto.
- La descripción incluye atributos principales y comportamiento clave.

**3.3 Interfaces**
- **Tabla:** `Interfaz | Métodos`
- Listar cada interfaz y sus métodos con tipo de retorno.

**3.4 Métodos adicionales por clase** *(si existen métodos fuera de la interfaz)*
- **Tabla:** `Clase | Método | Descripción`

**3.5 Fórmulas / Lógica de negocio** *(si el proyecto tiene cálculos o reglas)*
- **Tabla:** `Clase | Fórmula o regla | Factor o detalle`

**3.6 Visualización de Pruebas**

- **Ejecución de [AppPrincipal]:** bloque de código oscuro con la salida real de consola al ejecutar el programa.
- **Pruebas Unitarias:** un bloque oscuro por cada clase de test con los resultados PASS/FAIL y el resumen final.
- **Archivo .txt** *(si el proyecto genera un archivo de texto)*: bloque con fondo claro mostrando el contenido del archivo generado.

---

## Reglas de salto de página (CRÍTICO)

Estas reglas CSS son obligatorias para evitar que imágenes, tablas y bloques de código
queden partidos entre dos páginas:

```css
/* Imágenes y diagramas: el título y la imagen nunca se separan */
.figure {
  page-break-inside: avoid;
  break-inside: avoid;
}

/* Tablas: nunca partir una tabla entre páginas */
table {
  page-break-inside: avoid;
  break-inside: avoid;
}

/* Bloques de código: nunca partir entre páginas */
pre {
  page-break-inside: avoid;
  break-inside: avoid;
}

/* Títulos h2 y h3: nunca dejar el título solo al final de una página */
h2, h3 {
  page-break-after: avoid;
  break-after: avoid;
}
```

El HTML del diagrama UML debe seguir siempre esta estructura:

```html
<div class="figure">
  <h3>Diagrama UML</h3>
  <div class="uml-img">
    <img src="[imagen.jpeg]" alt="Diagrama de Clases UML">
  </div>
</div>
```

---

## Comandos para generar PDF y DOCX

### Paso 1 — Crear el HTML temporal
Guardar como `_manual_temp.html` en la carpeta del proyecto.

### Paso 2 — Generar PDF con Chrome headless
```powershell
$htmlPath = "[ruta completa]\_manual_temp.html"
$pdfPath  = "[ruta completa]\Manual de Programacion - [Actividad].pdf"
$chrome   = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$fileUrl  = "file:///" + $htmlPath.Replace("\", "/").Replace(" ", "%20")

& $chrome --headless=new --disable-gpu --print-to-pdf="$pdfPath" --no-pdf-header-footer $fileUrl
Start-Sleep -Seconds 5
```

### Paso 3 — Generar DOCX con LibreOffice
```powershell
$soffice = "C:\Program Files\LibreOffice\program\soffice.exe"
$outDir  = "[ruta carpeta proyecto]"
& $soffice --headless --infilter="HTML" --convert-to "docx:MS Word 2007 XML" --outdir "$outDir" "$htmlPath"
Start-Sleep -Seconds 8
```

### Paso 4 — Eliminar el HTML temporal
```powershell
Remove-Item "$htmlPath"
```

---

## Estilos CSS completos a usar en el HTML

```css
body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; margin: 0; color: #000; }
.page { width: 21cm; min-height: 29.7cm; margin: 0 auto; padding: 2.5cm; box-sizing: border-box; }
.cover { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 29.7cm; text-align: center; }
h1 { font-size: 20pt; font-weight: bold; margin-bottom: 0.3cm; }
h2 { font-size: 14pt; font-weight: bold; margin-top: 1cm; page-break-after: avoid; break-after: avoid; }
h3 { font-size: 11pt; font-weight: bold; margin-top: 0.5cm; page-break-after: avoid; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 0.4cm 0; font-size: 10.5pt; page-break-inside: avoid; break-inside: avoid; }
th { background-color: #f2f2f2; font-weight: bold; text-align: center; border: 1px solid #ccc; padding: 6px 8px; }
td { border: 1px solid #ccc; padding: 5px 8px; vertical-align: top; }
pre { background: #1e1e1e; color: #d4d4d4; padding: 12px 16px; border-radius: 4px; font-size: 9pt; line-height: 1.5; white-space: pre-wrap; page-break-inside: avoid; break-inside: avoid; }
pre.light { background: #f5f5f5; color: #000; border: 1px solid #ddd; }
.figure { page-break-inside: avoid; break-inside: avoid; margin: 0.5cm 0; }
.uml-img { text-align: center; }
.uml-img img { max-width: 100%; }
.page-break { page-break-after: always; }
@media print { .page { margin: 0; padding: 2cm; } }
```
