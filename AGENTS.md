# AGENTS.md — Project Instructions for AI Coding Agents

## Project

**WordPress → Hugo Migration for rowanemilia.com**

Migrating https://www.rowanemilia.com/ from WordPress to a local, self-hosted Hugo static site.

## Process: Document-First, Iteration-Driven

This project uses a **document-first workflow**. Before any code is written, and after any significant change, you must update the project documentation.

### The Two Canonical Documents

| File | Purpose |
|------|---------|
| `spec.md` | The **source of truth** for what the site is and should be — design, content inventory, structure, requirements |
| `prompt.md` | The **execution prompt** for an LLM coding agent — step-by-step instructions to build/re-build the site |

### Workflow Rules

1. **Always start by reading both `spec.md` and `prompt.md`** — they define the current state and plan.
2. **Before making any change** (adding a feature, fixing a bug, adjusting content):
   - First update `spec.md` to reflect the intended new state.
   - Then update `prompt.md` to include the execution steps for the change.
3. **After making any change** (code written, content migrated, config adjusted):
   - Update `spec.md` if the change altered anything the spec describes (layout, content list, URLs, dependencies, etc.).
   - Update `prompt.md` if the change introduced new steps or modified the build process.
4. **Keep both documents in sync with the actual codebase.** If a future agent runs `prompt.md` from scratch, it should produce a site that matches `spec.md`.

### Why This Matters

- This project may be worked on by multiple agents across multiple sessions.
- `spec.md` and `prompt.md` are the shared state between sessions.
- Outdated docs = wasted work. Keeping them current means every agent picks up where the last one left off.

### Scope of Updates

Update `spec.md` when you change:
- The theme design (colors, fonts, layout, images)
- Content (new posts, updated text, added/removed media)
- Site structure (new pages, changed URLs, different taxonomies)
- External dependencies (new embeds, changed hosting strategy)
- Build configuration (Hugo version, theme, parameters)

Update `prompt.md` when you change:
- The build or migration workflow steps
- Tools or commands used
- Order of operations
- Any new step a fresh agent would need to know

### Git Workflow

- Commit after each meaningful iteration.
- Commit messages should reference updates to `spec.md` and `prompt.md` when applicable.
- Example: `"Add contact page. Update spec.md with new page details and prompt.md with build step."`
