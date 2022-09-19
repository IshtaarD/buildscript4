import requests
import json
import inquirer


# reads the API KEY that is stored in a separate file. 
try:
    with open('apikey.txt', 'r') as file:
        apiKey = file.read()
# if there is no file, it notifies the user. 
except:
    print('File apikey.txt not found')
    exit(1)


print('WELCOME TO THE RECIPE HELPER')
print('-------------------------------------------')

# asks the user if they have any dietary restrictions
print("\nI'm here to help you find something to eat tonight! \n Do you have any of these dietary restrictions? ")

# created a dictionary with the dietary options.
diets = { 'A' : 'Gluten Free', 'B' : 'Ketogenic', 'C': 'Vegetarian', 'D' : 'Pescetarian'}

#iterates through the dictionary to print out the options for the user
for letter, diet in diets.items(): 
    print(f'{letter}. {diet}')
    
# maybe rename variable user_diet to letter
# asks the user for a letter selection and outputs their dietary restriction to get the diet parameter
letter = input('Please select your diet by letter or type "No": ')
if letter in diets.keys(): 
    user_diet = diets[letter]
    print(f'You have a {user_diet.upper()} diet.') 
#if the user does not have any dietary restrictions, it removes the parameter from the url
if letter == 'no': 
    user_diet = ''
    print('You have no dietary restrictions!')
   
print('-----------------------------------------------')

#asks user for the includeIngredients parameter. 
must_have = input('Choose a main ingredient you want in your dish: ')

# asks the user if allergic to any ingredients to get the exludeIngredients parameter.
answer = input('\nDo you have any food allergies? (yes/no) ')

# if user selects yes, he/she has to enter the ingredients separated by a comma. Their input is then displayed
if answer.lower() == 'yes':
    allergies = input('Please enter all ingredients you are allergic to separated by commas: ')
    print(f'You are allergic to: {allergies.upper()}')
# if the user does not have any allergies, prints "You have no allergies"  
if answer == 'no': 
    allergies = ''
    print('You have no allergies!')
print('---------------------------------------------------------')

# asks the user how much time they have to make their meal to get the maxReadyTime parameter
time = input('\nHow much time do you have to cook and prep in minutes? ')

print('--------------------------------------------------------')

# asks the user to select how indecisive they are and assigns the number of choices he/she gets to the number parameter
scale = int(input('\nFinally, how indecisive are you from a scale of 1 to 3. \n 1 = Very Decisive \n 2 = In Between \n 3 = Very Indecisive  \n'))
choices = {1 : 4, 2 : 2, 3 : 1 }
num_of_choices = choices[scale]



url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={apiKey}&maxReadyTime={time}&number={num_of_choices}&instructionsRequired=true&excludeIngredients={allergies}&diet={user_diet}&includeIngredients={must_have}"
#print(url)
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
recipes = json.loads(response.text)

recipes = recipes['results']
total_options = len(recipes)

if total_options > 1:
    print(f'You will get {total_options} available options!')
    questions = [
    inquirer.List('dish',
                message="Which of these dishes would you like to make?",
                choices=[recipe['title'] for recipe in recipes],
            ),
    ]
    answers = inquirer.prompt(questions)
    dish = answers['dish']
    print(f'You are making {dish}!' )
else:
    dish = recipes[0]['title']
    print(f'You are making {dish}!')


for recipe in recipes: 
    if dish == recipe['title']:
        id = recipe['id']

url = f'https://api.spoonacular.com/recipes/{id}/information?apiKey={apiKey}'

response = requests.request("GET", url)
recipe_info = json.loads(response.text)

select_recipe_info = {}

select_recipe_info['id'] = id
select_recipe_info['title'] = recipe['title']
select_recipe_info['Total Prep and Cook Time'] = recipe_info['readyInMinutes']
select_recipe_info['servings'] = recipe_info['servings']
select_recipe_info['Source URL'] = recipe_info['sourceUrl']
select_recipe_info['Spoonacular URL'] = recipe_info['spoonacularSourceUrl']

print(select_recipe_info)















#recipe_list = response.text
#print(recipe_list)
#print(recipe_list["results"])

#recipes = r['results']
#print(recipes)
#print('Your recipe choices are: ')
#for recipe in recipes: 
    #print(recipe['title'])



#print('Feeling adventurous? Type "yes" for a random recipe!')
#GET https://api.spoonacular.com/recipes/random



#while answer1 != 'yes' and answer1 != 'no':
   # answer1 = input('Please enter a valid answer.') 


#allergies = []
   #for allergy in answer2.split():
        #allergies.append(allergy)