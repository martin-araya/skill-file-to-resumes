---
parent: slides-from-docs
file: 02-discovery-questions.md
phase: 2 — Preguntas de Descubrimiento
***

# Fase 2 — Preguntas de Descubrimiento

Esta fase convierte el ACE crudo en una presentación con propósito real.
Sin estas preguntas, el deck podría ser técnicamente correcto pero
completamente desalineado con lo que el usuario necesita.

**Regla de oro:** Haz TODAS las preguntas en UNA SOLA ronda.
Nunca hagas preguntas en múltiples turnos. Agrupa todo en un mensaje
claro, organizado por bloques.

***

## 1. Cuándo preguntar vs. cuándo inferir

No todas las preguntas son necesarias siempre.
Usa esta matriz para decidir qué preguntar y qué inferir del ACE.

| Dato | Preguntar si... | Inferir si... |
|---|---|---|
| Propósito del deck | Siempre preguntar | — |
| Audiencia | Siempre preguntar | — |
| Cantidad de slides | El doc tiene >8 secciones o >5000 palabras | Doc pequeño → inferir del tamaño |
| Idioma de la presentación | `detected_language` ≠ idioma del usuario | Mismo idioma → no preguntar |
| Estilo visual | Siempre preguntar (opciones concretas) | — |
| Colores de marca | El usuario menciona empresa/marca | Texto genérico → no preguntar |
| Logo | El usuario menciona empresa/marca | Texto genérico → no preguntar |
| Slides obligatorios | Siempre preguntar | — |
| Qué NO incluir | Siempre preguntar | — |
| Contexto de presentación | Siempre preguntar | — |

***

## 2. Los 7 Bloques de Preguntas

### Bloque A — Propósito & Audiencia *(siempre obligatorio)*

**A1. ¿Para qué es esta presentación?**

Opciones (mostrar como lista seleccionable):
- 🎯 **Pitch / venta** — Convencer a inversores, clientes o socios
- 📊 **Reporte ejecutivo** — Actualización de resultados para directivos
- 🎓 **Clase / tutorial** — Explicar conceptos a estudiantes o equipo
- 🎤 **Charla / conferencia** — Presentación en un evento público
- 📋 **Propuesta interna** — Proponer un proyecto o iniciativa al equipo
- 📧 **Deck para enviar** — Se verá solo, sin presentador en vivo
- 🔄 **Otro** — El usuario describe libremente

**A2. ¿Quién es la audiencia principal?**

Opciones:
- Inversores / board
- C-Suite / directivos
- Equipo interno / colaboradores
- Clientes / prospectos
- Estudiantes / comunidad académica
- Público general
- Expertos técnicos del área
- Otro (describir)

**A3. ¿Cuánto sabe la audiencia sobre el tema?**

Opciones:
- Muy poco — hay que contextualizar todo
- Algo — conocen el área pero no los detalles
- Bastante — son expertos, ir directo al punto

**A4. ¿Hay un call-to-action claro al final?**
*(Ej: "aprobar presupuesto", "agendar demo", "inscribirse al curso")*

Respuesta libre o "No necesito CTA".

***

### Bloque B — Contenido & Alcance *(siempre obligatorio)*

**B1. ¿Cuántos slides aproximadamente?**

Opciones:
- Corto (5–10 slides) — Para pitches rápidos o actualizaciones breves
- Medio (10–20 slides) — Presentación estándar
- Largo (20–35 slides) — Deep dive o deck completo
- Decidir automáticamente según el contenido del documento

**B2. ¿Hay información en el documento que NO debe aparecer en el deck?**

*(Ej: datos confidenciales, secciones de contexto interno, anexos técnicos)*

Respuesta libre o "Incluir todo".

**B3. ¿Hay datos, cifras o conclusiones que son absolutamente prioritarios?**

*(Ej: "el número de $4.2B debe estar muy destacado", "la conclusión de la página 8 es lo más importante")*

Respuesta libre o "Los que el documento destaque son suficientes".

**B4. ¿El documento es la fuente única o hay información adicional que quieras agregar?**

Opciones:
- Solo el documento — no agregar nada externo
- Tengo datos adicionales que te voy a dar ahora
- Puedes complementar con información de contexto general del tema

***

### Bloque C — Contexto de Presentación *(siempre obligatorio)*

**C1. ¿Cómo se va a usar este deck?**

Opciones:
- 🖥️ **Pantalla grande** — Proyector o TV en sala de reuniones
- 💻 **Pantalla de laptop** — Reunión 1:1 o videollamada compartida
- 📤 **Enviado por email/link** — Se navega solo sin presentador
- 🖨️ **Impreso** — Se entregará en papel *(aviso: los efectos visuales no aplican)*
- 📱 **Móvil** — Se verá principalmente en teléfono

