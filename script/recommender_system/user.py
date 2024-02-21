import json

physical_activity_level = {'1':1.2, '2':1.375, '3':1.55, '4':1.725, '5':1.9}
weight_option = {'1':'Lose', '2':'Maintain', '3':'Gain'}

def calculate_user_intake():
  #Read food table
  with open('food.json', 'r') as f:
    food_table = json.load(f)

  #Calculate user this meal intake
  with open('prompt.json', 'r') as f:
    user_information = {"calorie":0, "protein":0, "fat":0, "carbohydrate":0}
    
    data = json.load(f)
    for key in data['user']['food']:
      user_information['calorie'] += data['user']['food'][key] * (food_table[key]['calorie'] / 100)
      user_information['protein'] += data['user']['food'][key] * (food_table[key]['protein'] / 100)
      user_information['fat'] += data['user']['food'][key] * (food_table[key]['fat'] / 100)
      user_information['carbohydrate'] += data['user']['food'][key] * (food_table[key]['carbohydrate'] / 100)
  print(user_information)

  data['user']['intake'] = user_information

  with open('prompt.json', 'w') as f:
    json.dump(data, f, indent=2)

def create_user_prompt():
  prompt_template = """
  User Information:

  Age: {age}
  Weight: {weight} kg
  Height: {height} cm
  Physical Activity Level: {physical_activity_multiplier}
  Develop a daily meal plan that strictly adheres to the Health TEA recommendations for nutritional intake. The goals for the day are:

  Carbohydrates: 180 grams
  Protein: 42 grams
  Vegetables: Approximately 375 grams
  Fruits: Approximately 240 grams
  Fat: 25 grams
  Since the user has consumed a 400-calorie breakfast, the meal plan should strategically allocate the remainder of the daily nutritional targets across lunch and dinner.

  Please prioritize the following available foods with their nutritional content (per 100g serving), adjusting the amounts to meet the exact nutritional targets:
  //Food list
  
  The meal plan should incorporate the user's preferred foods: {preferred food}, ensuring the following:

  Correct proportions of macronutrients to fulfill health objectives.
  Accurate serving sizes to meet the specific gram targets for each food group.
  A diverse range of foods to provide a balanced intake of nutrients.
  Formulate lunch and dinner menus that will bring the user's total daily intake in line with the Health TEA recommendations. The menus should be designed to maximize nutritional value while satisfying taste preferences. It is essential that the meal plan does not exceed the specified daily limits for each macronutrient and aligns precisely with the serving size definitions.

  Please adjust the quantities of each food item so that the total fat content does not surpass 25 grams and the total intake of vegetables and fruits meets the required amounts in grams. If any macronutrient exceeds the daily goal, suggest alternative quantities or food items that will correct the imbalance.
  """

  with open('prompt.json', 'r') as f:
    user = json.load(f)['user']
  # Replace the placeholders with actual user data
  user_data = {
      "age": user['age'],
      "weight": user['weight'],
      "height": user['height'],
      "physical_activity_multiplier":  user['physical_activity_multiplyer'],
      "TDEE": user['TDEE'],
      "weight_option": user['weight_option']['option'],
      "weight_daily_intake": user['weight_option']['daily_intake'],
      "preferred food": user['preferred_food']
  }

  # Filling in the template with the user's data
  filled_prompt = prompt_template.format(**user_data)

  # Now, to save this filled prompt into an external file:
  filename = "user_gpt_prompt.txt"

  with open(filename, 'w') as file:
      file.write(filled_prompt)

  print(f"Prompt saved to {filename}.")

def modify_user_information():
  with open('prompt.json', 'r') as f:
    user = json.load(f)
    user['user']['gender'] = input("Please type your gender(m/f):")
    user['user']['age'] = int(input("Please type your age(y):"))
    user['user']['weight'] = float(input("Please type your weight(kg):"))
    user['user']['height'] = float(input("Please type your height(cm):"))
    user['user']['physical_activity_multiplyer'] = physical_activity_level[input("Please type your physical activity level(number):\n1.Sedentary\n2.Lightly active\n3.Moderately active\n4.Very active\n5.Super active\n")]
    
    BMR_offset = 5 if user['user']['gender'] == 'm' else -161
    user['user']['BMR'] = (10 * user['user']['weight']) + (6.25 * user['user']['height']) - (5 * user['user']['age']) + BMR_offset
    user['user']['TDEE'] = user['user']['BMR'] * user['user']['physical_activity_multiplyer']

    user['user']['weight_option'] = {}
    user['user']['weight_option']['option'] = weight_option[input("Please type your weight goal:\n1.Lose weight\n2.Maintain weight\n3.Gain weight\n")]
    user['user']['weight_option']['value'] = float(input("Please type your weight goal value for a month(kg):"))
    user['user']['weight_option']['daily_intake'] = user['user']['weight_option']['value'] * 7700 / 30

  with open('prompt.json', 'w') as f:
    json.dump(user, f, indent=2)


#calculate_user_intake()
modify_user_information()
create_user_prompt()