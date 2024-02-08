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
  - Age: {age}
  - Weight: {weight} kg
  - Height: {height} cm
  - Physical Activity Level: {physical_activity_multiplyer}
  - Total Daily Energy Expenditure (TDEE): {TDEE} calories
  - Weight Goal: {weight_option} by adjusting daily calorie intake by {weight_daily_intake} calories
  - Daily calorie intake so far (breakfast only): 400 kcal

  Given the user's initial breakfast intake of 400 calories, recommend a comprehensive meal plan for lunch and dinner that aligns with the user's dietary needs and weight management goals. This plan should ensure the user does not exceed their TDEE of {TDEE} calories while aiming to {weight_option} weight by adjusting daily calorie intake by {weight_daily_intake} calories.

  Available Foods with Nutritional Information(per 100g serving):
  - Seafood: Kabayaki sea bream fillet (127 kcal, 18.3g protein, 3.2g fat, 6.2g carbs), Fish cake (201 kcal, 13.65g protein, 10.49g fat, 12.38g carbs)
  - Meat and Meat Products: Spam (292 kcal, 15g protein, 24.3g fat, 3.2g carbs), Pig blood curd (29 kcal, 6.3g protein, 0.3g fat, 0.5g carbs)
  - Tofu and Tofu Products: Creamy tofu (196 kcal, 13.4g protein, 13.4g fat, 6.3g carbs), Egg tofu (82.35 kcal, 7.06g protein, 5.29g fat, 1.18g carbs)
  - Vegetables: Cabbage (42 kcal, 0.99g protein, 2.79g fat, 4.36g carbs), Pumpkin (115 kcal, 2.7g protein, 4.38g fat, 19.85g carbs)
  - Fruits: Apple -sliced- (52 kcal, 0.26g protein, 0.17g fat, 13.81g carbs), Guava -sliced- (68 kcal, 2.55g protein, 0.95g fat, 14.32g carbs)
  - Starchy Foods: Fried potato (125 kcal, 2.41g protein, 3.25g fat, 22.05g carbs), Rice (354 kcal, 7g protein, 0.6g fat, 77.8g carbs)

  The meal plan should prioritize the user's preferred foods where possible: {preferred food}. It should also balance macronutrients (proteins, fats, carbohydrates) effectively, contributing towards the user's health and weight management objectives.

  Based on the nutritional information provided for each available food, construct lunch and dinner suggestions that help the user meet their remaining daily nutritional requirements without exceeding the TDEE, considering the goal to {weight_option} weight by adjusting daily calorie intake by {weight_daily_intake} calories.
  """

  with open('prompt.json', 'r') as f:
    user = json.load(f)['user']
  # Replace the placeholders with actual user data
  user_data = {
      "age": user['age'],
      "weight": user['weight'],
      "height": user['height'],
      "physical_activity_multiplyer":  user['physical_activity_multiplyer'],
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