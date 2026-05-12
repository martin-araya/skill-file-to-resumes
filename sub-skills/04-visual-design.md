# 04 — Visual Design System

> **Propósito de este archivo:** Define el sistema de diseño completo del skill de presentaciones. Cubre derivación de paletas desde marcas/industrias/emociones, tipografía con reglas estrictas de display vs body, tokens `@theme` de Tailwind v4, modo oscuro y claro, glassmorfismo, animaciones, efectos atmosféricos y reglas de contraste WCAG. Este archivo es la fuente de verdad para cada decisión visual en la generación de slides.

***

## Índice

1. [Filosofía de Diseño](#1-filosofía-de-diseño)
2. [Sistema de Colores](#2-sistema-de-colores)
3. [Derivación Automática de Paleta](#3-derivación-automática-de-paleta)
4. [Recetas Estéticas Completas](#4-recetas-estéticas-completas)
5. [Sistema Tipográfico](#5-sistema-tipográfico)
6. [Tokens `@theme` de Tailwind v4](#6-tokens-theme-de-tailwind-v4)
7. [Modo Oscuro vs Claro](#7-modo-oscuro-vs-claro)
8. [Glassmorfismo](#8-glassmorfismo)
9. [Sistema de Fondos Animados](#9-sistema-de-fondos-animados)
10. [Efectos Tipográficos](#10-efectos-tipográficos)
11. [Contraste WCAG y Accesibilidad](#11-contraste-wcag-y-accesibilidad)
12. [Reglas Anti-Patrones](#12-reglas-anti-patrones)
13. [Cheat Sheet de Clases Tailwind](#13-cheat-sheet-de-clases-tailwind)

***

## 1. Filosofía de Diseño

### El Principio Central

**Cada elección visual debe sentirse inevitable**, no decorativa. El color, la tipografía y el movimiento deben derivar del contenido — no imponerse sobre él.

Un deck de healthcare no puede verse igual a uno de gaming. Un pitch de startups no puede verse igual a un white paper académico. La paleta, la tipografía y la densidad visual deben hacer que la audiencia sienta el tema antes de leer una palabra.

### Las 5 Preguntas de Dirección de Arte

Antes de elegir cualquier token, responder estas 5 preguntas:

| Pregunta | Respuesta posible | Impacto |
|---|---|---|
| ¿Cuál es el tema? | Finanzas, Tech, Arte, Salud... | Derivación de paleta |
| ¿Quién es la audiencia? | Inversores, estudiantes, clientes, equipo interno | Nivel de formalidad |
| ¿Dónde se presenta? | Sala oscura, pantalla de laptop, impresión | Dark vs Light |
| ¿Hay marca existente? | Logo, colores corporativos | Override de paleta |
| ¿Cuál es la emoción objetivo? | Confianza, energía, autoridad, calidez | Acento y tipografía |

### Pirámide de Decisiones Visuales

```
         ┌─────────────────┐
         │   MARCA/BRAND   │  ← Máxima prioridad
         │  (si existe)    │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │    INDUSTRIA    │  ← Segunda prioridad
         │  (sector/tema)  │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │    EMOCIÓN      │  ← Tercera prioridad
         │   (tono/mood)   │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │    PRESET       │  ← Fallback final
         │  (receta base)  │
         └─────────────────┘
```

***

## 2. Sistema de Colores

### Espacio de Color: OKLCH

**Siempre usar OKLCH** como espacio de color primario. OKLCH garantiza que los gradientes sean perceptualmente uniformes — sin "grises" inesperados en el medio de un gradiente.

```css
/* ✅ CORRECTO — gradiente perceptualmente uniforme */
background: linear-gradient(in oklch, oklch(0.48 0.20 200), oklch(0.65 0.18 280));

/* ❌ INCORRECTO — puede crear grises sucios en el medio */
background: linear-gradient(#01696f, #7a39bb);
```

### Anatomía de un Token de Color

Cada color del sistema tiene 4 variantes:

```
--color-{nombre}           →  Color base (uso principal)
--color-{nombre}-hover     →  10-15% más oscuro (estados hover)
--color-{nombre}-active    →  20-25% más oscuro (estados activos/presionados)
--color-{nombre}-highlight →  Versión muy desaturada para fondos (10-15% del tono)
```

### Roles Semánticos de Color

| Rol | Token | Uso |
|---|---|---|
| Fondo base | `--color-bg` | Background del slide |
| Fondo profundo | `--color-bg-deep` | Slides de título/cierre, secciones dramáticas |
| Superficie | `--color-surface` | Cards, paneles, glassmorfismo |
| Texto principal | `--color-text` | Headings, body text de alta importancia |
| Texto secundario | `--color-text-secondary` | Body text estándar |
| Texto muted | `--color-text-muted` | Captions, labels, metadata |
| Acento primario | `--color-accent-1` | Color dominante de la marca/tema |
| Acento secundario | `--color-accent-2` | Par de gradiente con accent-1 |
| Acento terciario | `--color-accent-3` | Puente o contraste |
| Glass bg | `--color-glass-bg` | Fondo de paneles glassmorfismo |
| Glass border | `--color-glass-border` | Borde de elementos glass |
| Viñeta | `--color-vignette` | Overlay de bordes en slides |
| Glow RGB | `--glow-color-rgb` | RGB separado por comas para efectos glow |

### Jerarquía de Neutrales

**Regla de oro:** La mayor parte de cada slide debe ser neutral. El color es un acento, no el fondo completo.

```
OSCURO:
  #0a0a0f → #111118 → #1a1a24 → #22222e → #2e2e3a
  Más oscuro                              Más claro

CLARO:
  #ffffff → #fafcf8 → #f5f2ec → #ede8e0 → #e0dbd2
  Más claro                               Más oscuro
```

> **Importante:** En temas claros, NUNCA usar `#ffffff` puro como fondo. Usar siempre un off-white con ligero tinte de calor o frío (`#faf8f5`, `#fafcf8`, `#f8fafc`). El blanco puro se confunde con el chrome del navegador.

***

## 3. Derivación Automática de Paleta

### Paso 1: Detección de Marca

Si el usuario proporcionó logo, URL del sitio, o colores corporativos en las preguntas de descubrimiento:

```
1. Extraer color dominante del logo/sitio
2. Usar ese color como --color-accent-1
3. Encontrar color análogo (±30° en OKLCH) para --color-accent-2
4. Encontrar tono más oscuro/desaturado para --color-accent-3
5. Derivar bg desde versión muy oscura del accent-1 (modo dark)
   o mantener off-white con tinte del accent-1 (modo light)
```

### Paso 2: Tabla de Routing por Industria/Tema

Si no hay marca explícita, usar esta tabla:

| Industria / Tema | Tema | Accent 1 | Accent 2 | Accent 3 | Receta |
|---|---|---|---|---|---|
| **Tecnología / IA / SaaS** | Dark | Violeta eléctrico `#7C3AED` | Cian `#06B6D4` | Lavanda `#A78BFA` | Aurora Borealis |
| **Finanzas / Inversión** | Dark o Light | Oro real `#C9A84C` | Champagne `#E8D5B5` | Ámbar `#8B6914` | Midnight Cathedral |
| **Healthcare / Biotech** | Light | Teal clínico `#0891B2` | Menta suave `#34D399` | Gris cálido `#6B7280` | Clinical Precision |
| **Arte / Cultura / Historia** | Light | Oro cálido `#D4A574` | Azul galería `#5B9BD5` | Verde salvia `#7BAF6E` | Sunlit Gallery |
| **Startup / Pitch deck** | Dark | Coral eléctrico `#F97316` | Teal brillante `#14B8A6` | Blanco cálido `#FEF3C7` | Venture Pitch |
| **Gaming / Entretenimiento** | Dark | Rosa hot `#FF006E` | Azul eléctrico `#3A86FF` | Amarillo neón `#FFBE0B` | Tokyo Neon |
| **Sostenibilidad / ESG** | Dark | Verde vivo `#22C55E` | Oro musgo `#A3B18A` | Tierra marrón `#8B6914` | Forest Floor |
| **Educación / Tutorial** | Light | Azul océano `#2563EB` | Coral cálido `#F97066` | Oro arena `#D4A574` | Coastal Morning |
| **Arquitectura / Real Estate** | Dark | Champagne `#D4C5A9` | Azul acero `#94A3B8` | Blanco cálido `#F5F5F4` | Steel & Glass |
| **Ciberseguridad / DevTools** | Dark | Verde matrix `#00FF41` | Ámbar advertencia `#FFA500` | Rojo alerta `#FF0000` | Cyberpunk Terminal |
| **Investigación / Académico** | Light | Carbón profundo `#1E293B` | Naranja óxido `#C2410C` | Oliva `#65713A` | Paper Studio |
| **Gobierno / Política** | Light | Azul institucional `#1E40AF` | Gris plata `#6B7280` | Rojo `#DC2626` | Clean Institutional |
| **Moda / Lifestyle** | Light | Nude cálido `#C4A882` | Terracota `#C1644A` | Sage `#8FA37C` | Warm Editorial |
| **Comida / Gastronomía** | Light | Naranja calabaza `#EA580C` | Verde fresco `#16A34A` | Crema `#FEF9C3` | Harvest Table |
| **Música / Entretenimiento** | Dark | Magenta `#D946EF` | Índigo `#6366F1` | Dorado `#F59E0B` | Velvet Stage |

### Paso 3: Dark vs Light — Reglas de Decisión

**Elegir Dark cuando:**

- Sala de presentación oscura o proyector
- Tema de tecnología, gaming, finanzas dramáticas, o lujo
- Se quieren efectos de glow, partículas brillantes, glassmorfismo oscuro
- Audiencia espera estética premium/cinematográfica

**Elegir Light cuando:**

- Presentación impresa o enviada por email
- Sala con mucha luz natural
- Healthcare, educación, gobierno, arte
- Audiencia conservadora o institucional

**Override absoluto:** Si el usuario especificó explícitamente oscuro o claro en las preguntas de descubrimiento, esa preferencia gana sobre cualquier regla de industria.

### Paso 4: Construcción del Gradiente de Accent

El gradiente title-slide siempre va de accent-1 → accent-2 → accent-1 (triángulo):

```css
/* Texto con gradiente */
background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2), var(--color-accent-1));
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;

/* Blobs del mesh gradient — cada uno usa un accent diferente */
.blob-1 { background: var(--color-accent-1); opacity: 0.15; }
.blob-2 { background: var(--color-accent-2); opacity: 0.12; }
.blob-3 { background: var(--color-accent-3); opacity: 0.10; }
```

***

## 4. Recetas Estéticas Completas

Cada receta incluye: tokens `@theme`, fuentes, CSS custom y notas de uso.

***

### Receta 1: Midnight Cathedral

**Industria:** Finanzas, banca de inversión, marcas de lujo  
**Mood:** "Sala de juntas de private equity a medianoche"

```css
@theme {
  --color-bg: #0a0f1e;
  --color-bg-deep: #050810;
  --color-surface: #111827;
  --color-text: #f1f0ec;
  --color-text-secondary: #d4cdb8;
  --color-text-muted: #8a8070;
  --color-accent-1: #C9A84C;
  --color-accent-2: #E8D5B5;
  --color-accent-3: #8B6914;
  --color-glass-bg: rgba(255,255,255,0.04);
  --color-glass-border: rgba(201,168,76,0.15);
  --color-vignette: rgba(0,0,0,0.45);
  --font-display: 'Playfair Display', serif;
  --font-body: 'Source Sans 3', sans-serif;
}
```

```css
/* CSS custom para Midnight Cathedral */
:root { --glow-color-rgb: 201,168,76; }

/* Borde dorado sutil en cards de alto impacto */
.card-premium {
  border: 1px solid oklch(from var(--color-accent-1) l c h / 0.25);
  box-shadow: 0 0 20px oklch(from var(--color-accent-1) l c h / 0.08);
}

/* Línea divisora dorada */
.gold-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-accent-1), transparent);
  opacity: 0.4;
}

/* Número de stat con glow dorado */
.stat-number {
  font-family: var(--font-display);
  font-weight: 900;
  text-shadow: 0 0 30px rgba(201,168,76,0.5), 0 0 60px rgba(201,168,76,0.2);
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600;700&display=swap" rel="stylesheet">
```

***

### Receta 2: Aurora Borealis

**Industria:** Tecnología, IA, SaaS, innovación  
**Mood:** "Red neuronal disparándose en la oscuridad"

```css
@theme {
  --color-bg: #0f0a2a;
  --color-bg-deep: #07041a;
  --color-surface: #1a1240;
  --color-text: #f0eeff;
  --color-text-secondary: #c4b8f0;
  --color-text-muted: #7a6faa;
  --color-accent-1: #7C3AED;
  --color-accent-2: #06B6D4;
  --color-accent-3: #A78BFA;
  --color-glass-bg: rgba(255,255,255,0.06);
  --color-glass-border: rgba(167,139,250,0.15);
  --color-vignette: rgba(7,4,26,0.5);
  --font-display: 'Instrument Serif', serif;
  --font-body: 'Inter', sans-serif;
}
```

```css
:root { --glow-color-rgb: 124,58,237; }

/* Línea de gradiente violeta→cian en headings de sección */
.section-accent-line {
  width: 48px; height: 3px;
  background: linear-gradient(90deg, var(--color-accent-1), var(--color-accent-2));
  border-radius: 2px;
  margin-bottom: 1rem;
}

/* Card con borde aurora */
.card-aurora {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(167,139,250,0.2);
  backdrop-filter: blur(12px);
  border-radius: 16px;
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

***

### Receta 3: Tokyo Neon

**Industria:** Gaming, entretenimiento, cultura pop, eventos  
**Mood:** "Cruce de Shibuya a las 2 AM"

```css
@theme {
  --color-bg: #0a0a0f;
  --color-bg-deep: #050508;
  --color-surface: #12121a;
  --color-text: #f8f8ff;
  --color-text-secondary: #d0d0e8;
  --color-text-muted: #6868a0;
  --color-accent-1: #FF006E;
  --color-accent-2: #3A86FF;
  --color-accent-3: #FFBE0B;
  --color-glass-bg: rgba(255,255,255,0.03);
  --color-glass-border: rgba(255,0,110,0.15);
  --color-vignette: rgba(0,0,0,0.6);
  --font-display: 'Bebas Neue', sans-serif;
  --font-body: 'Inter', sans-serif;
}
```

```css
:root { --glow-color-rgb: 255,0,110; }

/* Borde neon animado pulsante */
@keyframes neon-pulse {
  0%, 100% { box-shadow: 0 0 5px rgba(255,0,110,0.5), 0 0 20px rgba(255,0,110,0.3); }
  50% { box-shadow: 0 0 10px rgba(255,0,110,0.8), 0 0 40px rgba(255,0,110,0.5); }
}
.card-neon { animation: neon-pulse 2s ease-in-out infinite; }

/* Texto glitch effect */
@keyframes glitch {
  0% { text-shadow: 2px 0 #FF006E, -2px 0 #3A86FF; }
  25% { text-shadow: -2px 0 #FF006E, 2px 0 #3A86FF; }
  50% { text-shadow: 2px 0 #FFBE0B, -2px 0 #FF006E; }
  75% { text-shadow: -2px 0 #3A86FF, 2px 0 #FFBE0B; }
  100% { text-shadow: 2px 0 #FF006E, -2px 0 #3A86FF; }
}
.text-glitch { animation: glitch 4s ease-in-out infinite; }

/* Scanlines overlay en slides hero */
.scanlines::before {
  content: '';
  position: absolute; inset: 0; z-index: 3; pointer-events: none;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px);
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
```

***

### Receta 4: Sunlit Gallery

**Industria:** Arte, cultura, fotografía, museos, moda  
**Mood:** "Domingo por la tarde en el Musée d'Orsay"

```css
@theme {
  --color-bg: #faf7f0;
  --color-bg-deep: #f0eadc;
  --color-surface: #f5f0e8;
  --color-text: #1a1510;
  --color-text-secondary: #4a3f32;
  --color-text-muted: #8a7a68;
  --color-accent-1: #D4A574;
  --color-accent-2: #5B9BD5;
  --color-accent-3: #7BAF6E;
  --color-glass-bg: rgba(255,255,255,0.85);
  --color-glass-border: rgba(0,0,0,0.06);
  --color-vignette: rgba(0,0,0,0.05);
  --font-display: 'Abril Fatface', serif;
  --font-body: 'Epilogue', sans-serif;
}
```

```css
:root { --glow-color-rgb: 212,165,116; }

/* Tarjeta estilo galería — sin blur visible en temas claros */
.card-gallery {
  background: rgba(255,255,255,0.9);
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 24px rgba(0,0,0,0.04);
  border-radius: 4px; /* Esquinas más cuadradas = más editorial */
}

/* Pull quote estilo galería */
.pull-quote {
  border-left: 3px solid var(--color-accent-1);
  padding-left: 1.5rem;
  font-style: italic;
  font-size: 1.25rem;
  color: var(--color-text-secondary);
}

/* Ruido muy sutil en temas claros */
.slide::before {
  opacity: 0.015; /* Mucho más sutil que en dark */
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Epilogue:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

***

### Receta 5: Clinical Precision

**Industria:** Healthcare, biotech, farmacéutica, investigación médica  
**Mood:** "Artículo de investigación convertido en visual"

```css
@theme {
  --color-bg: #f8fafc;
  --color-bg-deep: #eff6ff;
  --color-surface: #ffffff;
  --color-text: #0f172a;
  --color-text-secondary: #334155;
  --color-text-muted: #64748b;
  --color-accent-1: #0891B2;
  --color-accent-2: #34D399;
  --color-accent-3: #6B7280;
  --color-glass-bg: rgba(255,255,255,0.92);
  --color-glass-border: rgba(0,0,0,0.07);
  --color-vignette: rgba(0,0,0,0.04);
  --font-display: 'Manrope', sans-serif;
  --font-body: 'Manrope', sans-serif;
}
```

```css
:root { --glow-color-rgb: 8,145,178; }

/* Regla: CERO partículas canvas en Clinical. Demasiado "ruidoso" para healthcare */
/* En lugar de blobs animados, usar formas geométricas muy sutiles */

/* Línea de acento clínica — teal horizontal */
.clinical-accent-bar {
  height: 4px;
  background: linear-gradient(90deg, var(--color-accent-1), var(--color-accent-2));
  border-radius: 0 0 2px 2px;
  margin-bottom: 2rem;
}

/* Indicador de datos con semáforo clínico */
.data-indicator-good  { color: #16a34a; background: #f0fdf4; border: 1px solid #bbf7d0; }
.data-indicator-warn  { color: #d97706; background: #fffbeb; border: 1px solid #fde68a; }
.data-indicator-alert { color: #dc2626; background: #fef2f2; border: 1px solid #fecaca; }
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

***

### Receta 6: Venture Pitch

**Industria:** Startups, pitch decks, lanzamiento de productos  
**Mood:** "Demo Day en Series B"

```css
@theme {
  --color-bg: #18181b;
  --color-bg-deep: #09090b;
  --color-surface: #27272a;
  --color-text: #fafafa;
  --color-text-secondary: #d4d4d8;
  --color-text-muted: #71717a;
  --color-accent-1: #F97316;
  --color-accent-2: #14B8A6;
  --color-accent-3: #FEF3C7;
  --color-glass-bg: rgba(255,255,255,0.05);
  --color-glass-border: rgba(249,115,22,0.15);
  --color-vignette: rgba(0,0,0,0.4);
  --font-display: 'Archivo Black', sans-serif;
  --font-body: 'DM Sans', sans-serif;
}
```

```css
:root { --glow-color-rgb: 249,115,22; }

/* Contador animado — el número crece */
@keyframes count-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.stat-callout { animation: count-up 0.6s cubic-bezier(0.16,1,0.3,1) both; }

/* Badge de "stage" — Seed, Series A, etc */
.stage-badge {
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  background: oklch(from var(--color-accent-1) l c h / 0.15);
  color: var(--color-accent-1);
  border: 1px solid oklch(from var(--color-accent-1) l c h / 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

***

### Receta 7: Forest Floor

**Industria:** Sostenibilidad, ESG, medioambiente, impacto social  
**Mood:** "Documental sobre bosques milenarios"

```css
@theme {
  --color-bg: #0d1b0e;
  --color-bg-deep: #070e08;
  --color-surface: #1a2e1c;
  --color-text: #e8f0e8;
  --color-text-secondary: #a8c4a8;
  --color-text-muted: #5a7860;
  --color-accent-1: #22C55E;
  --color-accent-2: #A3B18A;
  --color-accent-3: #8B6914;
  --color-glass-bg: rgba(255,255,255,0.04);
  --color-glass-border: rgba(34,197,94,0.12);
  --color-vignette: rgba(0,0,0,0.45);
  --font-display: 'Outfit', sans-serif;
  --font-body: 'Outfit', sans-serif;
}
```

```css
:root { --glow-color-rgb: 34,197,94; }

/* Partículas ambientales (no interactivas) — más orgánicas, count 18 */
/* Círculos de datos CO2/impacto con colores semáforo verde */
.impact-ring {
  width: 80px; height: 80px;
  border-radius: 50%;
  border: 3px solid var(--color-accent-1);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 20px oklch(from var(--color-accent-1) l c h / 0.3);
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

***

### Receta 8: Paper Studio

**Industria:** Investigación, reportes, white papers, académico  
**Mood:** "Artículo de journal perfectamente tipografiado"

```css
@theme {
  --color-bg: #fefcf8;
  --color-bg-deep: #fdf8ef;
  --color-surface: #f7f3ec;
  --color-text: #1c1612;
  --color-text-secondary: #3d3228;
  --color-text-muted: #7a6a58;
  --color-accent-1: #1E293B;
  --color-accent-2: #C2410C;
  --color-accent-3: #65713A;
  --color-glass-bg: rgba(255,255,255,0.92);
  --color-glass-border: rgba(0,0,0,0.07);
  --color-vignette: rgba(0,0,0,0.04);
  --font-display: 'Literata', serif;
  --font-body: 'Source Sans 3', sans-serif;
}
```

```css
:root { --glow-color-rgb: 194,65,12; }

/* Números de figuras y tablas estilo paper */
.figure-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-accent-2);
  margin-bottom: 0.25rem;
}

/* Blockquote estilo citation académica */
.academic-cite {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  border-left: 2px solid var(--color-accent-2);
  padding-left: 1rem;
  margin-top: 1rem;
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,wght@0,400;0,500;0,700;1,400&family=Source+Sans+3:wght@300;400;600;700&display=swap" rel="stylesheet">
```

***

### Receta 9: Cyberpunk Terminal

**Industria:** Ciberseguridad, DevOps, infraestructura, APIs  
**Mood:** "Dashboard de SOC monitoring a las 3 AM"

```css
@theme {
  --color-bg: #0a0a0a;
  --color-bg-deep: #030303;
  --color-surface: #111111;
  --color-text: #00FF41;
  --color-text-secondary: #a0ffa0;
  --color-text-muted: #408040;
  --color-accent-1: #00FF41;
  --color-accent-2: #FFA500;
  --color-accent-3: #FF3333;
  --color-glass-bg: rgba(0,255,65,0.04);
  --color-glass-border: rgba(0,255,65,0.15);
  --color-vignette: rgba(0,0,0,0.7);
  --font-display: 'JetBrains Mono', monospace;
  --font-body: 'JetBrains Mono', monospace;
}
```

```css
:root { --glow-color-rgb: 0,255,65; }

/* Scanlines de terminal */
.terminal-scanlines::before {
  content: '';
  position: absolute; inset: 0; pointer-events: none; z-index: 3;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(0,255,65,0.03) 3px, rgba(0,255,65,0.03) 4px
  );
}

/* Prompt de terminal en subtítulos */
.terminal-prompt::before {
  content: '> ';
  color: var(--color-accent-1);
  opacity: 0.6;
}

/* Cursor parpadeante */
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
.cursor::after { content: '█'; animation: blink 1s step-end infinite; }
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

***

### Receta 10: Coastal Morning

**Industria:** Educación, tutoriales, e-learning, lifestyle  
**Mood:** "Clase matutina en universidad frente al mar"

```css
@theme {
  --color-bg: #f0f7ff;
  --color-bg-deep: #e8f4fd;
  --color-surface: #ffffff;
  --color-text: #0c1a2e;
  --color-text-secondary: #1e3a5f;
  --color-text-muted: #5a7fa0;
  --color-accent-1: #2563EB;
  --color-accent-2: #F97066;
  --color-accent-3: #D4A574;
  --color-glass-bg: rgba(255,255,255,0.88);
  --color-glass-border: rgba(0,0,0,0.07);
  --color-vignette: rgba(0,0,0,0.04);
  --font-display: 'Plus Jakarta Sans', sans-serif;
  --font-body: 'Inter', sans-serif;
}
```

```css
:root { --glow-color-rgb: 37,99,235; }

/* Número de paso en tutoriales */
.step-number {
  width: 2.5rem; height: 2.5rem;
  background: var(--color-accent-1);
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 1rem;
  flex-shrink: 0;
}

/* Highlight de concepto clave */
.concept-highlight {
  background: oklch(from var(--color-accent-1) l c h / 0.1);
  border-radius: 4px;
  padding: 0.1em 0.4em;
  color: var(--color-accent-1);
  font-weight: 600;
}
```

**Google Fonts:**

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

***

## 5. Sistema Tipográfico

### La Regla Fundamental: Display vs Body

**Display fonts** → Solo para tamaños grandes (≥24px). Son los fonts de headings.  
**Body fonts** → Para todo lo demás (text, bullets, captions, labels).

```
TERRITORIO DISPLAY (--font-display SOLAMENTE):
  h1 título        →  clamp(2.5rem, 6vw, 5rem)     ← 40px–80px
  h1 normal        →  clamp(2rem, 4.5vw, 3.5rem)   ← 32px–56px
  h2 sección       →  clamp(1.75rem, 3.5vw, 2.75rem) ← 28px–44px
  h2 contenido     →  clamp(1.5rem, 3vw, 2.25rem)  ← 24px–36px  ← MÍNIMO display

TERRITORIO BODY (--font-body SOLAMENTE):
  h3 subheading    →  clamp(1.1rem, 2vw, 1.5rem)   ← 18px–24px  ← body bold
  body text        →  clamp(1rem, 1.5vw, 1.25rem)  ← 16px–20px
  bullets          →  clamp(0.95rem, 1.4vw, 1.15rem) ← 15px–18px
  labels           →  clamp(0.8rem, 1vw, 1rem)     ← 13px–16px
  captions/meta    →  clamp(0.7rem, 0.9vw, 0.875rem) ← 11px–14px  ← MÍNIMO 11px
```

### Tabla de Decisión de Fuente por Preset

| Preset | Display Font | Body Font | Carácter |
|---|---|---|---|
| Midnight Cathedral | Playfair Display | Source Sans 3 | Drama serif + claridad sans |
| Aurora Borealis | Instrument Serif | Inter | Elegancia con precisión moderna |
| Tokyo Neon | Bebas Neue | Inter | Impacto condensado + legibilidad |
| Sunlit Gallery | Abril Fatface | Epilogue | Expresión bold + texto editorial |
| Clinical Precision | Manrope | Manrope | Familia única, variación por peso |
| Venture Pitch | Archivo Black | DM Sans | Máximo impacto + accesibilidad |
| Forest Floor | Outfit | Outfit | Familia única, orgánica y amable |
| Paper Studio | Literata | Source Sans 3 | Serif de lectura + sans limpio |
| Cyberpunk Terminal | JetBrains Mono | JetBrains Mono | Monospace puro, código/terminal |
| Coastal Morning | Plus Jakarta Sans | Inter | Geométrico amable + neutro |

### Pesos Permitidos por Nivel

```
h1 título principal   →  font-weight: 900 (Black)
h1 hero normal        →  font-weight: 800 (ExtraBold)
h2 sección            →  font-weight: 700 (Bold)
h2 contenido          →  font-weight: 700 (Bold) o 600 (SemiBold)
h3 subheading         →  font-weight: 600 (SemiBold)
body/bullets          →  font-weight: 400 (Regular)
énfasis inline        →  font-weight: 600 (SemiBold) — nunca negrita completa
labels/captions       →  font-weight: 500 (Medium) o 400 (Regular)
```

### Espaciado de Letras (Letter-Spacing)

```css
/* H1 display grande — tracking tight para impacto */
.h1-hero       { letter-spacing: -0.03em; }

/* H2 heading normal */
.h2-section    { letter-spacing: -0.015em; }

/* Labels uppercase — tracking wide para legibilidad */
.label-upper   { letter-spacing: 0.12em; text-transform: uppercase; font-size: 0.75rem; }

/* Subtítulo de título slide — tracking muy amplio */
.slide-subtitle { letter-spacing: 0.3em; text-transform: uppercase; font-size: 0.9rem; }
```

### Altura de Línea (Line-Height)

```css
/* Headings grandes — línea muy compacta */
h1 { line-height: 1.05; }
h2 { line-height: 1.15; }
h3 { line-height: 1.25; }

/* Body text — cómodo para leer */
p, li { line-height: 1.65; }

/* Labels/captions cortos — neutro */
.label { line-height: 1.3; }
```

### Jerarquía de Estilos — Máximo 4 por Slide

Cada slide debe usar **máximo 4 estilos tipográficos distintos**:

1. **Heading principal** — display font, tamaño grande, weight alto
2. **Subheading** — body font, bold, tamaño medio
3. **Body text** — body font, regular, tamaño base
4. **Label/caption** — body font, medium, tamaño pequeño, uppercase

Si se necesita un 5to estilo, es señal de que el slide está sobrecargado — dividir en dos.

***

## 6. Tokens `@theme` de Tailwind v4

### Estructura Completa del Bloque `@theme`

Este es el bloque canónico que va en `<style type="text/tailwindcss">`:

```css
@theme {
  /* ─── COLORES DE FONDO ─── */
  --color-bg: /* derivado de receta */;
  --color-bg-deep: /* versión más oscura/profunda */;
  --color-surface: /* para cards y paneles */;

  /* ─── JERARQUÍA DE TEXTO ─── */
  --color-text: /* contraste máximo */;
  --color-text-secondary: /* 70-80% de contraste */;
  --color-text-muted: /* 40-60% de contraste */;

  /* ─── ACENTOS ─── */
  --color-accent-1: /* color dominante */;
  --color-accent-2: /* par de gradiente */;
  --color-accent-3: /* terciario/puente */;

  /* ─── GLASSMORFISMO ─── */
  --color-glass-bg: /* rgba con alpha bajo */;
  --color-glass-border: /* rgba con alpha muy bajo */;

  /* ─── EFECTOS ESPECIALES ─── */
  --color-vignette: /* rgba para overlay de bordes */;

  /* ─── TIPOGRAFÍA ─── */
  --font-display: /* 'Font Name', fallback stack */;
  --font-body: /* 'Font Name', fallback stack */;
}
```

### CSS Variables en `<style>` Regular (NO en `@theme`)

Estas variables van en el bloque `<style>` normal porque usan sintaxis que `@theme` no soporta:

```css
:root {
  /* Glow color como RGB separado para uso en rgba() */
  --glow-color-rgb: R,G,B;

  /* Duplicate de --color-bg para que body renderice ANTES de que Tailwind CDN cargue */
  --color-bg: /* mismo valor que en @theme */;
  --color-text: /* mismo valor que en @theme */;
}
```

### Clases Tailwind Generadas Automáticamente desde `@theme`

Cuando Tailwind v4 procesa el bloque `@theme`, genera automáticamente estas utility classes:

| Token | Utilities generadas |
|---|---|
| `--color-bg` | `bg-bg`, `text-bg`, `border-bg` |
| `--color-accent-1` | `bg-accent-1`, `text-accent-1`, `border-accent-1`, `from-accent-1`, `to-accent-1`, `via-accent-1` |
| `--color-glass-bg` | `bg-glass-bg` |
| `--color-glass-border` | `border-glass-border` |
| `--font-display` | `font-display` |
| `--font-body` | `font-body` |

### Tailwind v4 CDN — Script Tag Correcto

```html
<!-- SIEMPRE usar @tailwindcss/browser@4, nunca tailwindcss@3 CDN -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

***

## 7. Modo Oscuro vs Claro

### Diferencias Estructurales

| Elemento | Modo Oscuro | Modo Claro |
|---|---|---|
| Fondo base | `#0a0a0f` — `#1a1a2a` | `#fafcf8` — `#f0f0ea` (NUNCA `#ffffff`) |
| Texto principal | Off-white `#f0f0f5` | Near-black `#1a1510` |
| Cards | Glass: `rgba(255,255,255,0.05-0.08)` | Solid: `rgba(255,255,255,0.85-0.95)` |
| Sombras | Innecesarias (glass da profundidad) | `box-shadow: 0 2px 8px rgba(0,0,0,0.08)` |
| Blur en glass | 12-20px (visible y llamativo) | 4-8px (casi invisible, usar sombras en cambio) |
| Viñeta | `rgba(0,0,0,0.4-0.6)` | `rgba(0,0,0,0.04-0.08)` |
| Noise texture | `opacity: 0.03` | `opacity: 0.012` |
| Blobs | Opacidad `0.10-0.18` | Opacidad `0.06-0.12` |
| Partículas | 55 interactivas, visibles | 0 en temas clásicos claros; 18 ambient si se usan |

### Glass en Modo Claro — El Problema

En fondos claros el `backdrop-filter: blur()` **no se ve**. El glass sobre fondo claro parece simplemente una caja blanca. Usar en cambio:

```css
/* ✅ CORRECTO para tema claro */
.card-light {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.07);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 24px rgba(0,0,0,0.04);
  border-radius: 16px;
  /* Sin backdrop-filter — es invisible aquí */
}

/* ❌ INCORRECTO para tema claro */
.card-light-wrong {
  background: rgba(255,255,255,0.06); /* Casi transparente sobre blanco = invisible */
  backdrop-filter: blur(12px); /* No hace nada visible */
}
```

### Partículas en Modo Claro

Las partículas canvas se ven bien en fondos oscuros. En fondos claros se ven sucias o difíciles de leer. Reglas:

| Receta Claro | Partículas |
|---|---|
| Sunlit Gallery (Arte/Cultura) | **Ninguna** — demasiado "ruidoso" para estética editorial |
| Clinical Precision (Healthcare) | **Ninguna** — debe verse limpia y clínica |
| Paper Studio (Académico) | **Ninguna** — foco en tipografía pura |
| Coastal Morning (Educación) | **Ambient 18** — muy sutiles, color del accent-1 |
| Recetas oscuras | **Interactivas 55** en título/cierre, **ambient 18** en secciones |

***

## 8. Glassmorfismo

### Los 4 Elementos del Glass Correcto

```css
.glass-panel {
  /* 1. Fondo semi-transparente */
  background: var(--color-glass-bg);

  /* 2. Blur del fondo (SOLO visible si hay gradiente detrás) */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);

  /* 3. Borde muy sutil */
  border: 1px solid var(--color-glass-border);

  /* 4. Forma */
  border-radius: 16px;
}
```

### Niveles de Blur por Uso

| Nivel | Blur | Uso |
|---|---|---|
| Sutil | 8px | Cards de contenido en fondo con poco gradiente |
| Estándar | 12px | Cards principales, paneles de datos |
| Intenso | 20px | Modal overlay, panel de alto contraste |
| Frost | 40px | Efecto "vidrio esmerilado" dramático (solo en title slides) |

### Bordes Glass — Nunca Sólidos

```css
/* ✅ CORRECTO — borde alpha-blended */
border: 1px solid oklch(from var(--color-accent-1) l c h / 0.18);
/* o */
border: 1px solid rgba(255, 255, 255, 0.10);

/* ❌ INCORRECTO — borde sólido de color */
border: 1px solid #7C3AED;   /* Demasiado rígido */
border: 1px solid #444444;   /* Gris plano, no se integra */
```

### Regla de los 3 Paneles por Slide

**Máximo 3 elementos glass por slide.** Más que eso diluye el efecto y crea "ruido visual":

```
✅  1 glass panel grande + fondo gradiente = impacto correcto
✅  3 cards glass iguales en grid = comparación limpia
❌  5 elementos glass + partículas + blobs = caos visual
```

***

## 9. Sistema de Fondos Animados

### Gradient Mesh — Estructura Obligatoria

**Todo slide debe tener `.gradient-mesh` con blobs animados.** Los blobs deben variar entre slides para evitar repetición.

```html
<!-- Slide de título: 3-4 blobs, mayor opacidad -->
<div class="gradient-mesh">
  <div class="blob" style="width:500px; height:500px; top:-100px; right:-100px; background:var(--color-accent-1); opacity:0.15;"></div>
  <div class="blob" style="width:300px; height:300px; bottom:-80px; left:-60px; background:var(--color-accent-2); opacity:0.12;"></div>
  <div class="blob" style="width:200px; height:200px; top:40%; left:15%; background:var(--color-accent-3); opacity:0.10;"></div>
</div>

<!-- Slide de contenido: 2 blobs, menor opacidad -->
<div class="gradient-mesh">
  <div class="blob" style="width:350px; height:350px; top:-80px; right:-80px; background:var(--color-accent-1); opacity:0.07;"></div>
  <div class="blob" style="width:250px; height:250px; bottom:-60px; left:-40px; background:var(--color-accent-2); opacity:0.05;"></div>
</div>
```

### Animaciones de Blobs — Keyframes

```css
@keyframes float-slow {
  0%   { transform: translate(0, 0) scale(1); }
  25%  { transform: translate(60px, -50px) scale(1.12); }
  50%  { transform: translate(-40px, 40px) scale(0.9); }
  75%  { transform: translate(50px, 20px) scale(1.08); }
  100% { transform: translate(0, 0) scale(1); }
}

@keyframes float-drift {
  0%   { transform: translate(0, 0) scale(1) rotate(0deg); }
  33%  { transform: translate(-50px, -60px) scale(1.15) rotate(3deg); }
  66%  { transform: translate(40px, 30px) scale(0.88) rotate(-2deg); }
  100% { transform: translate(0, 0) scale(1) rotate(0deg); }
}

/* Aplicación por posición en DOM */
.blob:nth-child(1) { animation: float-slow 10s ease-in-out infinite; }
.blob:nth-child(2) { animation: float-drift 14s ease-in-out infinite; }
.blob:nth-child(3) { animation: float-slow 18s ease-in-out infinite reverse; }
.blob:nth-child(4) { animation: float-drift 22s ease-in-out infinite reverse; }
```

### Sistema de Capas Z-Index

```
z-index: 0   →  .gradient-mesh (blobs en fondo)
z-index: 1   →  .particle-canvas / .particle-canvas-ambient
z-index: 2   →  .content (texto, cards, todo el contenido)
z-index: 3   →  ::before (noise texture), ::after (vignette)
z-index: 99  →  .mouse-spotlight
z-index: 100 →  .nav-controls (siempre encima de todo)
```

### Capas Atmosféricas — Noise + Vignette

```css
/* Texture de ruido — via SVG filter inline */
.slide::before {
  content: '';
  position: absolute; inset: 0; z-index: 3; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 256px 256px;
  opacity: 0.03; /* Dark: 0.03, Light: 0.012 */
  mix-blend-mode: overlay;
}

/* Viñeta radial */
.slide::after {
  content: '';
  position: absolute; inset: 0; z-index: 3; pointer-events: none;
  background: radial-gradient(ellipse at center, transparent 50%, var(--color-vignette) 100%);
}
```

### Mouse Spotlight

```html
<!-- Antes del .deck — posición fija, z-index 99 -->
<div class="mouse-spotlight" style="position:fixed;inset:0;z-index:99;pointer-events:none;"></div>
```

```javascript
document.addEventListener('mousemove', (e) => {
  const spotlight = document.querySelector('.mouse-spotlight');
  if (spotlight) {
    const rgb = getComputedStyle(document.documentElement)
      .getPropertyValue('--glow-color-rgb').trim() || '56,189,248';
    spotlight.style.background = `radial-gradient(600px circle at ${e.clientX}px ${e.clientY}px, rgba(${rgb}, 0.06), transparent 40%)`;
  }
});
```

***

## 10. Efectos Tipográficos

### Texto con Gradiente (Títulos Hero)

```css
/* Usando clases Tailwind v4 generadas desde @theme */
.gradient-title {
  @apply bg-linear-to-br from-accent-1 via-accent-2 to-accent-1 bg-clip-text text-transparent;
}

/* O en CSS puro si Tailwind no lo genera bien */
.gradient-title-css {
  background: linear-gradient(135deg,
    var(--color-accent-1) 0%,
    var(--color-accent-2) 50%,
    var(--color-accent-1) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Glow en Números de Stats

```css
/* Glow estático */
.text-glow {
  text-shadow:
    0 0 20px rgba(var(--glow-color-rgb), 0.5),
    0 0 40px rgba(var(--glow-color-rgb), 0.2);
}

/* Glow pulsante para métricas clave */
@keyframes glow-pulse {
  0%, 100% {
    text-shadow:
      0 0 20px rgba(var(--glow-color-rgb), 0.5),
      0 0 40px rgba(var(--glow-color-rgb), 0.2);
  }
  50% {
    text-shadow:
      0 0 30px rgba(var(--glow-color-rgb), 0.8),
      0 0 60px rgba(var(--glow-color-rgb), 0.3),
      0 0 90px rgba(var(--glow-color-rgb), 0.15);
  }
}
.stat-glow { animation: glow-pulse 3s ease-in-out infinite; }
```

### Odómetro (Números Rolling)

```html
<!-- Uso en slides de stats -->
<div class="odometer font-display text-5xl font-black text-accent-1 stat-glow"
     data-value="2.3" data-suffix="M" data-prefix="$">
</div>
```

```javascript
/* Se inicializa automáticamente en animateSlideEffects() */
slide.querySelectorAll('.odometer:not(.odo-init)').forEach(el => {
  el.classList.add('odo-init');
  const target = el.dataset.value;
  const suffix = el.dataset.suffix || '';
  const prefix = el.dataset.prefix || '';
  el.innerHTML = '';

  if (prefix) {
    const s = document.createElement('span');
    s.className = 'odometer-separator'; s.textContent = prefix;
    el.appendChild(s);
  }

  target.split('').forEach((char, i) => {
    if (char === '.' || char === ',') {
      const sep = document.createElement('span');
      sep.className = 'odometer-separator'; sep.textContent = char;
      el.appendChild(sep); return;
    }
    const digit = parseInt(char);
    const col = document.createElement('div');
    col.className = 'odometer-digit';
    col.style.cssText = 'height:1em; overflow:hidden;';
    for (let n = 0; n <= 9; n++) {
      const s = document.createElement('span'); s.textContent = n;
      col.appendChild(s);
    }
    col.style.transform = 'translateY(0)';
    el.appendChild(col);
    setTimeout(() => {
      col.style.transition = `transform 1.5s cubic-bezier(0.16,1,0.3,1)`;
      col.style.transform = `translateY(-${digit}em)`;
    }, 200 + i * 150);
  });

  if (suffix) {
    const s = document.createElement('span');
    s.className = 'odometer-separator'; s.textContent = suffix;
    el.appendChild(s);
  }
});
```

### Contador Incremental

```html
<!-- Para números enteros que deben "contar" hasta el valor -->
<span class="text-5xl font-black text-accent-1 stat-glow"
      data-count="2300000" data-suffix="" data-prefix="">0</span>
```

```javascript
/* Se activa en animateSlideEffects() cuando el slide se activa */
slide.querySelectorAll('[data-count]:not(.counted)').forEach(el => {
  el.classList.add('counted');
  const target = parseInt(el.dataset.count);
  const suffix = el.dataset.suffix || '';
  const prefix = el.dataset.prefix || '';
  let current = 0;
  const step = target / 50;
  const timer = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = prefix + Math.round(current).toLocaleString() + suffix;
  }, 30);
});
```

***

## 11. Contraste WCAG y Accesibilidad

### Requisitos Mínimos WCAG AA

| Tipo de texto | Contraste mínimo |
|---|---|
| Body text (16px+) | 4.5:1 |
| Texto grande (24px+ normal, 18.66px+ bold) | 3:1 |
| Texto decorativo/faint | Recomendado 3:1, permitido menor |
| Componentes UI (botones, inputs) | 3:1 vs fondo |

### Verificación de Contraste por Receta

Verificaciones pre-calculadas para las combinaciones críticas:

**Aurora Borealis (Dark):**

- `#f0eeff` sobre `#0f0a2a` → **14.8:1** ✅ (muy alto)
- `#c4b8f0` sobre `#0f0a2a` → **9.2:1** ✅
- `#7a6faa` sobre `#0f0a2a` → **3.2:1** ⚠️ (solo para texto grande o decorativo)

**Clinical Precision (Light):**

- `#0f172a` sobre `#f8fafc` → **17.1:1** ✅
- `#334155` sobre `#f8fafc` → **9.8:1** ✅
- `#64748b` sobre `#f8fafc` → **4.6:1** ✅

**Regla de alerta:** Si `--color-text-muted` sobre `--color-bg` da menos de 3:1, oscurecer el muted en tema claro o aclararlo en tema oscuro.

### Función de Verificación OKLCH

Para verificar contraste al derivar colores custom:

```javascript
// Diferencia de luminancia OKLCH — aproximación rápida
function oklchContrastCheck(L1, L2) {
  const lighter = Math.max(L1, L2);
  const darker = Math.min(L1, L2);
  // Contraste aproximado (no exacto WCAG, pero útil para decisiones rápidas)
  return (lighter + 0.05) / (darker + 0.05);
}

// Ejemplo: text L=0.95 sobre bg L=0.12
// (0.95 + 0.05) / (0.12 + 0.05) = 5.88:1 ✅
```

### Accesibilidad de Navegación

```html
<!-- Skip link — primer elemento focusable -->
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-accent-1 focus:text-bg focus:p-3 focus:rounded-lg">
  Ir al contenido principal
</a>

<!-- ARIA en controles de navegación -->
<button class="nav-btn" onclick="changeSlide(-1)" aria-label="Slide anterior">&#8249;</button>
<button class="nav-btn" onclick="changeSlide(1)" aria-label="Siguiente slide">&#8250;</button>
<div class="slide-dots" id="dots" role="tablist" aria-label="Navegación de slides"></div>
```

```css
/* Respeto a prefers-reduced-motion — OBLIGATORIO */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.2s !important;
  }
  .blob { animation: none !important; }
  .particle-canvas, .particle-canvas-ambient { display: none; }
}
```

***

## 12. Reglas Anti-Patrones

### Patrones Estéticos Prohibidos ("AI Slop")

Estos patrones son la señal más clara de una presentación genérica. Nunca usarlos:

| Patrón | Por qué está mal | Alternativa |
|---|---|---|
| Gradiente violeta/morado en fondo completo | La paleta más sobreusada de AI design | Derivar de la industria/marca |
| Botones con `background: linear-gradient(...)` | Grita "template de startup" | Color sólido del accent |
| Grid 3 columnas con icono en círculo de color + título + 2 líneas repetidas | El layout AI más reconocible | Variar tamaños, hacer una card full-width |
| Texto centrado en todos los slides | Default flojo de AI | Izquierda en contenido, centrado solo en título/cierre |
| Mismo padding/altura en todas las secciones | Ritmo monótono | Variar `padding-block` entre secciones |
| Emojis como iconos de sección | Demasiado casual para presentaciones pro | Lucide/Phosphor icons SVG o tipografía pura |
| Fondo `#ffffff` puro en temas claros | Se confunde con el chrome del browser | Off-white con tinte (`#fafcf8`) |
| Blob decorativo grande centrado en slides de contenido | Distrae del texto | Blobs solo en bordes/esquinas, opacidad reducida en contenido |
| Border-left de color sólido grueso en cards | Estilo Material Design 1.0 / Notion | Surface elevation o borde alpha-blended |
| Todos los rounds iguales en todos los elementos | Sin jerarquía de forma | `radius-sm` para dense, `radius-xl` para hero |

### Densidad de Contenido — Límites Absolutos

```
Título del slide        →  máximo 8 palabras
Bullets por slide       →  máximo 5
Palabras por bullet     →  máximo 20
Cards por fila          →  máximo 3
Líneas de texto por card →  máximo 4
Nodos en timeline       →  máximo 5
Stats callout por slide →  máximo 4
```

**Si el contenido excede estos límites → dividir en múltiples slides, nunca reducir el font-size.**

### Lo que NUNCA se Anima

```css
/* ❌ NUNCA animar estas propiedades — causan reflow y son lentas */
width, height, top, left, right, bottom, margin, padding, font-size

/* ✅ SOLO animar estas propiedades — compositing del GPU, sin reflow */
transform: translate(), scale(), rotate()
opacity
box-shadow (con moderación)
filter: blur() (con moderación, costoso en algunos browsers)
```

***

## 13. Cheat Sheet de Clases Tailwind

### Cards

```html
<!-- Card Glass (Dark) -->
<div class="bg-glass-bg backdrop-blur-xl border border-glass-border rounded-2xl p-8 hover:-translate-y-1 hover:shadow-xl transition duration-300">

<!-- Card Solid (Light) -->
<div class="bg-white/90 border border-black/7 shadow-md rounded-2xl p-8 hover:-translate-y-1 hover:shadow-lg transition duration-300">

<!-- Card con accent border izquierdo (exec summary, alertas) -->
<div class="bg-glass-bg backdrop-blur-xl border-l-4 border-accent-1 rounded-r-xl p-6">
```

### Tipografía

```html
<!-- Hero title con gradiente -->
<h1 class="font-display text-[clamp(2.5rem,6vw,5rem)] font-black tracking-tight bg-linear-to-br from-accent-1 via-accent-2 to-accent-1 bg-clip-text text-transparent reveal">

<!-- Section heading -->
<h2 class="font-display text-[clamp(1.75rem,3.5vw,2.75rem)] font-bold text-text reveal">

<!-- Subheading (body font) -->
<h3 class="font-body text-[clamp(1.1rem,2vw,1.5rem)] font-semibold text-text-secondary reveal">

<!-- Subtitle de título slide -->
<p class="font-body text-sm text-text-muted tracking-[0.3em] uppercase reveal">

<!-- Label / badge -->
<span class="font-body text-xs font-medium uppercase tracking-widest text-accent-1 bg-accent-1/10 px-3 py-1 rounded-full">
```

### Layout

```html
<!-- Grid 2 columnas iguales -->
<div class="grid grid-cols-2 gap-6">

<!-- Grid 3 columnas iguales -->
<div class="grid grid-cols-3 gap-5">

<!-- Grid 4 columnas stats -->
<div class="grid grid-cols-4 gap-4">

<!-- Split asimétrico 60/40 -->
<div class="grid grid-cols-[3fr_2fr] gap-8 items-center">

<!-- Flex con gap -->
<div class="flex items-center gap-4">
```

### Stats

```html
<!-- Stat callout individual -->
<div class="flex flex-col items-center text-center">
  <div class="odometer font-display text-5xl font-black text-accent-1 stat-glow"
       data-value="94.7" data-suffix="%"></div>
  <p class="font-body text-sm text-text-muted uppercase tracking-wider mt-2">Métrica Clave</p>
</div>

<!-- Stat con contador (número entero) -->
<span class="font-display text-6xl font-black text-accent-1 stat-glow"
      data-count="2300000" data-prefix="$" data-suffix="">0</span>
```

### Gradientes y Líneas

```html
<!-- Línea decorativa gradiente -->
<div class="h-px bg-gradient-to-r from-transparent via-accent-1 to-transparent opacity-30 my-6"></div>

<!-- Accent bar pequeña (antes de heading) -->
<div class="w-12 h-1 bg-gradient-to-r from-accent-1 to-accent-2 rounded-full mb-4 reveal"></div>

<!-- Fondo de sección con tinte de accent -->
<div class="absolute inset-0 bg-gradient-to-br from-bg via-bg to-accent-1/5 -z-10"></div>
```

***

*Fin de `04-visual-design.md`*  
*Siguiente archivo: `05-slide-templates.md` — HTML completo de cada tipo de slide con todos los elementos animados.*
