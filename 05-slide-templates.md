# 05-slide-templates

Este archivo define el catálogo completo de plantillas de slides para el skill de presentaciones. Su función es transformar bloques de contenido estructurado en slides HTML consistentes, visualmente potentes y compatibles con el sistema de navegación tipo deck.

## Objetivo

Estas plantillas existen para resolver tres problemas a la vez:

1. Convertir contenido heterogéneo (Markdown, PDF, Word, TXT) en slides claros.
2. Mantener coherencia visual y técnica entre decks distintos.
3. Forzar límites de densidad para que ninguna slide desborde el viewport.

Cada slide debe comunicar **una sola idea principal**. Si un bloque de contenido no entra con claridad, debe dividirse en dos o más slides.

***

## Principios globales

### 1. Regla de una idea

Cada slide debe tener un foco inequívoco:

- una tesis,
- una comparación,
- una cifra clave,
- una secuencia,
- o una visualización.

Nunca mezclar dos argumentos principales en la misma slide.

### 2. Regla de viewport

Toda slide debe caber íntegramente en pantalla.

- Prohibido scroll interno.
- Prohibido ocultar overflow como solución de maquetación.
- Prohibido bajar la tipografía por debajo de tamaños legibles para “hacer que entre”.
- Si no entra, se divide.

### 3. Regla de contenido investigado

Una plantilla bonita no compensa contenido vago. Cada slide generada desde estas plantillas debe priorizar:

- cifras concretas,
- fechas,
- comparaciones,
- datos verificables,
- contexto breve pero útil.

### 4. Regla de consistencia

Todas las slides comparten:

- sistema de navegación deck,
- fondo animado,
- jerarquía tipográfica,
- tokens `@theme`,
- animación de entrada con `.reveal`,
- y controles fijos de navegación.

### 5. Regla de variedad

No repetir la misma plantilla en slides consecutivas salvo que exista una razón fuerte, por ejemplo:

- una sección analítica de varias comparaciones homogéneas,
- una serie de benchmarks equivalentes,
- o una narrativa deliberadamente modular.

***

## Contrato técnico común

Toda plantilla debe insertarse dentro de la arquitectura general del deck.

### Estructura mínima de una slide

```html
<div class="slide slide-N" data-slide="N">
  <div class="gradient-mesh">
    <div class="blob" style="width: 320px; height: 320px; top: -60px; right: -60px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 220px; height: 220px; bottom: -40px; left: -20px; background: var(--color-accent-2); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <!-- contenido de la slide -->
  </div>
</div>
```

### Reglas obligatorias por slide

- Debe tener `class="slide slide-N"`.
- Debe tener `data-slide="N"` secuencial, sin huecos.
- Debe incluir `.gradient-mesh` con 2 a 4 blobs.
- Todo elemento visible importante debe llevar la clase `.reveal`.
- No usar colores hardcodeados cuando puedan resolverse con tokens.
- No redefinir la lógica de navegación dentro de una slide.

### Clases utilitarias esperadas

Estas clases aparecen frecuentemente en las plantillas:

- `font-display`
- `font-body`
- `text-accent-1`
- `text-text`
- `text-text-secondary`
- `text-text-muted`
- `bg-glass-bg`
- `border-glass-border`
- `bg-surface`
- `bg-bg`
- `bg-bg-deep`
- `reveal`

### Tarjeta base recomendada

```html
<div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-8 shadow-lg reveal">
  <div class="text-sm uppercase tracking-[0.14em] text-text-muted mb-3">Label</div>
  <h3 class="text-2xl font-semibold text-text mb-3">Título</h3>
  <p class="text-base leading-relaxed text-text-secondary">Descripción breve del bloque.</p>
</div>
```

### Variantes light theme

En temas claros, la profundidad se consigue más por superficie y sombra que por blur extremo. Reemplazo recomendado:

```html
<div class="rounded-3xl border border-glass-border bg-surface p-8 shadow-md reveal">
  <h3 class="text-2xl font-semibold text-text mb-3">Título</h3>
  <p class="text-base leading-relaxed text-text-secondary">Contenido.</p>
</div>
```

***

## Reglas de densidad por plantilla

| Tipo de contenido | Máximo recomendado |
|---|---|
| Título principal | 8 palabras |
| Heading de sección | 10 palabras |
| Bullets por slide | 5 |
| Palabras por bullet | 20 |
| Cards por fila | 3 |
| Líneas de texto por card | 4 |
| Callouts numéricos por slide | 3 o 4 |
| Nodos de timeline | 5 |
| Barras en un gráfico simple | 6 |

Si cualquier bloque supera estos límites, el motor debe partir el contenido en varias slides.

***

## Enrutamiento contenido → plantilla

Antes de ver las plantillas, el skill debe decidir cuál usar.

### Reglas de asignación rápidas

- `Título + subtítulo + contexto general` → **Template 01 o 02**
- `Agenda o estructura del deck` → **Template 03**
- `Lista de puntos clave` → **Template 04 o 14**
- `Texto explicativo + visual fuerte` → **Template 05**
- `Comparación binaria` → **Template 06**
- `Tres pilares o tres features` → **Template 07**
- `Seis capacidades o seis hallazgos` → **Template 08**
- `KPIs múltiples` → **Template 09 o 10**
- `Resumen ejecutivo de insights` → **Template 11**
- `Secuencia temporal o roadmap` → **Template 12**
- `Métricas + barras comparativas` → **Template 13**
- `Cierre o agradecimiento` → **Template 15**
- `Slides de chart avanzado o interacción` → **Template 16**

### Priorización cuando un bloque encaja en más de una plantilla

1. Priorizar claridad sobre espectacularidad.
2. Si hay una cifra dominante, usar una plantilla de stats.
3. Si hay relación temporal, usar timeline aunque también haya bullets.
4. Si la comparación es binaria, no usar grid de tres cards.
5. Si hay demasiados bullets, dividir en dos slides y repartir por afinidad.

***

## Template 01 — Title Slide Cinemática

### Cuándo usarla

Usar como primera slide obligatoria del deck. Sirve para abrir con impacto visual, establecer tono y dejar clarísimo el tema.

### Objetivo narrativo

- Presentar el tema.
- Introducir marca o sujeto principal.
- Crear un primer golpe visual memorable.

