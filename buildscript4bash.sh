#!/bin/bash 

echo "Your recipe has been saved to finalRecipe.csv!"

cat selectedRecipe.json | jq -r '. | ["ID", "Title", "Total Prep and Cook Time", "Servings", "Source URL", "Spoonacular URL"], [.id, .title, .cooktime, .servings, .sourceUrl, .spoonacularUrl] | @csv' | tee finalRecipe.csv
