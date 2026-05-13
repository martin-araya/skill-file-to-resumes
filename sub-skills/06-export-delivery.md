# 06-export-delivery

Este archivo define todo el proceso de exportación y entrega de presentaciones generadas por el skill. Cubre tres etapas: generación del archivo HTML final, conversión automática a PPTX y entrega al usuario con instrucciones claras de uso.

***

## Contexto del sistema

El skill genera presentaciones como archivos HTML autocontenidos. Estos archivos son el formato primario: corren en cualquier navegador sin instalaciones, sin cuentas, sin conexión a internet.

A partir del HTML se genera adicionalmente un archivo PPTX para los casos en que el usuario necesita:

- compartir el deck con personas que no abren HTML,
- subirlo a Google Slides o PowerPoint para editar,
- enviarlo por email corporativo con formato reconocible,
- integrarlo en un flujo de documentos existente.

La entrega incluye siempre ambos archivos salvo que el usuario haya pedido solo uno.

***

## Estructura del output

### Archivos generados

| Archivo | Descripción |
|---|---|
| `{nombre}.slides.html` | Presentación completa, autocontenida, lista para correr en browser |
| `{nombre}.pptx` | Versión PowerPoint exportada desde el HTML |

### Convención de nombres

El nombre base del archivo debe ser:

- en minúsculas,
- sin espacios (usar guiones),
- descriptivo del contenido,
- sin versiones ni fechas salvo que el usuario las pida.

Ejemplos correctos:

- `estrategia-producto-2026.slides.html`
- `informe-mercado-latam.slides.html`
- `pitch-seed-round.slides.html`

Ejemplos incorrectos:

- `presentacion.html`
- `slides_v2_final_FINAL.html`
- `output.html`

***

## Fase 1 — Validación del HTML antes de exportar

Antes de generar el PPTX y antes de entregar al usuario, el motor debe correr el siguiente checklist sobre el HTML generado.

### Checklist obligatorio de QA

#### Estructura y navegación

- [ ] El tag `<meta name="slides-format" content="viewport">` está presente.
- [ ] Cada `<div class="slide">` tiene `data-slide="N"` secuencial sin huecos.
- [ ] La primera slide tiene clase `active`.
- [ ] El total de slides en `.deck` coincide con el número de dots generados en `#dots`.
- [ ] El counter `#counter` usa `N / total` donde total es correcto.
- [ ] El bloque `<nav class="nav-controls">` está presente y fuera del `.deck`.

#### Contenido

- [ ] No hay textos placeholder sin reemplazar: `LOGO_URL`, `IMAGE_URL`, `Título de la presentación`, `Subtítulo o contexto breve`, `Descripción breve del bloque`, `Contenido.`, etc.
- [ ] No hay slides vacías o con contenido repetido idéntico.
- [ ] Todos los `<img>` tienen `alt` no vacío.
- [ ] No hay `src=""` en ningún `<img>`.

#### Viewport y overflow

- [ ] Ninguna slide tiene `overflow-y: scroll` ni `overflow: auto` explícito.
- [ ] No hay `position: fixed` dentro de slides que interfiera con el layout.
- [ ] El `.content` de cada slide no tiene `height: 100vh` hardcodeado.

#### Animaciones y reveal

- [ ] Todo elemento visible clave lleva la clase `reveal`.
- [ ] El bloque `<script>` incluye la función `animateSlide()`.
- [ ] El `particle-canvas` está presente en la slide 1 y en la última slide.

#### Tokens y estilos

- [ ] El bloque `@theme` está dentro de `<style type="text/tailwindcss">`.
- [ ] El bloque `:root { --color-bg: ...; --color-text: ...; }` está en `<style>` regular y sus valores coinciden con los del `@theme`.
- [ ] No hay colores hexadecimales hardcodeados fuera del `@theme` salvo en gradientes específicos de blob.
- [ ] Las fuentes del CDN coinciden con las declaradas en `--font-display` y `--font-body`.

#### Accesibilidad básica

- [ ] Existe un `<h1>` en la slide de portada.
- [ ] Los headings de slides de contenido usan `<h2>` o `<h3>`, nunca `<h1>` duplicado.
- [ ] Los botones de navegación tienen texto o `aria-label`.

***

## Fase 2 — Conversión PPTX

### Script de conversión

La conversión usa el script preinstalado:

```bash
python ~/skills/slides/scripts/convert_to_pptx.py nombre.slides.html
```

Esto genera automáticamente `nombre.pptx` en el mismo directorio.

### Qué hace el script

1. Parsea el HTML y extrae cada slide como un bloque de contenido.
2. Para cada slide detecta:
   - título y subtítulo,
   - párrafos y bullets,
   - imágenes con sus URLs,
   - datos numéricos en callouts,
   - estructura básica de layout.
3. Genera un archivo PPTX usando `python-pptx` con:
   - fondo de color plano derivado del `--color-bg`,
   - tipografía web-safe más parecida a la elegida,
   - contenido posicionado según layout detectado,
   - colores de acento aproximados.

### Cuándo el script puede fallar

