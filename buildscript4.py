# Ishtaar Desravines
# Build Script #4
# Due September 15, 2022

# Objective: This program uses the Spoonacular API to access a database of recipe information to give the user meal options to select from. 

# Restrictions: 
# I. Must have your own API key from Spoonacular. Make an account at https://spoonacular.com/food-api.
# II. API key that is stored in a file must be in the same directory as this file.

# Additional Note: selectedRecipe.json and finalRecipe.csv are inlcuded on ther Github repository as examples of the file outputs of this script. 



#calling various modules to be used in the script below. 
import requests
import json
import inquirer
import subprocess


# reads the API KEY that is stored in a separate file. 
try:
    with open('apikey.txt', 'r') as file:
        apiKey = file.read()
# if there is no file, it notifies the user. 
except:
    print('File apikey.txt not found')
    exit(1)




print('WELCOME TO THE RECIPE HELPER')
print('-----------------------------------------')


# asks the user if they have any dietary restrictions
print("\nI'm here to help you find something to eat tonight! \n Do you have any of these dietary restrictions? ")

# creates a dictionary with the dietary options.
diets = { 'A' : 'Gluten Free', 'B' : 'Ketogenic', 'C': 'Vegetarian', 'D' : 'Pescetarian'}

#iterates through the dictionary to print out the options for the user
for letter, diet in diets.items(): 
    print(f'{letter}. {diet}')


# asks the user for a letter selection and assigns their dietary restriction the 'diet' parameter that will be used in the url
letter = input('Please select your diet by letter or type "No": ')
if letter in diets.keys():  
    user_diet = diets[letter]
    print(f'You have a {user_diet.upper()} diet.') 
# if the user does not have any dietary restrictions, it leaves the parameter 'diet' in the url blank. 
if letter.lower() == 'no': 
    user_diet = ''
    print('You have no dietary restrictions!')
   
print('-----------------------------------------------')


# asks user for a main ingredient they want in their dish and assigns it to a variable that will be used for the includeIngredients parameter
must_have = input('Choose a main ingredient you want in your dish: ')


# asks the user if allergic to any ingredients to get the exludeIngredients parameter.
answer = input('\nDo you have any food allergies? (yes/no) ')


# if user selects yes, he/she has to enter the ingredients separated by a comma. Their input is then displayed
if answer.lower() == 'yes':
    allergies = input('Please enter all ingredients you are allergic to separated by commas: ')
    print(f'You are allergic to: {allergies.upper()}')
# if the user does not have any allergies, prints "You have no allergies" and leaves the excludeIngredients parameter blank. 
if answer == 'no': 
    allergies = ''
    print('You have no allergies!')
print('---------------------------------------------------------')


# asks the user how much time they have to make their meal and assigns the value to the time variable that will be used for the maxReadyTime parameter
time = input('\nHow much time do you have to cook and prep in minutes? ')

print('--------------------------------------------------------')


# asks the user to select how indecisive they are ona scale and assigns the number of choices he/she gets to the number parameter
scale = int(input('\nFinally, how indecisive are you from a scale of 1 to 3. \n 1 = Very Decisive \n 2 = In Between \n 3 = Very Indecisive  \n'))
choices = {1 : 4, 2 : 2, 3 : 1 }
num_of_choices = choices[scale]


# GET request to Spoonacular API with their preset search parameters. The values of the parameters are given through
url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={apiKey}&maxReadyTime={time}&number={num_of_choices}&instructionsRequired=true&excludeIngredients={allergies}&diet={user_diet}&includeIngredients={must_have}"
# returns all recipes that fit the parameters in a json format
response = requests.request("GET", url)
# converts the json string to a dictionary and assigns it to the variable "recipes"
recipes = json.loads(response.text)


# reassigns the variable "recipes" with the value of 'results", which is a list of the recipe options and their filtered information
recipes = recipes['results']
# counts the number of items in the list of recipe options and assigns it to the variable 'total_options'
total_options = len(recipes)


# if the number of recipes returned from the search parameters in the url is greater than 1, allow the user to choose their recipe.
if total_options > 1:
    print(f'You will get {total_options} available options!')
    # inquirer.List creates an interactive selecting process of recipe choices for the user. It lists the recipe choices and allows the user to make a choice.  
    questions = [
    inquirer.List('dish',
                message="Which of these dishes would you like to make?",
                choices=[recipe['title'] for recipe in recipes],
            ),
    ]
    answers = inquirer.prompt(questions)
    dish = answers['dish']
    print(f'You are making {dish}!' )
# if the number of recipes returned from the search parameters in the url is 1, tell the user what he/she is making
elif total_options == 1:
    dish = recipes[0]['title']
    print(f'You are making {dish}!')
# if the number of recipes returned from the search parameters in the url is 0, tell the user that no results were returned and to start over
else: 
    print("No recipes found with these choices. Please start the program again! ")
    exit(0)


# iterates through the list of recipes to find the id number of the dish the user selects or is given and it is assigned to the variable 'id'
for recipe in recipes: 
    if dish == recipe['title']:
        id = recipe['id']


# GET request to Spoonacular API with their preset parameters to get more information about one specific recipe (user's choice)
url = f'https://api.spoonacular.com/recipes/{id}/information?apiKey={apiKey}'
# returns the recipe information that matches the id value in the url in json format
response = requests.request("GET", url)
# converts the json string to a dictionary and assigns it to the variable 'recipe_info'
recipe_info = json.loads(response.text)

# creates an empty dictionary and appends key-value pairs to it. Values are taken from the recipe_info dictionary
select_recipe_info = {}

select_recipe_info['id'] = id
select_recipe_info['title'] = recipe_info['title']
select_recipe_info['cooktime'] = recipe_info['readyInMinutes']
select_recipe_info['servings'] = recipe_info['servings']
select_recipe_info['sourceUrl'] = recipe_info['sourceUrl']
select_recipe_info['spoonacularUrl'] = recipe_info['spoonacularSourceUrl']


# creates a json file with writing permissions and adds the dictionary key-pair values in json format to the file
with open('selectedRecipe.json', 'w') as file:
    file.write(json.dumps(select_recipe_info))
file.close()

# calls the bash script 'buildscript4bash' and allows it to run in the python script
subprocess.call("./buildscript4bash.sh")
