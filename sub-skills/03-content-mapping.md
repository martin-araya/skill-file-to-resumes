---
parent: slides-from-docs
file: 03-content-mapping.md
phase: 3 — Mapeo de Contenido
***

# Fase 3 — Mapeo de Contenido

Esta fase toma el **ACE** (de la Fase 1) y los **generation_params**
(de la Fase 2) y produce el **Plan de Slides**: una lista ordenada de
slides con su template asignado, su contenido exacto y su posición en el deck.

El Plan de Slides es el blueprint que usarás en la Fase 5 para generar
el HTML. No escribas HTML hasta tener el Plan completo.

***

## 1. Algoritmo Principal de Mapeo

Ejecuta estos pasos en orden:

### Paso 1 — Calcular el número objetivo de slides

```
SI generation_params.slide_count == "short"  → target = 8
SI generation_params.slide_count == "medium" → target = 15
SI generation_params.slide_count == "long"   → target = 28
SI generation_params.slide_count == "auto"   →
    base = cantidad de secciones nivel-1 en el ACE
    + 1 por cada StatBlock con >2 números relacionados
    + 1 por cada tabla con >3 filas
    + slides_obligatorios de generation_params.required_slides
    + 2 (portada + cierre)
    target = base (sin límite fijo)

Ajustes por duración:
    duration_minutes < 10  → target = min(target, 8)
    duration_minutes < 20  → target = min(target, 15)
    duration_minutes > 45  → target puede exceder el "long" máximo
```

### Paso 2 — Construir la estructura base del deck

Todo deck sigue esta estructura base. Las secciones intermedias se
expanden con el contenido del ACE.

```
[1] PORTADA              ← siempre primero
[2] AGENDA               ← solo si required_slides incluye "agenda"
[...] SECCIONES          ← contenido del documento
[N-1] CTA / CIERRE       ← siempre (con o sin CTA explícito)
[N] CONTACTO             ← solo si required_slides incluye "contacto"
[Backup...] BACKUP       ← solo si backup_slides = true
```

### Paso 3 — Mapear cada sección del ACE a slides

Para cada `Section` en el ACE (en orden), aplica la **Tabla de Decisión
de Templates** (sección 2 de este archivo) y asigna uno o más slides.

### Paso 4 — Verificar balance de layouts

Nunca dos slides consecutivos con el mismo template.
Si hay repetición, aplicar las reglas de variación (sección 4).

### Paso 5 — Verificar conteo final

```
SI slides_generados > target * 1.3:
    → Consolidar: combinar secciones cortas en un solo slide
SI slides_generados < target * 0.7:
    → Expandir: dividir secciones largas, agregar slides de transición
```

***

## 2. Tabla de Decisión de Templates

Para cada `ContentBlock` en el ACE, usa esta tabla para asignar template.
Los templates referenciados están definidos en `05-slide-templates.md`.

### 2.1 Mapeo directo por tipo de ContentBlock

| Tipo de bloque en ACE | Condición adicional | Template asignado |
|---|---|---|
| Título del deck | — | `T01-portada` |
| Section nivel-1 | Es un divisor entre grandes secciones | `T02-divisor-seccion` |
| Paragraph único | < 60 palabras, es una idea central | `T03-cita-destacada` |
| Paragraph único | ≥ 60 palabras | `T04-bullets` (condensar en 3-5 bullets) |
| Bullets (3-5 items) | — | `T04-bullets` |
| Bullets (6-10 items) | — | Dividir en dos slides `T04-bullets` |
| Bullets (>10 items) | — | Dividir en múltiples slides o usar `T08-grid-6` |
| Numbered list (3-5 items) | Items son pasos o fases | `T12-timeline` |
| Numbered list (3-5 items) | Items son opciones/características | `T05-cards-2col` o `T06-cards-3col` |
| StatBlock (1 número grande) | — | `T10-stat-callout` integrado en slide adyacente |
| StatBlock (2-3 números) | — | `T10-stat-callout` (slide propio) |
| StatBlock (4+ números) | — | `T09-grid-metricas` |
| Table (2 cols, ≤6 filas) | Es comparación binaria | `T05-cards-2col` |
| Table (3 cols, ≤6 filas) | Es comparación triple | `T06-cards-3col` |
| Table (4+ cols, cualquier filas) | — | `T14-tabla-html` |
| Table (2-4 cols, >6 filas) | Datos ordenables/analizables | `T15-grafico-barras` o `T14-tabla-html` |
| Code block | Cualquier lenguaje | `T16-slide-codigo` |
| Quote/blockquote | — | `T03-cita-destacada` |
| Image_ref | Tiene caption descriptivo | `T17-split-imagen-texto` |
| Timeline (4-5 items) | — | `T12-timeline` |
| Timeline (>5 items) | — | Dividir en dos `T12-timeline` |
| Sección "Equipo" / "Autores" | Personas con roles | `T06-cards-3col` o `T05-cards-2col` |
| Sección "Agenda" | Lista de puntos | `T11-agenda` |
| Sección "Conclusión" / "Resumen" | — | `T04-bullets` + `T13-cta-cierre` |
| CTA explícito | — | `T13-cta-cierre` |