> Si elige "Enviado por email/link" o "Móvil":
> → Aumentar densidad de texto por slide (más contexto, menos depende del presentador)
> → Agregar notas de speaker visibles inline si es posible

**C2. ¿Cuánto tiempo dura la presentación?**

Opciones:
- < 5 minutos (lightning talk)
- 10–15 minutos
- 20–30 minutos
- 45–60 minutos
- Sin límite de tiempo / es para leer

> Usar para calibrar densidad:
> - <5 min → máx 8 slides, texto mínimo
> - 10-15 min → 10-15 slides
> - 20-30 min → 15-25 slides
> - 45-60 min → hasta 35 slides con slides de respaldo (backup)

**C3. ¿Necesitas slides de respaldo (backup) al final?**

*(Slides adicionales con detalle técnico para responder preguntas)*

Opciones:
- Sí, agregar sección de Backup al final
- No es necesario

***

### Bloque D — Identidad & Marca *(preguntar solo si se detectó empresa/marca)*

> **Activar este bloque si:** el ACE contiene un nombre de empresa,
> el usuario mencionó una organización, o `detected_industry` ≠ `general`.

**D1. ¿Hay colores corporativos o de marca que deba usar?**

Opciones:
- Sí — (pedir hex o descripción: "azul marino y dorado")
- No — usar paleta generada automáticamente
- Tengo logo, úsalo como referencia de color

**D2. ¿Tienes un logo para incluir en la portada?**

Opciones:
- Sí — lo subo ahora / aquí está la URL
- No tengo logo disponible
- Usar solo el nombre de la empresa en texto

**D3. ¿Hay fuentes tipográficas corporativas?**

Opciones:
- Sí — (nombrarlas: "usamos Helvetica Neue")
- No — elegir tipografía automáticamente

***

### Bloque E — Estilo Visual *(siempre obligatorio)*

**E1. ¿Fondo oscuro o claro?**

Opciones con preview visual en palabras:
- 🌑 **Oscuro** — Más dramático, ideal para pitches y keynotes. Fondos negros/navy con texto claro y acentos brillantes.
- ☀️ **Claro** — Más profesional/editorial. Fondos crema o blanco con tipografía oscura. Ideal para reportes y educación.
- 🤖 **Decídelo tú** — Según el contenido y la industria del documento.

**E2. ¿Qué estilo visual prefieres?**

Mostrar estas opciones según la industria detectada:

*Si `detected_industry` es `fintech_startup` o `tech_producto`:*
- ⚡ **Bold Signal** — Oscuro, impactante, para pitches
- 🌌 **Aurora** — Violeta/cian, futurista, para tech
- 🟢 **Terminal** — Verde sobre negro, vibe developer

*Si `detected_industry` es `finanzas_corporativas` o `estrategia`:*
- 🏛️ **Midnight Cathedral** — Navy + dorado, boardroom premium
- 📰 **Swiss Modern** — Mínimo, tipografía precisa, datos limpios
- 📋 **Editorial Ink** — Blanco + tinta, autoridad periodística

*Si `detected_industry` es `healthcare` o `sostenibilidad`:*
- 🏥 **Clinical Precision** — Blanco/azul clínico, confianza
- 🌿 **Forest Floor** — Verde oscuro, ESG, naturaleza
- 🌅 **Coastal Morning** — Azul/coral, educación y salud

*Si `detected_industry` es `educacion` o `marketing`:*
- 🎨 **Creative Voltage** — Energético, retro-moderno
- 🌸 **Pastel Geometry** — Amigable, colores suaves
- 🌊 **Coastal Morning** — Limpio, accesible

*Siempre agregar opción:*
- ✨ **Otro / descríbelo** — El usuario describe su visión

**E3. ¿Qué tan densa debe ser la información por slide?**

Opciones:
- Mínima — Una idea por slide, mucho espacio en blanco, impacto visual
- Normal — Balance entre contenido y diseño (recomendado)
- Densa — Más información por slide, más texto, menos imágenes

**E4. ¿Qué tan formal debe sentirse?**

Opciones:
- Muy formal — Corporativo, sin elementos decorativos
- Profesional — Diseñado pero sobrio
- Moderno — Dinámico, con animaciones y efectos
- Creativo — Experimental, colores fuertes, mucho movimiento

***

### Bloque F — Idioma & Localización

> **Activar siempre que `detected_language` ≠ idioma del usuario,
> o si el documento está en un idioma y la interfaz en otro.**

