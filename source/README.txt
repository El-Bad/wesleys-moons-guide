Wesley's Moons Field Guide - build kit

Main file to share: ..\Wesleys-Moons-Field-Guide.html (single file, images embedded)

Layout (scripts expect this folder as their base, S):
  dump/      raw wikitext of both wikis
  parsed/    rendered HTML of every Wesley's Moons wiki page
  build/     index.html (page template), data/*.json, img/ (full-quality images), imgmap.json
  scripts/   build.py (pages + moons) -> build_items.py (items) -> post_build.py (merge) -> build_vanilla_ents.py + build_vanilla_loot.py + build_vanilla_ints.py + build_lore.py + build_crafting.py (then mod_recipeicons.py on build/index.html if rebuilding the template) (vanilla creatures, vanilla est. loot; fetch from the Lethal wiki) -> package_share.py (single file)
  mod*.py were one-off patches to build/index.html; they are already applied.

Rebuild the single file:
  python -X utf8 scripts/package_share.py build ../Wesleys-Moons-Field-Guide.html 420 1100 50