### 2.2 Reglas de condensación de párrafos a bullets

Cuando un `paragraph` debe convertirse en bullets (`T04-bullets`),
sigue estas reglas de condensación:

```
REGLA 1 — Una bullet por idea principal
  Identifica las ideas principales del párrafo (usualmente separadas
  por punto seguido o conectores: "además", "por otro lado", "también").
  Cada idea = una bullet.

REGLA 2 — Máximo 20 palabras por bullet
  Si la idea tiene >20 palabras, extrae el núcleo semántico.
  Preservar: sujeto + verbo + objeto + cifra clave
  Eliminar: adverbios innecesarios, repeticiones, calificativos vagos

REGLA 3 — Los números van primero o al final, nunca en medio
  MAL:  "La empresa, que fue fundada en 2019, tiene 450 empleados"
  BIEN: "450 empleados desde su fundación en 2019"
  BIEN: "Fundada en 2019 — hoy con 450 empleados"

REGLA 4 — Preservar cifras exactas siempre
  Si el párrafo dice "$4.2 millones", el bullet dice "$4.2M".
  Nunca redondear ni aproximar números del documento original.

REGLA 5 — Verbos en presente o infinitivo
  Unifica el tiempo verbal de todos los bullets del mismo slide.
  Preferir presente o infinitivo para consistencia visual.
```

### 2.3 Reglas de conversión de tablas

```
TABLA → CARDS (T05 o T06):
  Usar cuando la tabla compara entidades (filas = entidades, cols = atributos)
  y tiene ≤ 4 columnas y ≤ 6 filas.
  Cada fila de la tabla = una card.
  Headers de columna = labels dentro de la card.

TABLA → GRÁFICO DE BARRAS (T15):
  Usar cuando hay una columna numérica principal y una columna de categorías.
  La columna numérica = altura de las barras.
  La columna de categorías = etiquetas del eje X.

TABLA → TABLA HTML (T14):
  Usar cuando hay >4 columnas, o cuando la tabla tiene estructura
  de datos que no es comparación de entidades (ej: horarios, matrices).
  Limitar a 8 filas visibles — si hay más, indicar "Ver documento completo".

TABLA → HEATMAP:
  Usar cuando la tabla es una matriz cuadrada o rectangular donde
  los valores representan intensidad (rankings, correlaciones, scores).
```

***

## 3. Slides Especiales por Propósito

Según `generation_params.purpose`, agregar slides que no están en el documento:

### 3.1 Si `purpose == "pitch"`

Verificar que el deck incluya estos slides. Si no están en el ACE,
crearlos con contenido inferido o dejando placeholders claros:

```
□ Slide "El Problema" — qué dolor resuelve
  → Si el ACE tiene una sección de "contexto" o "problema", mapearla aquí
  → Si no existe, crear slide con estructura: [PROBLEMA] + [IMPACTO CUANTIFICADO]

□ Slide "La Solución" — qué ofrece el producto/servicio
  → Buscar en ACE sección de "propuesta de valor", "producto", "solución"

□ Slide "Tracción / Resultados" — evidencia de que funciona
  → Mapear StatBlocks al formato T09-grid-metricas o T10-stat-callout

□ Slide "Equipo" — quiénes son (si hay info en el ACE)
  → Solo si el ACE menciona personas con roles

□ Slide "Próximos pasos / CTA"
  → Siempre al final, con el CTA de generation_params.cta
```

### 3.2 Si `purpose == "reporte"`

```
□ Slide "Resumen Ejecutivo" — los 3-5 puntos más importantes
  → Siempre como segundo slide (después de portada)
  → Extraer los StatBlocks más relevantes + conclusión principal

□ Slide de cada KPI / métrica principal
  → Usar T09-grid-metricas o T10-stat-callout

□ Slide "Conclusiones y Recomendaciones"
  → Siempre antes del cierre
```

### 3.3 Si `purpose == "clase"` o `purpose == "charla"`

```
□ Slide de agenda obligatorio (aunque no esté en required_slides)

□ Si audience_level == "novato":
  → Agregar slide de "Conceptos clave" antes de cada sección técnica
  → Formato T04-bullets con definiciones simples

□ Slide de "Puntos clave" al final de cada sección grande
  → Resumir la sección en 3-4 bullets

□ Slide final de "¿Preguntas?" en lugar de CTA comercial
```