### Estructura

- Hero visual: logo o emoji.
- Título grande con tratamiento visual fuerte.
- Subtítulo corto en mayúsculas o tracking amplio.
- Fondo con 3 blobs y `particle-canvas`.

### Límites

- Título: máximo 8 palabras.
- Subtítulo: máximo 12 palabras.
- No añadir párrafos ni bullets.

### HTML base

```html
<div class="slide slide-1 active" data-slide="1">
  <div class="gradient-mesh">
    <div class="blob" style="width: 520px; height: 520px; top: -120px; right: -120px; background: var(--color-accent-1); opacity: 0.15;"></div>
    <div class="blob" style="width: 320px; height: 320px; bottom: -90px; left: -60px; background: var(--color-accent-2); opacity: 0.12;"></div>
    <div class="blob" style="width: 220px; height: 220px; top: 42%; left: 14%; background: var(--color-accent-3); opacity: 0.10;"></div>
  </div>

  <canvas class="particle-canvas" style="position:absolute; inset:0; z-index:1;"></canvas>

  <div class="content text-center">
    <img
      class="max-h-[110px] max-w-[280px] object-contain mb-6 animate-[float_3s_ease-in-out_infinite] drop-shadow-lg mx-auto reveal"
      src="LOGO_URL"
      alt="Marca o entidad"
    >

    <h1 class="font-display text-[clamp(2.8rem,6vw,5.4rem)] font-black tracking-tight mb-4 reveal bg-linear-to-br from-accent-1 via-accent-2 to-accent-1 bg-clip-text text-transparent">
      Título de la presentación
    </h1>

    <p class="text-[clamp(0.92rem,1.4vw,1.25rem)] uppercase tracking-[0.35em] text-text-muted reveal">
      Subtítulo o contexto breve
    </p>
  </div>
</div>
```

### Fallback con emoji

```html
<div class="text-[120px] mb-6 animate-[float_3s_ease-in-out_infinite] reveal">🚀</div>
```

### Buenas prácticas

- Preferir logo si existe uno de alta calidad.
- Si el logo no contrasta con el fondo, usar variante blanca o encapsularlo en una cápsula translúcida.
- Nunca meter agenda ni claims extensos aquí.

***

## Template 02 — Title Slide Corporativa / Light

### Cuándo usarla

Versión más sobria para decks formales, consultoría, healthcare, educación o reportes ejecutivos donde el dramatismo debe bajar.

### Objetivo narrativo

Abrir con autoridad y limpieza visual sin exceso de efectos.

### Estructura

- Hero visual discreto.
- Título grande, normalmente sólido, sin glow fuerte.
- Subtítulo institucional.
- Fondo más limpio y blobs menos opacos.

### HTML base

```html
<div class="slide slide-1 active" data-slide="1">
  <div class="gradient-mesh">
    <div class="blob" style="width: 420px; height: 420px; top: -120px; right: -100px; background: var(--color-accent-1); opacity: 0.10;"></div>
    <div class="blob" style="width: 280px; height: 280px; bottom: -80px; left: -50px; background: var(--color-accent-2); opacity: 0.08;"></div>
    <div class="blob" style="width: 180px; height: 180px; top: 45%; left: 18%; background: var(--color-accent-3); opacity: 0.06;"></div>
  </div>

  <div class="content text-center">
    <img class="max-h-[88px] max-w-[240px] object-contain mb-6 mx-auto reveal" src="LOGO_URL" alt="Logo">
    <p class="text-sm uppercase tracking-[0.3em] text-text-muted mb-4 reveal">Informe / Presentación</p>
    <h1 class="font-display text-[clamp(2.4rem,5vw,4.6rem)] font-bold text-text mb-4 reveal">
      Título principal
    </h1>
    <p class="text-[clamp(1rem,1.4vw,1.2rem)] text-text-secondary reveal">
      Subtítulo conciso y profesional
    </p>
  </div>
</div>
```

### Cuándo preferirla sobre Template 01

- Entornos de comité ejecutivo.
- Presentaciones impresas o enviadas por email.
- Sectores sensibles: salud, regulación, investigación, gobierno.

***

## Template 03 — Agenda / Table of Contents

### Cuándo usarla

Cuando el deck necesita explicar estructura o recorrido. Muy útil en decks medianos o largos.

### Objetivo narrativo

Ordenar expectativas y demostrar control del contenido.

### Estructura

- Heading de sección.
- Grid de 2 columnas.
- Entre 5 y 8 puntos agrupados por bloques.
- Badge numérico para cada item.

### Límites

- Máximo 8 items.
- Cada descripción secundaria: máximo 5 o 6 palabras.

### HTML base

```html
<div class="slide slide-2" data-slide="2">
  <div class="gradient-mesh">
    <div class="blob" style="width: 360px; height: 360px; top: -80px; right: -80px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -50px; left: -30px; background: var(--color-accent-2); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Agenda</p>
    <h2 class="font-display text-[clamp(2rem,4.2vw,3.1rem)] font-bold text-text mb-10 reveal">Cómo se organiza esta presentación</h2>

    <div class="grid grid-cols-2 gap-5">
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 flex gap-4 reveal">
        <div class="w-10 h-10 rounded-full bg-accent-1 text-bg font-bold flex items-center justify-center shrink-0">1</div>
        <div>
          <h3 class="text-xl font-semibold text-text mb-1">Mercado</h3>
          <p class="text-sm text-text-secondary">Tamaño, tendencia y drivers</p>
        </div>
      </div>

      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 flex gap-4 reveal">
        <div class="w-10 h-10 rounded-full bg-accent-2 text-bg font-bold flex items-center justify-center shrink-0">2</div>
        <div>
          <h3 class="text-xl font-semibold text-text mb-1">Producto</h3>
          <p class="text-sm text-text-secondary">Oferta, diferenciación y propuesta</p>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Uso correcto

- Ideal después de la portada.
- No listar cada slide individual; agrupar en módulos conceptuales.
- Si el deck es corto, omitirla.

***

## Template 04 — Bullet List

### Cuándo usarla

Cuando existe una lista clara de mensajes clave y cada punto merece el mismo peso visual.

### Objetivo narrativo

Permitir lectura rápida, muy clara, sin distraer con exceso de estructura visual.

### Límites

- Máximo 5 bullets.
- Máximo 20 palabras por bullet.
- No combinar con grid pesado en la misma slide.

### HTML base

```html
<div class="slide slide-3" data-slide="3">
  <div class="gradient-mesh">
    <div class="blob" style="width: 300px; height: 300px; top: -60px; right: -60px; background: var(--color-accent-1); opacity: 0.07;"></div>
    <div class="blob" style="width: 220px; height: 220px; bottom: -40px; left: -20px; background: var(--color-accent-2); opacity: 0.05;"></div>
  </div>

  <div class="content max-w-[980px]">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Key points</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-8 reveal">Los cinco mensajes que importan</h2>

    <ul class="space-y-5">
      <li class="flex gap-4 items-start reveal">
        <span class="mt-1 w-3 h-3 rounded-full bg-accent-1 shrink-0"></span>
        <span class="text-[clamp(1.05rem,1.4vw,1.25rem)] leading-relaxed text-text-secondary">Primer punto clave explicado con suficiente contexto, pero sin excederse.</span>
      </li>
      <li class="flex gap-4 items-start reveal">
        <span class="mt-1 w-3 h-3 rounded-full bg-accent-2 shrink-0"></span>
        <span class="text-[clamp(1.05rem,1.4vw,1.25rem)] leading-relaxed text-text-secondary">Segundo punto con dato o insight concreto.</span>
      </li>
    </ul>
  </div>