| Situación | Comportamiento |
|---|---|
| SVG inline complejo | Se omite y se deja un placeholder |
| Canvas particles | No se exporta, es solo HTML |
| Gradientes de blobs animados | No se exportan |
| Layouts muy custom con CSS Grid fraccional | Puede simplificarse |
| Fuentes de Google o Fontshare | Se sustituyen por equivalentes web-safe |

### Fallback manual

Si el script falla, seguir el proceso de degradación documentado en `~/skills/slides/pptx_generation.md`.

***

## Fase 3 — Composición del mensaje de entrega

El mensaje de entrega al usuario debe incluir exactamente:

1. Confirmación de qué se generó.
2. Guía rápida de navegación del HTML.
3. Nota sobre el PPTX.
4. Instrucciones de edición si el usuario quiere modificar.
5. Oferta de iteración.

### Plantilla de mensaje de entrega

```
Aquí están los dos archivos de tu presentación.

## Cómo usar el HTML

Abre el archivo `.slides.html` en cualquier navegador.

**Navegación:**
- Flecha derecha o barra espaciadora → siguiente slide
- Flecha izquierda → slide anterior
- Puntos del panel inferior → ir directamente a cualquier slide
- Swipe en móvil o tablet

El archivo no necesita conexión a internet. Puedes compartirlo, proyectarlo o enviarlo como adjunto.

## Sobre el PPTX

El archivo `.pptx` es una versión adaptada para PowerPoint o Google Slides. Las animaciones de fondo y partículas no se exportan porque son nativas de HTML, pero la estructura de contenido, los colores principales y la tipografía están preservados.

## Si quieres editar

Para cambiar texto, abre el `.slides.html` con cualquier editor de texto o de código. Cada slide es un bloque `<div class="slide slide-N">` fácil de identificar.

¿Hay algo que quieras ajustar?
```

***

## Fase 4 — Iteración post-entrega

### Tipos de cambio frecuentes

| Tipo de cambio | Acción del motor |
|---|---|
| Cambiar texto en una slide | Editar directamente el HTML, re-exportar PPTX, re-entregar |
| Cambiar paleta de colores | Modificar los tokens en `@theme` y el bloque `:root`, re-exportar |
| Añadir o eliminar una slide | Agregar o remover bloque `<div class="slide">`, actualizar `data-slide` secuenciales, re-entregar |
| Cambiar fuente | Actualizar CDN link, `--font-display` y/o `--font-body` en `@theme` |
| Cambiar estilo general | Puede requerir reescritura del `@theme` completo |
| Añadir un gráfico | Insertar HTML del chart en la slide correspondiente, re-exportar |

### Regla de re-exportación

**Siempre re-exportar el PPTX después de cualquier cambio al HTML.**

No entregar un HTML modificado sin PPTX actualizado, salvo que el usuario lo pida explícitamente.

### Regla de re-entrega

**Siempre llamar a `share_files` con ambos archivos después de cualquier modificación**, aunque solo haya cambiado una slide.

***

## Entrega de archivos

### Llamada a share_files

```python
share_files(files=[
    "/ruta/nombre.slides.html",
    "/ruta/nombre.pptx"
])
```

Siempre usar rutas absolutas desde el sandbox.

### Orden de entrega

Entregar primero el HTML, luego el PPTX. El HTML es el artefacto principal.

### Solo HTML (sin PPTX)

Si la conversión PPTX falla y no hay fallback disponible, entregar solo el HTML con nota clara:

```
El archivo HTML está listo y completo.
No fue posible generar el PPTX en esta sesión.
Puedes convertirlo manualmente en Google Slides usando Archivo → Importar presentación,
o abrirlo en el navegador para proyectarlo directamente.
```

***

## Guía de proyección

Incluir siempre en el mensaje de entrega si el contexto sugiere uso en presentación en vivo.

### Para proyectar desde el navegador

1. Abrir el archivo `.slides.html` en Chrome, Firefox o Safari.
2. Entrar en pantalla completa: `F11` en Windows/Linux, `Cmd+Shift+F` en Mac, o botón de pantalla completa del navegador.
3. Navegar con flechas del teclado o los botones de la barra inferior.

### Para proyectar desde PowerPoint o Keynote

1. Abrir el `.pptx` en PowerPoint.
2. Ir a Vista → Presentación con diapositivas.
3. Las animaciones básicas de texto estarán activas.

***

## Casos especiales

### Deck muy largo (más de 30 slides)

En decks largos, añadir al mensaje de entrega:

```
Este deck tiene N slides. Para navegar más rápido durante la presentación,
usa los puntos del panel inferior para saltar directamente a cualquier sección.
```

### Deck enviado por email

Si el usuario menciona que va a enviarlo por email, añadir al mensaje:

```
Si vas a enviar el HTML por email, algunos clientes de correo bloquean archivos .html
como adjunto por seguridad. En ese caso, comparte el .pptx o sube el HTML a Google Drive
y comparte el enlace de visualización.
```

### Deck para imprimir

Si el usuario pide versión imprimible:

