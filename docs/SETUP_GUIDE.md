# Squad Explorations Setup Guide

> Quick start guide for designers setting up their own exploration workspace

---

## Prerequisites

Before starting, ensure you have:

✅ **Git installed** — Check with: `git --version`  
✅ **Claude Code** — Desktop app, CLI, or web version  
✅ **GitHub access** — Can clone public repos (no auth needed)

**If git is missing:**
- Mac: `brew install git` or [download here](https://git-scm.com)
- Windows/Linux: [Download here](https://git-scm.com)

---

## For New Users (Setting up a workspace)

### Option 1: Copy-Paste Setup Prompt (Easiest)

**See:** [`SETUP_PROMPT.md`](./SETUP_PROMPT.md) for the full prompt

1. Copy the entire prompt from SETUP_PROMPT.md
2. Paste into Claude Code
3. Answer 5 questions (squad name, themes, location, etc.)
4. Done! Workspace created in ~30 seconds

**What happens:**
- Clones the [template repository](https://github.com/schildsG2/squad-explorations-template)
- Personalizes files to your squad
- Creates epics for your themes
- Adds Elevate Prototyping Kit design system
- Installs `/new-epic` and `/new-exploration` skills

### Option 2: Use the Skill Directly

If you're already in a project with the skill:

```bash
cd ~/projects/
# In Claude Code:
/setup-squad-explorations
```

This runs the same interactive wizard as Option 1.

---

## For Existing Users (Using the workspace)

### Creating a New Epic

```bash
/new-epic
```

This will ask you for:
- Epic name (kebab-case, e.g., "pricing-optimization")
- Display title (e.g., "Pricing Optimization")
- Description (1-2 sentences)
- Tag for filtering (reads existing tags from your workspace, or creates new)
- Icon + color scheme
- Optional CLAUDE.md content

**Then it:**
- Creates epic directory structure
- Updates your homepage with epic card
- Updates epic count
- Offers to open the epic or create first exploration

### Creating a New Exploration

```bash
/new-exploration {epic-name}
```

Example:
```bash
/new-exploration pricing-optimization
```

**This will:**
- Auto-number your exploration (01, 02, 03...)
- Ask for an exploration name
- Copy the starter template
- Update the epic's index.html
- Update exploration count
- Offer to open the file

---

## What You Get

### Workspace Structure

```
your-squad-explorations/
├── index.html                 # Portal page (personalized to your squad)
├── epics/                     # Your epic themes
│   ├── pricing-optimization/
│   │   ├── index.html         # Epic gallery page
│   │   └── explorations/      # Numbered explorations (01, 02, 03...)
│   ├── purchase-flow/
│   └── company-insights/
├── shared/
│   ├── elevate-prototyping-kit/          # Design system (git submodule)
│   │   ├── tokens/elevate.css
│   │   ├── components/
│   │   ├── utilities.css
│   │   └── design-system/DESIGN.md
│   └── exploration-starter.html
├── research/spikes/           # Research & competitive analysis
├── .claude/                   # Skills (already installed!)
│   ├── new-epic.md
│   ├── new-exploration.md
│   └── setup-squad-explorations.md
├── CLAUDE.md                  # Squad-specific agent context
└── README.md                  # Template documentation
```

### Skills Available

All workspaces include these skills:

- `/new-epic` — Create a new epic with full structure
- `/new-exploration {epic-name}` — Start a numbered exploration
- `/setup-squad-explorations` — Set up a workspace (for helping teammates)

---

## Key Features

### Template-Based Setup
Setup clones the [squad-explorations-template](https://github.com/schildsG2/squad-explorations-template) and personalizes it. This ensures:
- Guaranteed consistency
- Tested, working code
- Fast setup (~30 seconds)

### Path-Agnostic Skills
All skills auto-detect the repository root using git. Works from anywhere in your workspace.

### Elevate Design System
Includes Elevate Prototyping Kit as a git submodule:
- Design tokens (CSS variables)
- Component templates
- Utility classes
- Complete DESIGN.md specifications
- Icon library

### Theme-Based Filtering
Filter chips on your homepage let you filter epics by theme/project area:
- "All" shows everything
- "Pricing Optimization" shows pricing-related epics
- "Purchase Flow" shows purchase-related epics

### Auto-Numbered Explorations
Explorations are automatically numbered (01, 02, 03...) for chronological tracking within each epic.

---

## Quick Start Workflow

1. **Set up workspace** (one-time, ~30 seconds):
   - Copy prompt from [`SETUP_PROMPT.md`](./SETUP_PROMPT.md)
   - Paste into Claude Code
   - Answer questions

2. **Create your first epic**:
   ```
   /new-epic
   ```

3. **Start exploring**:
   ```
   /new-exploration {epic-name}
   ```

4. **Build prototypes**:
   - Reference `shared/elevate-prototyping-kit/design-system/DESIGN.md`
   - Browse [Elevate Lookbook](https://www.g2.test/elevate/lookbook)
   - Use templates from `shared/elevate-prototyping-kit/components/templates/`

---

## Tips

### For Design Team Leads
Share [`SETUP_PROMPT.md`](./SETUP_PROMPT.md) with your squad. Anyone with Claude Code can set up a workspace in 30 seconds.

### For Individual Designers
You can create multiple workspaces for different projects:
```
~/projects/
├── buyer-intent-explorations/
├── search-discovery-explorations/
└── onboarding-explorations/
```

Each workspace is independent but uses the same Elevate Prototyping Kit design system.

### Keeping Elevate Prototyping Kit Updated
```bash
cd ~/projects/your-squad-explorations/
git submodule update --remote shared/elevate-prototyping-kit
```

This pulls the latest design system updates.

---

## Sharing Your Workspace

### Push to GitHub

```bash
cd ~/projects/your-squad-explorations/
git remote add origin <your-repo-url>
git push -u origin main
```

### Share with Your Squad

Other designers can clone and start immediately:
```bash
git clone --recurse-submodules <your-repo-url>
cd your-squad-explorations
/new-exploration {epic-name}
```

**Note:** `--recurse-submodules` ensures Elevate Prototyping Kit is cloned too.

---

## Troubleshooting

### "git: command not found"
Install git first:
- Mac: `brew install git` or [git-scm.com](https://git-scm.com)
- Windows/Linux: [git-scm.com](https://git-scm.com)

### "repository not found" when cloning template
The template repo is public. Check your network connection or GitHub access.

### Elevate Prototyping Kit submodule is empty
Run:
```bash
git submodule update --init --recursive
```

### Skills aren't available
Skills are in `.claude/` directory. Make sure you're running Claude Code from within your workspace.

---

## Questions?

- **Setup help**: See [`SETUP_PROMPT.md`](./SETUP_PROMPT.md) for the full walkthrough
- **Elevate questions**: See `shared/elevate-prototyping-kit/design-system/DESIGN.md`
- **Skill documentation**: See `.claude/new-epic.md` and `.claude/new-exploration.md`
- **Template repo**: [github.com/schildsG2/squad-explorations-template](https://github.com/schildsG2/squad-explorations-template)

---

**Happy prototyping! 🚀**