</div>
```

### Variante con párrafo introductorio

Antes de la lista, se puede añadir un párrafo de 2 o 3 líneas si ayuda a contextualizar:

```html
<p class="text-lg leading-relaxed text-text-secondary max-w-[72ch] mb-8 reveal">
  Esta sección resume los cambios más importantes observados en el periodo analizado.
</p>
```

### Cuándo no usarla

- Si los puntos tienen naturaleza distinta y deberían ser cards.
- Si existe una secuencia temporal.
- Si una sola cifra domina el mensaje.

***

## Template 05 — Two-Column Split: Texto + Visual

### Cuándo usarla

Cuando el contenido tiene una mitad verbal fuerte y una mitad visual clara: imagen, gráfico, captura, diagrama, ilustración o gran emoji.

### Objetivo narrativo

Equilibrar explicación y evidencia visual.

### Estructura

- Columna izquierda: titular, copy, badge opcional.
- Columna derecha: visual protagonista.

### HTML base

```html
<div class="slide slide-4" data-slide="4">
  <div class="gradient-mesh">
    <div class="blob" style="width: 360px; height: 360px; top: -70px; right: -70px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -50px; left: -20px; background: var(--color-accent-3); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <div class="grid grid-cols-2 gap-14 items-center">
      <div>
        <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Overview</p>
        <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-5 reveal">Una explicación clara con apoyo visual</h2>
        <p class="text-lg leading-relaxed text-text-secondary mb-5 reveal">
          La columna izquierda debe sintetizar el argumento. Idealmente un párrafo principal y, si hace falta, un segundo párrafo breve.
        </p>
        <div class="inline-flex items-center gap-3 rounded-full border border-glass-border bg-glass-bg px-4 py-2 text-sm text-text-secondary reveal">
          <span class="w-2.5 h-2.5 rounded-full bg-accent-1"></span>
          Insight principal o etiqueta contextual
        </div>
      </div>

      <div class="rounded-[2rem] border border-glass-border bg-glass-bg backdrop-blur-xl p-8 min-h-[380px] flex items-center justify-center reveal">
        <img src="IMAGE_URL" alt="Visual principal" class="max-h-[340px] object-contain">
      </div>
    </div>
  </div>
</div>
```

### Variantes de visual permitidas

- Imagen real.
- Logo grande.
- Screenshot de producto.
- SVG simple.
- Emoji grande.
- Mini chart.

### Recomendaciones

- El texto no debe invadir la columna visual.
- Si el visual requiere explicación larga, probablemente necesita su propia slide.

***

## Template 06 — Two-Column Glass Cards (Comparación binaria)

### Cuándo usarla

Para comparar dos opciones, dos escenarios, dos estrategias o un antes/después.

### Objetivo narrativo

Hacer visible una tensión, diferencia o trade-off.

### Estructura

- Heading arriba.
- Dos cards simétricas en grid.
- Cada card con título, 2 a 4 líneas y opcionalmente una métrica.

### HTML base

```html
<div class="slide slide-5" data-slide="5">
  <div class="gradient-mesh">
    <div class="blob" style="width: 320px; height: 320px; top: -80px; right: -80px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -50px; left: -20px; background: var(--color-accent-2); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Comparison</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-10 reveal">Dos caminos posibles</h2>

    <div class="grid grid-cols-2 gap-6">
      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-8 shadow-lg reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-sm uppercase tracking-[0.2em] text-text-muted mb-3">Opción A</div>
        <h3 class="text-2xl font-semibold text-text mb-4">Crecimiento agresivo</h3>
        <p class="text-base leading-relaxed text-text-secondary mb-4">Mayor velocidad de expansión, más requerimientos de capital y más presión operativa.</p>
        <div class="text-4xl font-black text-accent-1">3.2x</div>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-8 shadow-lg reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-sm uppercase tracking-[0.2em] text-text-muted mb-3">Opción B</div>
        <h3 class="text-2xl font-semibold text-text mb-4">Crecimiento disciplinado</h3>
        <p class="text-base leading-relaxed text-text-secondary mb-4">Menor velocidad de despliegue, pero mejor control de riesgo y mayor eficiencia en caja.</p>
        <div class="text-4xl font-black text-accent-2">18%</div>
      </article>
    </div>
  </div>
