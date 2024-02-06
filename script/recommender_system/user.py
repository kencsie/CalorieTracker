import json

def calculate_user_intake():

  user_information = {"calorie":0, "protein":0, "fat":0, "carbohydrate":0}

  #Read food table
  with open('food.json', 'r') as f:
    food_table = json.load(f)

  #Calculate user this meal intake
  with open('prompt.json', 'r') as f:
    data = json.load(f)
    for key in data['user']['food']:
      user_information['calorie'] += data['user']['food'][key] * (food_table[key]['calorie'] / 100)
      user_information['protein'] += data['user']['food'][key] * (food_table[key]['protein'] / 100)
      user_information['fat'] += data['user']['food'][key] * (food_table[key]['fat'] / 100)
      user_information['carbohydrate'] += data['user']['food'][key] * (food_table[key]['carbohydrate'] / 100)
  print(user_information)


def create_user_prompt():
  prompt_template = """
User information:
- Age: {age}
- Weight: {weight} kg
- Height: {height} cm
- Physical activity level: {physical_activity_level}
- Daily calorie intake so far (including lunch): {calorie} kcal
- Daily protein intake so far: {protein} g
- Daily fat intake so far: {fat} g
- Daily carbohydrate intake so far: {carbohydrate} g
- Weight goal: {weight_option[option]} by {weight_option[value]} calories
- Total Daily Energy Expenditure (TDEE): {TDEE} calories

Considering the intake so far is for lunch, suggest a balanced meal plan for dinner that aligns with the user's dietary needs and weight goal. The dinner plan should help the user meet their remaining daily nutritional requirements without exceeding the TDEE, considering the goal to {weight_option[option]} weight by adjusting daily calorie intake by {weight_option[value]} calories.

Foods available for dinner:
1. Kabayaki sea bream fillet
2. Spam
3. Apple -sliced-
4. Cabbage
5. Coin
6. Creamy tofu
7. Creamy tofu -without sauce-
8. Cucumber
9. Egg tofu
10. Firm tofu
11. Fish cake
12. Fried chicken cutlet
13. Fried potato
14. Grilled pork
15. Guava -sliced-
16. Mustard greens
17. Pig blood curd
18. Pig liver
19. Pineapple
20. Pumpkin
21. Red grilled pork
22. Soy egg
23. Sweet potato leaves
24. Rice

The meal plan should consider not only the caloric content but also the balance of macronutrients (proteins, fats, carbohydrates) to ensure the user's nutritional needs are met by the end of the day. Please provide suggestions for dinner that contribute to the user's health and weight management goals.
"""


  with open('prompt.json', 'r') as f:
    user = json.load(f)['user']
  # Replace the placeholders with actual user data
  user_data = {
      "age": user['age'],
      "weight": user['weight'],
      "height": user['height'],
      "physical_activity_level":  user['physical_activity_level'],
      "calorie": user['intake']['calorie'],
      "protein": user['intake']['protein'],
      "fat": user['intake']['fat'],
      "carbohydrate": user['intake']['carbohydrate'],
      "weight_option": user['weight_option'],
      "TDEE": user['TDEE_value']
  }

  # Filling in the template with the user's data
  filled_prompt = prompt_template.format(**user_data)

  # Now, to save this filled prompt into an external file:
  filename = "user_gpt_prompt.txt"

  with open(filename, 'w') as file:
      file.write(filled_prompt)

  print(f"Prompt saved to {filename}.")


create_user_prompt()