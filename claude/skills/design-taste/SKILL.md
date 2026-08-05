---
name: design-taste
description: Opinionated rules for view transitions, motion, and UI polish that prevent generic AI-generated design. Use when building or styling any web UI, adding animations, hover effects, page/route transitions, or when the user mentions view transitions, motion design, "AI slop", or making a site feel less generic.
---

# Design Taste

Core rule: **motion must communicate something** — spatial relationship, causality, or continuity. If an animation is decorative only, delete it. A site with 3 intentional animations beats one with 30 default ones.

## View transitions

Transition **only meaningfully shared elements** — the same logical object visible before AND after navigation:

- Card thumbnail → detail hero image (same image, same subject)
- List item title → page heading (same text, same entity)
- Persistent chrome (nav, player bar) that should feel anchored

Rules:

1. `view-transition-name` goes on the specific shared pair only. Never sprinkle names across a page hoping it "feels dynamic".
2. Names must be unique per page — in lists, assign the name dynamically to the clicked item only (or use `attr()`/inline style), not every row.
3. Elements that are NOT the same object must not morph into each other. A grid of unrelated posts cross-fades; it does not fly around.
4. Default root cross-fade is fine as-is. Don't add motion to it unless navigation has real spatial direction (e.g. drill-down → slide).
5. Exiting content: fade out fast (~120ms). Entering content: fade/slide in slightly slower (~200ms). Never animate both heavily.
6. Wrap in `@supports (view-transition-name: none)` or feature-detect `document.startViewTransition` — no polyfill jank.

## Hover states

Hover communicates affordance, not spectacle.

- Default vocabulary: color shift, underline, background tint, border emphasis. Pick ONE per element type and use it consistently.
- **Banned as default: `hover:scale-*` on everything.** Scale-up hover on every card/button/icon is the #1 AI-slop tell.
- Scale is acceptable only for: pressed state (`active:scale-[0.98]`), or a single hero interactive element — never sitewide.
- Interactive elements of the same type must share the same hover treatment. Mixed hover effects read as unintentional.

## Motion specs

- UI feedback (hover, press, toggle): 100–150ms. Small movements (dropdown, tooltip): 150–200ms. Larger (modal, page): 200–300ms. Nothing over 400ms except deliberate hero moments.
- Animate `transform` and `opacity` only. Never `width`/`height`/`top`/`margin` (layout thrash).
- Easing: `ease-out` for entering, `ease-in` for exiting, never `linear` for UI. One custom curve max per project, used everywhere.
- Always respect `prefers-reduced-motion: reduce` — disable transitions, keep instant state changes.
- No scroll-triggered fade-in-up on every section. If used at all: once, subtle (<16px travel), first viewport only.

## Anti-slop checklist

Reject these defaults unless there is a specific reason:

- Purple/blue gradient hero backgrounds, gradient text on headings
- Glassmorphism cards everywhere, `backdrop-blur` as decoration
- `rounded-2xl` + `shadow-lg` on every container
- Emoji as section icons in headings
- Uniform "lift" (`-translate-y-1 shadow-xl`) hover on all cards
- Marketing filler copy: "Supercharge", "Seamless", "Blazing fast", "Effortless"
- Three-column feature grid with icon-title-blurb as the default layout answer
- Animated counters, typewriter headlines, particle backgrounds

## Personal principles

Edit this section — this is the point of the skill. Current:

- Prefer fewer, stronger design moves over many weak ones.
- Typography and spacing carry the design; motion and color support it.
- When unsure, remove the effect.
