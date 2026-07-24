# RecipeForToday

Gamble on dinner. Three rolls a day, drawn blind from the pot. Half the recipes are genuinely good, half are genuinely not, and you don't find out which until after you've eaten it.

Static site. No build step, no dependencies, no server. Drop it on GitHub Pages and it works.

---

## Deploy it in five minutes

1. Create a new repo on GitHub named `recipefortoday`.
2. Copy the contents of this folder into it and push:

   ```bash
   git init
   git add .
   git commit -m "First pot"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/recipefortoday.git
   git push -u origin main
   ```

3. In the repo, go to **Settings → Pages**. Under "Build and deployment", set Source to **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
4. Wait about a minute. Your site is at `https://YOUR-USERNAME.github.io/recipefortoday/`.

### Custom domain

Buy a domain, then add a file named `CNAME` at the repo root containing just your domain:

```
recipefortoday.com
```

At your registrar, point the DNS at GitHub:

| Type  | Name | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | YOUR-USERNAME.github.io |

Back in Settings → Pages, enter the domain and tick **Enforce HTTPS**.

---

## What's in here

```
index.html          The entire site. HTML, CSS, JS, and the 30 seed recipes.
data/recipes.json   The same 30 recipes as a standalone database file.
tools/ingest.py     Pulls new recipes from TheMealDB's open API.
CONTRIBUTING.md     Submission format and the license grant.
```

`index.html` is deliberately one file. It ships with the recipe data inlined so it works from `file://`, off a CDN, or anywhere else with zero configuration.

---

## How the game actually works

**The coin flip comes first.** Every roll flips a fair coin, *then* picks a recipe inside the winning bracket — 2.6–5.0 stars for heads, 0–2.5 for tails. Doing it in that order guarantees an exact 50/50 no matter how lopsided the database gets as it grows. Verified at 50.00% over 200,000 simulated rolls.

**You see all 30 before anything repeats.** If your coin lands on a bracket you've already exhausted, the draw crosses to the other side rather than handing you a duplicate.

**The rating is sealed.** The player gets the complete recipe — every ingredient, every step — but the star rating, vote count and verdict stay under a lid until they press "I cooked it." That's the whole point of the product, so it's enforced in the render, not just hidden with CSS.

**Three rolls a day**, reset at local midnight.

---

## The three honest limitations

### 1. The recipes are original, not scraped

You asked me to scour the internet. I can't, and neither should the site.

Recipe **ingredient lists** are facts and generally aren't copyrightable in the US. The **written instructions, headnotes and photographs** absolutely are. Copying them onto your own domain is straightforward infringement, and food publishers are unusually aggressive about it — this is a well-trodden way to get a repo taken down.

So all 30 seed recipes are original work, written for this project, released CC BY-SA 4.0. Half were written to be genuinely good and half to be genuinely bad, which serves the gamble better than scraped content would anyway.

To grow the pot legitimately, in order of effort:

- **Write more.** Match the schema in `data/recipes.json`.
- **Take submissions.** `CONTRIBUTING.md` has the format and the license grant.
- **Use an open API.** `tools/ingest.py` pulls from [TheMealDB](https://www.themealdb.com/api.php), which is free for developers and expects attribution. Run `python3 tools/ingest.py --random 25`. It writes to `data/incoming.json` for review and never touches your live database.
- **Mine public-domain cookbooks.** Anything published in the US before 1930 is PD. Project Gutenberg has hundreds of them, and they are a phenomenal source of authentically terrible recipes.

Note that TheMealDB has no ratings, so ingested recipes come through with `rating: null` and the app skips them until you assign one. That's the manual step, and there isn't a way around it — the rating *is* the game.

### 2. Bad means unappetizing, never unsafe

Every low-rated recipe is disgusting, not dangerous. Nothing undercooks meat, nothing improvises with canning, nothing risks botulism. The mug meatloaf specifies a thermometer check; the garlic confit specifies refrigeration. **Hold any recipe you add to the same line.** A site that randomly serves strangers a food-safety hazard is a genuinely different and much worse product than the one you described.

### 3. Accounts and the daily limit are local, not real

GitHub Pages serves static files. There is no server, so there is no real authentication and no way to enforce anything.

What's implemented: a handle-only local profile in `localStorage`, carrying your pantry, roll history and cooked recipes. Signing in migrates anything you collected as a guest. The 3-per-day limit lives in the same place.

What that means: it's per-browser, it's gone if you clear site data, and anyone who opens devtools can give themselves unlimited rolls. Fine for launch. Not fine once people care.

---

## When you're ready for a real backend

The two things that need to change are marked in `index.html` as sections **1. DATA LAYER** and **2. STORAGE**. Nothing else touches persistence.

**Supabase** is the shortest path — free tier, hosted Postgres, built-in auth, and it works from a static page with no server of your own:

1. Create a project, then a `recipes` table matching the JSON schema and a `rolls` table of `(user_id, recipe_id, rolled_at, cooked)`.
2. Turn on Row Level Security so users can only read their own rolls.
3. Replace `loadRecipes()` with a Supabase query. Replace `load()`/`save()` with calls to the `rolls` table.
4. Move the daily limit into a Postgres function that counts today's rows server-side and refuses a fourth. **This is the only way the limit becomes real.**

Search, which you flagged as a later phase, wants the database in place first — then it's a `title ILIKE` query plus a tag filter, or Postgres full-text search if you want it to be good. Worth deciding early whether search is allowed to reveal ratings, because if it is, it undercuts the sealed-lid mechanic that the whole site is built on.

---

## License

Code: MIT. Recipes: CC BY-SA 4.0.
