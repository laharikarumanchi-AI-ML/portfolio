# Portfolio v2 — Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the portfolio v2 redesign (Stripe-style Aurora aesthetic + 7,800-word engineering deep-dive for the data-analysis-agent project) as 4 incremental PRs on a `feat/v2` branch, with a sign-off pause before replicating to the other 4 projects.

**Architecture:** Astro v6 static site, MDX content collections, Vercel deploy. The pilot is implemented as a frontmatter-gated layout system (`v2: true` on a project file routes through `ProjectLayoutV2.astro`), so the four non-pilot projects keep working on the legacy `ProjectLayout.astro` until each gets its own content PR. After PR #8 ships, PR #9 removes the gate and the legacy layout.

**Tech Stack:** Astro 6.3.8, MDX (`@astrojs/mdx`), Inter + JetBrains Mono via `@fontsource/*` (self-hosted), Shiki (bundled with Astro) for code-block syntax highlighting with `github-dark-dimmed` theme. No new frameworks (no React, no Tailwind, no Framer Motion).

**Spec:** [`docs/superpowers/specs/2026-06-03-portfolio-v2-design.md`](../specs/2026-06-03-portfolio-v2-design.md)

---

## A note on TDD in this codebase

The portfolio has no test suite — the existing CI runs `npm run build` only. Most of this work is CSS, Astro template edits, and MDX content; automated UI tests would be 10× the work for ~5% extra confidence on a single-author static site. The honest test contract per PR is:

1. `npm run build` succeeds locally (no Astro errors, no zod schema errors, no broken imports)
2. `git push` triggers GitHub Actions `build.yml` workflow → green
3. Vercel preview deploy succeeds
4. Manual visual checklist on the preview URL (specific items per PR — listed below)
5. Lighthouse on the preview meets thresholds (Performance ≥ 90, Accessibility ≥ 95, Best Practices = 100, SEO ≥ 90)

For the one piece of stateful client-side logic — `TocSidebar`'s IntersectionObserver — PR #3 includes a **manual verification checklist** (scroll, click, resize). Adding Playwright for one component is YAGNI for this scope; if TocSidebar becomes problematic later, that's a separate decision.

Where "Step: Write the failing test" would appear in a Python TDD plan, this plan substitutes "Step: Add manual checklist item" or "Step: Run build to verify it doesn't break."

---

## File structure (full inventory)

### New files (created across PRs)

| Path | PR | Responsibility |
|---|---|---|
| `src/data/metrics.ts` | #2 | Single source of truth for the landing-page metrics strip (project count, test count, ABQ, graduation year) |
| `src/components/MetricsStrip.astro` | #2 | Renders the one-line metrics row below the hero |
| `src/components/ProjectHero.astro` | #3 | Eyebrow / h1 / subtitle / headline-number / meta strip / chips / CTAs at top of every deep-dive |
| `src/components/TocSidebar.astro` | #3 | Sticky aside listing MDX H2/H3 headings + actions slot, with inline IntersectionObserver client script |
| `src/layouts/ProjectLayoutV2.astro` | #3 | Full deep-dive page shell: ProjectHero + 1100px grid (240 TOC / 720 text / 140 gutter) + prose styles |
| `public/diagrams/da-agent-architecture.svg` | #4 | SVG of the agent architecture diagram (orchestrator → sandbox / llm_client / trace) referenced from §5 of the DA Agent MDX |

### Modified files

| Path | PR | What changes |
|---|---|---|
| `src/styles/global.css` | #1 | Full token replacement; retire warm-accent + serif + `.numbered-sections`; new prose styles for deep-dive |
| `package.json` | #1 | Add `@fontsource/inter` + `@fontsource/jetbrains-mono` |
| `astro.config.mjs` | #1 | Configure Shiki `markdown.shikiConfig` for `github-dark-dimmed` theme |
| `src/components/Hero.astro` | #2 | Drop `.hero-rule` div, restyle for gradient-mesh hero, change copy slightly |
| `src/components/Nav.astro` | #2 | Sticky + `backdrop-filter: blur(12px)`, no border-bottom |
| `src/components/ProjectCard.astro` | #2 | Restyle all three variants (mesh backdrop on featured) |
| `src/components/PostCard.astro` | #2 | Mostly token-driven; small spacing tweaks |
| `src/components/Footer.astro` | #2 | Drop inline `font-family:var(--font-serif)` |
| `src/layouts/BaseLayout.astro` | #1 | Import `@fontsource/inter/400.css`, `/600.css`, `/700.css` + JetBrains Mono 400 |
| `src/layouts/BlogLayout.astro` | #1 | Token swap only (no structural change) |
| `src/layouts/ProjectLayout.astro` | #2 | Drop inline `font-family:var(--font-serif)` (keep file until PR #9) |
| `src/pages/index.astro` | #2 | Drop `<div class="numbered-sections">` wrapper; insert `<MetricsStrip />` between Hero and Featured |
| `src/pages/projects/[...slug].astro` | #3 | Branch on `entry.data.v2` — route through `ProjectLayoutV2` if true, else legacy `ProjectLayout` |
| `src/content.config.ts` | #3 | Add `category`, `status`, `lastUpdated`, `readTimeMinutes`, `v2` fields to the projects schema |
| `src/content/projects/data-analysis-agent.mdx` | #3 + #4 | PR #3: add `category` + `v2: true` + `lastUpdated`. PR #4: full 7,800-word rewrite with worked-examples and test-suite subsection. |
| `src/content/projects/document-qa-rag.mdx` | #3 | Add `category` (migration). Stays on legacy layout until PR #5. |
| `src/content/projects/churn-prediction.mdx` | #3 | Add `category` (migration). Stays on legacy layout until PR #6. |
| `src/content/projects/multi-tool-agent.mdx` | #3 | Add `category` (migration). Stays on legacy layout until PR #7. |
| `src/content/projects/movie-recommender.mdx` | #3 | Add `category` (migration). Stays on legacy layout until PR #8. |

### Deleted files

| Path | PR | Why |
|---|---|---|
| `src/layouts/ProjectLayout.astro` | #9 | Replaced entirely by `ProjectLayoutV2.astro` once all 5 projects use v2 |

---

## Branching strategy

```
main ──┬──── feat/v2-tokens         (PR #1) ──┐
       │                                       ├─► merge ─► main
       │     feat/v2-landing         (PR #2) ──┤
       │                                       │
       │     feat/v2-deepdive-shell  (PR #3) ──┤
       │                                       │
       │     feat/v2-da-agent-content (PR #4) ─┤
       │                                       │
       │     🛑 SIGN-OFF PAUSE                  │
       │                                       │
       │     feat/v2-rag-content     (PR #5) ──┤
       │     feat/v2-churn-content   (PR #6) ──┤
       │     feat/v2-mt-content      (PR #7) ──┤
       │     feat/v2-rec-content     (PR #8) ──┤
       │                                       │
       │     feat/v2-cleanup         (PR #9) ──┘
       └──────────────────────────────────────────►
```

Each branch is created off the latest `main` after the previous PR merges. We do *not* stack the PRs — that complicates rebasing and Vercel previews. Mergeability is checked at PR-open time.

---

# Phase 1 — PR #1: Aurora design tokens

**Branch:** `feat/v2-tokens`
**Goal:** Replace the minimal-academic token set with the Aurora system. Subtle visible change (slight color and font shift); no layout changes; no new components.
**Estimated LoC:** ~150
**Estimated time:** 45–60 min including build + Lighthouse + PR

### Task 1.1: Create the branch + install fonts

**Files:**
- Modify: `package.json`
- Modify: `package-lock.json` (auto-updated)

- [ ] **Step 1: Create branch from latest main**

```bash
cd /Users/anilkumar/portfolio
git checkout main && git pull origin main
git checkout -b feat/v2-tokens
```

- [ ] **Step 2: Install the two font packages**

```bash
npm install --save-exact @fontsource/inter@5.1.0 @fontsource/jetbrains-mono@5.1.0
```

Pin exact versions — fonts are leaf dependencies that rarely benefit from caret-range updates and exact pins make Lighthouse-regression triage easier.

- [ ] **Step 3: Verify package.json reflects both packages**

```bash
grep -E "fontsource" package.json
```

Expected: two lines, `"@fontsource/inter": "5.1.0"` and `"@fontsource/jetbrains-mono": "5.1.0"`.

- [ ] **Step 4: Commit**

```bash
git add package.json package-lock.json
git commit -m "chore(deps): pin Inter + JetBrains Mono via @fontsource"
```

### Task 1.2: Replace the design token block in global.css

**Files:**
- Modify: `src/styles/global.css:1-32` (the `:root` block + retired warm-accent vars)

- [ ] **Step 1: Read the current `:root` block**

```bash
sed -n '1,32p' src/styles/global.css
```

- [ ] **Step 2: Replace the entire `:root` block with the Aurora token set**

Replace lines 1–32 with:

```css
:root {
  /* Greyscale */
  --ink:   #0a0a0a;
  --paper: #ffffff;
  --muted: #525252;
  --rule:  #e5e5e5;
  --hover: rgba(10, 10, 10, 0.04);

  /* Aurora accents */
  --accent-mint:        #a7f3d0;
  --accent-sky:         #93c5fd;
  --accent-violet:      #c4b5fd;
  --accent-teal:        #0d9488;   /* primary action + link color */
  --accent-violet-deep: #7c3aed;   /* secondary / TOC active highlight */

  /* The signature gradient — used on hero, featured backdrop, CTA blocks */
  --gradient-hero:
    radial-gradient(at 20% 30%, var(--accent-mint)   0%, transparent 55%),
    radial-gradient(at 80% 20%, var(--accent-sky)    0%, transparent 55%),
    radial-gradient(at 60% 80%, var(--accent-violet) 0%, transparent 55%),
    linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;

  /* Widths */
  --content-width:  720px;
  --shell-width:    1200px;
  --shell-deepdive: 1100px;

  /* Spacing scale (unchanged from v1) */
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --space-4: 2.5rem;
  --space-5: 4rem;

  /* Radii — softer */
  --radius:    8px;
  --radius-sm: 6px;

  --t-fast: 120ms ease-out;
}
```

Note: `--font-serif` is gone. `--accent-cream`, `--accent-cream-edge`, `--accent-gold`, and the old `--link` are gone. The `--ink`/`--paper`/etc. greyscale values shifted slightly (cooler).

- [ ] **Step 3: Update the `html` rule to use the new sans font and base color**

In `src/styles/global.css`, find the `html` block (was around line 36) and confirm/update:

```css
html {
  font-family: var(--font-sans);
  color: var(--ink);
  background: var(--paper);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
```

- [ ] **Step 4: Replace the link rule to use teal**

Find the `a { ... }` block. Change to:

```css
a {
  color: var(--accent-teal);
  text-decoration: underline;
  text-underline-offset: 2px;
  text-decoration-thickness: 1px;
  transition: text-decoration-thickness var(--t-fast);
}
a:hover { text-decoration-thickness: 2px; }
```

- [ ] **Step 5: Update heading rules — drop serif, switch to Inter**

Find the `h1, h2, h3, h4 { ... }` block. Change to:

```css
h1, h2, h3, h4 {
  font-family: var(--font-sans);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  margin-block: var(--space-4) var(--space-2);
}

h1 { font-size: 3rem;   line-height: 1.05; }
h2 { font-size: 1.875rem; }
h3 { font-size: 1.25rem;  font-weight: 600; letter-spacing: -0.015em; }
```

- [ ] **Step 6: Update `pre`, `code` to the new mono font + dark code block bg**

Find the `code, pre { ... }` and `pre { ... }` blocks. Change to:

```css
code, pre {
  font-family: var(--font-mono);
  font-size: 0.875em;
}

pre {
  background: #0d1117;       /* matches github-dark-dimmed Shiki theme */
  color: #c9d1d9;
  padding: var(--space-2);
  overflow-x: auto;
  border-radius: var(--radius);
  border: 1px solid #21262d;
  line-height: 1.55;
}

:not(pre) > code {
  background: #f5f5f5;
  color: var(--ink);
  padding: 0.15em 0.35em;
  border-radius: 4px;
  border: 1px solid var(--rule);
}
```

- [ ] **Step 7: Build to verify no syntax errors**

```bash
npm run build
```

