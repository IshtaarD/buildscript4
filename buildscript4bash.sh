#!/bin/bash 

echo ""
echo "Your recipe has been saved to finalRecipe.csv! View the contents below: "
echo ""
echo "-------------------------------------------------------------------------"

# takes the created json file from the python script and pipes it into jq to parse data and convert to a csv format. The output piped to the tee command to write to a csv file and output the results for the user in the terminal
cat selectedRecipe.json | jq -r '. | ["ID", "Title", "Total Prep and Cook Time", "Servings", "Source URL", "Spoonacular URL"], [.id, .title, .cooktime, .servings, .sourceUrl, .spoonacularUrl] | @csv' | tee finalRecipe.csv