</div>
```

### Cuándo es ideal

- Bull vs bear case.
- Build vs buy.
- On-premise vs cloud.
- Antes vs después.
- Producto actual vs roadmap futuro.

***

## Template 07 — Three-Card Grid

### Cuándo usarla

Cuando existen exactamente tres pilares, tres capacidades, tres hallazgos o tres principios.

### Objetivo narrativo

Dar el mismo peso a un trío conceptual.

### Límites

- Tres cards máximo.
- Cada card: título + 2 o 3 líneas.

### HTML base

```html
<div class="slide slide-6" data-slide="6">
  <div class="gradient-mesh">
    <div class="blob" style="width: 320px; height: 320px; top: -70px; right: -70px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 210px; height: 210px; bottom: -40px; left: -10px; background: var(--color-accent-2); opacity: 0.05;"></div>
  </div>

  <div class="content text-center">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Framework</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-10 reveal">Tres pilares de la estrategia</h2>

    <div class="grid grid-cols-3 gap-6 text-left">
      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-8 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-[2.4rem] mb-4">⚙️</div>
        <h3 class="text-xl font-semibold text-text mb-3">Operación</h3>
        <p class="text-base leading-relaxed text-text-secondary">Reducir fricción, automatizar pasos y bajar costos marginales.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-8 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-[2.4rem] mb-4">📈</div>
        <h3 class="text-xl font-semibold text-text mb-3">Crecimiento</h3>
        <p class="text-base leading-relaxed text-text-secondary">Expandir demanda mediante canales y segmentos mejor priorizados.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-8 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-[2.4rem] mb-4">🛡️</div>
        <h3 class="text-xl font-semibold text-text mb-3">Defensibilidad</h3>
        <p class="text-base leading-relaxed text-text-secondary">Crear barreras mediante datos, integración y mejor experiencia.</p>
      </article>
    </div>
  </div>
</div>
```

### Cuándo evitarla

- Si uno de los tres puntos es muchísimo más importante que los otros.
- Si cada pilar necesita demasiada explicación.

***

## Template 08 — Six-Card Feature Grid (3×2)

### Cuándo usarla

Para presentar un sistema de capacidades, una taxonomía breve o seis hallazgos relativamente equivalentes.

### Objetivo narrativo

Transmitir amplitud de cobertura sin perder modularidad.

### Límites

- 6 cards máximo.
- 3 líneas de cuerpo por card idealmente.

### HTML base

```html
<div class="slide slide-7" data-slide="7">
  <div class="gradient-mesh">
    <div class="blob" style="width: 330px; height: 330px; top: -60px; right: -60px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -50px; left: -20px; background: var(--color-accent-2); opacity: 0.05;"></div>
  </div>

  <div class="content">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Capabilities</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-8 reveal">Seis capacidades que definen el producto</h2>

    <div class="grid grid-cols-3 gap-5">
      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-3xl mb-3">🔍</div>
        <h3 class="text-lg font-semibold text-text mb-2">Búsqueda</h3>
        <p class="text-sm leading-relaxed text-text-secondary">Encuentra información y la organiza rápidamente.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-3xl mb-3">🧠</div>
        <h3 class="text-lg font-semibold text-text mb-2">Síntesis</h3>
        <p class="text-sm leading-relaxed text-text-secondary">Convierte múltiples fuentes en una narrativa usable.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-3xl mb-3">📊</div>
        <h3 class="text-lg font-semibold text-text mb-2">Análisis</h3>
        <p class="text-sm leading-relaxed text-text-secondary">Destaca tendencias, comparaciones y oportunidades.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-3xl mb-3">🎨</div>
        <h3 class="text-lg font-semibold text-text mb-2">Diseño</h3>
        <p class="text-sm leading-relaxed text-text-secondary">Alinea el resultado con una dirección visual elegida.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-3xl mb-3">⚡</div>
        <h3 class="text-lg font-semibold text-text mb-2">Velocidad</h3>
        <p class="text-sm leading-relaxed text-text-secondary">Reduce horas de trabajo a minutos en flujos repetitivos.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-3xl mb-3">📦</div>
        <h3 class="text-lg font-semibold text-text mb-2">Entrega</h3>
        <p class="text-sm leading-relaxed text-text-secondary">Exporta HTML, PPTX y activos reutilizables.</p>
      </article>
    </div>
  </div>
</div>
```

### Regla importante

Usar grid, no flex. El grid asegura altura consistente entre cards.

***

## Template 09 — Four-Column Metric Grid

### Cuándo usarla

Cuando el valor de la slide está en varios KPIs presentados al mismo nivel.

### Objetivo narrativo

Entregar una foto rápida y ejecutiva del estado del negocio, producto o fenómeno analizado.

### Estructura

- Heading.
- Línea breve de contexto.
- Grid de 4 cards métricas.

### HTML base

```html
<div class="slide slide-8" data-slide="8">
  <div class="gradient-mesh">
    <div class="blob" style="width: 300px; height: 300px; top: -60px; right: -60px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -30px; left: -20px; background: var(--color-accent-3); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Metrics</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-3 reveal">Cuatro cifras para entender el momento</h2>
    <p class="text-base text-text-secondary mb-8 max-w-[70ch] reveal">Estas métricas resumen escala, eficiencia, crecimiento y retención en un solo vistazo.</p>

    <div class="grid grid-cols-4 gap-5">
      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-3">Usuarios</div>
        <div class="text-4xl font-black text-accent-1 mb-2" data-count="2400000">0</div>
        <p class="text-sm text-text-secondary">Base activa mensual</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-3">Crecimiento</div>
        <div class="text-4xl font-black text-accent-2">47%</div>
        <p class="text-sm text-text-secondary">YoY en ingresos</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-3">Margen</div>
        <div class="text-4xl font-black text-accent-3">68%</div>
        <p class="text-sm text-text-secondary">Gross margin</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal hover:-translate-y-1 hover:shadow-xl transition">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-3">Retención</div>
        <div class="text-4xl font-black text-accent-1">91%</div>
        <p class="text-sm text-text-secondary">Logo retention anual</p>
      </article>
    </div>
  </div>