Expected: build succeeds. Site looks different in colors/fonts but layout is intact. (Don't worry about visual ugliness — the components catch up in PR #2.)

- [ ] **Step 8: Commit**

```bash
git add src/styles/global.css
git commit -m "feat(tokens): swap to Aurora design tokens"
```

### Task 1.3: Retire `.numbered-sections`, warm-accent classes, hero-rule, skill-category

**Files:**
- Modify: `src/styles/global.css` (remove blocks)

Per spec §3.1: drop the CSS counter system and the warm-accent component styles. They'll be replaced by gradient backdrops + new component CSS in PR #2.

- [ ] **Step 1: Delete the `.card-featured`, `.card-featured .eyebrow`, `.card-featured .headline-number` blocks**

Find them in `global.css` (search `.card-featured`). Delete all three. (They'll be replaced in PR #2.)

- [ ] **Step 2: Delete the `.numbered-sections` and `.numbered-sections h2::before` blocks**

Find them (search `.numbered-sections`). Delete both.

- [ ] **Step 3: Delete the `.hero-rule` block**

Find it (search `.hero-rule`). Delete the block and the `::before` / `::after` pseudo-elements.

- [ ] **Step 4: Delete the `.skill-category` block (will be re-added with Aurora styling in PR #2)**

Find it (search `.skill-category`). Delete the block and the `.skill-category:first-of-type` rule.

- [ ] **Step 5: Build — expect home page to look broken until PR #2**

```bash
npm run build
```

Expected: build succeeds. The home page's featured card, numbered sections, hero rule, and skill chip group labels will all look unstyled — that's fine; PR #2 fixes them.

- [ ] **Step 6: Commit**

```bash
git add src/styles/global.css
git commit -m "feat(tokens): retire warm-accent + numbered-sections + hero-rule CSS"
```

### Task 1.4: Wire font imports in BaseLayout

**Files:**
- Modify: `src/layouts/BaseLayout.astro:1-4` (the import block)

- [ ] **Step 1: Add font CSS imports at the top of BaseLayout's frontmatter**

Replace lines 1–4 of `src/layouts/BaseLayout.astro` (the import block) with:

```ts
---
import '../styles/global.css';
// Self-hosted fonts (no Google Fonts CDN — privacy + reliability)
import '@fontsource/inter/400.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import '@fontsource/jetbrains-mono/400.css';
import Nav from '../components/Nav.astro';
import Footer from '../components/Footer.astro';
```

- [ ] **Step 2: Add `<link rel="preload">` for the above-fold heading weight**

Per spec §4.2 risk register and review recommendation #2: preload Inter 700 to protect Lighthouse Performance.

After the existing `<link rel="canonical">` line in `<head>`, add:

```astro
<link rel="preload" href="/_astro/inter-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin />
```

(The actual hashed filename may differ — Astro's build picks a content hash. We'll fix this in Task 1.7 after first build by inspecting `dist/`.)

- [ ] **Step 3: Build**

```bash
npm run build
```

Expected: build succeeds. Both fonts should be referenced in `dist/_astro/*.woff2`.

- [ ] **Step 4: Verify font files are emitted**

```bash
ls dist/_astro/ | grep -E "(inter|jetbrains)" | head -10
```

Expected: 4 woff2 files (one per imported weight).

- [ ] **Step 5: Fix the preload href to match the actual emitted filename**

```bash
# Find the actual emitted filename for Inter 700
ls dist/_astro/ | grep "inter-latin-700-normal" | head -1
```

If the filename matches what you put in the preload, fine. If it differs (e.g., `inter-latin-700-normal.B7gKp2.woff2`), update the preload href in `BaseLayout.astro` to match.

If the filename has a build hash (it will), use a wildcard-safe pattern: change the preload to an inline `<style>` that adds `font-display: swap` for Inter, which gives most of the benefit without the hash-tracking pain:

```astro
<style>
  @font-face {
    font-family: 'Inter';
    font-display: swap;
  }
</style>
```

Pick whichever is less fragile.

- [ ] **Step 6: Commit**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat(fonts): self-host Inter + JetBrains Mono via @fontsource"
```

### Task 1.5: Clean up inline serif references in components

**Files:**
- Modify: `src/components/Footer.astro:11`
- Modify: `src/layouts/ProjectLayout.astro:14`

Per spec review finding: these are the only inline `var(--font-serif)` references outside `global.css`. After this task, `grep -r "font-serif" src/` should return zero hits.

- [ ] **Step 1: Verify grep finds exactly two hits before the change**

```bash
grep -rn "font-serif" src/
```

Expected output:

```
src/components/Footer.astro:11:  ...font-family:var(--font-serif); color:var(--ink);
src/layouts/ProjectLayout.astro:14:  ...font-family:var(--font-serif); font-size:1.5rem; ...
```

- [ ] **Step 2: Remove `font-family:var(--font-serif);` from Footer.astro line 11**

The `<p>` on line 11 currently reads:

```astro
<p style="margin:0 0 var(--space-1); font-family:var(--font-serif); color:var(--ink);">Lahari Karumanchi</p>
```

Change to:

```astro
<p style="margin:0 0 var(--space-1); font-weight:600; color:var(--ink);">Lahari Karumanchi</p>
```

Inter at 600 weight visually replaces what serif was doing (visual emphasis on the footer name).

- [ ] **Step 3: Remove `font-family:var(--font-serif);` from ProjectLayout.astro line 14**

The `<p>` on line 14 currently reads:

```astro
<p style="font-family:var(--font-serif); font-size:1.5rem; margin:1rem 0 0.75rem;">
  {entry.data.headlineNumber}
</p>
```

Change to:

```astro
<p style="font-size:1.5rem; font-weight:600; letter-spacing:-0.015em; margin:1rem 0 0.75rem;">
  {entry.data.headlineNumber}
</p>
```

This makes the legacy ProjectLayout (still used by 4 of 5 projects until PRs #5–8 land) look acceptable with the new tokens.

- [ ] **Step 4: Verify grep returns zero hits**

```bash
grep -rn "font-serif" src/
```

Expected: no output (zero hits).

- [ ] **Step 5: Build**

```bash
npm run build
```

Expected: success.

- [ ] **Step 6: Commit**

```bash
git add src/components/Footer.astro src/layouts/ProjectLayout.astro
git commit -m "chore(cleanup): remove inline var(--font-serif) refs"
```

### Task 1.6: Build + Lighthouse + open PR #1

- [ ] **Step 1: Final local build + dev preview check**

```bash
npm run build
npm run preview
```

Open `http://localhost:4321` in a browser. Quick visual smoke check — colors should be slightly cooler, fonts should be Inter, but the layout should be unchanged. Featured card on home will look a bit unstyled (no backdrop) — that's expected; PR #2 restores it.

- [ ] **Step 2: Push the branch**

```bash
git push -u origin feat/v2-tokens
```

- [ ] **Step 3: Open PR**

```bash
gh pr create --base main --title "chore(tokens): swap to Aurora design system" --body "$(cat <<'EOF'
## Summary

PR #1 of the v2 redesign. Swaps the minimal-academic token set for the Aurora system per [spec §3.1](../blob/main/docs/superpowers/specs/2026-06-03-portfolio-v2-design.md#31-design-tokens). No layout or content changes — just CSS tokens + font self-hosting + retiring CSS that PR #2 will replace.

- Aurora palette (mint / sky / violet, teal accent)
- Inter + JetBrains Mono via `@fontsource/*` (self-hosted, not Google Fonts CDN)
- Retired: `--font-serif`, `--accent-cream*`, `--accent-gold`, `.numbered-sections`, `.hero-rule`, `.skill-category`, `.card-featured` styles (PR #2 reintroduces a new featured-card style with mesh backdrop)

## Visual changes you'll see on the Vercel preview

- Colors slightly cooler (white paper vs cream paper)
- Sans-serif everywhere (no more Iowan Old Style serif headings)
- Links are teal (#0d9488) instead of warm blue
- Home page featured card looks unstyled — **expected**; PR #2 brings it back

## Test plan

- [ ] CI green
- [ ] Vercel preview deploys
- [ ] Lighthouse on the preview: Performance ≥ 90 / Accessibility ≥ 95 / Best Practices = 100 / SEO ≥ 90
- [ ] `grep -r "font-serif" src/` → zero hits
- [ ] `grep -r "accent-cream\|accent-gold\|numbered-sections\|hero-rule" src/` → zero hits

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 4: After CI green + your visual review on Vercel preview, squash-merge**

```bash
gh pr merge --squash --delete-branch
git checkout main && git pull origin main
```

---

# Phase 2 — PR #2: Landing-page metrics strip + Aurora restyle

**Branch:** `feat/v2-landing`
**Goal:** Restyle the home page for Aurora. Add `MetricsStrip` between hero and featured. Restyle all existing landing components (Hero, Nav, ProjectCard, PostCard, Footer). The home page becomes the first fully v2 page.
**Estimated LoC:** ~250
**Estimated time:** 90–120 min

### Task 2.1: Branch + create metrics data source

**Files:**
- Create: `src/data/metrics.ts`

- [ ] **Step 1: Branch from latest main**

```bash
git checkout main && git pull origin main
git checkout -b feat/v2-landing
```

- [ ] **Step 2: Create `src/data/metrics.ts`**

```ts
// Single source of truth for the landing-page metrics strip.
// Update these values here, not inline in the component.

export interface Metric {
  value: string;
  label: string;
}

export const landingMetrics: Metric[] = [
  { value: '5',    label: 'projects shipped'   },
  { value: '33',   label: 'tests passing'      },
  { value: '75%',  label: 'ABQ on DABench'     },
  { value: '2027', label: 'graduating'         },
];
```

- [ ] **Step 3: Commit**

```bash
git add src/data/metrics.ts
git commit -m "feat(data): metrics constants for landing strip"
```

### Task 2.2: Build `MetricsStrip.astro`

**Files:**
- Create: `src/components/MetricsStrip.astro`

- [ ] **Step 1: Create the component**

```astro
---
import { landingMetrics } from '../data/metrics';
---
<section class="metrics-strip" aria-label="By the numbers">
  <ul>
    {landingMetrics.map((m, i) => (
      <li>
        {i > 0 && <span class="sep" aria-hidden="true">·</span>}
        <span class="value">{m.value}</span>
        <span class="label">{m.label}</span>
      </li>
    ))}
  </ul>
</section>

<style>
  .metrics-strip {
    margin-block: var(--space-3);
    padding: var(--space-2) var(--space-3);
    border: 1px solid var(--rule);
    border-radius: var(--radius);
    background:
      linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
  }
  .metrics-strip ul {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: center;
    gap: 0.5rem 1rem;
    margin: 0;
    padding: 0;
    list-style: none;
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-variant-numeric: tabular-nums;
  }
  .metrics-strip li {
    display: inline-flex;
    align-items: baseline;
    gap: 0.4rem;
  }
  .value {
    color: var(--accent-teal);
    font-weight: 600;
  }
  .label {
    color: var(--muted);
    font-family: var(--font-sans);
    font-size: 0.85rem;
  }
  .sep {
    color: var(--rule);
    margin-right: 0.6rem;
  }
  @media (max-width: 560px) {
    .metrics-strip ul { gap: 0.4rem 0.8rem; }
    .label { font-size: 0.78rem; }
  }
</style>
```

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: success. Component isn't used anywhere yet — we'll wire it in Task 2.7.

- [ ] **Step 3: Commit**

```bash
git add src/components/MetricsStrip.astro
git commit -m "feat(landing): MetricsStrip component"
```

### Task 2.3: Restyle `Hero.astro`

**Files:**
- Modify: `src/components/Hero.astro` (full rewrite — 12 lines becomes ~50)

- [ ] **Step 1: Rewrite the component**

Replace the entire contents of `src/components/Hero.astro` with:

```astro
---
---
<section class="hero">
  <div class="hero-inner">
    <p class="eyebrow">ML ENGINEER · 2026 · SHIPPING</p>
    <h1>Lahari Karumanchi</h1>
    <p class="tagline">
      ML engineering with citations. Code-as-action agents,
      retrieval-augmented Q&amp;A, and honest evaluation.
    </p>
    <div class="cta-row">
      <a href="#featured" class="btn btn-primary">View projects →</a>
      <a href="/resume.pdf" class="btn btn-secondary">Résumé</a>
    </div>
    <p class="hero-meta">
      Hyderabad, India · Recruiting for Summer 2026 ML / SWE internships
    </p>
  </div>
</section>

<style>
  .hero {
    margin-block: var(--space-3) var(--space-4);
    padding: var(--space-4) var(--space-3);
    border-radius: var(--radius);
    background: var(--gradient-hero);
    border: 1px solid var(--rule);
  }
  .hero-inner { max-width: 720px; }
  .eyebrow {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    color: var(--accent-violet-deep);
    margin: 0 0 var(--space-2);
  }
  .hero h1 {
    margin: 0 0 var(--space-1);
    font-size: 3.5rem;
    line-height: 1;
    letter-spacing: -0.025em;
  }
  .tagline {
    font-size: 1.2rem;
    color: var(--muted);
    margin: var(--space-2) 0 var(--space-3);
    max-width: 540px;
  }
  .cta-row { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-bottom: var(--space-3); }
  .btn {
    display: inline-block;
    padding: 0.55rem 1.1rem;
    border-radius: var(--radius-sm);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    transition: transform var(--t-fast), box-shadow var(--t-fast);
  }
  .btn-primary {
    background: var(--ink);
    color: var(--paper);
    border: 1px solid var(--ink);
  }
  .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(10,10,10,0.15); }
  .btn-secondary {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(8px);
    color: var(--ink);
    border: 1px solid var(--rule);
  }
  .btn-secondary:hover { background: rgba(255,255,255,0.9); border-color: var(--ink); }
  .hero-meta {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--muted);
    margin: 0;
  }
  @media (max-width: 560px) {
    .hero h1 { font-size: 2.5rem; }
    .tagline { font-size: 1.05rem; }
  }
</style>
```

The `<div class="hero-rule">§</div>` is gone (its CSS was already removed in Task 1.3).

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: success. Home page hero now has the Aurora mesh background.

- [ ] **Step 3: Commit**

```bash
git add src/components/Hero.astro
git commit -m "feat(hero): Aurora gradient mesh hero with CTAs"
```

### Task 2.4: Restyle `Nav.astro` (sticky + backdrop-blur)

**Files:**
- Modify: `src/components/Nav.astro`
- Modify: `src/styles/global.css` (the `nav.site-nav` block)

- [ ] **Step 1: Replace `Nav.astro` content**

```astro
---
const pages = [
  { href: '/projects',   label: 'Projects' },
  { href: '/blog',       label: 'Blog'     },
  { href: '/about',      label: 'About'    },
  { href: '/resume.pdf', label: 'Résumé'   },
];
---
<nav class="site-nav" aria-label="Primary">
  <div class="site-nav-inner">
    <a href="/" class="brand">Lahari Karumanchi</a>
    <div class="links">
      {pages.map(p => <a href={p.href}>{p.label}</a>)}
    </div>
  </div>
</nav>
```

- [ ] **Step 2: Replace the `nav.site-nav` block in `global.css`**

Find the existing `nav.site-nav { ... }` block and the `nav.site-nav .brand` rules. Replace with:

```css
nav.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(229, 229, 229, 0.6);
  padding-block: 0.75rem;
  margin-inline: calc(-1 * var(--space-2));
  padding-inline: var(--space-2);
}
.site-nav-inner {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.75rem 1.25rem;
  font-family: var(--font-sans);
}
.site-nav .brand {
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
  flex: 1 1 100%;
  text-decoration: none;
  color: var(--ink);
}
.site-nav .links { display: flex; flex-wrap: wrap; gap: 0.75rem 1.25rem; }
.site-nav .links a {
  font-size: 0.9rem;
  text-decoration: none;
  color: var(--muted);
}
.site-nav .links a:hover { color: var(--ink); }
@media (min-width: 560px) {
  .site-nav .brand { flex: 0 0 auto; margin-right: auto; font-size: 1rem; }
}
```

- [ ] **Step 3: Build**

```bash
npm run build
```

Expected: success. Nav sticks to top on scroll with a frosted-glass effect.

- [ ] **Step 4: Commit**

```bash
git add src/components/Nav.astro src/styles/global.css
git commit -m "feat(nav): sticky + backdrop-blur restyle"
```

### Task 2.5: Restyle `ProjectCard.astro` (all three variants)

**Files:**
- Modify: `src/components/ProjectCard.astro` (mostly the CSS, which lives in `global.css` for the legacy variants)
- Modify: `src/styles/global.css` (add new featured + index card styles, restyle compact)

- [ ] **Step 1: Add the new `.card-featured` block in `global.css`** (replacing what we deleted in Task 1.3)

Inside `global.css`, add this block (place it near the other card styles, around where the old `.card-featured` used to be):

```css
/* Featured card — full-bleed on landing, gradient backdrop */
.card-featured {
  display: block;
  position: relative;
  color: inherit;
  text-decoration: none;
  border: 1px solid var(--rule);
  padding: var(--space-3);
  margin-block: var(--space-3);
  border-radius: var(--radius);
  background: var(--gradient-hero);
  transition: transform var(--t-fast), box-shadow var(--t-fast), border-color var(--t-fast);
}
a.card-featured:hover {
  transform: translateY(-2px);
  border-color: var(--accent-teal);
  box-shadow: 0 8px 24px rgba(13, 148, 136, 0.12);
}
.card-featured .eyebrow {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-violet-deep);
  margin: 0 0 var(--space-1);
}
.card-featured .headline-number {
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 1.35rem;
  color: var(--accent-teal);
  margin: var(--space-2) 0;
  letter-spacing: -0.005em;
}
```

- [ ] **Step 2: Update `.card-index` block in `global.css`** for Aurora

Find the `.card-index` block. Replace the `headline` rule and add Aurora-flavored hover:

```css
.card-index {
  border: 1px solid var(--rule);
  border-radius: var(--radius);
  padding: var(--space-3);
  margin-block: var(--space-3);
  background: var(--paper);
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
}
.card-index:hover {
  border-color: var(--accent-teal);
  box-shadow: 0 4px 16px rgba(13, 148, 136, 0.08);
}
/* keep .card-index-head, .card-index-title, .card-index-year as-is */
.card-index-headline {
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 1.15rem;
  color: var(--accent-teal);
  margin: 0.5rem 0;
}
```

- [ ] **Step 3: Restyle `.chips`** for the rounded-full pill look

Find `.chips` block. Replace with:

```css
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0.5rem 0 0 0;
  padding: 0;
  list-style: none;
}
.chips li {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  line-height: 1;
  padding: 0.35rem 0.65rem;
  border: 1px solid var(--rule);
  border-radius: 999px;
  color: var(--muted);
  background: #fafafa;
  letter-spacing: 0.01em;
}
```

- [ ] **Step 4: Restyle `.button-sm`** to use teal accent

Find `.button-sm` and `.button-sm-quiet`. Replace with:

```css
.button-sm {
  display: inline-block;
  padding: 0.4rem 0.85rem;
  border: 1px solid var(--ink);
  border-radius: var(--radius-sm);
  text-decoration: none;
  color: var(--ink);
  font-size: 0.82rem;
  font-weight: 600;
  transition: background-color var(--t-fast), color var(--t-fast), transform var(--t-fast);
}
.button-sm:hover {
  background: var(--ink);
  color: var(--paper);
  transform: translateY(-1px);
  text-decoration: none;
}
.button-sm-quiet {
  border-color: var(--rule);
  color: var(--muted);
  font-weight: 500;
}
.button-sm-quiet:hover {
  background: var(--paper);
  color: var(--accent-teal);
  border-color: var(--accent-teal);
  transform: none;
}
```

- [ ] **Step 5: Restyle `.button`** (résumé download CTA) to use teal primary

Find `.button` block. Replace with:

```css
.button {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-sm);
  background: var(--accent-teal);
  color: var(--paper);
  border: 1px solid var(--accent-teal);
  text-decoration: none;
  font-weight: 600;
  transition: transform var(--t-fast), box-shadow var(--t-fast);
}
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2);
  text-decoration: none;
}
```

- [ ] **Step 6: Build**

```bash
npm run build
```

Expected: success.

- [ ] **Step 7: Commit**

```bash
git add src/styles/global.css
git commit -m "feat(cards): Aurora-styled card + button + chip variants"
```

### Task 2.6: Restyle `PostCard.astro` (small tweaks)

**Files:**
- Modify: `src/components/PostCard.astro` (mostly inherits new tokens; just visual tweaks)

- [ ] **Step 1: Read current file**

PostCard is mostly token-driven — the new tokens already make it Aurora-flavored. One small tweak: bump the time/date typography to mono.

- [ ] **Step 2: Update line 14 (the `<time>` element)** to use mono

In `src/components/PostCard.astro`, find the line with `<time datetime={iso} class="sm muted">{pretty}</time>` and wrap it with mono font:

```astro
<p style="margin:0;">
  <time datetime={iso} class="sm muted" style="font-family:var(--font-mono); font-size:0.8rem;">{pretty}</time>
