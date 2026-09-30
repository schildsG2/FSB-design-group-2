# Squad Explorations Setup Prompt

> Copy-paste this entire prompt into Claude Code to set up your own exploration workspace

---

## Prerequisites

Before running the setup, ensure you have:

✅ **Git installed** — Check with: `git --version`  
✅ **Claude Code** — Desktop app, CLI, or web version  
✅ **GitHub access** — Can clone public repos (no auth needed)  

**If git is missing:**
- Mac: `brew install git` or download from [git-scm.com](https://git-scm.com)
- Windows: Download from [git-scm.com](https://git-scm.com)

---

## The Prompt

```markdown
Set up a new squad exploration workspace for me, similar to Chicago Labs but personalized to my squad.

This should create a complete HTML prototyping workspace with:
- Personalized portal page (index.html) with my squad name
- Elevate Prototyping Kit design system (as git submodule from https://github.com/schildsG2/elevate-prototyping-kit)
- Placeholder epic structures for my squad's themes
- Research directory for competitive analysis
- /new-epic and /new-exploration skills installed locally
- Squad-specific CLAUDE.md documentation

**Please follow this process:**

### Step 0: Verify git is installed

Check that git is available:
```bash
git --version
```

If git is not found, stop and tell me to install it first:
- Mac: `brew install git` or download from git-scm.com
- Windows/Linux: Download from git-scm.com

### Step 1: Ask me for information one question at a time

1. **Squad name** (e.g., "Buyer Intent", "Agent Marketplace")
2. **Directory name** — "I suggest: `{squad-kebab}-explorations` — type 'yes' to use this, or type your own"
3. **Installation location** — "I suggest: `~/projects/{dir-name}` — type 'yes' to use this, or type your own path"
4. **2-3 main themes/epics** I'll be exploring (e.g., "Pricing Optimization, Purchase Flow, Insights")
   - Note: Each theme will become both an epic AND a filter tag on the homepage
5. **Initialize as git repository?** (yes/no)

**Important:** For questions with suggestions, make it clear users can either type 'yes' to accept or type their own value directly.

### Step 2: Show me a summary and confirm

Before creating anything, show me:
- What will be created
- Where it will be located
- The epic placeholders
- Whether git will be initialized

Ask for confirmation to proceed.

### Step 3: Clone the template repository

**First, ensure the parent directory exists:**
```bash
# If installation path is ~/projects/buyer-intent-explorations
# Create ~/projects/ if it doesn't exist
mkdir -p ~/projects/
```

**Then clone the template:**
```bash
git clone https://github.com/schildsG2/squad-explorations-template.git {installation-path}
cd {installation-path}
rm -rf .git
```

**If I chose to initialize git, run:** `git init`

**Template structure (what gets cloned):**
```
{dir-name}/
├── index.html                    # Portal page (with {{PLACEHOLDERS}})
├── epics/
│   └── example-epic/             # Will be renamed/duplicated for my themes
│       ├── index.html            # Epic gallery page
│       └── explorations/
│           └── 01-example.html   # Placeholder exploration
├── shared/
│   ├── elevate-prototyping-kit-PLACEHOLDER.md  # (Will be replaced with actual submodule)
│   └── exploration-starter.html
├── research/spikes/
├── .claude/                      # Skills already included!
│   ├── new-epic.md
│   ├── new-exploration.md
│   └── setup-squad-explorations.md
├── CLAUDE.md                     # (with {{PLACEHOLDERS}})
└── README.md                     # Template documentation
```

### Step 4: Personalize all files

Use find/replace across all files to replace placeholders:

**Placeholders to replace:**
- `FSB Design Group 2` → My squad name (e.g., "Buyer Intent")
- `fsb-design-group-2` → kebab-case (e.g., "buyer-intent")
- `FSB-design-group-2` → directory name (e.g., "buyer-intent-explorations")
- `2026-09-30` → Today's date (e.g., "2026-04-29")
- `Sep 30, 2026` → Formatted date (e.g., "Apr 29, 2026")

**Files that get personalized:**
- `index.html` — Squad name in header, filter chips
- `CLAUDE.md` — Squad context and references
- `research/spikes/README.md` — Squad name references

### Step 5: Create epics from themes

Transform the `example-epic` for each of my themes:

**For first theme:**
```bash
mv epics/example-epic epics/{theme-1-kebab}
```

Replace in `epics/{theme-1-kebab}/index.html`:
- `{{EPIC_TITLE}}` → "Pricing Optimization"
- `{{EPIC_KEBAB}}` → "pricing-optimization"  
- `{{EPIC_DESCRIPTION}}` → Theme description

**For additional themes:** Copy the first epic and personalize:
```bash
cp -r epics/{theme-1-kebab} epics/{theme-2-kebab}
# Update placeholders for theme 2
cp -r epics/{theme-1-kebab} epics/{theme-3-kebab}
# Update placeholders for theme 3
```

**Update main index.html:**
- Add filter chip for each theme
- Duplicate epic card for each theme (with appropriate icons/colors)
- Update epic count from `(1)` to `({N})`

### Step 6: Add Elevate Prototyping Kit design system

Remove placeholder:
```bash
rm shared/elevate-prototyping-kit-PLACEHOLDER.md
```

If git initialized:
```bash
git submodule add https://github.com/schildsG2/elevate-prototyping-kit.git shared/elevate-prototyping-kit
```

When you reference the kit in HTML, use all 4 CSS files in this order:
```html
<link rel="stylesheet" href="../../shared/elevate-prototyping-kit/tokens/elevate.css">
<link rel="stylesheet" href="../../shared/elevate-prototyping-kit/components/elevate.css">
<link rel="stylesheet" href="../../shared/elevate-prototyping-kit/utilities.css">
<link rel="stylesheet" href="../../shared/elevate-prototyping-kit/icons/icons.css">
```

If no git:
```bash
git clone https://github.com/schildsG2/elevate-prototyping-kit.git shared/elevate-prototyping-kit
```

### Step 7: Initial commit (if git enabled)

```bash
git add .
git commit -m "Initial setup: {Squad Name} explorations workspace

- Created {N} epics: {list themes}
- Added Elevate Prototyping Kit design system
- Personalized for {Squad Name} squad

Generated with /setup-squad-explorations"
```

### Step 8: Final report

Show me:
- ✅ What was created (with file counts)
- 📍 Installation path
- 📝 Next steps:
  1. How to open the workspace
  2. How to create my first exploration
  3. Where to find Elevate design resources
- 🚀 Offer to open index.html in my browser

### Important guidelines:

**For epic icons and colors**, use these defaults unless I specify otherwise:
- First epic: Purple theme (#f2f0f9 background, #5746b2 icon)
- Second epic: Orange theme (#fff5f2 background, #ff492c icon)
- Third epic: Neutral theme (#f5f5f6 background, #201f23 icon)

**For epic icons**, choose from:
- Bar chart (analytics/performance themes)
- Shopping cart (purchase/buyer themes)
- Search icon (discovery/search themes)
- Building (dashboard/company themes)
- Document (content/reporting themes)

**Follow Elevate design system conventions:**
- Use Figtree font only
- 4px spacing units
- Semantic color tokens (text-default, bg-neutral-0, etc.)
- No pure black (#000000), use text-default (#201f23)

**All file paths must be correct:**
- Explorations reference: `../../shared/elevate-prototyping-kit/...`
- Epic index references: `../../shared/elevate-prototyping-kit/...`
- Main index references: `./shared/elevate-prototyping-kit/...`
- Always include `utilities.css` between `components/elevate.css` and `icons/icons.css`

**Error handling:**
- If path already exists, ask before overwriting
- If git is not available, warn and skip git steps
- If submodule fails, offer to clone elevate-prototyping-kit directly

### Verification checklist (before final report):

- ✅ All directories created
- ✅ index.html has correct number of epic cards
- ✅ Each epic has index.html and explorations/ directory
- ✅ exploration-starter.html exists with correct paths
- ✅ Skills copied to .claude/
- ✅ CLAUDE.md personalized to squad
- ✅ research/spikes/ structure created
- ✅ Git initialized (if requested)
- ✅ Elevate Prototyping Kit added as submodule or cloned
- ✅ Epic count badge matches actual epic count

---

After setup is complete, I should be able to:
1. Open index.html and see my personalized portal
2. Run `/new-epic` to create new epics
3. Run `/new-exploration {epic-name}` to start prototyping
4. Reference Elevate design specs at `shared/elevate-prototyping-kit/design-system/DESIGN.md`

Let's get started! 🚀
```

---

## How to Use This Prompt

1. **Copy the entire markdown block above** (everything between the triple backticks)
2. **Open Claude Code** in your terminal or desktop app
3. **Paste the prompt** and hit enter
4. **Answer the questions** as Claude walks you through setup
5. **Confirm the summary** when Claude shows you what will be created
6. **Done!** Your workspace is ready

---

## What Happens Next

Claude will:
- Ask you questions about your squad
- Show you a summary for confirmation
- Create the entire workspace structure
- Personalize everything to your squad
- Install the skills so you can start creating epics
- Offer to open your new workspace

Total time: ~5 minutes

---

## Example Interaction

```
You: [paste the prompt above]

Claude: Great! Let's set up your squad exploration workspace.

What is your squad name? (e.g., "Buyer Intent", "Agent Marketplace")

You: Buyer Intent

Claude: Directory name? (I suggest: buyer-intent-explorations — type 'yes' to use this, or type your own)

You: yes

Claude: Installation location? (I suggest: ~/projects/buyer-intent-explorations — type 'yes' to use this, or type your own path)

You: yes

Claude: What are 2-3 main themes or product areas your squad will be exploring?
(Each theme will become both an epic and a filter tag)

You: Pricing Optimization, Purchase Flow, Company Insights

Claude: Initialize as git repository? (yes/no)

You: yes

... [Claude shows summary and confirms] ...

Claude: Here's what I'll create:
- Squad: Buyer Intent
- Location: ~/projects/buyer-intent-explorations
- Epics: Pricing Optimization, Purchase Flow, Company Insights
- Git: Yes

Proceed? (yes/no)

You: yes

Claude: [creates everything]

✅ Setup complete! Your workspace is ready at ~/projects/buyer-intent-explorations
```

---

## Troubleshooting

**If git submodule fails:**
Claude will offer to clone Elevate Prototyping Kit directly instead.

**If the path already exists:**
Claude will ask if you want to choose a different location or overwrite.

**If you want to customize icons/colors:**
Just mention it when Claude asks for your epic themes, or customize later by editing the epic cards in index.html.

---

## After Setup

Once your workspace is created, see `SETUP_GUIDE.md` in your new workspace for daily workflow instructions.

**Quick reference:**
- Create epic: `/new-epic`
- Create exploration: `/new-exploration {epic-name}`
- View design specs: `shared/elevate-prototyping-kit/design-system/DESIGN.md`
- Browse components: https://www.g2.test/elevate/lookbook

---

**Questions?** Reach out to Sam.