### 3.4 Si `purpose == "deck_autonomo"` (se envía sin presentador)

```
□ Cada slide debe tener más texto del usual (+30% del límite normal)
□ Agregar contexto en headings (no solo "Resultados" sino "Resultados Q3 2025")
□ Usar T17-split-imagen-texto más que T10-stat-callout solo
  (los números siempre necesitan contexto si no hay presentador)
□ Agregar slide de "Cómo leer este deck" si es técnico o denso
```

***

## 4. Reglas de Balance de Layouts

Nunca dos slides consecutivos con el mismo template.
Usa esta matriz de variación forzada:

### 4.1 Secuencias prohibidas

```
❌ T04-bullets → T04-bullets (mismo template)
❌ T06-cards-3col → T06-cards-3col
❌ T10-stat-callout → T10-stat-callout
❌ T05-cards-2col → T05-cards-2col
❌ T12-timeline → T12-timeline
```

### 4.2 Cómo romper la repetición

Si dos secciones consecutivas del ACE mapean al mismo template,
aplica una de estas estrategias:

| Template repetido | Estrategia de variación |
|---|---|
| Dos `T04-bullets` seguidos | Convertir el segundo en `T05-cards-2col` con los bullets como cards |
| Dos `T06-cards-3col` seguidos | Insertar `T02-divisor-seccion` entre ellos |
| Dos `T10-stat-callout` seguidos | Combinar en un `T09-grid-metricas` |
| Dos `T05-cards-2col` seguidos | Convertir el segundo en `T17-split-imagen-texto` |
| Dos `T12-timeline` seguidos | Fusionar en un único timeline más largo (si ≤ 6 items) |

### 4.3 Ritmo recomendado de layouts

Un deck bien construido alterna entre estos tres registros:

```
REGISTRO VISUAL (impacto, poco texto)
  → T01-portada, T02-divisor, T03-cita, T10-stat-callout, T13-cta

REGISTRO MIXTO (balance texto/visual)
  → T05-cards-2col, T06-cards-3col, T09-grid-metricas, T17-split

REGISTRO INFORMATIVO (más texto, más datos)
  → T04-bullets, T11-agenda, T12-timeline, T14-tabla, T15-grafico
```

Secuencia ideal para un deck de 15 slides:

```
Visual → Mixto → Informativo → Visual → Mixto → Informativo → ...
```

***

## 5. Reglas de Priorización de Contenido

### 5.1 Qué va primero dentro de un slide

```
1. El dato más sorprendente o impactante
2. La conclusión (no el proceso que lleva a ella)
3. El nombre/concepto principal
4. El contexto o explicación
5. Los detalles de soporte
```

Este orden aplica tanto al ordenar bullets dentro de un slide
como al decidir qué secciones van antes en el deck.

### 5.2 Qué elevar a stat callout

Elevar a `T10-stat-callout` (número gigante) cualquier cifra que cumpla:

```
□ Es un número con unidad ($, %, x, M, B, K)
   Y
□ Es el argumento más fuerte de esa sección del documento
   O
□ Es la cifra que más sorprendería a la audiencia
   O
□ Es el número que el usuario marcó como "prioritario" en B3
```

### 5.3 Qué eliminar o comprimir

```
ELIMINAR:
  - Texto de introducción genérico ("En el presente informe...")
  - Agradecimientos y saludos protocolares
  - Notas al pie y referencias bibliográficas
  - Repeticiones de información ya presentada
  - Texto marcado en generation_params.exclude_sections

COMPRIMIR A UNA LÍNEA:
  - Definiciones de términos conocidos por la audiencia
    (según audience_level: experto → comprimir más)
  - Contexto histórico que no es el foco del deck
  - Metodología técnica (a menos que purpose == "clase")

MOVER A BACKUP:
  - Detalle técnico de soporte
  - Tablas de datos completas (en el deck va el resumen)
  - Cálculos y fórmulas
  - Todo lo que en B2 el usuario quiso excluir pero que
    podría ser útil en Q&A
```

***

## 6. Estructura del Plan de Slides

### 6.1 Formato del Plan

Construye el Plan de Slides como una lista ordenada con esta estructura
para cada slide:

```
SLIDE N
  template:     [código de template, ej: T06-cards-3col]
  heading:      [título del slide, ≤8 palabras]
  subheading:   [subtítulo opcional, ≤12 palabras]
  content_type: [bullets | cards | stat | tabla | timeline | código | imagen | cita]
  content:      [el contenido exacto — bullets, cifras, texto de cards, etc.]
  notes:        [nota para el generador: ej. "usar accent-1 en el número", "animación lenta"]
  speaker_note: [si speaker_notes=true: texto guía para el presentador]
```