</p>
```

- [ ] **Step 3: Build**

```bash
npm run build
```

- [ ] **Step 4: Commit**

```bash
git add src/components/PostCard.astro
git commit -m "feat(post-card): monospace date typography"
```

### Task 2.7: Update `src/pages/index.astro` — insert MetricsStrip + restyle skills

**Files:**
- Modify: `src/pages/index.astro` (drop `.numbered-sections` wrapper, insert MetricsStrip, restyle skill section)
- Modify: `src/styles/global.css` (add new `.skill-category` block since it was deleted in Task 1.3)

- [ ] **Step 1: Add the new `.skill-category` style to `global.css`**

```css
.skill-category {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 1.5rem 0 0.5rem;
}
.skill-category:first-of-type { margin-top: 0.5rem; }
```

- [ ] **Step 2: Rewrite `src/pages/index.astro`**

Replace the entire file with:

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';
import Hero from '../components/Hero.astro';
import MetricsStrip from '../components/MetricsStrip.astro';
import ProjectCard from '../components/ProjectCard.astro';
import PostCard from '../components/PostCard.astro';

const projects = (await getCollection('projects'));
const featured = projects.find(p => p.data.featured);
const selected = projects
  .filter(p => !p.data.featured)
  .sort((a, b) => (b.data.year - a.data.year) || (a.data.order - b.data.order))
  .slice(0, 2);

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => +b.data.publishedAt - +a.data.publishedAt)
  .slice(0, 2);
---
<BaseLayout title="Lahari Karumanchi — ML projects + agents"
            description="Third-year CS student. Code-as-action agents, RAG, classical ML. Recruiting for Summer 2026 ML/SWE internships.">
  <Hero />
  <MetricsStrip />

  {featured && (
    <section id="featured">
      <h2>Featured</h2>
      <ProjectCard entry={featured} variant="featured" />
    </section>
  )}

  {selected.length > 0 && (
    <section id="selected" style="margin-top:3rem;">
      <h2>Selected work</h2>
      <div style="display:grid; gap:1.5rem;">
        {selected.map(p => <ProjectCard entry={p} variant="compact" />)}
      </div>
      <p style="margin-top:1.25rem;">
        <a href="/projects" class="button-sm button-sm-quiet">
          See all {projects.length} projects →
        </a>
      </p>
    </section>
  )}

  <section id="skills" style="margin-top:3rem;">
    <h2>What I work with</h2>
    <p class="skill-category">Languages</p>
    <ul class="chips">
      <li>Python</li><li>Java</li><li>C</li><li>SQL</li>
    </ul>
    <p class="skill-category">ML / data</p>
    <ul class="chips">
      <li>PyTorch</li><li>scikit-learn</li><li>XGBoost</li>
      <li>sentence-transformers</li><li>FAISS</li><li>Pandas</li><li>NumPy</li>
    </ul>
    <p class="skill-category">Tools</p>
    <ul class="chips">
      <li>Git</li><li>Docker</li><li>FastAPI</li><li>Streamlit</li>
      <li>Jupyter</li><li>pytest</li><li>GitHub Actions</li>
    </ul>
    <p class="skill-category">Areas</p>
    <ul class="chips">
      <li>RAG</li><li>Code-as-action agents</li><li>Vector search</li>
      <li>Honest evaluation</li><li>NLP</li>
    </ul>
  </section>

  {posts.length > 0 && (
    <section id="writing" style="margin-top:3rem;">
      <h2>Recent writing</h2>
      <div style="display:grid; gap:1.5rem;">
        {posts.map(p => <PostCard entry={p} />)}
      </div>
    </section>
  )}

  <section id="about" style="margin-top:3rem;">
    <h2>About</h2>
    <p>Third-year CS @ CVR College of Engineering, Hyderabad. Recruiting for Summer 2026 ML/SWE internships. <a href="/about">More →</a></p>
    <p style="margin-top:0.75rem;"><a href="/resume.pdf" class="button">Download résumé →</a></p>
  </section>
</BaseLayout>
```

