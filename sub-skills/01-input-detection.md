---
parent: slides-from-docs
file: 01-input-detection.md
phase: 1 — Detección & Extracción
***

# Fase 1 — Detección & Extracción de Contenido

Este archivo define cómo detectar el formato del documento entrante,
extraer su contenido y construir el **Árbol de Contenido Estructurado (ACE)**
que alimentará todas las fases siguientes.

***

## 1. Detección de Formato

### 1.1 Orden de detección

Evalúa en este orden exacto:

```
1. ¿El usuario subió un archivo?
   ├─ Extensión .pdf         → Modo PDF
   ├─ Extensión .docx/.doc   → Modo DOCX
   ├─ Extensión .md/.mdx     → Modo Markdown
   ├─ Extensión .txt         → Modo Texto Plano
   └─ Otra extensión         → Intentar como texto plano; avisar al usuario

2. ¿El usuario pegó texto?
   ├─ Contiene "# " o "## "  → Modo Markdown
   ├─ Contiene \t o columnas → Modo Tabla/CSV (tratar como texto estructurado)
   └─ Sin marcadores         → Modo Texto Plano

3. ¿El usuario dio una URL?
   └─ Usar fetch_url → detectar por contenido recibido (pasos 1-2)
```

### 1.2 Extracción según formato

#### PDF

```
→ Ejecutar: python ~/skill-slides-from-docs/scripts/extract_content.py <archivo.pdf>
→ El script retorna JSON con secciones, párrafos y posibles headings
→ Si el script falla: usar fetch_url o pedir al usuario que copie el texto
```

#### DOCX

```
→ Ejecutar: python ~/skill-slides-from-docs/scripts/extract_content.py <archivo.docx>
→ El script extrae párrafos con sus estilos (Heading 1, Heading 2, Normal, etc.)
→ Los estilos Heading son los divisores naturales de secciones
```

#### Markdown

```
→ Parsear inline sin script externo
→ Seguir las reglas de la sección 2.1 de este archivo
```

#### Texto Plano

```
→ Parsear inline sin script externo
→ Seguir las reglas de la sección 2.4 de este archivo
```

***

## 2. Reglas de Parseo por Formato

### 2.1 Markdown

El Markdown tiene jerarquía natural — respétala.

#### Mapeo heading → nivel ACE

| Markdown | Nivel ACE | Uso típico en slides |
|---|---|---|
| `# Título` | Nivel 0 — Título del deck | Slide de portada |
| `## Sección` | Nivel 1 — Sección principal | Slide divisor de sección |
| `### Subsección` | Nivel 2 — Contenido principal | Heading del slide |
| `#### Sub-subsección` | Nivel 3 — Contenido secundario | Subheading o label |
| Párrafo normal | Contenido | Bullet, párrafo o descripción |
| `- item` / `* item` | Lista | Bullets del slide |
| `1. item` | Lista ordenada | Steps / proceso numerado |
| `| col |` | Tabla | Tabla, gráfico o cards comparativas |
| ` ```code``` ` | Bloque de código | Slide técnico con código |
| `> blockquote` | Cita | Pull quote o insight destacado |
| `**texto**` | Énfasis fuerte | Stat callout o highlight |
| `---` o `***` | Separador horizontal | Divisor de sección |

#### Ejemplo de parseo

```markdown
# Reporte Anual 2025
## Resultados Financieros
### Ingresos
Los ingresos totales alcanzaron **$4.2B**, un crecimiento del 23% YoY.
- Segmento A: $2.1B (+31%)
- Segmento B: $1.4B (+18%)
- Segmento C: $0.7B (+8%)
```

Se convierte en ACE:

```
[DECK TITLE] "Reporte Anual 2025"
  [SECTION] "Resultados Financieros"
    [SLIDE] "Ingresos"
      [STAT] "$4.2B" — ingresos totales, +23% YoY
      [BULLETS]
        - Segmento A: $2.1B (+31%)
        - Segmento B: $1.4B (+18%)
        - Segmento C: $0.7B (+8%)
```

#### Reglas especiales Markdown

- Si `**texto**` contiene un número con unidad (€, $, %, x, B, M, K),
  trátalo como **STAT CALLOUT** — va a un slide de números grandes.
