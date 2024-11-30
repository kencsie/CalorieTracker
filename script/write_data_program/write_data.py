import os
import re
import csv
import json
from shutil import move
from subprocess import call
from tempfile import NamedTemporaryFile
from collections import deque

# Global Constants
FOOD_ID_DICT = {
    "0": "Kabayaki sea bream fillet",
    "1": "Spam",
    "2": "apple -sliced-",
    "3": "cabbage",
    "4": "coin",
    "5": "creamy tofu",
    "6": "creamy tofu -without sauce-",
    "7": "cucumber",
    "8": "egg tofu",
    "9": "firm tofu",
    "10": "fish cake",
    "11": "fried chicken cutlet",
    "12": "fried potato",
    "13": "grilled pork",
    "14": "guava -sliced-",
    "15": "mustard greens",
    "16": "pig blood curd",
    "17": "pig liver",
    "18": "pineapple",
    "19": "pumpkin",
    "20": "red grilled pork",
    "21": "soy egg",
    "22": "sweet potato leaves"
}

def load_user_name_format(user_number) -> dict:
    user_dict = {
            '1': {'name': 'Ken', 're_exp': r'IMG_(?P<date>\d{8})_(?P<time>\d{6})'},
            '2': {'name': 'Kenrick', 're_exp': r'(?<!IMG_)(?P<date>\d{8})_(?P<time>\d{6})'},
    }
    return user_dict[user_number]


def create_unfinished_date_list(csv_file_path, user_profile) -> list:
    unfin_dates_set = set()
    with open(csv_file_path, 'r') as csvfile:
        # Convert CSV to dict
        # ex.
        # {
        # 'image_name': '20231103_115433',
        # 'object_id' : '10.0',
        # 'x_center'  : '0.65703125',
        # 'y_center'  : '0.70703125',
        # 'width'     : '0.43125',
        # 'height'    : '0.365625',
        # 'image_area': '35839',
        # 'area'      : '6742.7250566721395',
        # 'mass'      : ''
        # }
        reader = csv.DictReader(csvfile)
        for row in reader:
            image_name = row['image_name']
            match = re.search(user_profile['re_exp'], image_name)

            # Image_name match & mass field is empty
            if match and not row['mass']:
                date = match.group('date')
                # time = match.group('time')
                # print(f"Date: {date}, Time: {time}")
                unfin_dates_set.add(date)

    # Return a list
    # ex. ['20231103', '20231129']
    # print(f'unfin_dates:{sorted(unfin_dates_set)}')
    return sorted(unfin_dates_set)


def prompt_iterations() -> int:
    # Prompt the user for the number of iterations for that day
    iterations = int(input("Enter the number of iterations for that day: "))
    return iterations


def prompt_interval() -> tuple:
    print("Enter the start and end time of day range separated by spaces (eg: 115433 123355): ")
    start, end = input().split()
    return (start, end)


def clear_screen():
    _ = call('clear' if os.name == 'posix' else 'cls')


def prompt_mass(id_list) -> dict:
    # clear_screen()

    # Show the food items present in the image
    print("The food items present in the image are as follows:")
    print("--------------------")
    for index, food_id in enumerate(id_list):
        print(f"{index + 1}) {FOOD_ID_DICT[food_id[:-2]]}")

    # Obtain masses as list
    print("--------------------")
    print("Enter mass values separated by spaces (eg: 12 34 11 58): ")
    mass_list = [int(mass) for mass in input().split()]

    # Create and populate dictionary object
    mass_dict = dict()
    for food_id, mass in zip(id_list, mass_list):
        mass_dict.update({food_id: mass})

    # TODO: Add confirmation screen after adding masses

    return mass_dict


