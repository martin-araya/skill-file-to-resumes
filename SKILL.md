---
name: slides-from-docs
version: 1
description: >
  Convierte documentos (Markdown, PDF, Word, texto plano) en presentaciones
  HTML profesionales con animaciones, partículas y navegación fluida.
  Exporta automáticamente a PPTX. Hace preguntas de descubrimiento antes
  de generar para asegurar que el output sea preciso y relevante.
agents: [main_agent, general_purpose]
***

# Slides From Docs — Skill Maestro

Convierte cualquier documento en una presentación HTML de alto nivel.
El output es un archivo `.slides.html` autónomo (sin dependencias externas)
con animaciones spring, partículas canvas, modo oscuro/claro y navegación
por teclado, touch y clicks.

***

## Índice de Sub-archivos

Lee cada sub-archivo **en orden** según la fase en que te encuentres.
No cargues todos a la vez — carga solo el que necesitas en cada momento.

| Archivo | Fase | Cuándo leer |
|---|---|---|
| `01-input-detection.md` | Ingesta | Al recibir el documento del usuario |
| `02-discovery-questions.md` | Descubrimiento | Después de parsear el documento |
| `03-content-mapping.md` | Estructura | Después de las preguntas de descubrimiento |
| `04-visual-design.md` | Diseño | Al armar la paleta y tipografía |
| `05-slide-templates.md` | Generación | Al escribir el HTML de cada slide |
| `06-export-delivery.md` | Entrega | Al finalizar el HTML |
| `scripts/extract_content.py` | Utilidad | Cuando el usuario sube un PDF o DOCX |

***

## Filosofía del Skill

1. **El contenido manda.** Una presentación bella con datos superficiales
   es inútil. Extrae y preserva toda la información relevante del documento.

2. **Descubrir antes de construir.** Nunca generes slides sin antes hacer
   las preguntas de descubrimiento. Un deck para inversores no se construye
   igual que uno para una clase universitaria.

3. **Condensar con criterio.** Transforma el contenido del documento en
   lenguaje de presentación: párrafos → bullets, tablas → gráficos,
   números sueltos → stat callouts, procesos → timelines.

4. **Cero dependencias externas.** El `.slides.html` debe funcionar sin
   internet, sin CDN, sin servidor. Todo inline.

5. **Calidad de producción.** Cada slide debe sentirse diseñado a mano,
   no generado por plantilla. Varía layouts, evita repetición.

***

## Flujo Completo

```
ENTRADA
  └─ Usuario sube o pega: PDF / DOCX / MD / TXT / texto crudo
        │
        ▼
FASE 1 — DETECCIÓN & EXTRACCIÓN          [leer 01-input-detection.md]
  └─ Detectar formato → extraer texto estructurado → identificar jerarquía
        │
        ▼
FASE 2 — PREGUNTAS DE DESCUBRIMIENTO     [leer 02-discovery-questions.md]
  └─ 7 bloques de preguntas → máximo 1 ronda de preguntas al usuario
        │
        ▼
FASE 3 — MAPEO DE CONTENIDO              [leer 03-content-mapping.md]
  └─ Contenido + respuestas → estructura de slides → lista de templates
        │
        ▼
FASE 4 — DISEÑO VISUAL                   [leer 04-visual-design.md]
  └─ Industria + marca + estilo → paleta @theme → tipografía
        │
        ▼
FASE 5 — GENERACIÓN HTML                 [leer 05-slide-templates.md]
  └─ Template por template → archivo .slides.html completo
        │
        ▼
FASE 6 — EXPORT & ENTREGA                [leer 06-export-delivery.md]
  └─ Convertir a PPTX → share_files con ambos archivos
```

***

## Reglas Universales (aplican en todas las fases)

### Sobre el contenido

- **Nunca omitas datos clave** del documento original (cifras, fechas,
  nombres propios, conclusiones). Si no caben en un slide, crea más slides.
- **Nunca inventes datos.** Si el documento no menciona algo, no lo agregues.
- **Condensa, no trunca.** Un bullet debe capturar la idea completa
  en ≤20 palabras, no cortar una idea a la mitad.

### Sobre los slides

- **Máx. 5 bullets por slide.** Si hay más, divide en múltiples slides.
- **Máx. 3-4 cards por fila.** Nunca más — pierden legibilidad.
- **Un solo mensaje por slide.** Si un slide tiene dos ideas, son dos slides.
- **Siempre class="reveal"** en cada elemento de contenido.
- **Siempre .gradient-mesh** con .blob en cada slide.
- **data-slide="N"** secuencial sin saltos.

### Sobre el diseño

- **Nunca dos slides consecutivos con el mismo layout.**
- **Nunca hardcodear colores.** Usar siempre var(--color-*) o clases
  Tailwind que usen @theme tokens.
- **Tipografía mínima 12px** en cualquier elemento visible.
- **Contraste WCAG AA** obligatorio: 4.5:1 para texto normal, 3:1 para grande.

### Sobre la entrega

- **Siempre entregar ambos archivos:** `.slides.html` + `.pptx`
- **Siempre llamar share_files** como último paso.
- **Verificar QA** antes de entregar (ver 06-export-delivery.md).

***

## Detección Rápida de Modo

Al recibir el mensaje del usuario, identifica uno de estos modos:

| Modo | Descripción | Acción |
|---|---|---|
| **A — Documento adjunto** | El usuario sube un archivo (PDF/DOCX/MD) | Ejecutar `scripts/extract_content.py` |
| **B — Texto pegado** | El usuario pega contenido directamente | Parsear inline según 01-input-detection.md |
| **C — URL de documento** | El usuario da un link a un documento | Usar fetch_url + parsear como texto |
| **D — Descripción verbal** | El usuario describe lo que quiere sin subir nada | Hacer preguntas de descubrimiento primero |

***

## Anti-patrones Críticos (NUNCA hacer)

- ❌ Generar slides sin antes hacer las preguntas de descubrimiento
- ❌ Usar el mismo layout en 3 o más slides consecutivos
- ❌ Poner más de 5 bullets en un slide
- ❌ Usar `flex items-center` para grids de cards (usar CSS Grid)
- ❌ Hardcodear colores hex en el HTML (usar @theme tokens)
- ❌ Dejar placeholders como "LOGO_URL" o "SECTION TITLE" sin reemplazar
- ❌ Generar texto vago ("mejoró significativamente" → usar números exactos)
- ❌ Omitir el export PPTX
- ❌ Omitir la llamada a share_files
- ❌ Crear slides que necesiten scroll para verse completos

***

## Inicio Rápido para Claude

Cuando el usuario active este skill, sigue estos pasos exactos:

1. **Lee** `01-input-detection.md`
2. **Ejecuta** la extracción del documento
3. **Lee** `02-discovery-questions.md`
4. **Haz las preguntas** al usuario (una sola ronda)
5. **Lee** `03-content-mapping.md` y `04-visual-design.md`
6. **Lee** `05-slide-templates.md`
7. **Genera** el HTML completo
8. **Lee** `06-export-delivery.md` y exporta
9. **Llama** `share_files` con ambos archivos
