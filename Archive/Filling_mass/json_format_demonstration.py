import json

date = 20221124
iter = 2
range = ['123052 125714', '133333 144444']
food_mass = [{'Kabayaki sea bream fillet':12, "Spam": 24, "apple -sliced-": 36, "cabbage": 48}
  ,{'Kabayaki sea bream fillet':1, "Spam": 2, "apple -sliced-": 3, "cabbage": 4}]

dict = {}
dict[date] = {'iteratiion':iter, 'range':range, 'food_mass':food_mass}
print(dict)

with open('data.json', 'w') as file:
    json.dump(dict, file, indent=4)