#!/usr/bin/env python3
"""
ingest.py — expand the RecipeForToday database.

This pulls from TheMealDB, a free public recipe API built for developers.
It does NOT scrape recipe websites, and you shouldn't either: the written
instructions, headnotes and photos on a food blog are copyrighted work.
Ingredient lists are facts and generally aren't protected, but the prose
around them is, and republishing it on your own domain is infringement.

Legitimate ways to grow the pot, in rough order of how much work they are:
  1. Write your own. The 30 seed recipes are original and CC BY-SA 4.0.
  2. User submissions with an explicit license grant (see CONTRIBUTING.md).
  3. Open APIs like TheMealDB, with attribution. That's what this does.
  4. Public-domain cookbooks — anything published in the US before 1930
     is PD. Project Gutenberg has hundreds. Great source of cursed recipes.

Everything this writes lands in data/incoming.json for you to review.
It never overwrites data/recipes.json.

Usage:
    python3 tools/ingest.py --letters a b c
    python3 tools/ingest.py --random 25
"""

import argparse
import json
import pathlib
import sys
import time
import urllib.request

API = "https://www.themealdb.com/api/json/v1/1"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "incoming.json"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "RecipeForToday/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def normalize(meal):
    """Map TheMealDB's flat 20-slot ingredient shape into our schema."""
    ingredients = []
    for i in range(1, 21):
        name = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if name:
            ingredients.append(f"{measure} {name}".strip())

    raw = (meal.get("strInstructions") or "").replace("\r\n", "\n")
    steps = [s.strip() for s in raw.split("\n") if len(s.strip()) > 3]
    if len(steps) < 2:
        steps = [s.strip() + "." for s in raw.split(". ") if len(s.strip()) > 3]

    return {
        "id": "mdb" + str(meal.get("idMeal")),
        "title": meal.get("strMeal"),
        "author": meal.get("strSource") or "TheMealDB",
        "source": meal.get("strSource") or "https://www.themealdb.com",
        # TheMealDB has no ratings. You have to supply these yourself before
        # a recipe can enter the pot — the app skips anything with rating null.
        "rating": None,
        "votes": 0,
        "time": "—",
        "servings": 4,
        "difficulty": "Medium",
        "tags": [t for t in [meal.get("strCategory"), meal.get("strArea")] if t],
        "ingredients": ingredients,
        "steps": steps,
        "verdict": "",
        "_needs": ["rating", "votes", "time", "verdict"],
        "_license": "Sourced via TheMealDB. Confirm attribution terms before publishing.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--letters", nargs="*", help="fetch every meal starting with these letters")
    ap.add_argument("--random", type=int, default=0, help="fetch N random meals")
    args = ap.parse_args()

    if not args.letters and not args.random:
        ap.error("give me --letters or --random")

    seen, out = set(), []

    for letter in args.letters or []:
        print(f"  fetching '{letter}'...", file=sys.stderr)
        data = get(f"{API}/search.php?f={letter}") or {}
        for meal in data.get("meals") or []:
            if meal["idMeal"] not in seen:
                seen.add(meal["idMeal"])
                out.append(normalize(meal))
        time.sleep(0.4)

    for n in range(args.random):
        data = get(f"{API}/random.php") or {}
        for meal in data.get("meals") or []:
            if meal["idMeal"] not in seen:
                seen.add(meal["idMeal"])
                out.append(normalize(meal))
        time.sleep(0.4)

    OUT.write_text(json.dumps({"recipes": out}, indent=2, ensure_ascii=False))

    print(f"\nWrote {len(out)} recipes to {OUT.relative_to(ROOT)}")
    print("Next: set a rating on each one, then merge into data/recipes.json.")
    print("Keep the two brackets balanced — the coin flip needs both sides stocked.")


if __name__ == "__main__":
    main()
