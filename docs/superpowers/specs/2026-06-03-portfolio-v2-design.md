# Portfolio v2 — design

**Author:** Lahari Karumanchi (paired w/ Claude)
**Date:** 2026-06-03
**Status:** Design — ready to plan
**Replaces:** the current minimal-academic design shipped through PR #1–#9 (May–June 2026)

## 1. Context

The portfolio site at <https://laharikarumanchi.vercel.app> ships today as a
minimal-academic Astro app: 680px content column, Iowan Old Style serif
headings, warm-gold accent. Five project case studies live in
`src/content/projects/*.mdx`, two of which (data-analysis-agent,
document-qa-rag) have been expanded to ~700 words. The other three are
~300-word stubs. A real `/projects/` index page exists; the home page shows
a featured card + two compact teasers.

This works as a v1, but a single 8-second recruiter scan today returns:
"engineering-blog vibe, light on demonstrated depth, no clear category in
the AI/ML tooling landscape." The user wants to pivot to a **tech-company
aesthetic** that lands a stronger product-engineering signal, plus
**engineering deep-dives** (5–6 sections × 1000–1500 words each) per
project, plus **test-cases** as a first-class section.

This spec defines the v2 redesign + content expansion as a pilot on the
data-analysis-agent project, with a deliberate pause before replicating
the pattern across the remaining four projects.

## 2. Locked-in decisions

These were chosen through 6 visual + textual clarifying questions during
brainstorming. Decisions are listed in dependency order — each one
constrains the ones below it.

| Decision | Choice | Rejected alternatives |
|---|---|---|
| **Sequencing** | All 5 projects, sequentially, DA Agent first | Single project only; parallel writing of all 5 |
| **Aesthetic vocabulary** | Stripe-style — gradient mesh, glassy chrome, Inter heavy weights, 8px radii | Vercel mono-minimal; hybrid (Vercel structure + Stripe accent) |
| **Color palette** | Aurora — mint / sky / violet (cool, ML-research signal) | Stripe-classic pink/purple/blue; Sunset coral/rose/amber; Indigo violet/cyan |
| **Deep-dive structure** | Hybrid: blog narrative + paper rigor (8 sections, ~7,500 words/project) | Engineering blog only; pure research paper; consulting case study |
| **Test cases** | Both — worked examples (own section) + pytest summary (subsection inside Architecture) | Worked examples only; pytest summary only |
| **Landing page structure** | Standard 7 sections (current 6 + new metrics strip) | Minimal 4 sections; maximal 9 (with testimonials + contact CTA) |
| **Deep-dive page layout** | Sticky TOC sidebar — 240px aside + 720px text column = 1100px shell | Single 720px text column |
| **Implementation approach** | Incremental PRs on `feat/v2` branch (9 PRs total) | One big redesign PR; parallel `/v2/*` routes |

### 2.1 Net visual identity

Aurora + Stripe-mesh chrome = "design-polished ML research." The palette
(mint, sky, violet, teal accent) reads cool and serious; the chrome
(gradient mesh backdrops, glassy buttons, soft rounded corners) reads
modern and shipped. Closest reference points in the wild: Anthropic
marketing pages, Linear documentation, Pinecone landing.

## 3. Design

### 3.1 Design tokens

Replace the current minimal-academic token set in `src/styles/global.css`:

```css
:root {
  /* Greyscale */
  --ink:   #0a0a0a;    /* was: #1a1a1a */
  --paper: #ffffff;    /* was: #fafaf7 */
  --muted: #525252;    /* was: #555    */
  --rule:  #e5e5e5;    /* was: #d8d8d3 */
  --hover: rgba(10, 10, 10, 0.04);

  /* Aurora accents */
  --accent-mint:        #a7f3d0;
  --accent-sky:         #93c5fd;
  --accent-violet:      #c4b5fd;
  --accent-teal:        #0d9488;   /* primary action + link color */
  --accent-violet-deep: #7c3aed;   /* secondary action / TOC active highlight */

  /* The signature gradient — used on hero, featured card backdrop, CTA blocks */
  --gradient-hero:
    radial-gradient(at 20% 30%, var(--accent-mint)   0%, transparent 55%),
    radial-gradient(at 80% 20%, var(--accent-sky)    0%, transparent 55%),
    radial-gradient(at 60% 80%, var(--accent-violet) 0%, transparent 55%),
    linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);

  /* Typography — serif retired */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;

  /* Widths */
  --content-width:  720px;    /* was: 680px — slightly wider text */
  --shell-width:    1200px;   /* NEW — landing-page sections */
  --shell-deepdive: 1100px;   /* NEW — TOC + text + gutter */

  /* Radii — softer */
  --radius:    8px;           /* was: 4px */
  --radius-sm: 6px;

  /* Spacing scale unchanged */
}
```

**Retired entirely (do not preserve):**

- The Iowan Old Style / Charter / Georgia serif font stack
- `--accent-cream`, `--accent-cream-edge`, `--accent-gold` (warm accent system)
- The `.numbered-sections` CSS counter that auto-numbers `01.` / `02.` / etc.
- `.hero-rule` decorative `§` rule on the landing hero

**Typography rules:**

- Body: Inter 400, 17px, line-height 1.65
- H1: Inter 700, 60px (landing), 48px (deep-dive), letter-spacing −0.02em
- H2: Inter 700, 32px, letter-spacing −0.015em
- H3: Inter 600, 22px
- Eyebrow / monospace metadata: JetBrains Mono 11px, uppercase, letter-spacing 0.12em
- Code blocks: JetBrains Mono 14px on `#0a0a0a` background with syntax highlighting (Shiki, github-dark-dimmed theme)

**Font loading:** self-hosted via `@fontsource/inter` and
`@fontsource/jetbrains-mono` npm packages. No Google Fonts CDN
(performance + privacy).

### 3.2 Layout primitives

Three reusable shell widths:

| Class | Width | Used for |
|---|---|---|
| `.shell-wide` | 1200px (max) | Landing-page sections (hero, metrics strip, featured block, projects grid) |
| `.shell-text` | 720px (max) | Blog posts, About page, narrow reading content |
| `.shell-deepdive` | 1100px (max) | Project deep-dive pages: 240px sticky TOC + 720px text column + 140px gutter |

All shells center-align with `margin-inline: auto` and use a fluid padding
clamp for sub-720px viewports.

### 3.3 New components

```
src/components/
  Hero.astro                 # EXISTING — restyled, gradient mesh background
  Nav.astro                  # EXISTING — restyled, no border-bottom, sticky w/ backdrop-blur
  MetricsStrip.astro         # NEW — landing-page stat row
  ProjectCard.astro          # EXISTING — restyled, mesh backdrop on featured variant
  ProjectHero.astro          # NEW — eyebrow + h1 + headline number + meta strip
                             #       (used at top of every deep-dive page)
  TocSidebar.astro           # NEW — sticky aside, reads MDX headings,
                             #       IntersectionObserver-driven active state
  PostCard.astro             # EXISTING — restyled
  Footer.astro               # EXISTING — restyled

src/layouts/
  BaseLayout.astro           # EXISTING — token swap only
  BlogLayout.astro           # EXISTING — token swap only
  ProjectLayout.astro        # EXISTING — kept temporarily for non-v2 projects
  ProjectLayout-v2.astro     # NEW — TOC sidebar + ProjectHero + 1100px shell
```

#### 3.3.1 `MetricsStrip.astro`

One-line strip below the hero:

```
5 projects · 33 tests passing · 75% ABQ on DABench · graduating 2027
```

Monospace numerals (`font-variant-numeric: tabular-nums`), slate-700 text,
muted dividers between items. Source values come from a single constants
file `src/data/metrics.ts` so they can update in one place.

#### 3.3.2 `ProjectHero.astro`

Used at the top of every deep-dive page:

