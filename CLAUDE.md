# FSB Design Group 2 Explorations — Agent Context

> Auto-loaded context for any work in this repository.

---

## Squad Overview

**FSB Design Group 2 Explorations** is a unified repository for FSB Design Group 2 product design explorations and rapid HTML prototypes. This is a design-first workspace for validating concepts before production implementation.

**Purpose:**
- Rapid HTML prototyping using the Elevate design system
- Design explorations for new FSB Design Group 2 features
- Competitive research and reference material
- Shared component library for prototyping

**Philosophy:**
- Design-first: validate UX before building features
- Elevate-first: maintain 1:1 fidelity with production design system
- Rapid iteration: HTML prototypes over full implementations
- Lightweight: simple static HTML, no build tools required

---

## Repository Structure

```
FSB-design-group-2/
├── index.html              ← Portal to all epics
├── shared/                 ← Design system, components, tokens
│   ├── elevate-prototyping-kit/       ← Elevate design system (git submodule)
│   └── exploration-starter.html
├── epics/                  ← Individual feature explorations
│   └── example-epic/       ← Replace with your actual epics
└── research/               ← Competitive analysis, spikes
    └── spikes/
```

---

## Design System: Elevate First

**CRITICAL:** Always use the Elevate design system. Never invent UI patterns.

### Primary Resources:

1. **Specifications**: `./shared/elevate-prototyping-kit/design-system/DESIGN.md`
2. **Visual Reference**: [Elevate Lookbook](https://www.g2.test/elevate/lookbook)
3. **HTML Templates**: `./shared/elevate-prototyping-kit/components/templates/`
4. **Design Tokens**: `./shared/elevate-prototyping-kit/tokens/elevate.css`

### Workflow:
1. Read DESIGN.md section for component
2. Extract exact specifications
3. Check if HTML template exists
4. Build from specs if template doesn't exist
5. Reference Lookbook for visual confirmation

---

## Exploration Conventions

### Starting a New Exploration

Use the `/new-exploration {epic-name}` skill to create numbered explorations.

### File Naming

- **Explorations**: `##-descriptive-name.html` (e.g., `01-initial-concept.html`)
- **Components**: `kebab-case.html`

### Code Style

- **Elevate utilities**: Use `elv-` prefix
- **Component classes**: Use BEM-like pattern
- **Semantic HTML**: Use proper tags
- **Accessibility**: Always include ARIA attributes

---

## Key Design Principles

Follow Elevate design system principles:

- **Trust-First**: G2's trust layer is first-class UI
- **Answer-First**: Every screen answers a clear question
- **Calm Density**: Information-rich but not cluttered
- **Typography**: Only Figtree, never pure black
- **Color**: Use semantic tokens
- **Spacing**: 4px base unit
- **Shadows**: Subtle, diffused, max 12% opacity

---

## Available Skills

- `/new-epic` — Create a new epic with complete scaffolding
- `/new-exploration {epic-name}` — Start a numbered exploration in an epic

---

## Questions?

- **Design system**: Check `./shared/elevate-prototyping-kit/design-system/DESIGN.md`
- **Components**: Browse Elevate Lookbook
- **Project structure**: This file

---

**This is a design exploration workspace.** Prioritize rapid iteration and Elevate fidelity.