</div>
```

### Recomendaciones

- Máximo 4 cards por fila.
- Si hay más métricas, repartir en 2 slides o combinar con otra visualización.

***

## Template 10 — Stat Callout (Big Numbers)

### Cuándo usarla

Para enfatizar 2 o 3 cifras que por sí solas cuentan la historia.

### Objetivo narrativo

Que la audiencia recuerde esas cifras aunque olvide el resto de la slide.

### Diferencia respecto al Template 09

- Menos cards.
- Números más grandes.
- Mayor peso emocional y visual.

### HTML base

```html
<div class="slide slide-9" data-slide="9">
  <div class="gradient-mesh">
    <div class="blob" style="width: 360px; height: 360px; top: -70px; right: -70px; background: var(--color-accent-1); opacity: 0.10;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -40px; left: -20px; background: var(--color-accent-2); opacity: 0.08;"></div>
  </div>

  <div class="content text-center">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Headline numbers</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-10 reveal">Tres números que cambian la conversación</h2>

    <div class="grid grid-cols-3 gap-6">
      <div class="rounded-[2rem] border border-glass-border bg-glass-bg backdrop-blur-xl p-8 reveal">
        <div class="text-[clamp(2.8rem,5vw,4.5rem)] font-black text-accent-1 stat-glow mb-3">$17.6B</div>
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">Mercado</div>
        <p class="text-sm text-text-secondary">Tamaño estimado en 2026</p>
      </div>

      <div class="rounded-[2rem] border border-glass-border bg-glass-bg backdrop-blur-xl p-8 reveal">
        <div class="text-[clamp(2.8rem,5vw,4.5rem)] font-black text-accent-2 stat-glow mb-3">3.4x</div>
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">Velocidad</div>
        <p class="text-sm text-text-secondary">Más rápido que el baseline</p>
      </div>

      <div class="rounded-[2rem] border border-glass-border bg-glass-bg backdrop-blur-xl p-8 reveal">
        <div class="text-[clamp(2.8rem,5vw,4.5rem)] font-black text-accent-3 stat-glow mb-3">91%</div>
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">Retención</div>
        <p class="text-sm text-text-secondary">Clientes que renuevan</p>
      </div>
    </div>
  </div>
</div>
```

### Regla editorial

Si una cifra necesita cinco líneas de explicación, no es un callout. Es otra plantilla.

***

## Template 11 — Executive Summary (Stacked Cards)

### Cuándo usarla

Cuando se necesita resumir 3 o 4 hallazgos ejecutivos con algo más de contexto que un bullet, pero menos que una slide entera por insight.

### Objetivo narrativo

Hacer síntesis de alto nivel, ideal para comités o summary slides.

### HTML base

```html
<div class="slide slide-10" data-slide="10">
  <div class="gradient-mesh">
    <div class="blob" style="width: 330px; height: 330px; top: -80px; right: -80px; background: var(--color-accent-1); opacity: 0.08;"></div>
    <div class="blob" style="width: 230px; height: 230px; bottom: -50px; left: -20px; background: var(--color-accent-2); opacity: 0.06;"></div>
  </div>

  <div class="content max-w-[1040px]">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Executive summary</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-8 reveal">Lo más importante en cuatro hallazgos</h2>

    <div class="space-y-4">
      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 border-l-4 border-l-accent-1 reveal">
        <h3 class="text-xl font-semibold text-text mb-2">La demanda creció antes que la oferta</h3>
        <p class="text-base leading-relaxed text-text-secondary">Eso explica presión en precios, saturación de onboarding y oportunidad para capturar margen adicional.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 border-l-4 border-l-accent-2 reveal">
        <h3 class="text-xl font-semibold text-text mb-2">El canal enterprise muestra mejor retención</h3>
        <p class="text-base leading-relaxed text-text-secondary">Aunque el ciclo de venta es más largo, el payback es más estable y el churn cae de forma significativa.</p>
      </article>

      <article class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 border-l-4 border-l-accent-3 reveal">
        <h3 class="text-xl font-semibold text-text mb-2">El principal cuello de botella es operacional</h3>
        <p class="text-base leading-relaxed text-text-secondary">No es un problema de demanda ni de pricing; es de capacidad para absorber más clientes sin degradar servicio.</p>
      </article>
    </div>
  </div>
</div>
```

### Nota de estilo

Aquí sí puede haber un poco más de texto, pero cada card sigue siendo corta.

***

## Template 12 — Vertical Timeline

### Cuándo usarla

Para hitos, roadmap, evolución temporal, historia de producto o secuencia de eventos.

### Objetivo narrativo

Introducir orden temporal y progresión.

### Límites

- Máximo 5 nodos.
- Cada nodo: fecha o periodo + una explicación breve.

### HTML base

```html
<div class="slide slide-11" data-slide="11">
  <div class="gradient-mesh">
    <div class="blob" style="width: 320px; height: 320px; top: -70px; right: -70px; background: var(--color-accent-1); opacity: 0.07;"></div>
    <div class="blob" style="width: 220px; height: 220px; bottom: -50px; left: -20px; background: var(--color-accent-2); opacity: 0.05;"></div>
  </div>

  <div class="content max-w-[980px]">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Timeline</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-10 reveal">Cómo evolucionó la historia</h2>

    <div class="relative pl-12">
      <div class="absolute left-[11px] top-2 bottom-2 w-[2px] bg-linear-to-b from-accent-1 via-accent-2 to-accent-3"></div>

      <div class="relative mb-8 reveal">
        <div class="absolute left-[-1px] top-1 w-6 h-6 rounded-full bg-accent-1 shadow-[0_0_20px_rgba(255,255,255,0.25)]"></div>
        <p class="text-sm uppercase tracking-[0.16em] text-text-muted mb-2">Q1 2025</p>
        <h3 class="text-xl font-semibold text-text mb-2">Lanzamiento inicial</h3>
        <p class="text-base leading-relaxed text-text-secondary">Se validó la propuesta con los primeros clientes de diseño.</p>
      </div>

      <div class="relative mb-8 reveal">
        <div class="absolute left-[-1px] top-1 w-6 h-6 rounded-full bg-accent-2 shadow-[0_0_20px_rgba(255,255,255,0.25)]"></div>
        <p class="text-sm uppercase tracking-[0.16em] text-text-muted mb-2">Q3 2025</p>
        <h3 class="text-xl font-semibold text-text mb-2">Escalamiento comercial</h3>
        <p class="text-base leading-relaxed text-text-secondary">La distribución empezó a acelerarse por partnerships y outbound especializado.</p>
      </div>
    </div>
  </div>