```
[eyebrow]    AGENTS · 2026 · SHIPPED
[h1]         Data Analysis Agent
[subtitle]   A code-as-action agent that answers questions about CSV data…
[metric]     75% ABQ on InfiAgent-DABench (9-task pilot)
[meta]       📖 28 min read · ⚙ updated 2026-06-03
[chips]      Python · jupyter_client · Groq · Llama-3.3 · Streamlit
[buttons]    [Code →]  [Live demo →]
```

The `eyebrow` reads from new frontmatter (`category` + `year` + `status`).
The `meta` reads from new frontmatter (`readTimeMinutes` + `lastUpdated`).
Both fall back gracefully when fields are absent.

#### 3.3.3 `TocSidebar.astro`

```astro
---
import type { MarkdownHeading } from 'astro';
interface Props { headings: MarkdownHeading[]; }
const { headings } = Astro.props;
---
<aside class="toc-sidebar">
  <p class="toc-title">On this page</p>
  <ol>
    {headings.filter(h => h.depth === 2 || h.depth === 3).map(h => (
      <li class={`toc-link toc-depth-${h.depth}`}>
        <a href={`#${h.slug}`} data-toc-slug={h.slug}>{h.text}</a>
      </li>
    ))}
  </ol>
  <hr/>
  <slot name="actions" />  {/* Optional: GitHub + demo buttons */}
</aside>

<script>
  // IntersectionObserver: ~30 lines client-side
  // Watches every <section data-toc-slug> and toggles aria-current="location"
  // on the matching TOC link. Smooth-scroll on click via scroll-behavior: smooth.
</script>
```

The MDX heading list is passed in by the parent `ProjectLayout-v2.astro`
via Astro's `render()` API:

```astro
const { Content, headings } = await render(entry);
<ProjectLayout-v2 entry={entry} headings={headings}>
  <Content />