- Si hay una tabla con 2-4 columnas y ≤8 filas, conviértela en **CARDS COMPARATIVAS**.
- Si hay una tabla con >4 columnas o >8 filas, conviértela en **TABLA HTML** dentro del slide.
- Si hay un bloque de código, créale un **SLIDE TÉCNICO** propio con fondo oscuro
  independientemente del tema general.
- Si hay ≥4 items en una lista ordenada, considera un **TIMELINE** si los items
  tienen formato de fecha o paso ("Paso 1...", "Q1 2024...", "Primero...").

***

### 2.2 PDF

Los PDFs no tienen estructura semántica nativa. El script `extract_content.py`
usa heurísticas para reconstruirla.

#### Heurísticas de detección de headings en PDF

| Señal | Peso | Interpretación |
|---|---|---|
| Tamaño de fuente > 16pt | Alto | Probable H1 o H2 |
| Tamaño de fuente 13-16pt | Medio | Probable H3 |
| Texto en negrita, línea sola | Alto | Probable heading |
| Texto en MAYÚSCULAS, línea sola | Medio | Probable heading o label |
| Línea corta (< 6 palabras) seguida de párrafo largo | Medio | Probable heading |
| Primera línea de página | Bajo | Posible heading de sección |
| Número de página, header/footer | Ignorar | Eliminar del ACE |

#### Manejo de elementos visuales en PDF

- **Imágenes**: Si el PDF contiene imágenes, registrar su posición relativa
  (antes/después de qué párrafo) pero **no extraerlas** — usar emoji o
  descripción como placeholder en el slide correspondiente.
- **Tablas**: El script intentará detectar tablas por alineación de columnas.
  Si falla, el texto de la tabla llegará como párrafos — recomponer manualmente
  usando el contexto semántico.
- **Gráficos**: Ignorar el visual, preservar los datos textuales adyacentes
  (títulos, leyendas, valores en etiquetas si son texto).

#### Estructura de output del script para PDF

```json
{
  "format": "pdf",
  "title": "Texto del heading más prominente o nombre del archivo",
  "pages": 24,
  "sections": [
    {
      "level": 1,
      "heading": "Introducción",
      "page_start": 1,
      "content": [
        { "type": "paragraph", "text": "..." },
        { "type": "list", "items": ["...", "..."] },
        { "type": "table", "headers": [...], "rows": [[...], [...]] }
      ]
    }
  ],
  "stats_detected": ["$4.2B", "23%", "Q3 2025"],
  "metadata": { "author": "...", "date": "...", "subject": "..." }
}
```

***

### 2.3 DOCX (Word)

Word usa **estilos de párrafo** como estructura semántica nativa.
Es el formato más limpio para extraer jerarquía.

#### Mapeo de estilos Word → nivel ACE

| Estilo Word | Nivel ACE |
|---|---|
| `Heading 1` / `Title` | Nivel 0 — Título del deck o sección principal |
| `Heading 2` | Nivel 1 — Sección |
| `Heading 3` | Nivel 2 — Slide heading |
| `Heading 4` / `Heading 5` | Nivel 3 — Subheading |
| `Normal` / `Body Text` | Contenido de slide |
| `List Bullet` / `List Bullet 2` | Bullets |
| `List Number` | Lista ordenada / steps |
| `Quote` / `Intense Quote` | Pull quote |
| `Caption` | Etiqueta de imagen o tabla |
| `Table Grid` / cualquier tabla | Tabla → Cards o tabla HTML |

#### Reglas especiales DOCX

- El **primer `Heading 1`** o el estilo `Title` es siempre el título del deck.
- Si hay múltiples `Heading 1`, cada uno es un **divisor de sección**.
- Texto con `runs` en negrita dentro de un párrafo Normal → candidate a STAT
  si contiene números.
- Tablas de Word → aplicar misma lógica que tablas Markdown (≤4 cols → cards,
  >4 cols → tabla HTML).
- Imágenes inline → placeholder `[IMAGEN: caption]` en el ACE.

#### Estructura de output del script para DOCX