Key changes vs current version:
1. `<div class="numbered-sections">` wrapper removed (sections no longer auto-numbered)
2. `<MetricsStrip />` inserted between Hero and Featured
3. Everything else preserved structurally — section IDs intact for fragment links

- [ ] **Step 3: Build**

```bash
npm run build
```

Expected: success. Home page is fully v2.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro src/styles/global.css
git commit -m "feat(landing): insert MetricsStrip + drop section numbering"
```

### Task 2.8: Build + Lighthouse + visual checklist + open PR #2

- [ ] **Step 1: Build + preview locally**

```bash
npm run build && npm run preview
```

Open `http://localhost:4321` and run the **PR #2 visual checklist:**

| Item | Pass criteria |
|---|---|
| Hero gradient | Mint/sky/violet mesh visible behind name |
| Hero CTAs | Two buttons (black primary, glassy outline secondary). Primary lifts 1px on hover. |
| Sticky nav | Frosted-glass effect, sticks to top on scroll |
| Metrics strip | Below hero, mono numerals, `5 · 33 · 75% · 2027`, mint→white subtle gradient bg |
| Featured card | Mesh backdrop, headline number in teal, "Featured project" eyebrow in violet mono |
| Compact teasers | Two cards in "Selected work", no mesh backdrop, clean borders |
| "See all 5 projects" | Quiet pill button, teal on hover |
| Skill chips | Rounded-full, mono font, subtle borders |
| Recent writing | Two post cards with mono dates |
| Résumé button | Teal primary, lifts on hover |
| Footer | Sans-serif throughout (no Iowan Old Style) |
| Section spacing | No `01.` / `02.` / `03.` prefixes on section headings |

- [ ] **Step 2: Push + open PR**

```bash
git push -u origin feat/v2-landing
gh pr create --base main --title "feat(landing): metrics strip + Aurora restyle" --body "$(cat <<'EOF'
## Summary

PR #2 of the v2 redesign. Makes the home page the first fully-v2 page. Adds `MetricsStrip` between hero and featured. Restyles Hero (gradient mesh + CTAs), Nav (sticky + backdrop-blur), ProjectCard (all 3 variants), PostCard (mono dates), Footer.

Section auto-numbering (01. / 02. / 03.) is retired per [spec §3.5](../blob/main/docs/superpowers/specs/2026-06-03-portfolio-v2-design.md#35-landing-page-structure) — Stripe-style hierarchy comes from gradient backdrops + spacing instead.

## Test plan

- [ ] CI green
- [ ] Vercel preview deploys
- [ ] Lighthouse on the preview: Performance ≥ 90 / Accessibility ≥ 95 / Best Practices = 100 / SEO ≥ 90
- [ ] Visual checklist (12 items, see commit description on the squash merge)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: After CI + visual + Lighthouse pass, squash-merge**

```bash
gh pr merge --squash --delete-branch
git checkout main && git pull origin main
```

---

# Phase 3 — PR #3: ProjectLayoutV2 + TocSidebar (the deep-dive shell)

**Branch:** `feat/v2-deepdive-shell`
**Goal:** Build the framework for the engineering-deep-dive pages. New schema fields, ProjectHero component, TocSidebar with IntersectionObserver, ProjectLayoutV2 shell, frontmatter-gated routing. DA Agent project page transforms (content unchanged — that's PR #4).
**Estimated LoC:** ~400
**Estimated time:** 2.5–3 hours

### Task 3.1: Branch + schema spike

**Files:**
- Modify: `src/content.config.ts`

- [ ] **Step 1: Branch**

```bash
git checkout main && git pull origin main
git checkout -b feat/v2-deepdive-shell
```

- [ ] **Step 2: Add the new fields to the projects schema**

Replace the existing `projects = defineCollection({ ... })` in `src/content.config.ts` with:

```ts
const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: z.object({
    // Existing v1 fields
    title:          z.string(),
    oneLiner:       z.string(),
    headlineNumber: z.string(),
    techStack:      z.array(z.string()),
    year:           z.number(),
    githubUrl:      z.string().url().optional(),
    demoUrl:        z.string().url().optional(),
    featured:       z.boolean().default(false),
    order:          z.number(),

    // NEW v2 fields
    category:        z.enum(['Agents', 'RAG', 'Classical ML']),
    status:          z.enum(['shipped', 'in-progress']).default('shipped'),
    lastUpdated:     z.coerce.date().optional(),
    readTimeMinutes: z.number().int().positive().optional(),

    // Migration flag (removed in PR #9)
    v2:              z.boolean().default(false),
  }),
});
```

- [ ] **Step 3: Build — expect errors because the 5 MDX files don't have `category` yet**

```bash
npm run build
```

Expected: 5 build errors, one per MDX file, each complaining "category" is required. Good — confirms the schema change is in effect.

- [ ] **Step 4: Don't commit yet** — fix the MDX files in the next task before committing the schema change.

### Task 3.2: Backfill `category` on all 5 MDX files

**Files:**
- Modify: `src/content/projects/data-analysis-agent.mdx` frontmatter
- Modify: `src/content/projects/document-qa-rag.mdx` frontmatter
- Modify: `src/content/projects/churn-prediction.mdx` frontmatter
- Modify: `src/content/projects/multi-tool-agent.mdx` frontmatter
- Modify: `src/content/projects/movie-recommender.mdx` frontmatter

Categories per spec §3.4:

| File | category |
|---|---|
| `data-analysis-agent.mdx` | `Agents` |
| `document-qa-rag.mdx` | `RAG` |
| `multi-tool-agent.mdx` | `Agents` |
| `churn-prediction.mdx` | `Classical ML` |
| `movie-recommender.mdx` | `Classical ML` |

- [ ] **Step 1: Add `category: Agents` to data-analysis-agent.mdx**

In the YAML frontmatter (between `---` blocks at top of file), add after the `order:` line:

```yaml
category: Agents
```

- [ ] **Step 2: Same pattern for the other 4 MDX files** with their respective categories from the table above.

- [ ] **Step 3: Build to verify the schema is satisfied**

```bash
npm run build
```

Expected: success. All 5 projects build with categories.

- [ ] **Step 4: Commit the schema change + all 5 migrations together**

```bash
git add src/content.config.ts src/content/projects/*.mdx
git commit -m "feat(schema): add v2 project fields + backfill category on all 5 MDX"
```

### Task 3.3: Spike — verify Astro's `render()` heading shape

Per spec §4.2 risk register: a 5-min test confirms the `headings` array's shape before building `TocSidebar`.

- [ ] **Step 1: Quick test by inspecting an existing project page's render output**

```bash
# In any Astro page, you can use `render()` to check headings
# Easier: write a one-off debug log in [...slug].astro
```

Add this *temporarily* to `src/pages/projects/[...slug].astro` just before the JSX:

```astro
console.log('=== HEADINGS DEBUG ===');
console.log(JSON.stringify(headings, null, 2));
```

(`headings` is returned from `render(entry)`; you'll need to add it to the destructure: `const { Content, headings } = await render(entry);`)

- [ ] **Step 2: Run `npm run build` and look at the output**

```bash
npm run build 2>&1 | grep -A 20 "HEADINGS DEBUG"
```

Expected: an array of `{ depth, slug, text }` objects, e.g.:

```json
[
  { "depth": 2, "slug": "try-it", "text": "Try it" },
  { "depth": 2, "slug": "problem", "text": "Problem" },
  ...
]
```

- [ ] **Step 3: Remove the debug logging** — don't commit it

Revert your changes to `[...slug].astro`.

If the shape matches `{ depth, slug, text }`: proceed. If it differs: stop, document the actual shape, adjust `TocSidebar` accordingly.

### Task 3.4: Build `ProjectHero.astro`

**Files:**
- Create: `src/components/ProjectHero.astro`

- [ ] **Step 1: Create the component**

```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  entry: CollectionEntry<'projects'>;
}
const { entry } = Astro.props;
const d = entry.data;

const eyebrowParts = [
  d.category.toUpperCase(),
  String(d.year),
  d.status.toUpperCase(),
];
const eyebrow = eyebrowParts.join(' · ');

const lastUpdatedFmt = d.lastUpdated
  ? d.lastUpdated.toISOString().slice(0, 10)
  : null;
---
<section class="project-hero">
  <div class="project-hero-inner">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{d.title}</h1>
    <p class="oneliner">{d.oneLiner}</p>
    <p class="headline-number">{d.headlineNumber}</p>
    <p class="meta">
      {d.readTimeMinutes && (
        <span><span aria-hidden="true">📖</span> {d.readTimeMinutes} min read</span>
      )}
      {lastUpdatedFmt && (
        <>
          {d.readTimeMinutes && <span class="sep" aria-hidden="true">·</span>}
          <span><span aria-hidden="true">⚙</span> updated <time datetime={lastUpdatedFmt}>{lastUpdatedFmt}</time></span>
        </>
      )}
    </p>
    <ul class="chips" aria-label="Tech stack">
      {d.techStack.map(t => <li>{t}</li>)}
    </ul>
    <div class="cta-row">
      {d.githubUrl && <a href={d.githubUrl} class="button-sm" rel="noopener">Code →</a>}
      {d.demoUrl  && <a href={d.demoUrl}  class="button-sm" rel="noopener">Live demo →</a>}
    </div>
  </div>
</section>

<style>
  .project-hero {
    margin-block: var(--space-3) var(--space-4);
    padding: var(--space-4) var(--space-3);
    border-radius: var(--radius);
    background: var(--gradient-hero);
    border: 1px solid var(--rule);
  }
  .project-hero-inner { max-width: 760px; }
  .eyebrow {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    color: var(--accent-violet-deep);
    margin: 0 0 var(--space-2);
  }
  .project-hero h1 {
    margin: 0 0 var(--space-1);
    font-size: 2.75rem;
    line-height: 1.05;
    letter-spacing: -0.02em;
  }
  .oneliner {
    font-size: 1.15rem;
    color: var(--muted);
    margin: var(--space-2) 0;
  }
  .headline-number {
    font-family: var(--font-sans);
    font-weight: 600;
    font-size: 1.4rem;
    color: var(--accent-teal);
    margin: var(--space-2) 0 var(--space-1);
    letter-spacing: -0.01em;
  }
  .meta {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: var(--muted);
    margin: 0 0 var(--space-2);
  }
  .meta .sep { margin: 0 0.5rem; }
  .cta-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: var(--space-2); }
  @media (max-width: 640px) {
    .project-hero h1 { font-size: 2rem; }
  }
</style>
```

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: success. Component isn't wired anywhere yet.

- [ ] **Step 3: Commit**

```bash
git add src/components/ProjectHero.astro
git commit -m "feat(project-hero): Aurora project-hero with eyebrow, headline, meta"
```

### Task 3.5: Build `TocSidebar.astro`

**Files:**
- Create: `src/components/TocSidebar.astro`

- [ ] **Step 1: Create the component**

```astro
---
import type { MarkdownHeading } from 'astro';

interface Props {
  headings: MarkdownHeading[];
}
const { headings } = Astro.props;

// Show H2 + H3 only. H3s appear indented under their parent H2.
const tocHeadings = headings.filter(h => h.depth === 2 || h.depth === 3);
---
<aside class="toc-sidebar" aria-label="Table of contents">
  <details class="toc-mobile-disclosure">
    <summary>Jump to section</summary>
    <p class="toc-title">On this page</p>
    <ol>
      {tocHeadings.map(h => (
        <li class:list={[`toc-depth-${h.depth}`]}>
          <a href={`#${h.slug}`} data-toc-slug={h.slug}>{h.text}</a>
        </li>
      ))}
    </ol>
    <hr/>
    <slot name="actions" />
  </details>
</aside>

<script>
  // Active-section highlight via IntersectionObserver.
  // Observes every <section data-toc-slug> in the main column and toggles
  // aria-current="location" on the matching TOC <a>.
  const links = document.querySelectorAll<HTMLAnchorElement>('aside.toc-sidebar a[data-toc-slug]');
  if (links.length > 0) {
    const linkBySlug = new Map<string, HTMLAnchorElement>();
    links.forEach(a => linkBySlug.set(a.dataset.tocSlug!, a));

    // Find the headings in the main column and observe their parent sections.
    const headingEls = document.querySelectorAll<HTMLElement>('main h2[id], main h3[id]');

    let activeSlug: string | null = null;
    const setActive = (slug: string | null) => {
      if (slug === activeSlug) return;
      if (activeSlug) linkBySlug.get(activeSlug)?.removeAttribute('aria-current');
      if (slug)       linkBySlug.get(slug)?.setAttribute('aria-current', 'location');
      activeSlug = slug;
    };

    const observer = new IntersectionObserver(
      (entries) => {
        // Pick the topmost heading that's currently in view.
        const visible = entries
          .filter(e => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) {
          setActive((visible[0].target as HTMLElement).id);
        }
      },
      { rootMargin: '-80px 0px -60% 0px' } // top offset = sticky nav height
    );

    headingEls.forEach(h => observer.observe(h));

    // Smooth-scroll on click (works even without scroll-behavior: smooth in CSS)
    links.forEach(a => {
      a.addEventListener('click', (e) => {
        const slug = a.dataset.tocSlug!;
        const target = document.getElementById(slug);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, '', `#${slug}`);
        }
      });
    });
  }
</script>

<style>
  .toc-sidebar {
    font-family: var(--font-sans);
  }
  .toc-mobile-disclosure {
    /* On desktop, treat as always-open with sticky positioning */
  }
  .toc-mobile-disclosure summary {
    display: none;
    cursor: pointer;
    padding: 0.6rem 0;
    font-weight: 600;
    border-bottom: 1px solid var(--rule);
  }
  .toc-title {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 var(--space-2);
  }
  .toc-sidebar ol {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .toc-sidebar li {
    margin: 0;
  }
  .toc-sidebar a {
    display: block;
    padding: 0.35rem 0.5rem;
    border-radius: 4px;
    color: var(--muted);
    text-decoration: none;
    font-size: 0.88rem;
    line-height: 1.4;
    transition: color var(--t-fast), background-color var(--t-fast);
  }
  .toc-sidebar a:hover {
    color: var(--ink);
    background: var(--hover);
  }
  .toc-sidebar a[aria-current="location"] {
    color: var(--accent-violet-deep);
    background: rgba(167, 139, 250, 0.12);
    font-weight: 600;
  }
  .toc-depth-3 a {
    padding-left: 1.5rem;
    font-size: 0.82rem;
  }
  .toc-sidebar hr {
    margin: var(--space-2) 0;
    border: none;
    border-top: 1px solid var(--rule);
  }

  /* Mobile: collapse to disclosure */
  @media (max-width: 900px) {
    .toc-mobile-disclosure summary { display: block; }
    .toc-mobile-disclosure > *:not(summary) {
      display: none;
    }
    .toc-mobile-disclosure[open] > * { display: block; }
    .toc-mobile-disclosure[open] summary { display: block; }
  }
</style>
```

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: success.

- [ ] **Step 3: Commit**

```bash
git add src/components/TocSidebar.astro
git commit -m "feat(toc): sticky TOC sidebar with IntersectionObserver active state"
```

### Task 3.6: Build `ProjectLayoutV2.astro`

**Files:**
- Create: `src/layouts/ProjectLayoutV2.astro`

- [ ] **Step 1: Create the layout**

```astro
---
import BaseLayout from './BaseLayout.astro';
import ProjectHero from '../components/ProjectHero.astro';
import TocSidebar from '../components/TocSidebar.astro';
import type { CollectionEntry } from 'astro:content';
import type { MarkdownHeading } from 'astro';

interface Props {
  entry: CollectionEntry<'projects'>;
  headings: MarkdownHeading[];
}
const { entry, headings } = Astro.props;
const d = entry.data;
---
<BaseLayout
  title={`${d.title} — Lahari Karumanchi`}
  description={d.oneLiner}
  wide={true}
>
  <p style="font-size:0.85rem; color:var(--muted); margin:0 0 var(--space-1);">
    <a href="/projects">← All projects</a>
  </p>

  <ProjectHero entry={entry} />

  <div class="deepdive-shell">
    <TocSidebar headings={headings}>
      <div slot="actions" class="toc-actions">
        {d.githubUrl && <a href={d.githubUrl} class="button-sm button-sm-quiet" rel="noopener">📦 GitHub</a>}
        {d.demoUrl  && <a href={d.demoUrl}  class="button-sm button-sm-quiet" rel="noopener">🟢 Live demo</a>}
      </div>
    </TocSidebar>
    <main class="deepdive-main">
      <slot />
    </main>
  </div>
</BaseLayout>

<style>
  .deepdive-shell {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: var(--space-4);
    max-width: var(--shell-deepdive);
    margin-inline: auto;
    margin-top: var(--space-3);
  }
  .toc-sidebar {
    position: sticky;
    top: 4.5rem;
    align-self: start;
    max-height: calc(100vh - 6rem);
    overflow-y: auto;
  }
  .deepdive-main {
    max-width: 720px;
  }
  .toc-actions { display: flex; flex-direction: column; gap: 0.4rem; }

  /* Prose styles scoped to the deep-dive main column */
  .deepdive-main :global(h2) {
    font-size: 2rem;
    letter-spacing: -0.015em;
    margin-block: var(--space-4) var(--space-2);
    scroll-margin-top: 5rem; /* clear sticky nav on anchor jumps */
  }
  .deepdive-main :global(h3) {
    font-size: 1.35rem;
    margin-block: var(--space-3) var(--space-1);
    scroll-margin-top: 5rem;
  }
  .deepdive-main :global(p) {
    font-size: 1.05rem;
    line-height: 1.7;
    margin-block: var(--space-2);
  }
  .deepdive-main :global(blockquote) {
    margin-inline: 0;
    padding: var(--space-2) var(--space-3);
    border-left: 3px solid var(--accent-teal);
    background: rgba(13, 148, 136, 0.05);
    font-style: italic;
    color: var(--muted);
  }
  .deepdive-main :global(table) {
    width: 100%;
    border-collapse: collapse;
    margin-block: var(--space-3);
    font-size: 0.95rem;
  }
  .deepdive-main :global(table th),
  .deepdive-main :global(table td) {
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--rule);
    text-align: left;
  }
  .deepdive-main :global(table th) {
    background: #fafafa;
    font-weight: 600;
    border-bottom: 2px solid var(--rule);
  }
  .deepdive-main :global(img),
  .deepdive-main :global(svg) {
    max-width: 100%;
    height: auto;
    margin-block: var(--space-3);
    border: 1px solid var(--rule);
    border-radius: var(--radius);
    padding: var(--space-2);
    background: var(--paper);
  }

  /* Mobile: collapse the grid */
  @media (max-width: 900px) {
    .deepdive-shell {
      grid-template-columns: 1fr;
      gap: var(--space-2);
    }
    .toc-sidebar {
      position: static;
      max-height: none;
      margin-bottom: var(--space-3);
      border: 1px solid var(--rule);
      border-radius: var(--radius);
      padding: var(--space-2);
    }
    .deepdive-main { max-width: 100%; }
  }