def process_date_with_image(csv_file_path, date, user_profile) -> tuple:
    def convert_food_mass_list(original_dict) -> dict:
        transformed_dict = {}
        # Iterate through each item in the original dictionary
        for key, value in original_dict.items():
            convert_key = key[:-2] #index ex. 16.0 -> 16
            food_name = FOOD_ID_DICT.get(convert_key)
            if food_name:
                transformed_dict[food_name] = value
        return transformed_dict

    # Prepare user input for json file(automation)
    user_input_data = {}
    user_range_list = []
    user_food_mass_list = []

    # Process a date that has an associated image
    iterations = prompt_iterations()

    row_list = list()  # Store rows to be written to csv
    for _ in range(iterations):
        print(f"Processing iteration for date {date}...")

        # Obtain time period (per iteration)
        (start, end) = prompt_interval()

        # Obtain food IDs within the given range
        id_set = set()
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                image_name = row['image_name']
                match = re.search(user_profile['re_exp'], image_name)
                if match:
                    img_date = match.group('date')
                    img_time = match.group('time')

                    # Find entries within time range and store ID
                    if (date == img_date) and (start <= img_time <= end):
                        print(f"Storing ID for {image_name}...")
                        id_set.add(row['object_id'])

        # Obtain dictionary of masses (for current iteration)
        mass_dict = prompt_mass(sorted(id_set))

        # Obtain rows of csv file
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                image_name = row['image_name']
                match = re.search(user_profile['re_exp'], image_name)
                if match:
                    img_date = match.group('date')
                    img_time = match.group('time')

                    # If image dates match and times are in range, update that row
                    if (date == img_date) and (start <= img_time <= end):
                        print(f"Updating mass for {FOOD_ID_DICT[row['object_id'][:-2]]} in image {image_name}...")
                        row['mass'] = mass_dict.get(row['object_id'])
                        row_list.append(row)  # Only write the modified rows
                        #print(f'row:{row}\n\n')
    
        # Update user input list
        user_range_list.append(start+" "+end)
        user_food_mass_list.append(convert_food_mass_list(mass_dict))

    user_input_data[date] = {'iteratiion':iterations, 'range':user_range_list, 'food_mass':user_food_mass_list}
    return (row_list, user_input_data)


def comp_row(a: dict, b: dict) -> bool:
    return a['image_name'] == b['image_name'] and a['object_id'] == b['object_id']


def write_to_csv(csv_file_path, data_list):
    # Convert data_list to queue
    data_queue = deque(data_list)

    # Write data to a CSV file using temporary file
    ntf = NamedTemporaryFile(mode='w', delete=False)
    with open(csv_file_path, mode='r') as csvfile, ntf:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(ntf, fieldnames=reader.fieldnames)
        writer.writeheader()

        # Access every row in csv and compare using unique attributes (name and object_id)
        for row in reader:
            line = row
            if data_queue:
                if comp_row(row, data_queue[0]):  # Rows match
                    line = data_queue[0]          # Change the line to be written
                    data_queue.popleft()          # Dequeue front
            writer.writerow(line)

    # Overwrite the original csv file with the temp file
    move(ntf.name, csv_file_path)

def write_to_json(json_file_path, user_history_list, user_name):
    # Check if the file exists and has content
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        # Read existing data from the file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        # If the file does not exist or is empty, start with an empty dictionary
        data = {}

    if user_name not in data:
        data[user_name] = {}

    for date, contents in user_history_list.items():
        data[user_name][date] = contents

    # Write updated data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def debug_func(csv_file_path, user_profile):
    print(f'CSV_file_path:{csv_file_path}')
    print(f'user_profile:{user_profile}')


def main():
    csv_file_path = os.path.join(os.getcwd(), 'output.csv')
    user_number = input("Enter User Number (Ken [1], Kenrick [2]): ")
    user_profile = load_user_name_format(user_number)
    unfin_dates = create_unfinished_date_list(csv_file_path, user_profile)
    print(f"Remaining Dates: {unfin_dates}")

    # Process unfinished dates
    data_list = list()
    for date in unfin_dates[:1]:
        print(f'date:{date}')
        row_data, user_input_history = process_date_with_image(csv_file_path, date, user_profile)
        #print(f'row_data:{row_data}\n\n\n')
        data_list.extend(row_data)
        write_to_json('./data.json', user_input_history, user_profile['name'])

    # Write data to CSV
    # print(f'data_list:{data_list}')
    #clear_screen()
    date_range = date if len(unfin_dates) == 1 else f"{unfin_dates[0]} ~ {unfin_dates[-1]}" 
    print(f"Updates from {date_range} Complete!")
    write_to_csv(csv_file_path, data_list)


if __name__ == "__main__":
    main()