</div>
```

### Cuándo es mejor que bullets

Cuando el orden de los eventos cambia totalmente la interpretación.

***

## Template 13 — Stat Cards + Horizontal Bar Chart

### Cuándo usarla

Cuando se necesita combinar contexto ejecutivo arriba y comparación cuantitativa abajo.

### Objetivo narrativo

Dar una lectura rápida y luego profundizar con una comparación visual inmediata.

### Estructura

- Fila superior: 3 stats.
- Parte inferior: 3 a 5 barras horizontales.

### HTML base

```html
<div class="slide slide-12" data-slide="12">
  <div class="gradient-mesh">
    <div class="blob" style="width: 350px; height: 350px; top: -80px; right: -80px; background: var(--color-accent-1); opacity: 0.09;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -40px; left: -20px; background: var(--color-accent-2); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Performance</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-8 reveal">El resumen ejecutivo y la comparación detrás</h2>

    <div class="grid grid-cols-3 gap-5 mb-10">
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">Revenue</div>
        <div class="text-4xl font-black text-accent-1">$28M</div>
      </div>
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">Growth</div>
        <div class="text-4xl font-black text-accent-2">42%</div>
      </div>
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">Retention</div>
        <div class="text-4xl font-black text-accent-3">89%</div>
      </div>
    </div>

    <div class="space-y-4">
      <div class="bar-row reveal">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-[140px] text-sm text-text-secondary">Enterprise</div>
          <div class="flex-1 h-7 rounded-full bg-glass-bg border border-glass-border overflow-hidden">
            <div class="bar-fill h-full rounded-full bg-linear-to-r from-accent-1 to-accent-2" data-width="92"></div>
          </div>
          <div class="w-[56px] text-right text-sm text-text">92%</div>
        </div>
      </div>

      <div class="bar-row reveal">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-[140px] text-sm text-text-secondary">Mid-market</div>
          <div class="flex-1 h-7 rounded-full bg-glass-bg border border-glass-border overflow-hidden">
            <div class="bar-fill h-full rounded-full bg-linear-to-r from-accent-2 to-accent-3" data-width="76"></div>
          </div>
          <div class="w-[56px] text-right text-sm text-text">76%</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Cuándo usarla

- Benchmarks entre segmentos.
- Comparaciones entre líneas de producto.
- Canales o regiones.

***

## Template 14 — Fact List with Emoji / Icon Row

### Cuándo usarla

Cuando una lista necesita más personalidad visual que un bullet estándar, pero todavía no justifica cards completas.

### Objetivo narrativo

Dar ritmo y diferenciación ligera entre puntos.

### HTML base

```html
<div class="slide slide-13" data-slide="13">
  <div class="gradient-mesh">
    <div class="blob" style="width: 310px; height: 310px; top: -60px; right: -60px; background: var(--color-accent-1); opacity: 0.07;"></div>
    <div class="blob" style="width: 230px; height: 230px; bottom: -40px; left: -20px; background: var(--color-accent-2); opacity: 0.05;"></div>
  </div>

  <div class="content max-w-[980px]">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Highlights</p>
    <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-8 reveal">Cuatro hechos rápidos que vale la pena recordar</h2>

    <div class="space-y-4">
      <div class="flex gap-4 items-start rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-5 reveal">
        <div class="text-[1.8rem] shrink-0">🌍</div>
        <p class="text-base leading-relaxed text-text-secondary">La expansión internacional se concentra en menos mercados, pero con mejor rendimiento unitario.</p>
      </div>

      <div class="flex gap-4 items-start rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-5 reveal">
        <div class="text-[1.8rem] shrink-0">🧪</div>
        <p class="text-base leading-relaxed text-text-secondary">Los experimentos con pricing muestran mayor elasticidad positiva en el segmento SMB.</p>
      </div>
    </div>
  </div>
</div>
```

### Diferencia frente al Template 04

Este template es más expresivo y táctil. Sirve mejor cuando cada punto tiene identidad propia.

***

## Template 15 — Thank You / Closing Cinemática

### Cuándo usarla

Siempre como cierre del deck, salvo que el deck cierre con CTA operativo o contactos en otro formato.

### Objetivo narrativo

Cerrar con una sensación de acabado, energía o memorabilidad.

### Estructura

- Hero visual.
- Mensaje corto.
- Línea final opcional: contacto, CTA o llamada a preguntas.
- `particle-canvas` recomendado.

### HTML base

```html
<div class="slide slide-14" data-slide="14">
  <div class="gradient-mesh">
    <div class="blob" style="width: 520px; height: 520px; top: -140px; right: -120px; background: var(--color-accent-1); opacity: 0.15;"></div>
    <div class="blob" style="width: 320px; height: 320px; bottom: -80px; left: -60px; background: var(--color-accent-2); opacity: 0.12;"></div>
    <div class="blob" style="width: 200px; height: 200px; top: 44%; left: 16%; background: var(--color-accent-3); opacity: 0.10;"></div>
  </div>

  <canvas class="particle-canvas" style="position:absolute; inset:0; z-index:1;"></canvas>

  <div class="content text-center">
    <div class="text-[120px] mb-6 animate-[float_3s_ease-in-out_infinite] reveal">✨</div>
    <h2 class="font-display text-[clamp(2.8rem,6vw,5rem)] font-black tracking-tight mb-4 reveal bg-linear-to-br from-accent-1 via-accent-2 to-accent-1 bg-clip-text text-transparent">
      Gracias
    </h2>
    <p class="text-[clamp(1rem,1.4vw,1.25rem)] uppercase tracking-[0.28em] text-text-muted reveal">
      Preguntas, conversación o próximos pasos
    </p>
  </div>
</div>
```

### Variantes útiles

- “Questions”
- “Let’s build this”
- “Next steps”
- “Gracias / <contacto@dominio.com>”

***

## Template 16 — Interactive / Data Visualization Slide

### Cuándo usarla

Cuando el mensaje exige una visualización más elaborada: donut, radar, heatmap, línea, gauge, odometer o barras animadas.

### Objetivo narrativo

Convertir datos en evidencia visual sin perder legibilidad.

### Regla principal

La visualización no es decoración. Debe responder una pregunta concreta.

### Subtipos recomendados

- Donut → composición o share.
- Bar chart → ranking o comparación.
- Line chart → evolución temporal.
- Radar → comparación multidimensional.
- Heatmap → intensidad por matriz.
- Gauge → progreso o score.
- Odometer → cifra hero animada.

### Ejemplo A — Donut + insight lateral

