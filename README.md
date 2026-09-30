# Squad Explorations Template

> **This is a template repository.** Do not edit directly — use the setup wizard to create a personalized copy for your squad.

## What This Is

A ready-to-clone template for creating squad-specific design exploration workspaces at G2. Includes:

- ✅ Complete HTML structure with Elevate design system
- ✅ Example epic and exploration
- ✅ Research directory structure
- ✅ `/new-epic` and `/new-exploration` skills
- ✅ Squad-specific CLAUDE.md

## How to Use This Template

### Option 1: Setup Wizard (Recommended)

Use the `/setup-squad-explorations` skill in Claude Code:

```bash
cd ~/projects/
# In Claude Code:
/setup-squad-explorations
```

The wizard will:
1. Clone this template
2. Ask for your squad name and themes
3. Personalize all files
4. Add Elevate Prototyping Kit as a submodule
5. Create placeholder epics for your themes

### Option 2: Manual Setup

```bash
# Clone to your squad directory
git clone https://github.com/[org]/squad-explorations-template.git my-squad-explorations
cd my-squad-explorations

# Remove template .git
rm -rf .git

# Initialize as new repo
git init

# Add Elevate Prototyping Kit
git submodule add https://github.com/schildsG2/elevate-prototyping-kit.git shared/elevate-prototyping-kit

# Find and replace placeholders:
# FSB Design Group 2 → Your Squad Name
# fsb-design-group-2 → your-squad-kebab
# fsb-design-group-2 → your-squad-tag
# FSB-design-group-2 → your-directory-name
# {{EPIC_TITLE}} → Your Epic Title
# {{EPIC_KEBAB}} → epic-kebab
# {{EPIC_DESCRIPTION}} → Epic description
# 2026-09-30 → 2026-04-29
# Sep 30, 2026 → Apr 29, 2026
```

## What Gets Personalized

When you use the setup wizard, these files are customized:

- `index.html` — Squad name, epic cards, filters
- `CLAUDE.md` — Squad context and references
- `epics/*/index.html` — Epic titles, descriptions, breadcrumbs
- `research/spikes/README.md` — Squad name references

## Template Structure

```
squad-explorations-template/
├── README.md                       # This file
├── index.html                      # Portal (with placeholders)
├── CLAUDE.md                       # Agent context (with placeholders)
├── epics/
│   └── example-epic/               # Template epic to duplicate
│       ├── index.html              # Epic gallery
│       └── explorations/
│           └── 01-example.html     # Example exploration
├── shared/
│   ├── elevate-prototyping-kit/    # Added as submodule during setup
│   └── exploration-starter.html    # Template for new explorations
├── research/spikes/                # Research directory
└── .claude/                        # Skills
    ├── new-epic.md
    ├── new-exploration.md
    └── setup-squad-explorations.md
```

## Placeholders Reference

| Placeholder | Example | Description |
|-------------|---------|-------------|
| `FSB Design Group 2` | "Buyer Intent" | Display name |
| `fsb-design-group-2` | "buyer-intent" | Kebab-case identifier |
| `fsb-design-group-2` | "buyer-intent" | Filter tag |
| `FSB-design-group-2` | "buyer-intent-explorations" | Directory name |
| `{{EPIC_TITLE}}` | "Pricing Optimization" | Epic display name |
| `{{EPIC_KEBAB}}` | "pricing-optimization" | Epic directory name |
| `{{EPIC_DESCRIPTION}}` | "..." | Epic description |
| `2026-09-30` | "2026-04-29" | ISO date |
| `Sep 30, 2026` | "Apr 29, 2026" | Human-readable date |

## Maintaining the Template

To update this template:

1. Make changes to template files
2. Keep placeholders intact (`{{...}}`)
3. Test with setup wizard
4. Commit and push

Existing squad workspaces won't be affected — they're independent copies.

## Questions?

See the setup documentation in your personalized workspace, or reach out to Sam.