### 6.2 Ejemplo de Plan de Slides

```
=== PLAN DE SLIDES — "Reporte Anual 2025" ===
Total: 14 slides | Preset: Midnight Cathedral | Modo: Oscuro

SLIDE 1
  template:     T01-portada
  heading:      Reporte Anual 2025
  subheading:   Resultados y perspectivas del grupo
  content_type: portada
  content:      logo=null, emoji=📊, tagline="Crecimiento sostenido en mercados clave"
  notes:        Usar gradient text en el heading principal

SLIDE 2
  template:     T11-agenda (resumen ejecutivo)
  heading:      Lo más importante
  content_type: bullets
  content:
    - Ingresos $4.2B — crecimiento 23% YoY
    - Expansión a 3 nuevos mercados internacionales
    - Margen operativo alcanzó 31%, récord histórico
    - Lanzamiento de línea premium con 94% de satisfacción
    - Proyección 2026: $5.1B (+21%)
  notes:        Este es el resumen ejecutivo — destacar cifras en accent-1

SLIDE 3
  template:     T02-divisor-seccion
  heading:      Resultados Financieros
  subheading:   Ejercicio fiscal 2025
  content_type: divisor
  content:      null
  notes:        blob grande en accent-1, partículas activadas

SLIDE 4
  template:     T09-grid-metricas
  heading:      KPIs del ejercicio
  content_type: stat
  content:
    - valor="$4.2B"  label="Ingresos totales"   delta="+23% YoY"
    - valor="31%"    label="Margen operativo"    delta="+4pp vs 2024"
    - valor="$1.3B"  label="EBITDA"              delta="+31% YoY"
    - valor="94%"    label="Satisfacción cliente" delta="+6pp"
  notes:        Contadores animados en cada valor

SLIDE 5
  template:     T15-grafico-barras
  heading:      Ingresos por segmento
  content_type: grafico
  content:
    barras:
      - label="Segmento A" valor=2.1 color=accent-1 delta="+31%"
      - label="Segmento B" valor=1.4 color=accent-2 delta="+18%"
      - label="Segmento C" valor=0.7 color=accent-3 delta="+8%"
    unidad: "$B"
  notes:        Barras con animación de crecimiento al activar slide

SLIDE 6
  template:     T05-cards-2col
  heading:      Mercados con mayor crecimiento
  content_type: cards
  content:
    - titulo="América Latina"  body="Crecimiento 47% — mercado más dinámico del grupo. Expansión en Brasil, Chile y Colombia."
    - titulo="Asia Pacífico"   body="Ingreso a 2 mercados nuevos: Singapur y Vietnam. ARR proyectado $320M para 2026."
  notes:        Usar border-l-4 accent-1 en primera card, accent-2 en segunda

[... continúa hasta slide 14 ...]
```

***

## 7. Checklist de Validación del Plan

Antes de pasar a la Fase 4, verifica:

- [ ] **Cada slide tiene un solo mensaje central**
  (si tiene dos, dividir en dos slides)

- [ ] **No hay dos slides consecutivos con el mismo template**

- [ ] **Las cifras del documento original están preservadas exactamente**
  (no redondeadas, no parafraseadas)

- [ ] **El conteo de slides está dentro del target ±30%**

- [ ] **Los slides obligatorios de `required_slides` están incluidos**

- [ ] **El contenido de `exclude_sections` no aparece en ningún slide**

- [ ] **Los datos de `priority_data` están en slides con templates de alto impacto**
  (T09, T10, T03, T17 — no enterrados en bullets)

- [ ] **El ritmo de layouts alterna entre registros**
  (Visual → Mixto → Informativo)

- [ ] **El slide de cierre tiene el CTA de `generation_params.cta`**
  (si cta != null)

- [ ] **Si `backup_slides=true`, hay una sección de Backup al final**
  con al menos 3 slides de detalle técnico

***

## 8. Output de esta Fase

Al finalizar la Fase 3, debes tener:

- ✅ **Plan de Slides completo** (lista ordenada de N slides con template y contenido)
- ✅ **Templates requeridos identificados** (lista de códigos T01-T17 usados)
- ✅ **Contenido condensado y listo** (bullets, cifras, textos de cards — ya escritos)
- ✅ **Slides de backup identificados** (si aplica)

Pasa el Plan de Slides a la **Fase 4 — Diseño Visual** para definir
la paleta y tipografía, y luego a la **Fase 5** para generar el HTML.