```html
<div class="slide slide-15" data-slide="15">
  <div class="gradient-mesh">
    <div class="blob" style="width: 330px; height: 330px; top: -70px; right: -70px; background: var(--color-accent-1); opacity: 0.09;"></div>
    <div class="blob" style="width: 240px; height: 240px; bottom: -50px; left: -20px; background: var(--color-accent-2); opacity: 0.06;"></div>
  </div>

  <div class="content">
    <div class="grid grid-cols-2 gap-12 items-center">
      <div>
        <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Share</p>
        <h2 class="font-display text-[clamp(2rem,4vw,3rem)] font-bold text-text mb-4 reveal">La mayor parte del valor viene de un solo segmento</h2>
        <p class="text-base leading-relaxed text-text-secondary reveal">La composición no está distribuida uniformemente; el liderazgo depende de una categoría dominante.</p>
      </div>

      <div class="flex items-center justify-center reveal">
        <svg width="260" height="260" viewBox="0 0 100 100" class="overflow-visible">
          <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="10"></circle>
          <circle
            class="donut-ring"
            data-percent="72"
            cx="50" cy="50" r="40"
            fill="none"
            stroke="url(#donutGrad)"
            stroke-width="10"
            transform="rotate(-90 50 50)"
          ></circle>
          <defs>
            <linearGradient id="donutGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="var(--color-accent-1)"></stop>
              <stop offset="100%" stop-color="var(--color-accent-2)"></stop>
            </linearGradient>
          </defs>
          <text x="50" y="48" text-anchor="middle" class="fill-current text-text" style="font-size: 14px;">Dominio</text>
          <text x="50" y="60" text-anchor="middle" class="fill-current text-accent-1" style="font-size: 18px; font-weight: 800;">72%</text>
        </svg>
      </div>
    </div>
  </div>
</div>
```

### Ejemplo B — Heatmap simple

```html
<div class="heatmap-grid grid-cols-4 reveal" style="grid-template-columns: repeat(4, 1fr);">
  <div class="heatmap-cell rounded-xl" style="background: color-mix(in srgb, var(--color-accent-1) 22%, transparent);">81</div>
  <div class="heatmap-cell rounded-xl" style="background: color-mix(in srgb, var(--color-accent-1) 48%, transparent);">92</div>
  <div class="heatmap-cell rounded-xl" style="background: color-mix(in srgb, var(--color-accent-2) 34%, transparent);">67</div>
  <div class="heatmap-cell rounded-xl" style="background: color-mix(in srgb, var(--color-accent-3) 18%, transparent);">54</div>
</div>
```

### Ejemplo C — Odometer hero

```html
<div class="text-[clamp(3rem,7vw,6rem)] font-black text-accent-1 reveal">
  <span class="odometer" data-value="247" data-suffix="%"></span>
</div>
```

### Cuándo dividir

Si un gráfico necesita leyenda compleja, múltiples explicaciones y además bullets, probablemente requiere dos slides:

- una de chart,
- y otra de interpretación.

***

## Plantillas auxiliares recomendadas

Además de las 16 principales, el skill puede derivar subvariantes de manera controlada.

### A. Section Divider

Útil en decks largos, entre bloques mayores.

```html
<div class="slide slide-N" data-slide="N">
  <div class="gradient-mesh">
    <div class="blob" style="width: 440px; height: 440px; top: -100px; right: -80px; background: var(--color-accent-1); opacity: 0.12;"></div>
    <div class="blob" style="width: 300px; height: 300px; bottom: -70px; left: -40px; background: var(--color-accent-2); opacity: 0.10;"></div>
  </div>
  <canvas class="particle-canvas-ambient" style="position:absolute; inset:0; z-index:1;"></canvas>
  <div class="content text-center">
    <p class="text-sm uppercase tracking-[0.28em] text-text-muted mb-4 reveal">Section</p>
    <h2 class="font-display text-[clamp(2.4rem,5vw,4rem)] font-bold text-text reveal">Nombre de la sección</h2>
  </div>
</div>
```

### B. Quote / Pull Quote

Útil para narrativa, cultura, testimonio o visión.

```html
<div class="slide slide-N" data-slide="N">
  <div class="gradient-mesh">
    <div class="blob" style="width: 320px; height: 320px; top: -60px; right: -60px; background: var(--color-accent-1); opacity: 0.07;"></div>
    <div class="blob" style="width: 220px; height: 220px; bottom: -40px; left: -20px; background: var(--color-accent-2); opacity: 0.05;"></div>
  </div>
  <div class="content text-center max-w-[980px]">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-6 reveal">Quote</p>
    <blockquote class="font-display text-[clamp(2rem,4.5vw,3.6rem)] leading-tight text-text italic mb-6 reveal">
      “Una frase potente que justifique tener una slide propia.”
    </blockquote>
    <p class="text-base text-text-secondary reveal">Nombre — Cargo o fuente</p>
  </div>
</div>
```

### C. CTA / Next Steps

Ideal si el deck termina con acciones concretas.

```html
<div class="slide slide-N" data-slide="N">
  <div class="gradient-mesh">
    <div class="blob" style="width: 400px; height: 400px; top: -100px; right: -100px; background: var(--color-accent-1); opacity: 0.12;"></div>
    <div class="blob" style="width: 260px; height: 260px; bottom: -60px; left: -30px; background: var(--color-accent-2); opacity: 0.10;"></div>
  </div>
  <div class="content text-center max-w-[980px]">
    <p class="text-sm uppercase tracking-[0.24em] text-text-muted mb-4 reveal">Next steps</p>
    <h2 class="font-display text-[clamp(2.3rem,5vw,4rem)] font-bold text-text mb-8 reveal">Qué debería pasar ahora</h2>
    <div class="grid grid-cols-3 gap-5 text-left">
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">1</div>
        <h3 class="text-xl font-semibold text-text mb-2">Decidir</h3>
        <p class="text-sm text-text-secondary">Alinear criterio y aprobar dirección.</p>
      </div>
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">2</div>
        <h3 class="text-xl font-semibold text-text mb-2">Diseñar</h3>
        <p class="text-sm text-text-secondary">Bajar el plan a responsables y fechas.</p>
      </div>
      <div class="rounded-3xl border border-glass-border bg-glass-bg backdrop-blur-xl p-6 reveal">
        <div class="text-sm uppercase tracking-[0.18em] text-text-muted mb-2">3</div>
        <h3 class="text-xl font-semibold text-text mb-2">Ejecutar</h3>
        <p class="text-sm text-text-secondary">Lanzar el primer ciclo de implementación.</p>
      </div>
    </div>
  </div>
</div>
```