```json
{
  "format": "docx",
  "title": "Texto del primer Heading 1 o Title",
  "sections": [
    {
      "level": 1,
      "heading": "Capítulo 1: Contexto",
      "content": [
        { "type": "paragraph", "text": "...", "bold_fragments": ["$2.3M", "Q4"] },
        { "type": "list", "ordered": false, "items": ["...", "..."] },
        { "type": "table", "headers": [...], "rows": [[...]] },
        { "type": "image_placeholder", "caption": "Figura 1: ..." }
      ]
    }
  ],
  "stats_detected": ["$2.3M", "47%"],
  "metadata": { "author": "...", "created": "...", "modified": "..." }
}
```

***

### 2.4 Texto Plano

Sin marcadores de formato. Usar heurísticas de segmentación.

#### Algoritmo de segmentación

```
1. SEPARADORES EXPLÍCITOS
   ├─ "---", "===", "***" en línea sola → divisor de sección
   ├─ Línea en blanco doble (dos \n\n) → divisor de sección
   └─ Línea en blanco simple (\n\n) → divisor de párrafo dentro de sección

2. DETECCIÓN DE HEADINGS
   ├─ Línea corta (≤ 8 palabras) + MAYÚSCULAS → Heading nivel 1
   ├─ Línea corta + seguida inmediatamente de párrafo largo → Heading
   ├─ Línea que termina en ":" y tiene ≤ 6 palabras → Heading
   └─ Primera línea del documento → Título del deck (si es ≤ 10 palabras)

3. DETECCIÓN DE LISTAS
   ├─ Líneas que empiezan con "- ", "* ", "• " → Lista de bullets
   ├─ Líneas que empiezan con "1.", "2.", "a)", "b)" → Lista ordenada
   └─ 3+ líneas consecutivas con estructura similar → Posible lista

4. DETECCIÓN DE STATS
   └─ Patrones regex: \$[\d,.]+[BMK]? | \d+[.,]?\d*% | \d+x | [\d,.]+[BMK]
      → Candidatos a STAT CALLOUT

5. DETECCIÓN DE TABLAS SIMPLES
   └─ 3+ líneas con separación consistente por tabulación o múltiples espacios
      → Intentar reconstruir como tabla
```

#### Ejemplo de parseo de texto plano

```
RESULTADOS Q3 2025

La empresa cerró el trimestre con ingresos de $1.2B, superando
las expectativas del mercado en un 15%.

Principales logros:
- Expansión a 3 nuevos mercados
- Lanzamiento de producto estrella con 94% de satisfacción
- Reducción de costos operativos en 8%

Próximos pasos
El equipo se enfocará en consolidar la base de clientes existente
antes de la expansión planificada para Q1 2026.
```

Se convierte en ACE:

```
[DECK TITLE] "RESULTADOS Q3 2025"
  [STAT CALLOUT] "$1.2B" ingresos, +15% vs expectativas
  [SLIDE] "Principales logros"
    [BULLETS]
      - Expansión a 3 nuevos mercados
      - Lanzamiento producto estrella: 94% satisfacción
      - Reducción costos operativos: -8%
  [SLIDE] "Próximos pasos"
    [PARAGRAPH] Consolidar base de clientes → expansión Q1 2026
```

***

## 3. Construcción del Árbol de Contenido Estructurado (ACE)

El ACE es la representación interna del documento después de parsear.
Es el insumo de la Fase 3 (Mapeo de Contenido).

### 3.1 Estructura del ACE

```
ACE {
  deck_title: string
  source_format: "pdf" | "docx" | "md" | "txt"
  detected_language: "es" | "en" | "pt" | ...
  detected_industry: string | null        ← ver sección 3.3
  metadata: {
    author: string | null
    date: string | null
    subject: string | null
  }
  sections: [
    Section {
      level: 0 | 1 | 2 | 3
      heading: string
      content_blocks: [ContentBlock]
    }
  ]
  stats: [StatBlock]                      ← todos los números clave detectados
  global_notes: string[]                  ← fragmentos que no encajan en secciones
}

ContentBlock = uno de:
  { type: "paragraph",  text: string }
  { type: "bullets",    items: string[] }
  { type: "numbered",   items: string[] }
  { type: "table",      headers: string[], rows: string[][] }
  { type: "code",       language: string, code: string }
  { type: "quote",      text: string }
  { type: "stat",       value: string, context: string }
  { type: "image_ref",  caption: string }
  { type: "timeline",   items: { date: string, event: string }[] }

StatBlock = {
  value: string       ← e.g. "$4.2B", "23%", "3x"
  context: string     ← e.g. "ingresos totales", "crecimiento YoY"
  section: string     ← heading de la sección donde apareció
}
```