</ProjectLayout-v2>
```

### 3.4 Content collection schema additions

`src/content.config.ts`:

```ts
import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/projects' }),
  schema: z.object({
    // Existing fields
    title:          z.string(),
    oneLiner:       z.string(),
    headlineNumber: z.string(),
    techStack:      z.array(z.string()),
    year:           z.number(),
    githubUrl:      z.string().optional(),
    demoUrl:        z.string().optional(),
    featured:       z.boolean().default(false),
    order:          z.number(),

    // NEW v2 fields
    category:        z.enum(['Agents', 'RAG', 'Classical ML']),
    status:          z.enum(['shipped', 'in-progress']).default('shipped'),
    lastUpdated:     z.date().optional(),
    readTimeMinutes: z.number().int().positive().optional(),

    // Migration flag — temporary, removed in PR #9
    v2:              z.boolean().default(false),
  }),
});
```

**Migration:** All 5 existing MDX files need a `category` field added in PR
#3 (it's required). The other v2 fields are optional and added per-project
as each is upgraded.

### 3.5 Landing page structure

`src/pages/index.astro` — 7 sections, top to bottom:

| # | Section | Shell | Notes |
|---|---|---|---|
| 1 | Hero | wide | 60px Inter name, tagline, 2 buttons (teal primary / outline secondary). `--gradient-hero` fills the section background. |
| 2 | **Metrics strip** ← NEW | wide | `5 projects · 33 tests passing · 75% ABQ on DABench · graduating 2027` |
| 3 | Featured | wide | DA Agent card with subtle `--gradient-hero` backdrop. Headline number prominent. |
| 4 | Selected work | text | 2 compact teasers + "See all 5 projects →" pill button |
| 5 | What I work with | text | Restyled chip grid: rounded-full, slate-100 bg, slate-700 text. Category labels (Languages / ML+data / Tools / Areas) stay. |
| 6 | Recent writing | text | 2 PostCards |
| 7 | About | text | Short bio paragraph + teal "Download résumé →" button |

The `<div class="numbered-sections">` wrapper is dropped — Stripe-style
sites don't number sections. Hierarchy comes from gradient backdrops +
spacing instead.

### 3.6 Deep-dive page layout

`src/layouts/ProjectLayout-v2.astro`:

```
┌── Nav (sticky, backdrop-blur) ───────────────────────────┐
├── ProjectHero (full-width, subtle mesh) ─────────────────┤
│   eyebrow · h1 · subtitle · headline · meta · chips · CTAs
├── shell-deepdive (1100px) ───────────────────────────────┤
│   ┌── aside.toc-sidebar (240px, sticky) ──┐ ┌── main ────┐
│   │ ON THIS PAGE                          │ │            │
│   │   TL;DR                               │ │  rendered  │
│   │   Problem                             │ │  MDX,      │
│   │   Approach                            │ │  720px     │
│   │   Worked examples                     │ │  text col  │
│   │   Architecture                        │ │            │
│   │     · Test suite                      │ │  prose     │
│   │   Evaluation ●                        │ │  styles    │
│   │   Limitations                         │ │  via       │
│   │   What I'd do differently             │ │  :where()  │
│   │   ──────                              │ │            │
│   │   📦 GitHub                           │ │            │
│   │   🟢 Live demo                        │ │            │
│   └───────────────────────────────────────┘ └────────────┘
├── Footer ────────────────────────────────────────────────┤
```

**Prose styles (scoped to `.shell-deepdive main`):**

- H2: Inter 700, 32px, scroll-margin-top: 80px (so anchored jumps clear the sticky nav)
- H3: Inter 600, 22px
- Code blocks: Shiki `github-dark-dimmed`, JetBrains Mono 14px, 8px border-radius
- Inline code: slate-100 bg, slate-900 text, 4px padding
- Blockquote: teal-400 left border, slate-700 italic text
- Tables: full-width, slate-200 borders, header row slate-50 bg
- Images / SVG diagrams: max-width 100%, 1px slate-200 border, 8px radius

**Mobile (≤ 768px):** The sticky TOC sidebar collapses into a `<details>`
disclosure at the top of the page: `<summary>Jump to section</summary>`
followed by the same link list. Main text column becomes full-width.

### 3.7 DA Agent MDX content outline (the pilot)

`src/content/projects/data-analysis-agent.mdx` — 8 sections, ~7,800 words total.

Frontmatter additions:

```yaml
category: Agents
status: shipped
lastUpdated: 2026-06-03
readTimeMinutes: 28
v2: true
```

Section-by-section:

| # | Section | Words | Key content |
|---|---|---|---|
| 1 | **TL;DR** | 200 | One paragraph framing: the agent, the result, the caveat. Pull quote with the 75% ABQ headline. CTAs: Code + Live demo. |
| 2 | **Problem** | 1000 | Why tabular Q&A is a poor fit for chat LLMs. Why ReAct tool-call agents explode on multi-step pandas pipelines. The unaddressed gap: a model that thinks in code like a data analyst, cell by cell. Why InfiAgent-DABench specifically (real questions, official scorer with `@name[value]` regex extraction, gold labels). What "honest evaluation" means here. |
| 3 | **Approach** | 1200 | Code-as-action loop in plain English: model emits `<code>…</code>` → kernel runs → stdout/stderr/figures flow back → repeats until `<answer>…</answer>` or 10-step ceiling. Why no LangChain / LlamaIndex / CrewAI (~150 lines does it; frameworks hide behaviors I needed to debug: retry budgets, malformed-output recovery, step limits). Deliberate choices: real Jupyter sandbox (not `subprocess.run`), single per-cell deadline, matplotlib via IOPub PNG, provider abstraction, official InfiAgent scorer copied with attribution. End with a 2-step trace from a real iris.csv run. |
| 4 | **Worked examples** | 1000 | 5–6 real queries across the 3 vetted datasets: median sepal_length (iris), avg tip% by day (tips), fare-vs-class correlation (titanic), …. For each: the question → agent's first cell → output/figure → reasoning → final `@name[value]`. Include **one self-correction** example (agent recovers after `NameError`) and **one honest failure** (where it gets the answer wrong despite the loop). |
| 5 | **Architecture** | 1200 | ASCII→SVG architecture diagram from the README (`agent.svg`). Module-by-module walkthrough: `llm_client.py`, `sandbox.py`, `orchestrator.py`, `trace.py`, `eval/run_dabench.py`. The non-obvious bits: `wait_for_ready()` so first execute doesn't race kernel `status: busy`, deadline-based `get_msg` loop, drain-after-interrupt, `matplotlib.use('Agg')` inside the kernel. `LLMClient` interface (3 methods, swap implementations for Groq vs Gemini). Retry budget: Groq's 5-attempt `Retry-After`-aware backoff; Gemini's 15 RPM per-call throttle. |
| 5a | **Test suite** (subsection of Architecture) | 400 | Table: 6 test files × what each covers (sandbox lifecycle, LLM retry/backoff/key-scrub, orchestrator parsing + helpers, trace JSON, end-to-end with scripted mock LLM, eval loader/scorer integration). 33 tests total, all green. One representative pytest snippet (likely `test_sandbox_timeout_drains_messages` — shows the subtle behavior). CI badge link. |
| 6 | **Evaluation** | 1500 | Dataset: InfiAgent-DABench (257 closed-form questions, official labels, `@name[value]` schema). Why DABench, not WikiSQL or Spider. Scorer: official `eval_closed_form.py` copied from InfiAgent (with attribution headers). Models tested: Llama-3.3-70B via Groq + Gemini-2.0-Flash via Google AI Studio. Setup: 10-step ceiling, retry-on, kernel reuse across turns, throttling tuned per provider. Results table (Llama 9/80 → 75%; Gemini 50/50 → key-format + quota issue; planned retry-off ablation). The `/80 not /257` caveat (free-tier rate-limit budget). Latency breakdown: LLM time dominates, sandbox is ~5% per turn. |
| 7 | **Limitations** | 800 | Quota-bounded headline (would need paid tier or multi-day run for full 257). Local-only public demo — RCE-on-a-platter without Docker isolation, vetted-CSVs-only fallback ships safely but not deployed yet. No fine-tuning (out of scope; a LoRA on DABench format constraints would likely add several points). Single-model per run — no mid-run provider fallback. Threat model for the public demo: vetted CSVs only; arbitrary uploads disabled. |
| 8 | **What I'd do differently** | 500 | Treat free-tier rate limits as design constraint from day one (would have changed scope to 20-task subset with proper throttling, not 80). Smoke test against real API before writing the eval harness (would have caught matplotlib backend + retry budget off-by-one + prompt format bugs much cheaper). Phase-0 discovery (DABench schema + scorer regex) saved hours later — do this for any benchmark integration. Real-world security lesson: Gemini's `?key=…` URL-param pattern is why "shift left on security" matters even for student projects. |

**Voice:** First person, like the existing 700-word writeup but expanded
4×. Honest about scope and failures. No marketing-speak.

## 4. Implementation plan

Ship in 9 small PRs on a `feat/v2` branch off `main`. Each PR gets a
Vercel preview deploy + Lighthouse check before merge.

| PR | Title | Visible? | LoC est. |
|---|---|---|---|
| #1 | `chore(tokens): swap to Aurora design system` | Subtle color shifts | ~150 |
| #2 | `feat(landing): metrics strip + Aurora restyle` | Home transformed | ~250 |
| #3 | `feat(layout): ProjectLayout-v2 with sticky TOC sidebar` (gated on `v2: true` frontmatter; only DA Agent flips it) | DA Agent project page transformed (content unchanged) | ~400 |
| #4 | `content(da-agent): expand to 7,800-word deep-dive` | DA Agent writeup is the pilot | ~600 |
| 🛑 | **Sign-off pause** — review pilot before replication | — | — |
| #5 | `content(rag): expand to deep-dive` | RAG upgraded | ~600 |
| #6 | `content(churn): expand to deep-dive` | Churn upgraded | ~600 |
| #7 | `content(multi-tool): expand to deep-dive` | Multi-tool upgraded | ~600 |
| #8 | `content(recommender): expand to deep-dive` | Recommender upgraded | ~600 |
| #9 | `chore: remove legacy ProjectLayout + v2 flag` | None | ~30 |

The pause after PR #4 is the critical decision point: if you don't like
the pilot enough to want it 5×, we adjust before writing 30,000 more
words.

### 4.1 Quality gates per PR

Every PR must pass before merge:

1. CI green — `npm run build` via `.github/workflows/build.yml` on Node 22
2. Vercel preview deploys successfully
3. Visual review on the preview URL (you sign off)
4. Lighthouse on the preview: **Performance ≥ 90, Accessibility ≥ 95, Best Practices = 100, SEO ≥ 90**
5. No regression vs current `main` on any of those four metrics
6. Mobile viewport at 375px renders sensibly — sidebar collapses to disclosure
7. From PR #3 onward: TOC active-section highlight works; smooth-scroll on click works
8. From PR #4 onward: code blocks render with JetBrains Mono + Shiki; tables render with new borders; no broken images

### 4.2 Risk register

| Risk | Mitigation |
|---|---|
| Aurora gradient fights with dense eval / test-suite tables | PR #3 preview is the gate to verify table readability against the cool palette. If it looks bad, adjust borders + bg before PR #4 commits to the table treatment. |
| Mobile TOC sidebar doesn't fit below 768px | Fallback already designed: collapsible `<details>` disclosure at top of page. |
| Astro `render()` may not expose H2/H3 headings in the shape `TocSidebar` expects | Spike in PR #3: a 5-minute test in the Astro dev server confirms the data shape before building `TocSidebar`. |
| `@fontsource` Inter + JetBrains Mono adds ~140KB to bundle | Self-hosted is still the right call (privacy + reliability vs Google Fonts CDN). Subset to Latin + numerals only to keep size down. |
| Writing 5 × 7,800-word deep-dives is a slog and quality drops over time | The mandatory sign-off pause after PR #4 is the safeguard. If the writing voice in PR #4 isn't right, we fix the template before replicating. |

## 5. Out of scope (explicit)

To prevent quiet scope creep — items that have been brought up or are
adjacent but are deliberately excluded from this spec:

| Item | Why excluded |
|---|---|
| Dark mode | Doubles the palette work. Defer to v3 if recruiters ask. |
| Mobile-first redesign | v2 is desktop-first with responsive fallbacks. Phone-first is its own project. |
| Search across project pages | Not enough content to warrant the build cost. |
| RSS / Atom feed | Adds ~2 days of work; defer until there's writing volume to syndicate. |
| Analytics | Vercel already provides basic analytics for free. |
| Newsletter signup | No newsletter exists. |
| Framer Motion / scroll-triggered animations | The Stripe-mesh aesthetic doesn't need motion. Adds bundle size. |
| `BlogLayout.astro` redesign | Gets the new tokens but keeps current structure. |
| `/404.astro` redesign | Gets the new tokens. |
| Framework / MDX migration | Stays on Astro v6 + MDX. |
| Writing new pytest tests for the agent repo | We're documenting the existing 33, not adding more. |
| Per-project HF Space deployment redesign | The two live HF Spaces (DA Agent, RAG) are embedded via iframe and unchanged. |
| Recruiter contact form | A Calendly link in the footer is enough. |

## 6. Success criteria

The redesign succeeds when:

1. A recruiter scanning the landing for 8 seconds sees: "ML engineer, ships things, has taste."
2. A recruiter clicking through to the DA Agent page can jump to "Evaluation" in one click (TOC sidebar) and find a numerical result within 5 seconds.
3. The Lighthouse Performance score doesn't regress below 90 vs the current `main`.
4. Mobile renders without horizontal scroll at 375px.
5. All five projects use `ProjectLayout-v2` after PR #8, and PR #9 retires the legacy code path.
6. The current minimal-academic palette (warm-gold + cream) appears nowhere in the rendered HTML or CSS after PR #1.

## 7. Open questions

None — all design questions resolved in brainstorming. Implementation
details (exact PR commit boundaries, MDX prose styles, JS for
IntersectionObserver) are deferred to the implementation plan.