**F1. ¿En qué idioma debe estar la presentación?**

Opciones:
- El mismo idioma del documento original
- [Idioma detectado del usuario]
- Otro: ___

**F2. ¿Hay terminología técnica o nombres propios que NO deben traducirse?**

*(Ej: "el término 'churn rate' debe quedarse en inglés", "los nombres de productos no traducir")*

Respuesta libre o "Traducir todo libremente".

***

### Bloque G — Restricciones & Slides Obligatorios *(siempre obligatorio)*

**G1. ¿Qué slides son obligatorios aunque no estén en el documento?**

Checklist (marcar los que aplican):
- [ ] Slide de agenda / tabla de contenidos
- [ ] Slide de "Quiénes somos" / About
- [ ] Slide de contacto / next steps
- [ ] Slide de Q&A / preguntas
- [ ] Slide de disclaimer / nota legal
- [ ] Ninguno adicional

**G2. ¿Hay algo que definitivamente NO debe aparecer?**

*(Ej: competidores nombrados, datos de empleados, proyecciones financieras internas)*

Respuesta libre o "Sin restricciones".

**G3. ¿Quieres que incluya notas de presentador?**

*(Texto guía debajo de cada slide para el presentador, no visible en pantalla)*

Opciones:
- Sí — generar notas de speaker para cada slide
- No es necesario

***

## 3. Cómo Formular la Ronda de Preguntas

### 3.1 Qué bloques incluir según el contexto

| Situación | Bloques a incluir |
|---|---|
| Documento de empresa con datos financieros | A + B + C + D + E + G |
| Texto educativo / académico sin marca | A + B + C + E + F(si aplica) + G |
| Pitch deck / startup | A + B + C + D + E + G |
| Reporte técnico / científico | A + B + C + E + G |
| Documento personal sin marca | A + B + C + E + G |
| Documento en idioma diferente | Todos los bloques + F obligatorio |

### 3.2 Formato del mensaje de preguntas

Usa este formato exacto al presentar las preguntas al usuario.
Agrupa por bloque, usa emojis para escaneabilidad, sé conciso.

```
He analizado tu documento: "[TÍTULO DEL DECK]"
Detecté: [N] secciones principales, [N] datos clave, idioma [IDIOMA].
Antes de generar los slides, necesito que respondas esto:

---

🎯 PROPÓSITO

1. ¿Para qué es esta presentación?
   → [lista de opciones]

2. ¿Quién es la audiencia?
   → [lista de opciones]

3. ¿Cuánto sabe la audiencia sobre el tema?
   → Poco / Algo / Bastante

4. ¿Hay un call-to-action al final? (ej: "agendar demo", "aprobar presupuesto")
   → [respuesta libre o "No necesito CTA"]

---

📐 ALCANCE
5. ¿Cuántos slides aproximadamente?
   → Corto (5-10) / Medio (10-20) / Largo (20-35) / Automático

1. ¿Hay algo del documento que NO debe aparecer?
   → [respuesta libre o "Incluir todo"]

2. ¿Hay datos o conclusiones que son absolutamente prioritarios?
   → [respuesta libre o "Los que el doc destaque"]

---

🖥️ CONTEXTO
8. ¿Cómo se va a usar el deck?
   → [lista de opciones]

1. ¿Cuánto dura la presentación?
   → [lista de opciones]

---

🎨 ESTILO
10. ¿Fondo oscuro o claro?
    → Oscuro / Claro / Decidir automáticamente

1. ¿Qué estilo visual?
    → [lista de 3 opciones según industria + "Otro"]

2. ¿Qué tan densa la info por slide?
    → Mínima / Normal / Densa

---

📌 SLIDES EXTRA
13. ¿Qué slides obligatorios necesitas además del contenido?
    → [ ] Agenda  [ ] About  [ ] Contacto  [ ] Q&A  [ ] Ninguno

1. ¿Hay algo que definitivamente NO debe aparecer?
    → [respuesta libre o "Sin restricciones"]

---

Responde con los números (ej: "1→Pitch, 2→Inversores, 3→Poco, 4→Agendar demo...")
y genero el deck de inmediato.

```

### 3.3 Reglas del mensaje de preguntas

- **Máximo 14 preguntas** en una sola ronda. Si necesitas más, prioriza.
- **Siempre resumir lo que detectaste** antes de hacer las preguntas
  (título, secciones, datos clave). Muestra que ya leíste el documento.
- **Dar opciones concretas** — no preguntas abiertas sin sugerencias.
- **Las respuestas por default** deben estar indicadas implícitamente
  (la opción marcada como "recomendado" o "automático").