***

## Reglas de selección automática por forma del contenido

### Si el input contiene

#### 1. Un heading principal y un subtítulo corto

- Usar **Template 01** o **02**.

#### 2. Una lista de 3 puntos cortos y equivalentes

- Usar **Template 07**.

#### 3. Una lista de 6 elementos homogéneos

- Usar **Template 08**.

#### 4. Dos bloques claramente opuestos

- Usar **Template 06**.

#### 5. Fechas o hitos cronológicos

- Usar **Template 12**.

#### 6. Tres métricas que dominan la historia

- Usar **Template 10**.

#### 7. Una tabla con una dimensión dominante comparativa

- Convertir a **Template 13** o **16**.

#### 8. Una frase especialmente fuerte o cita

- Considerar subvariante **Quote / Pull Quote**.

***

## Adaptación por propósito del deck

### Pitch deck

Favorecer:

- 01, 03, 07, 09, 10, 13, CTA.

### Teaching / tutorial

Favorecer:

- 02, 04, 05, 12, 14, 16.

### Conference / keynote

Favorecer:

- 01, 05, 10, 12, Quote, 15.

### Internal / strategy

Favorecer:

- 02, 03, 06, 09, 11, 13, CTA.

***

## Adaptación por densidad del material fuente

### Fuente muy densa

Ejemplos: PDF largos, informes técnicos, documentos estratégicos.

Estrategia:

- resumir primero,
- usar más slides de tipo 11, 12, 13 y 16,
- evitar grids de 6 cards salvo que haya taxonomía clara.

### Fuente media

Ejemplos: memo corto, article largo, brief comercial.

Estrategia:

- combinar 04, 05, 07, 09, 10 y 12.

### Fuente ligera

Ejemplos: notas, Markdown corto, prompt textual.

Estrategia:

- usar slides visuales con más aire,
- menos agenda,
- más callouts y structure slides.

***

## Reglas de animación por plantilla

### Todas las plantillas

Todo elemento importante lleva `.reveal`.

### Plantillas que deben tener `particle-canvas`

- 01 Title Cinemática
- 15 Thank You / Closing
- Section Divider opcional fuerte

### Plantillas que se benefician de `hover`

- 06 Two-column cards
- 07 Three-card grid
- 08 Six-card grid
- 09 Metric grid
- CTA / Next Steps

### Plantillas con animación de datos

- 09 con `data-count`
- 10 con glow o count-up
- 13 con `.bar-fill[data-width]`
- 16 con `.donut-ring`, `.odometer`, `.line-path`, etc.

***

## Reglas de accesibilidad

Todas las plantillas deben respetar lo siguiente:

- texto suficientemente contrastado,
- alt text en imágenes,
- no depender solo del color para jerarquía,
- headings reales y en orden,
- tamaño legible,
- navegación por teclado intacta,
- reducción de motion si el sistema lo pide.

### Imágenes

Toda imagen debe incluir:

```html
<img src="..." alt="Descripción útil" />
```

### Botones o controles interactivos internos

Si existieran dentro de la slide, usar `aria-label` cuando el contenido visual no sea suficiente.

***

## Anti-patrones por plantilla

### Nunca hacer esto

- Meter 8 bullets en Template 04.
- Hacer 4 columnas en un split pensado para 2.
- Usar Template 08 con cards larguísimas.
- Usar una timeline cuando la secuencia temporal no importa.
- Usar glow extremo en decks clínicos o institucionales.
- Meter un chart complejo en una card minúscula.
- Poner body text centrado salvo en portada, quote o cierre.

### Señales de que elegiste mal la plantilla

- Tienes que reducir la tipografía demasiado.
- El contenido compite consigo mismo.
- La slide necesita un subtítulo para explicar qué se supone que estoy viendo.
- Hay más de un foco visual fuerte.

***

## Checklist de QA para 05-slide-templates

Antes de usar cualquier plantilla en producción, verificar:

- [ ] La plantilla cabe en viewport sin scroll.
- [ ] El heading no supera el límite recomendado.
- [ ] Hay solo una idea principal.
- [ ] Los elementos clave tienen `.reveal`.
- [ ] El grid usado es CSS Grid cuando hay cards múltiples.
- [ ] Los blobs no interfieren con la lectura.
- [ ] Los colores provienen de tokens del tema.
- [ ] Las cards de una misma fila comparten padding y altura visual comparable.
- [ ] El texto secundario no excede 4 líneas por bloque.
- [ ] Si hay chart, responde una pregunta concreta.

***

## Convención de naming sugerida

Para facilitar mapeo interno, se recomienda esta nomenclatura:

| Nombre lógico | Template |
|---|---|
| `title-hero` | 01 |
| `title-corporate` | 02 |
| `agenda-grid` | 03 |
| `bullet-list` | 04 |
| `split-visual` | 05 |
| `compare-two` | 06 |
| `three-pillars` | 07 |
| `six-features` | 08 |
| `metric-grid` | 09 |
| `stat-callout` | 10 |
| `executive-summary` | 11 |
| `vertical-timeline` | 12 |
| `stats-bars` | 13 |
| `fact-list-icons` | 14 |
| `closing-hero` | 15 |
| `interactive-dataviz` | 16 |

***

## Qué debe hacer el motor con este archivo

Este archivo no solo describe layouts; define comportamiento generativo.

El motor debe:

1. Detectar la forma del contenido.
2. Elegir la plantilla más clara.
3. Aplicar restricciones de densidad.
4. Inyectar contenido en la estructura HTML.
5. Ajustar la variante visual según el tema.
6. Dividir en múltiples slides si hace falta.
7. Preservar consistencia narrativa y visual entre slides consecutivas.

Cuando exista duda entre dos plantillas, debe priorizar:

1. legibilidad,
2. claridad del mensaje,
3. jerarquía visual,
4. y recién después impacto estético.

***

## Resultado esperado

Si este archivo se implementa correctamente, el skill podrá:

- transformar documentos largos en decks mucho más claros,
- mantener una línea visual consistente,
- evitar slides sobrecargadas,
- y convertir datos o texto plano en presentaciones que se sientan profesionales de verdad.
