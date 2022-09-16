import requests
try:
    with open('apikey.txt', 'r') as file:
        apiKey = file.read()
except:
    print('File apikey.txt not found')
    exit(1)
    #check to see if file exists  

print('WELCOME TO THE RECIPE HELPER')
print('-------------------------------------------')

# asks user if they have any dietary restrictions
print("\nI'm here to help you find something to eat tonight! \n Do you have any of these dietary restrictions? ")

diets = { 'A' : 'Gluten Free', 'B' : 'Ketogenic', 'C': 'Vegetarian', 'D' : 'Pescetarian'}

for letter, diet in diets.items(): 
    print(f'{letter}. {diet}')
    
# maybe rename variable user_diet to letter
letter = input('Please select your diet by letter or type "No": ')
if letter in diets.keys(): 
    user_diet = diets[letter]
    print(f'You have a {user_diet} diet') 
#elif letter == 'no':
    #url = f"https://api.spoonacular.com/recipes/random?apiKey={apiKey}&maxReadyTime=20&number=1&cuisine=italian"
print('-----------------------------------------------')

#asks user for ingredients to exclude from search (allergies)
answer = input('\nDo you have any food allergies? ')
if answer.lower() == 'yes':
    #allergies = []
    allergies = input('Please enter all ingredients you are allergic to separated by commas ')
    #for allergy in answer2.split():
        #allergies.append(allergy)
    print(f'You are allergic to: {allergies}')
    
elif answer1 == 'no': 
    print('You have no allergies!')

time = input('How much time do you have to cook and prep in minutes? ')

print('--------------------------------------------------')

scale = int(input('\nFinally, how indecisive are you from a scale of 1 to 3. \n 1 = Very Decisive \n 2 = In Between \n 3 = Very Indecisive  \n'))
choices = {1 : 3, 2 : 2, 3 : 1 }
num_of_choices = choices[scale]
print(f'You will get {num_of_choices} choices!')





url = f"https://api.spoonacular.com/recipes/random?apiKey={apiKey}&maxReadyTime={time}&number={num_of_choices}&cuisine=italian&diet={user_diet}&excludeIngredients={allergies}"

print(url)
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)



print('Feeling adventurous? Type "yes" for a random recipe!')
#GET https://api.spoonacular.com/recipes/random



#while answer1 != 'yes' and answer1 != 'no':
   # answer1 = input('Please enter a valid answer.') 