### 3.2 Reglas de limpieza del ACE

Aplica estas transformaciones al construir el ACE:

| Problema | Transformación |
|---|---|
| Párrafo > 80 palabras | Dividir en múltiples párrafos por idea |
| Lista > 7 items | Dividir en dos grupos temáticos |
| Sección sin heading | Asignar heading inferido del primer párrafo |
| Número aislado en párrafo | Extraer como StatBlock + dejar contexto en párrafo |
| Texto repetido (headers, footers PDF) | Eliminar |
| Notas al pie, referencias bibliográficas | Mover a global_notes |
| Texto de tabla de contenidos / índice | Eliminar — reconstruir desde estructura |

### 3.3 Detección automática de industria

Analiza el texto completo del documento buscando señales de industria.
Esto influirá en la paleta visual (Fase 4) sin necesidad de preguntarlo
explícitamente en todos los casos.

| Señales en el texto | Industria detectada |
|---|---|
| EBITDA, P&L, revenue, ARR, MRR, CAC, LTV, VC, Series A/B | `fintech_startup` |
| balance, activos, pasivos, utilidad neta, CAPEX, OPEX | `finanzas_corporativas` |
| paciente, diagnóstico, ensayo clínico, FDA, EMA, mg/kg | `healthcare` |
| ESG, carbono, emisiones, sostenibilidad, ODS, net zero | `sostenibilidad` |
| usuario, producto, sprint, roadmap, feature, KPI, DAU/MAU | `tech_producto` |
| ley, artículo, contrato, tribunal, regulación, compliance | `legal` |
| alumno, curso, módulo, aprendizaje, competencia, evaluación | `educacion` |
| estrategia, mercado, competencia, segmento, propuesta de valor | `estrategia` |
| campaña, audiencia, conversión, CTR, ROAS, funnel, brand | `marketing` |
| obra, presupuesto, contrato, licitación, BIM, m², partida | `construccion` |

Si no se detecta ninguna industria → `general`

***

## 4. Señales de Alerta al Parsear

Antes de pasar a la Fase 2, verifica estas condiciones y actúa en consecuencia:

| Condición | Acción |
|---|---|
| El documento tiene < 200 palabras | Avisar al usuario que el contenido es muy breve; preguntar si quiere agregar más |
| El documento tiene > 15,000 palabras | Avisar que se generará un deck largo (20+ slides); preguntar si prefiere un resumen |
| No se detectó ningún heading | Avisar que el documento no tiene estructura clara; pedir confirmación de la estructura esperada |
| > 60% del contenido son tablas | Sugerir al usuario que el deck será muy visual (gráficos y cards comparativas) |
| Idioma detectado ≠ idioma de la interfaz | Preguntar en qué idioma debe estar la presentación |
| Se detectaron >10 StatBlocks | Informar que hay muchos datos numéricos — preguntar si prefiere slides de stats o gráficos |
| El documento parece ser ya una presentación (títulos muy cortos, sin prosa) | Preguntar si quiere re-diseñar el deck existente o usarlo como base de contenido |

***

## 5. Output de esta Fase

Al finalizar la Fase 1, debes tener:

- ✅ **Formato detectado** (pdf / docx / md / txt)
- ✅ **ACE construido** (en memoria — no necesitas mostrárselo al usuario)
- ✅ **Idioma detectado**
- ✅ **Industria detectada** (o `general`)
- ✅ **Lista de StatBlocks** extraídos
- ✅ **Conteo estimado de slides** (= número de secciones nivel 1-2 + slides de stats)
- ✅ **Alertas identificadas** (si aplica)

Pasa estos datos a la **Fase 2 — Preguntas de Descubrimiento**.