- **Invitar a responder en formato corto** — "1→opción, 2→opción..."
  reduce la fricción del usuario.

***

## 4. Procesamiento de Respuestas

### 4.1 Mapeo de respuestas a parámetros de generación

Una vez que el usuario responde, convierte sus respuestas en estos
**parámetros de generación** que usarás en las fases 3, 4 y 5:

```

generation_params = {

  // De Bloque A
  purpose: "pitch" | "reporte" | "clase" | "charla" | "propuesta" | "deck_autonomo",
  audience: "inversores" | "directivos" | "equipo" | "clientes" | "estudiantes" | "publico" | "tecnicos",
  audience_level: "novato" | "intermedio" | "experto",
  cta: string | null,

  // De Bloque B
  slide_count: "short" | "medium" | "long" | "auto",
  exclude_sections: string[],
  priority_data: string[],
  extra_content: "none" | "user_provided" | "research_allowed",

  // De Bloque C
  usage_context: "pantalla_grande" | "laptop" | "email" | "impreso" | "movil",
  duration_minutes: number | null,
  backup_slides: boolean,

  // De Bloque D (si aplica)
  brand_colors: string[] | null,   // ej: ["#003087", "#FFD700"]
  logo_url: string | null,
  brand_fonts: string[] | null,

  // De Bloque E
  theme_mode: "dark" | "light" | "auto",
  visual_preset: string,           // nombre del preset seleccionado
  density: "minimal" | "normal" | "dense",
  formality: "muy_formal" | "profesional" | "moderno" | "creativo",

  // De Bloque F (si aplica)
  output_language: string,         // código ISO: "es", "en", "pt"...
  preserve_terms: string[],

  // De Bloque G
  required_slides: string[],       // ["agenda", "contacto", ...]
  forbidden_content: string[],
  speaker_notes: boolean
}

```

### 4.2 Inferencias cuando el usuario no responde algo

Si el usuario omite una pregunta o da una respuesta ambigua:

| Parámetro omitido | Default inteligente |
|---|---|
| `purpose` | Inferir del tipo de documento (reporte → "reporte", lista de features → "pitch") |
| `audience` | `"general"` — diseñar para audiencia mixta |
| `audience_level` | `"intermedio"` |
| `slide_count` | `"auto"` — una sección del ACE = un slide (aprox.) |
| `usage_context` | `"pantalla_grande"` |
| `duration_minutes` | `null` — no ajustar densidad por tiempo |
| `theme_mode` | Según `detected_industry` (ver tabla en 04-visual-design.md) |
| `visual_preset` | Según `detected_industry` (ver tabla en 04-visual-design.md) |
| `density` | `"normal"` |
| `formality` | `"profesional"` |
| `output_language` | `detected_language` del documento |
| `required_slides` | `[]` — solo el contenido del documento |
| `speaker_notes` | `false` |

### 4.3 Ajustes automáticos por combinación de parámetros

Estas combinaciones activan ajustes especiales:

| Combinación | Ajuste |
|---|---|
| `purpose=pitch` + `audience=inversores` | Agregar slide de "Problema / Solución", slide de tracción, slide de equipo si no existen |
| `usage_context=email` | Aumentar texto por slide +30%, agregar contexto en cada heading |
| `usage_context=movil` | Layouts de una columna, texto ≥16px, sin cards de 3 columnas |
| `duration_minutes < 10` | Máx. 8 slides, densidad mínima, CTA en slide 2 o 3 |
| `audience_level=novato` | Agregar slide de glosario si hay >5 términos técnicos |
| `backup_slides=true` | Agregar sección "Backup" al final con detalle técnico |
| `formality=muy_formal` | Sin partículas canvas, sin blobs animados, sin gradient mesh |
| `density=densa` | Hasta 7 bullets por slide, cards con más texto, tablas más complejas |
| `speaker_notes=true` | Generar `<aside class="speaker-notes">` debajo de cada slide |
| `brand_colors` definidos | Override completo de paleta — usar colores de marca como accent-1/2 |

***

## 5. Output de esta Fase

Al finalizar la Fase 2, debes tener:

- ✅ **`generation_params`** completo (ya sea por respuesta del usuario o por default)
- ✅ **Lista de slides obligatorios** adicionales al contenido (agenda, contacto, etc.)
- ✅ **Contenido excluido** marcado en el ACE
- ✅ **Datos prioritarios** identificados para destacar visualmente
- ✅ **Preset visual** seleccionado
- ✅ **Idioma de output** confirmado

Pasa estos datos junto con el ACE a la **Fase 3 — Mapeo de Contenido**.