```
Para imprimir el deck, abre el .pptx en PowerPoint y usa Archivo → Imprimir.
Desde el HTML también puedes imprimir con Cmd/Ctrl+P, aunque los fondos oscuros
consumen mucha tinta; considera activar "modo oscuro no imprimir" en tu navegador.
```

### Deck con datos sensibles

Si el deck contiene datos financieros, estratégicos o confidenciales, añadir al mensaje:

```
Este deck contiene información sensible. El archivo HTML es autocontenido:
no envía datos a ningún servidor y no requiere conexión.
Compártelo solo con las personas autorizadas.
```

***

## Compatibilidad del HTML

### Navegadores soportados

| Navegador | Soporte |
|---|---|
| Chrome 110+ | Completo |
| Firefox 115+ | Completo |
| Safari 16+ | Completo |
| Edge 110+ | Completo |
| Safari iOS 16+ | Completo (swipe funciona) |
| Chrome Android | Completo (swipe funciona) |
| IE / Edge Legacy | No soportado |

### Dependencias externas del HTML

El HTML generado tiene tres dependencias externas que requieren conexión para cargarse en el primer uso:

| Dependencia | URL | Propósito |
|---|---|---|
| Tailwind CSS v4 | `cdn.jsdelivr.net/npm/@tailwindcss/browser@4` | Utilidades CSS |
| Google Fonts | `fonts.googleapis.com` | Tipografías |
| Fontshare (si aplica) | `api.fontshare.com` | Tipografías alternativas |

Una vez que el navegador las carga por primera vez, quedan en caché y el archivo puede usarse sin conexión.

### Modo completamente offline

Si el usuario pide un deck que funcione sin ninguna conexión (por ejemplo, para avión o entorno sin internet), el motor debe:

1. Inlinear las fuentes como base64 dentro del `<style>`.
2. Usar el CDN de Tailwind con `integrity` hash fijo.
3. Documentarlo en el mensaje de entrega.

***

## Metadatos del HTML

Todo HTML generado debe incluir en el `<head>`:

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="slides-format" content="viewport">
<meta name="generator" content="Presentation Skill">
<title>Título descriptivo de la presentación</title>
```

El `<title>` debe coincidir con el nombre lógico del deck, no con el nombre del archivo.

***

## Checklist final antes de entregar

Antes de llamar a `share_files`, confirmar:

- [ ] El HTML pasa el checklist de QA de la Fase 1.
- [ ] El PPTX fue generado con el script de conversión.
- [ ] Los nombres de archivos siguen la convención `{nombre}.slides.html` y `{nombre}.pptx`.
- [ ] El mensaje de entrega incluye guía de navegación.
- [ ] Se ofrece iteración al final.
- [ ] `share_files` se llama con ambos archivos en orden: HTML primero, PPTX segundo.

***

## Errores comunes en entrega y cómo resolverlos

### Error: El usuario dice "no se ve bien en PowerPoint"

**Causa probable:** El PPTX tiene layouts simplificados porque algunos efectos HTML no son exportables.

**Respuesta recomendada:**

```
El HTML tiene animaciones y efectos visuales que PowerPoint no puede reproducir de forma nativa.
La versión PPTX es una adaptación funcional del contenido.
Si necesitas editar las slides en PowerPoint con más fidelidad visual,
puedo regenerar el PPTX con un estilo más compatible con Office.
¿Te gustaría eso?
```

### Error: El archivo HTML no carga las fuentes

**Causa probable:** No hay conexión o el CDN de fuentes no respondió.

**Respuesta recomendada:**

```
Las fuentes se cargan desde Google Fonts o Fontshare al abrir el archivo por primera vez.
Si no tienes conexión, el navegador usará fuentes del sistema como fallback.
El contenido y la estructura son completamente funcionales igual.
```

### Error: Las animaciones no funcionan

**Causa probable:** El navegador tiene modo de accesibilidad activo (`prefers-reduced-motion`).

**Respuesta recomendada:**

```
Es posible que tu navegador tenga activada la opción de "reducir movimiento"
en la configuración de accesibilidad del sistema operativo.
Con esa opción activa, las animaciones se desactivan intencionalmente.
El contenido es completamente usable sin ellas.
```

### Error: La navegación con teclado no funciona

**Causa probable:** El foco del teclado está en otro elemento de la página.

**Respuesta recomendada:**

```
Haz clic una vez en el área de la presentación para asegurarte de que tiene el foco,
y luego usa las flechas del teclado.
```

***

## Extensiones futuras del sistema de entrega

Estas capacidades están fuera del alcance actual pero son extensiones naturales del skill:

| Extensión | Descripción |
|---|---|
| Export a PDF | Usando Puppeteer o Chrome headless para capturar cada slide como página |
| Export a GIF / video | Captura animada de cada slide para uso en redes sociales |
| Versión embebible | Generar un `<iframe>` snippet para insertar el deck en una web |
| Notas del presentador | Añadir un panel de notas por slide visible en modo presentador |
| Modo offline completo | Inlinear todas las dependencias externas en el HTML |
| Zoom / Teams integration | Instrucciones de uso en pantalla compartida por plataforma |

Cuando cualquiera de estas extensiones se implemente, debe documentarse en este archivo como fase adicional.
