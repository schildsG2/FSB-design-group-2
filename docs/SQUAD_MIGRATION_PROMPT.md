# Migrate to Elevate G2

Your squad's explorations workspace currently uses `elevate-lite` — a manually-synced snapshot of G2's design system CSS. We've moved to `elevate-prototyping-kit`, which pulls CSS directly from [`@g2crowd/elevate`](https://github.com/g2crowd/elevate-g2) (the same package UE uses in production). This also brings in a browsable component examples gallery and a supplemental utilities file.

**Your old explorations are not affected.** Only forward-looking files (starter template, index pages, docs, skills) need updating.

Copy the prompt below into Claude Code while inside your squad workspace.

---

## Migration Prompt

```
Migrate this squad explorations workspace from elevate-lite to the Elevate Prototyping Kit (backed by @g2crowd/elevate).

The new repo is: https://github.com/schildsG2/elevate-prototyping-kit.git
The new local path is: shared/elevate-prototyping-kit/

Steps:

1. Check whether shared/elevate-lite exists:
   a) If it is a git submodule (check with: git submodule status | grep elevate-lite):
      - git submodule deinit shared/elevate-lite
      - git rm shared/elevate-lite
      - rm -rf .git/modules/shared/elevate-lite
   b) If it is regular files (not a submodule): leave it in place — do NOT delete it.
   c) If it does not exist at all: skip to step 2.

2. Add the new submodule:
   git submodule add https://github.com/schildsG2/elevate-prototyping-kit.git shared/elevate-prototyping-kit

3. In ALL .html files, update CSS <link> href attributes:
   shared/elevate-lite/tokens/elevate.css     → shared/elevate-prototyping-kit/tokens/elevate.css
   shared/elevate-lite/components/elevate.css  → shared/elevate-prototyping-kit/components/elevate.css
   shared/elevate-lite/icons/icons.css         → shared/elevate-prototyping-kit/icons/icons.css

   ALSO add a NEW 4th link tag between components and icons in every HTML file:
   <link rel="stylesheet" href="[SAME_PREFIX]shared/elevate-prototyping-kit/utilities.css">

   Use the same relative path prefix as the other 3 link tags in each file.
   Do NOT change epic card links, nav hrefs, or any other attributes — only <link rel="stylesheet"> hrefs.

4. In ALL .md files, replace: elevate-lite → elevate-prototyping-kit

5. In ANY .claude/*.skill files, update:
   - The git submodule add URL: elevate-lite.git → elevate-prototyping-kit.git
   - The submodule path argument: shared/elevate-lite → shared/elevate-prototyping-kit
   - Any CSS link href strings inside HTML templates in the skill
   - Add the utilities.css link tag to any HTML template strings in the skills
   - Text "Elevate Lite" → "Elevate Prototyping Kit"

6. Backward compatibility: if shared/elevate-lite/ no longer exists after step 1
   (because it was a submodule and was removed), copy the new kit as a fallback:
   cp -r shared/elevate-prototyping-kit/ shared/elevate-lite/
   This ensures any old exploration HTML files that still reference the old path continue to work.

7. Verify:
   - grep -r 'elevate-lite' --include="*.html" . | grep 'href.*elevate-lite'
     (should be zero — no CSS link hrefs pointing to elevate-lite)
   - grep -rc 'utilities.css' --include="*.html" .
     (every HTML file with CSS links should show a count of 1)

8. Commit everything:
   git add -A
   git commit -m "Migrate from elevate-lite to elevate-prototyping-kit (elevate-g2)"
```

---

## What changes

- **CSS source**: now from `@g2crowd/elevate` npm dist — same package UE uses in production
- **4 CSS files** instead of 3: `tokens/elevate.css`, `components/elevate.css`, `utilities.css` (new), `icons/icons.css`
- **Component examples gallery**: browse `shared/elevate-prototyping-kit/examples/index.html` for 45 live component pages
- **Icons, nav shells, templates**: all still available, same location within the kit

## Notes

- **No visual changes** — components render the same. The CSS source changed but the output is equivalent.
- **Old explorations keep working** — step 6 ensures backward compat for any HTML that still references `shared/elevate-lite/`.
- **Rollback** — if anything looks wrong, `git revert HEAD` takes you back immediately.
- **New explorations** — after migration, always use `shared/elevate-prototyping-kit/` with all 4 CSS link tags.
