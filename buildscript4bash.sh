#!/bin/bash 

echo ""
echo "Your recipe has been saved to finalRecipe.csv! View the contents below: "
echo ""
echo "-------------------------------------------------------------------------"

cat selectedRecipe.json | jq -r '. | ["ID", "Title", "Total Prep and Cook Time", "Servings", "Source URL", "Spoonacular URL"], [.id, .title, .cooktime, .servings, .sourceUrl, .spoonacularUrl] | @csv' | tee finalRecipe.csv