</style>
```

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: success.

- [ ] **Step 3: Commit**

```bash
git add src/layouts/ProjectLayoutV2.astro
git commit -m "feat(layout): ProjectLayoutV2 with TOC sidebar grid shell"
```

### Task 3.7: Wire layout routing in `[...slug].astro`

**Files:**
- Modify: `src/pages/projects/[...slug].astro`

- [ ] **Step 1: Replace the file**

```astro
---
import { getCollection, render } from 'astro:content';
import ProjectLayout    from '../../layouts/ProjectLayout.astro';
import ProjectLayoutV2  from '../../layouts/ProjectLayoutV2.astro';

export async function getStaticPaths() {
  const projects = await getCollection('projects');
  return projects.map(entry => ({
    params: { slug: entry.id.replace(/\.mdx?$/, '') },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content, headings } = await render(entry);
---
{entry.data.v2 ? (
  <ProjectLayoutV2 entry={entry} headings={headings}>
    <Content />
  </ProjectLayoutV2>
) : (
  <ProjectLayout entry={entry}>
    <Content />
  </ProjectLayout>
)}
```

- [ ] **Step 2: Build — expect no rendering change yet** (no project has `v2: true`)

```bash
npm run build
```

Expected: success. All 5 project pages still render through the legacy `ProjectLayout`.

- [ ] **Step 3: Commit**

```bash
git add src/pages/projects/[...slug].astro
git commit -m "feat(routing): branch project route on v2 frontmatter flag"
```

### Task 3.8: Flip DA Agent to v2 (content unchanged)

**Files:**
- Modify: `src/content/projects/data-analysis-agent.mdx` frontmatter

- [ ] **Step 1: Add `v2: true` + `lastUpdated` + `readTimeMinutes` to frontmatter**

Update the frontmatter block of `data-analysis-agent.mdx`. Current frontmatter has:

```yaml
---
title: "Data Analysis Agent"
oneLiner: "..."
headlineNumber: "..."
techStack: [...]
year: 2026
githubUrl: "..."
demoUrl: "..."
featured: true
order: 1
category: Agents
---
```

Add:

```yaml
status: shipped
lastUpdated: 2026-06-03
readTimeMinutes: 4
v2: true
```

`readTimeMinutes: 4` reflects the *current* ~700-word content; PR #4 will update this to ~28 once the deep-dive is written.

- [ ] **Step 2: Build + open in dev server**

```bash
npm run build && npm run preview
```

Open `http://localhost:4321/projects/data-analysis-agent`. You should see:

- New `ProjectHero` with "AGENTS · 2026 · SHIPPED" eyebrow
- TocSidebar on the left (showing "Try it / Problem / Approach / Results / What I'd do differently / Links" — the current 5 H2s)
- Aurora-mesh hero backdrop

The other 4 projects should still render through the old `ProjectLayout` — verify by opening `/projects/document-qa-rag` etc.

- [ ] **Step 3: Run the manual TocSidebar verification checklist** (the only stateful client logic in this PR)

| Check | Pass criteria |
|---|---|
| Initial load | First section ("Try it") highlighted in TOC |
| Scroll down | Active highlight follows as sections enter top viewport |
| Click TOC link | Smooth scroll to target; URL hash updates; active state updates |
| Resize to <900px | Sidebar collapses to "Jump to section" `<details>` disclosure; main column goes full-width |
| Resize back | Sidebar returns to sticky-aside layout |
| Reload at `/projects/data-analysis-agent#approach` | Page jumps to Approach section on load; TOC shows Approach active |

- [ ] **Step 4: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "feat(da-agent): opt into ProjectLayoutV2 (content unchanged)"
```

### Task 3.9: Open PR #3

- [ ] **Step 1: Push + open PR**

```bash
git push -u origin feat/v2-deepdive-shell
gh pr create --base main --title "feat(layout): ProjectLayoutV2 with sticky TOC sidebar" --body "$(cat <<'EOF'
## Summary

PR #3 of the v2 redesign. Ships the deep-dive page framework:

- New schema fields: `category`, `status`, `lastUpdated`, `readTimeMinutes`, `v2` (migration flag)
- New components: `ProjectHero.astro`, `TocSidebar.astro` (with IntersectionObserver)
- New layout: `ProjectLayoutV2.astro` — 1100px shell with 240px sticky TOC + 720px text
- Routing in `[...slug].astro` branches on `entry.data.v2`
- DA Agent project flipped to v2 (content unchanged — that's PR #4)
- Other 4 projects stay on legacy `ProjectLayout` until each gets its own content PR

## Test plan

- [ ] CI green
- [ ] Vercel preview deploys
- [ ] `/projects/data-analysis-agent` shows the new layout
- [ ] `/projects/document-qa-rag`, `/projects/churn-prediction`, `/projects/multi-tool-agent`, `/projects/movie-recommender` still show the legacy layout
- [ ] Manual TocSidebar checklist (6 items from commit description) passes on preview
- [ ] Lighthouse on `/projects/data-analysis-agent`: Performance ≥ 90 / A11y ≥ 95 / BP = 100 / SEO ≥ 90

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 2: After CI + TOC checklist passes on Vercel preview, squash-merge**

```bash
gh pr merge --squash --delete-branch
git checkout main && git pull origin main
```

---

# Phase 4 — PR #4: DA Agent 7,800-word deep-dive (the pilot)

**Branch:** `feat/v2-da-agent-content`
**Goal:** Replace the current ~700-word DA Agent MDX with the full 8-section, 7,800-word engineering deep-dive per [spec §3.7](../specs/2026-06-03-portfolio-v2-design.md#37-da-agent-mdx-content-outline-the-pilot).
**Estimated LoC:** ~600 (mostly MDX prose)
**Estimated time:** 4–6 hours of focused writing + 30 min build/review/PR

### Pre-task: Gather source material

Per the spec reviewer's findings, all content comes from existing artifacts — no new evals needed. Confirm access:

- [ ] **Step 1: Verify the agent repo eval JSONs are readable**

```bash
ls -lh /Users/anilkumar/Lahari/agent/eval/results/
# Expected: subset-llama-retry.json, subset50-gemini.json
```

- [ ] **Step 2: Verify the demo datasets**

```bash
ls /Users/anilkumar/Lahari/demo/datasets/
# Expected: iris.csv, tips.csv, titanic.csv
```

- [ ] **Step 3: Verify the test suite for the test-suite subsection**

```bash
ls /Users/anilkumar/Lahari/tests/*.py
# Expected: test_end_to_end.py, test_eval.py, test_llm_client.py,
#           test_orchestrator.py, test_sandbox.py, test_trace.py
```

- [ ] **Step 4: Read the agent README to internalize the voice**

```bash
cat /Users/anilkumar/Lahari/README.md
```

The deep-dive's voice should match this README's tone — honest, first-person, scoped about limitations.

### Task 4.1: Branch + skeleton frontmatter

**Files:**
- Modify: `src/content/projects/data-analysis-agent.mdx`

- [ ] **Step 1: Branch**

```bash
git checkout main && git pull origin main
git checkout -b feat/v2-da-agent-content
```

- [ ] **Step 2: Replace the current MDX with the empty 8-section skeleton**

Update the file so the body (below frontmatter) is just:

```mdx
## TL;DR

<!-- TODO: 200w -->

## Problem

<!-- TODO: 1000w -->

## Approach

<!-- TODO: 1200w -->

## Worked examples

<!-- TODO: 1000w -->

## Architecture

<!-- TODO: 1200w -->

### Test suite

<!-- TODO: 400w -->

## Evaluation

<!-- TODO: 1500w -->

## Limitations

<!-- TODO: 800w -->

## What I'd do differently

<!-- TODO: 500w -->
```

This step exists to verify the TocSidebar picks up the 8 sections (+ 1 subsection) before any prose is written.

- [ ] **Step 3: Build + verify TOC shows 9 items**

```bash
npm run build && npm run preview
```

Open `/projects/data-analysis-agent` and confirm:
- TocSidebar shows 8 H2 entries
- "Test suite" appears as an indented H3 under "Architecture"

- [ ] **Step 4: Commit the skeleton**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): 8-section skeleton w/ TOC verification"
```

### Task 4.2: Section 1 — TL;DR (200w)

**Content guidance per spec §3.7 row 1:** One paragraph framing the agent + the result + the caveat. Pull quote box with the 75% ABQ headline. CTAs at the end.

- [ ] **Step 1: Draft and replace the `<!-- TODO: 200w -->` under `## TL;DR`** with content along these lines:

> Data analysis questions — "what's the median order value by city," "is there a relationship between tenure and churn" — are everywhere in real work, and a poor fit for chat-only LLMs. This is a **code-as-action agent**: it answers questions about CSV data by writing and executing Python in a sandboxed Jupyter kernel, the same way an analyst would in a notebook. On a 9-task pilot of [InfiAgent-DABench](https://github.com/InfiAgent/InfiAgent) using Llama-3.3-70B via Groq, it scored **75% ABQ** under the official scorer. The pilot is honest about its scope — see [Evaluation](#evaluation).
>
> [→ Code on GitHub](https://github.com/laharikarumanchi-AI-ML/superpowers) · [→ Try the live demo](https://huggingface.co/spaces/laharikarumanchi/data-analysis-agent)

Use voice from the existing README "Headline result" section as the model.

- [ ] **Step 2: Build + read in preview** (check formatting, links work, copy reads cleanly)

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): TL;DR section"
```

### Task 4.3: Section 2 — Problem (~1000w)

**Content guidance per spec §3.7 row 2:**

- Why tabular Q&A is a poor fit for chat-only LLMs (they can't see the spreadsheet; pasting rows is guess-work)
- Why ReAct tool-call agents (LangChain et al.) explode on multi-step pandas pipelines — one tool call per pandas operation = exploding latency + token cost
- The gap: a model that thinks in code like a data analyst, iterating cell by cell
- Why InfiAgent-DABench specifically — real-world questions (median fare by region, correlation between tenure and churn, top-5 products by margin), official scorer with `@name[value]` regex extraction, gold labels in a separate file. Most "ML benchmarks" don't have honest evaluation infrastructure; DABench does.
- What "honest evaluation" means here — using the official scorer, not `predicted.lower() in expected.lower()`

Reference voice: existing MDX "Problem" section is a good start; expand 3× with the additional points above.

- [ ] **Step 1: Draft the section** (~1000 words). Reuse what's already there and expand. Keep paragraphs short (3–5 sentences). End each paragraph with a concrete sentence, not a hedge.

- [ ] **Step 2: Build + preview review**

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Problem section"
```

### Task 4.4: Section 3 — Approach (~1200w)

**Content guidance per spec §3.7 row 3:**

Core decision: code-as-action, not ReAct tool-calling. The loop in plain English:

1. System prompt says: "emit `<code>...</code>` to run Python, or `<answer>@name[value]</answer>` to finish."
2. Model emits a code block.
3. Orchestrator extracts the block, executes in a per-session Jupyter kernel.
4. Captures stdout, stderr, exceptions, matplotlib figures.
5. Formats the observation, appends to message history.
6. Model writes the next cell.
7. Repeats until `<answer>...</answer>` or 10-step ceiling.

Why no LangChain / LlamaIndex / CrewAI: ~150 lines does it; frameworks hide behaviors I needed to debug (retry budgets, malformed-output recovery, step limits).

Deliberate choices:
- Real Jupyter sandbox (`jupyter_client.KernelManager`), not `subprocess.run('python -c ...')`. Subprocess is not a sandbox — it has full host access and no message stream.
- Single deadline per cell (not per-message timeout) — long pandas operations stay honest about wall-clock budget.
- matplotlib captured via IOPub PNG (`display_data` messages) — set `matplotlib.use('Agg')` inside the kernel so figures don't try to open windows.
- Provider abstraction (Groq + Gemini behind a 3-method `LLMClient`) — quota crash on one provider doesn't kill the run.
- Official scorer from InfiAgent (copied with attribution) — no homegrown matching that could quietly inflate numbers.

End with a 2-step trace from a real iris.csv run. Pull the trace from one of the eval result JSONs:

```bash
python3 -c "
import json
data = json.load(open('/Users/anilkumar/Lahari/agent/eval/results/subset-llama-retry.json'))
# Find a task with a clean 2-step solution
for task in data['tasks'][:5]:
    print(task['task_id'], '-', task['question'][:60])
    print('Steps:', len(task['trace']))
"
```

Pick a clean 2-step task (e.g., one that reads a CSV in step 1 and answers in step 2) and inline the abridged trace as a code block.

- [ ] **Step 1: Draft the section**

- [ ] **Step 2: Build + preview review**

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Approach section"
```

### Task 4.5: Section 4 — Worked examples (~1000w)

**Content guidance per spec §3.7 row 4:**

5–6 real queries across the 3 vetted datasets. For each: question → agent's first cell → output/figure → agent's reasoning → final `@name[value]`. Include **one self-correction example** (recovers from `NameError`) and **one honest failure** (gets the answer wrong despite the loop).

Sources:
- Real traces from `/Users/anilkumar/Lahari/agent/eval/results/subset-llama-retry.json` (filter for tasks using the 3 vetted datasets or DABench's bundled tables; pull the ones with clean prose)
- Manual run of the live agent against `demo/datasets/iris.csv`, `tips.csv`, `titanic.csv` for 2–3 fresh examples

Suggested examples (adjust based on what's actually in the eval results):

1. **iris.csv — median sepal_length** (clean 2-step example)
2. **tips.csv — avg tip percent by day-of-week** (groupby example with a small chart)
3. **titanic.csv — fare-class correlation** (numerical reasoning)
4. **titanic.csv — survival by sex + class** (multi-axis groupby)
5. **Self-correction example** — agent writes a cell with `df.fare` when the column is `Fare` (case mismatch), sees `AttributeError`, fixes in next cell. Pull this from the eval results if one exists; otherwise reproduce by running the live agent with a deliberately ambiguous question.
6. **Honest failure** — pick a task from `subset-llama-retry.json` where the predicted answer didn't match the gold label. Show what the agent did, where it went wrong, and what type of failure it was (off-by-one rounding, misinterpreted question, wrong aggregation function).

Format each example as:

> **Q:** `<question>`
>
> **Cell 1:**
> ```python
> import pandas as pd
> df = pd.read_csv('iris.csv')
> df['sepal_length'].median()
> ```
> **Output:** `5.8`
>
> **Cell 2:**
> ```python
> # The median is 5.8.
> ```
>
> **Answer:** `<answer>@median_sepal_length[5.8]</answer>`

- [ ] **Step 1: Pull 2-3 traces from the existing eval JSONs** that map to the iris/tips/titanic datasets

```bash
python3 << 'EOF'
import json
data = json.load(open('/Users/anilkumar/Lahari/agent/eval/results/subset-llama-retry.json'))
# Look for tasks using simple closed-form questions
for t in data['tasks'][:20]:
    if t.get('passed'):
        print('---')
        print('Q:', t.get('question', '')[:120])
        print('Trace length:', len(t.get('trace', [])))
        print('Final answer:', t.get('final_answer', ''))
EOF
```

- [ ] **Step 2: Run the live agent for 2-3 fresh examples on the vetted datasets**

```bash
cd /Users/anilkumar/Lahari
source .venv/bin/activate
python -m agent ask --data demo/datasets/iris.csv "What is the median sepal_length?"
# Save the trace from agent/trace logs into the MDX
```

- [ ] **Step 3: Write the 5-6 examples** with the format above

- [ ] **Step 4: Build + preview review**

- [ ] **Step 5: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Worked examples section"
```

### Task 4.6: Build the architecture SVG

**Files:**
- Create: `public/diagrams/da-agent-architecture.svg`

The README has an ASCII diagram (lines 70–87). Convert it to a clean SVG.

- [ ] **Step 1: Sketch the SVG** (240×420 viewport, box-and-arrow)

Layout:

```
   ┌────────────────────────────────────────┐
   │     User (CLI / Streamlit)            │
   └─────────────────┬──────────────────────┘
                     │ question + dataset
                     ▼
   ┌────────────────────────────────────────┐
   │     Agent Loop (orchestrator.py)      │
   │  parses <code>, executes, repeats     │
   └──┬──────────┬──────────┬───────────────┘
      │          │          │
      ▼          ▼          ▼
  llm_client  sandbox     trace
  (Groq /    (Jupyter)   (JSON log)
  Gemini)
```

- [ ] **Step 2: Create the SVG file**

A reasonable inline SVG (keep colors Aurora-flavored — boxes in cool slate, arrows in mint/teal):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" font-family="Inter, sans-serif">
  <style>
    .box { fill: #f5f5f5; stroke: #525252; stroke-width: 1.5; rx: 8; }
    .label { font-size: 14px; fill: #0a0a0a; font-weight: 600; }
    .sub { font-size: 11px; fill: #525252; }
    .arrow { stroke: #0d9488; stroke-width: 2; fill: none; }
    .arrow-label { font-size: 10px; fill: #525252; font-family: 'JetBrains Mono', monospace; }
  </style>

  <!-- User -->
  <rect class="box" x="260" y="20" width="200" height="50"/>
  <text class="label" x="360" y="42" text-anchor="middle">User (CLI / Streamlit)</text>
  <text class="sub"   x="360" y="60" text-anchor="middle">question + dataset</text>

  <!-- Arrow down to Agent Loop -->
  <path class="arrow" d="M 360 70 L 360 110" marker-end="url(#arrowhead)"/>

  <!-- Agent Loop -->
  <rect class="box" x="200" y="110" width="320" height="80"/>
  <text class="label" x="360" y="138" text-anchor="middle">Agent Loop (orchestrator.py)</text>
  <text class="sub"   x="360" y="158" text-anchor="middle">parses &lt;code&gt;…&lt;/code&gt; from LLM output,</text>
  <text class="sub"   x="360" y="174" text-anchor="middle">executes, feeds result back, stops on &lt;answer&gt;</text>

  <!-- Three arrows down -->
  <path class="arrow" d="M 280 190 L 200 240" marker-end="url(#arrowhead)"/>
  <path class="arrow" d="M 360 190 L 360 240" marker-end="url(#arrowhead)"/>
  <path class="arrow" d="M 440 190 L 520 240" marker-end="url(#arrowhead)"/>

  <!-- llm_client -->
  <rect class="box" x="100" y="240" width="180" height="70"/>
  <text class="label" x="190" y="266" text-anchor="middle">llm_client.py</text>
  <text class="sub"   x="190" y="285" text-anchor="middle">Groq · Gemini</text>
  <text class="sub"   x="190" y="300" text-anchor="middle">retry · throttle</text>

  <!-- sandbox -->
  <rect class="box" x="280" y="240" width="160" height="70"/>
  <text class="label" x="360" y="266" text-anchor="middle">sandbox.py</text>
  <text class="sub"   x="360" y="285" text-anchor="middle">jupyter_client</text>
  <text class="sub"   x="360" y="300" text-anchor="middle">stdout · figures</text>

  <!-- trace -->
  <rect class="box" x="440" y="240" width="180" height="70"/>
  <text class="label" x="530" y="266" text-anchor="middle">trace.py</text>
  <text class="sub"   x="530" y="285" text-anchor="middle">JSON log</text>
  <text class="sub"   x="530" y="300" text-anchor="middle">every step</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#0d9488"/>
    </marker>
  </defs>
</svg>
```

- [ ] **Step 3: Save to `public/diagrams/da-agent-architecture.svg`**

```bash
mkdir -p public/diagrams
# Write the SVG above to public/diagrams/da-agent-architecture.svg
```

- [ ] **Step 4: Commit**

```bash
git add public/diagrams/da-agent-architecture.svg
git commit -m "content(da-agent): architecture SVG diagram"
```

### Task 4.7: Section 5 — Architecture (~1200w)

**Content guidance per spec §3.7 row 5:**

Reference the SVG at the top of the section:

```mdx
![Architecture diagram](/diagrams/da-agent-architecture.svg)
```

Then walk through each module. For each, give a 2–3 sentence description + the non-obvious bit:

| Module | Non-obvious bit |
|---|---|
| `llm_client.py` | Provider-agnostic 3-method interface. Groq client respects `Retry-After`; Gemini client adds 4-second inter-call throttle (15 RPM cap). Both scrub the API key from any logged URL. |
| `sandbox.py` | Wraps `jupyter_client.KernelManager`. `wait_for_ready()` so first execute doesn't race the kernel's initial `status: busy` message. Single per-cell *deadline* (not per-message timeout). Drains remaining messages after interrupt — otherwise the next cell sees ghost output. Captures matplotlib via `matplotlib.use('Agg')` set inside the kernel + `display_data` IOPub messages decoded as base64 PNGs. |
| `orchestrator.py` | The agent loop. Parses `<code>…</code>` / `<answer>…</answer>`. Retries on cell failures (configurable retry budget). Step ceiling = 10. |
| `trace.py` | JSON-serializable log of every (prompt, response, code, output) step. Used by both the eval harness and the Streamlit demo. |
| `cli.py` | `python -m agent ask --data X "Q"` — the single-question entry point. |
| `eval/run_dabench.py` | Loads DABench (joining questions + labels), runs the agent on each task, scores with the official `evaluate_responses`. Checkpoints after every task. |

Then explain LLMClient interface:

```python
class LLMClient(Protocol):
    def chat(self, messages: list[Message]) -> str: ...
    def with_budget(self, max_tokens: int) -> Self: ...
    def name(self) -> str: ...
```

Three methods. Swap implementations for Groq vs Gemini. The eval runner picks one at startup; the orchestrator never sees provider details.

Retry budget specifics:
- Groq: 5 attempts with `Retry-After`-aware exponential backoff. The free tier returns `Retry-After: 60` on quota crashes; we honor it.
- Gemini: 15 RPM hard cap. Inter-call throttle (4s between calls) baked into the client.

- [ ] **Step 1: Draft the section** with module table + interface code + retry specifics

- [ ] **Step 2: Build + preview review** (verify SVG renders, table styles look right)

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Architecture section"
```

### Task 4.8: Section 5a — Test suite subsection (~400w)

**Content guidance per spec §3.7 row 5a:**

Test coverage table:

| File | Tests | What it covers |
|---|---|---|
| `test_sandbox.py` | ? | Kernel lifecycle, per-cell deadline, drain-after-interrupt, matplotlib figure capture, state persistence across cells |
| `test_llm_client.py` | ? | Retry budget, `Retry-After` parsing, exponential backoff, URL key-scrub, per-call throttle |
| `test_orchestrator.py` | ? | `<code>` / `<answer>` parsing, step ceiling, cell failure retry |
| `test_trace.py` | ? | JSON serialization, redaction of API keys |
| `test_end_to_end.py` | ? | Full agent loop against a scripted mock LLM |
| `test_eval.py` | ? | DABench loader (questions × labels join), scorer integration |

Get the per-file test counts:

```bash
cd /Users/anilkumar/Lahari
source .venv/bin/activate
for f in tests/test_*.py; do
  count=$(pytest "$f" --collect-only -q 2>/dev/null | grep -c '::')
  echo "$f: $count tests"
done
```

A representative pytest snippet — pick `test_sandbox_timeout_drains_messages` if it exists (the most non-obvious behavior covered):

```bash
grep -A 25 "def test.*drain\|def test.*timeout" /Users/anilkumar/Lahari/tests/test_sandbox.py | head -40
```

Inline one well-chosen snippet (10–15 lines) showing the kind of subtle behavior tested.

CI badge URL (verified): `https://github.com/laharikarumanchi-AI-ML/superpowers/actions/workflows/test.yml/badge.svg`

End with:

> [![tests](https://github.com/laharikarumanchi-AI-ML/superpowers/actions/workflows/test.yml/badge.svg)](https://github.com/laharikarumanchi-AI-ML/superpowers/actions/workflows/test.yml)

- [ ] **Step 1: Run the per-file count script above** and fill in the table

- [ ] **Step 2: Draft the subsection** with table + snippet + badge

- [ ] **Step 3: Build + preview**

- [ ] **Step 4: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Test suite subsection w/ coverage table"
```

### Task 4.9: Section 6 — Evaluation (~1500w)

**Content guidance per spec §3.7 row 6:**

Sections within Evaluation:

**Dataset.** InfiAgent-DABench: 257 closed-form questions across CSV tables. Official labels in a *separate* file (questions reference table-IDs which join to labels via `question_id`). The Phase-0 discovery that labels are external (not inline) saved hours later — most "ML benchmarks" inline answers; DABench treats labels as a separate concern.

**Why DABench, not WikiSQL/Spider.** WikiSQL is SQL-only (no pandas). Spider is multi-table SQL with a different scoring rubric. DABench is closed-form pandas/data-analysis with an explicit `@name[value]` output schema — exactly what code-as-action agents emit.

**Scorer.** Copied `eval_closed_form.py` from InfiAgent's repo (with full attribution headers at the top of `agent/eval/scorers/infiagent/`). It extracts `@name[value]` tags with `re.findall(r"@(\w+)\[(.*?)\]", response)`, matches names against `common_answers`, and uses strict `is_equal` with float tolerance.

**Models tested:**

- Llama-3.3-70B via Groq (free tier)
- Gemini-2.0-Flash via Google AI Studio (free tier, 15 RPM cap)

**Setup:**

- 10-step ceiling per task
- Retry-on by default (configurable for ablation)
- Kernel reused across turns in the same task; fresh kernel per task
- Throttling tuned per provider (Groq: respects `Retry-After`; Gemini: 4s inter-call)

**Results table** (from `subset-llama-retry.json` + `subset50-gemini.json`):

| Configuration | Tasks scored | ABQ | Notes |
|---|---|---|---|
| Llama-3.3-70B + retry, 80-task subset attempt | 9 / 80 | **75%** | Free-tier quota cap hit at task 9 |
| Llama-3.3-70B + retry-off ablation | (planned) | — | Will quantify self-correction value |
| Gemini-2.0-Flash + retry, 50-task subset attempt | 0 / 50 | — | Key-format issue + quota cap |

Pull the actual numbers from the JSON:

```bash
python3 << 'EOF'
import json
data = json.load(open('/Users/anilkumar/Lahari/agent/eval/results/subset-llama-retry.json'))
total_attempted = len(data['tasks'])
total_passed = sum(1 for t in data['tasks'] if t.get('passed'))
print(f"Attempted: {total_attempted}, passed: {total_passed}")
print(f"ABQ: {total_passed/total_attempted*100:.1f}%")
EOF
```

**The /80 caveat.** Honest about why this is 9-of-80 and not 80-of-80 or 257-of-257: Groq free tier returns `429 Too Many Requests` with `Retry-After: 60` after enough TPM is spent. The retry budget honors `Retry-After`, but with 10-step tasks running ~2K tokens each, the daily TPM allotment gets eaten in ~9 successful tasks. Scaling needs a paid tier (~$5 on Groq Dev) or a multi-day run.

**Latency breakdown:** LLM time dominates. Per-task wall clock:

| Component | % of wall clock |
|---|---|
| LLM API call (Groq, p50) | ~88% |
| Sandbox execute (kernel msg loop) | ~5% |
| Trace I/O + scoring | ~7% |

The sandbox is fast; the bottleneck is the model.

- [ ] **Step 1: Draft the section** with all 5 subsections + the results table + latency breakdown

- [ ] **Step 2: Build + preview review**

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Evaluation section w/ results table + latency breakdown"
```

### Task 4.10: Section 7 — Limitations (~800w)

**Content guidance per spec §3.7 row 7.** Pull from the existing README "Limitations" section as the starting point; expand each bullet to 1–2 paragraphs:

1. **Quota-bounded headline** — 75% on 9 of 80 attempted; full 257 needs paid tier or multi-day run.
2. **Local-only public demo with arbitrary uploads** — Streamlit's `file_uploader` + a sandbox that runs LLM-emitted Python = RCE-on-a-platter without Docker isolation. The vetted-CSVs-only mode ships safely and is what's deployed to HF Spaces. The "upload your own" mode stays local-only until Docker isolation is wired per [spec §4a](https://github.com/laharikarumanchi-AI-ML/superpowers/blob/main/docs/superpowers/specs/2026-05-26-data-analysis-agent-design.md#4a-threat-model-public-streamlit-demo).
3. **No fine-tuning** — out of scope for this project (which is about agent design + evaluation, not training). A LoRA on DABench format constraints would likely add several points to ABQ.
4. **Single-model per run** — the eval doesn't fall back across providers mid-run when one quota exhausts. Would be a useful improvement; not yet built.
5. **Threat model for the deployed demo** — only the vetted datasets (iris, tips, titanic) are accessible. `st.file_uploader` is intentionally not exposed in the deployed `demo/app.py`. Even within vetted datasets, the sandbox runs as the host user with no namespace isolation — fine for a free-tier demo on HF, not OK for any meaningful data.

- [ ] **Step 1: Draft the section**

- [ ] **Step 2: Build + preview review**

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): Limitations section"
```

### Task 4.11: Section 8 — What I'd do differently (~500w)

**Content guidance per spec §3.7 row 8.** The existing README has bullet seeds for this (lines 276–293 of the current README). Expand each into a small paragraph in **first person**:

1. **Treat free-tier rate limits as a first-class design constraint, not a bug to retry around.** Would have changed scope from "80-task subset" to "20-task subset with proper throttling" on day one. The retry budget exists because I hit limits; if I'd planned for limits, I'd have written it differently.
2. **Run a single end-to-end smoke test against the real API *before* writing the eval harness.** Some of the bugs I caught (matplotlib backend, retry budget off-by-one, prompt format mismatch) would have surfaced cheaper.
3. **Phase-0 discovery saved hours later.** Finding out that DABench uses a separate labels file (not inline answers) and that the official scorer uses `@name[value]` regex extraction — I did this discovery for *this* benchmark; I'd do it for any benchmark integration going forward.
4. **Real-world security lesson.** The Gemini API leaks keys via `?key=...` URL parameter when you log raw request URLs. Shipping "shift left on security" matters for student projects too.

**Voice:** Match the existing README's tone. First person, honest, no PR-speak.

- [ ] **Step 1: Draft the section**

- [ ] **Step 2: Build + preview review**

- [ ] **Step 3: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): What I'd do differently section"
```

### Task 4.12: Update `readTimeMinutes` to actual word count

- [ ] **Step 1: Count words in the rendered prose**

```bash
# Strip MDX frontmatter + code blocks first, then count words
awk '/^---$/{f=!f;next} !f' src/content/projects/data-analysis-agent.mdx \
  | sed '/^```/,/^```/d' \
  | wc -w
```

Expected: ~7,500–8,000 words.

- [ ] **Step 2: Update `readTimeMinutes`** in the frontmatter to `Math.ceil(words / 280)` (280 wpm is standard reading speed for technical prose):

```yaml
readTimeMinutes: 28
```

- [ ] **Step 3: Update `lastUpdated`** to today's date

- [ ] **Step 4: Commit**

```bash
git add src/content/projects/data-analysis-agent.mdx
git commit -m "content(da-agent): set readTimeMinutes + lastUpdated"
```

### Task 4.13: Build + visual checklist + open PR #4

- [ ] **Step 1: Full local build + preview**

```bash
npm run build && npm run preview
```

Open `/projects/data-analysis-agent` and run the **PR #4 visual checklist:**

| Item | Pass criteria |
|---|---|
| TocSidebar shows 9 items | TL;DR / Problem / Approach / Worked examples / Architecture / Test suite (indented) / Evaluation / Limitations / What I'd do differently |
| All 8 H2s anchor correctly | Click each in TOC; smooth scroll lands cleanly with section heading at top |
| Code blocks | Dark theme, JetBrains Mono, syntax highlighted via Shiki |
| Tables (test suite + evaluation) | Aurora-styled borders, header row tinted, no horizontal scroll on desktop |
| SVG architecture diagram | Renders inline, max-width 100%, Aurora-tinted borders |
| Pull quote ("75% ABQ ...") | Teal left border, italic, light teal bg |
| TL;DR CTAs | Both buttons styled correctly, hover lifts |
| Read time + last updated | Show in meta strip below headline number |
| Mobile (375px) | TOC collapses to disclosure, main goes full-width, all content readable |

- [ ] **Step 2: Run Lighthouse on the preview URL**

Expected: Performance ≥ 90, Accessibility ≥ 95, Best Practices = 100, SEO ≥ 90.

- [ ] **Step 3: Push + open PR**

```bash
git push -u origin feat/v2-da-agent-content
gh pr create --base main --title "content(da-agent): expand to 7,800-word engineering deep-dive" --body "$(cat <<'EOF'
## Summary

PR #4 of the v2 redesign — **the pilot**. Replaces the ~700-word DA Agent MDX with the full 8-section engineering deep-dive per [spec §3.7](../blob/main/docs/superpowers/specs/2026-06-03-portfolio-v2-design.md#37-da-agent-mdx-content-outline-the-pilot).

8 sections:
1. TL;DR (200w)
2. Problem (1000w)
3. Approach (1200w)
4. Worked examples — 5–6 traces incl. self-correction + honest failure (1000w)
5. Architecture (1200w) + test-suite subsection (400w) + SVG diagram
6. Evaluation — DABench results, latency breakdown (1500w)
7. Limitations (800w)
8. What I'd do differently (500w)

**~7,800 words total.** All content backed by existing artifacts in the agent repo (no new evals run).

## ★ Critical: PAUSE point

After this PR merges, **do not start PR #5 (RAG content) until you sign off on the pilot.** Review the deployed page on production. If the writing voice, layout, table treatment, or anything else feels wrong, we fix the template here before replicating to 4 more projects.

## Test plan

- [ ] CI green
- [ ] Vercel preview deploys
- [ ] Visual checklist (9 items, see commit description)
- [ ] Lighthouse on preview: Perf ≥ 90 / A11y ≥ 95 / BP = 100 / SEO ≥ 90
- [ ] Final word-count audit reads as 7,500–8,500 words

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 4: Squash-merge after sign-off (you, not me)**

```bash
gh pr merge --squash --delete-branch
git checkout main && git pull origin main
```

---

# 🛑 PAUSE — Pilot sign-off

After PR #4 merges, the DA Agent page is the pilot. **Do not proceed to PRs #5–8 until:**

1. You've actually read the deployed page (or scrolled through it at minimum)
2. You're happy with the writing voice — if not, adjust the template here, not in 4 more PRs
3. The TocSidebar behavior on production matches your expectation
4. The eval results table reads cleanly
5. The mobile experience works for you

If anything's off: a short follow-up PR fixes it before the replication phase starts.

---

# Phase 5 — PRs #5–8: Replication template

Once the pilot is signed off, the remaining 4 projects each get their own PR following the same template. Each PR follows the **same task structure as PR #4** with content adapted per project:

| PR | Branch | Project | Spec material |
|---|---|---|---|
| #5 | `feat/v2-rag-content` | `document-qa-rag.mdx` | Source: `document-qa-rag` repo. Category: RAG. |
| #6 | `feat/v2-churn-content` | `churn-prediction.mdx` | Source: existing MDX (300w stub) + Kaggle notebook. Category: Classical ML. |
| #7 | `feat/v2-mt-content` | `multi-tool-agent.mdx` | Source: existing MDX stub. Category: Agents. |
| #8 | `feat/v2-rec-content` | `movie-recommender.mdx` | Source: existing MDX stub. Category: Classical ML. |

Each PR mirrors PR #4's task sequence:
- Branch + skeleton frontmatter (with `v2: true` set in this PR, since each project opts into v2 with its content rewrite)
- Section 1 (TL;DR) through Section 8 (What I'd do differently), with one commit per section
- `readTimeMinutes` + `lastUpdated` updated based on final word count
- Visual checklist + Lighthouse + PR

**Detailed task breakdowns for PRs #5–8 are deferred until after PR #4 sign-off.** The patterns that emerge from PR #4 (table styles, worked-examples format, voice) become the template, and that template can't be locked in until PR #4 ships and we've seen what worked.

---

# Phase 6 — PR #9: Cleanup

**Branch:** `feat/v2-cleanup`
**Goal:** Remove the legacy `ProjectLayout.astro`, the `v2` schema flag, and the layout-routing branch in `[...slug].astro`. Net result: one layout, one route, no migration scaffolding.
**Estimated LoC:** ~30 changed
**Prerequisite:** PRs #5, #6, #7, #8 all merged.

### Task 9.1: Branch + remove the v2 schema flag

**Files:**
- Modify: `src/content.config.ts`
- Modify: all 5 MDX files (remove `v2: true` line)

- [ ] **Step 1: Branch**

```bash
git checkout main && git pull origin main
git checkout -b feat/v2-cleanup
```

- [ ] **Step 2: Remove the `v2` field from the schema**

In `src/content.config.ts`, delete:

```ts
    v2:              z.boolean().default(false),
```

- [ ] **Step 3: Remove `v2: true` from all 5 MDX frontmatters**

```bash
for f in src/content/projects/*.mdx; do
  sed -i '' '/^v2: true$/d' "$f"
done
```

- [ ] **Step 4: Build — expect failure** in `[...slug].astro` because it references `entry.data.v2`

```bash
npm run build
```

Expected error: `Property 'v2' does not exist on type ...`

- [ ] **Step 5: Don't commit yet** — Task 9.2 fixes the layout routing.

### Task 9.2: Simplify `[...slug].astro` to always use V2

- [ ] **Step 1: Replace `src/pages/projects/[...slug].astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import ProjectLayoutV2 from '../../layouts/ProjectLayoutV2.astro';

export async function getStaticPaths() {
  const projects = await getCollection('projects');
  return projects.map(entry => ({
    params: { slug: entry.id.replace(/\.mdx?$/, '') },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content, headings } = await render(entry);
---
<ProjectLayoutV2 entry={entry} headings={headings}>
  <Content />
</ProjectLayoutV2>
```

- [ ] **Step 2: Delete the legacy layout**

```bash
git rm src/layouts/ProjectLayout.astro
```

- [ ] **Step 3: Build**

```bash
npm run build
```

Expected: success. All 5 project pages render through `ProjectLayoutV2`.

- [ ] **Step 4: Verify the routing works on all 5**

```bash
npm run preview
```

Visit `/projects/data-analysis-agent`, `/projects/document-qa-rag`, `/projects/churn-prediction`, `/projects/multi-tool-agent`, `/projects/movie-recommender` — all should render with the v2 layout.

- [ ] **Step 5: Commit all the cleanup in one commit**

```bash
git add src/content.config.ts src/pages/projects/\[...slug\].astro src/content/projects/*.mdx
git commit -m "chore: remove ProjectLayout v1 + v2 migration flag"
```

### Task 9.3: Open PR #9

- [ ] **Step 1: Push + open PR**

```bash
git push -u origin feat/v2-cleanup
gh pr create --base main --title "chore: remove legacy ProjectLayout + v2 migration flag" --body "$(cat <<'EOF'
## Summary

Final PR of the v2 redesign. With all 5 projects on `ProjectLayoutV2`, the migration scaffolding can come out:

- Delete `src/layouts/ProjectLayout.astro`
- Remove `v2: boolean` from the projects schema
- Remove `v2: true` from all 5 MDX frontmatters
- Simplify `[...slug].astro` to always use `ProjectLayoutV2`

Net: one layout, one route, no flags.

## Test plan

- [ ] CI green
- [ ] All 5 project pages render correctly on Vercel preview
- [ ] No visual regression vs the last v2 content PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 2: Squash-merge after green**

```bash
gh pr merge --squash --delete-branch
```

---

# Cross-cutting reference

## Quality gates (every PR)

1. **Build**: `npm run build` — zero errors, zero warnings
2. **CI**: `.github/workflows/build.yml` on Node 22 — green
3. **Vercel preview**: deploys successfully
4. **Lighthouse on preview**: Performance ≥ 90 / Accessibility ≥ 95 / Best Practices = 100 / SEO ≥ 90
5. **No regression** vs `main` on those four metrics
6. **Mobile at 375px**: renders without horizontal scroll; sidebar collapses to disclosure on deep-dive pages
7. **Visual checklist** (per-PR, listed in each Phase above) — pass
8. **No regressed scrub**: `grep -r "font-serif\|accent-cream\|accent-gold\|numbered-sections\|hero-rule" src/` returns zero hits (after PR #2)

## Skills to reference during execution

- @superpowers:subagent-driven-development — recommended for executing this plan one task per subagent
- @superpowers:executing-plans — alternative for inline execution
- @superpowers:committing-changes — for git workflow discipline

## Risks + mitigations (from spec §4.2, restated)

| Risk | Mitigation |
|---|---|
| Aurora gradient fights with dense eval / test-suite tables | PR #3 preview is the gate to verify table readability. Adjust before PR #4 commits to the table treatment. |
| Mobile TOC sidebar doesn't fit below 900px | Already designed: `<details>` disclosure fallback in `TocSidebar.astro` |
| Astro `render()` heading shape may not match expectations | Spike in Task 3.3 (5-min test) |
| `@fontsource` packages add ~140KB to bundle | Self-hosted is the right call (privacy + reliability). Subset to Latin only; weights limited to 400/600/700 |
| Writing 5 × 7,800-word deep-dives is a slog | Mandatory sign-off pause after PR #4. If pilot voice is wrong, fix template before replicating. |

## What's out of scope (from spec §5, restated)

Dark mode · Mobile-first redesign · Search · RSS · Analytics · Newsletter · Framer Motion · BlogLayout redesign · 404 redesign · Framework migration · New pytest tests · HF Space redesign · Contact form.

## Success criteria (from spec §6, restated)

1. Recruiter scans landing for 8s → "ML engineer, ships things, has taste."
2. Click to DA Agent → jump to Evaluation in one click via TOC.
3. Lighthouse Performance ≥ 90 (no regression).
4. Mobile renders cleanly at 375px.
5. After PR #8, all 5 projects use `ProjectLayoutV2`; PR #9 retires legacy code.
6. Zero `--font-serif` / `--accent-cream` / `--accent-gold` references after PR #1.
