# Adding recipes to the pot

## The one hard rule

**Only submit recipes you wrote yourself, or that are in the public domain.**

Do not copy from food blogs, cookbooks published after 1930, recipe apps, or
YouTube descriptions. Ingredient lists are facts and generally aren't
copyrightable, but the written method, the headnote and the photos are. Pasting
them here puts the whole site at risk.

Public domain is fine and encouraged. Anything published in the US before 1930
is fair game, and pre-war community cookbooks are a goldmine of authentically
terrible food.

## The second hard rule

**Bad has to mean unappetizing, not unsafe.**

A one-star recipe should be something nobody wants to finish. It must never be
something that could hurt someone. Concretely, a submission is rejected if it:

- undercooks meat, poultry, seafood or eggs, or omits a temperature check
  where one is needed
- stores anything at an unsafe temperature, or improvises with canning,
  fermenting or curing
- calls for an inedible, non-food or wildly excessive quantity of an ingredient
- ignores a common severe allergen without naming it in the ingredient list

Cursed is the goal. Hazardous is a rejection.

## Format

Add an object to the `recipes` array in `data/recipes.json`:

```json
{
  "id": "r031",
  "title": "Something Regrettable",
  "author": "@yourhandle",
  "source": "RecipeForToday Community",
  "rating": 1.7,
  "votes": 0,
  "time": "25 min",
  "servings": 4,
  "difficulty": "Easy",
  "tags": ["cursed", "dinner"],
  "ingredients": ["1 cup of the first mistake", "2 tbsp of the second"],
  "steps": ["Do the thing.", "Regret the thing."],
  "verdict": "One sentence on why it landed where it landed."
}
```

Notes on the fields:

- `id` — unique, sequential, `rNNN`.
- `rating` — 0.0 to 5.0, one decimal. **This is the punchline of the whole
  site**, so be honest. 2.5 and below is the bad bracket; 2.6 and up is the good
  one. Don't rate your own recipe generously.
- `steps` — write them properly. The player is cooking from this with no photos
  and no video. Say what "done" looks like, and call out the step people get
  wrong. The seed recipes are the standard to match.
- `verdict` — revealed with the rating. One or two sentences, dry.

## Keep the brackets balanced

The coin flip needs both sides stocked. If the pot has 40 good recipes and 12
bad ones, players in the bad bracket see the same twelve constantly. Check the
split before you open a PR:

```bash
python3 -c "import json;r=json.load(open('data/recipes.json'))['recipes'];print(sum(x['rating']>2.5 for x in r),'good /',sum(x['rating']<=2.5 for x in r),'bad')"
```

## Before you open a PR

```bash
python3 -c "import json;json.load(open('data/recipes.json'));print('valid JSON')"
```

Then open `index.html` in a browser and roll a few times.

By submitting, you agree to license your recipe under CC BY-SA 4.0.
