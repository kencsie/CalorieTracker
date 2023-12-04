import csv
import os
import re

def load_user_name_format(user_number):
    user_dict = {'1':{'name':'Ken', 're_exp':r'IMG_(\d{8})_(\d{6})'}, 
    '2':{'name':'Kenrick', 're_exp':r'(?<!IMG_)(\d{8})_(\d{6})'},
    }
    return user_dict[user_number]

def create_unfinished_date_list(csv_file_path, user_profile):
    unfin_dates_set = set()
    with open(csv_file_path, 'r') as csvfile:
        #Convert CSV to dict
        #ex.{'image_name': 'IMG_8712', 'object_id': '10.0', 'x_center': '0.65703125', 'y_center': '0.70703125', 'width': '0.43125', 'height': '0.365625', 'image_area': '35839', 'area': '6742.7250566721395', 'mass': ''}
        reader = csv.DictReader(csvfile)

        for row in reader:
            image_name = row['image_name']
            match = re.search(user_profile['re_exp'], image_name)

            #image_name match & mass field is empty
            if match and not row['mass']:
                date = match.group(1)
                #time = match.group(2)
                #print(f"Date: {date}, Time: {time}")
                unfin_dates_set.add(date)
    
    #Return a list
    #ex. ['20231103', '20231129']
    #print(f'unfin_dates:{sorted(unfin_dates_set)}')
    return sorted(unfin_dates_set)

def prompt_iterations():
    # Prompt the user for the number of iterations for that day
    iterations = int(input("Enter the number of iterations for that day: "))
    return iterations

def process_date_with_image(date, user_profile):
    # Process a date that has an associated image
    iterations = prompt_iterations()
    for _ in range(iterations):
        # Here you would implement the logic for obtaining a range and mass values
        # and then appending new lines with this mass information to the CSV
        print(f"Processing iteration for date {date}...") # Placeholder for actual processing

def write_to_csv(file_name, data):
    # Write data to a CSV file
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def debug_func(csv_file_path, user_profile):
  print(f'CSV_file_path:{csv_file_path}')
  print(f'user_profile:{user_profile}')

def main():
    csv_file_path = os.path.join(os.path.dirname(os.getcwd()), 'Generated_Files', 'output.csv')
    user_number = input("Enter User Number: \nKen:1, Kenrick:2\n")
    user_profile = load_user_name_format(user_number)
    unfin_dates = create_unfinished_date_list(csv_file_path, user_profile)
    print(unfin_dates)
    
    for date in unfin_dates:
            print(f'date:{date}')
            process_date_with_image(date, user_profile)
        #else:
        #    # If there is no image for the date, write to CSV
        #    write_to_csv('output.csv', [user_name, date])'''

if __name__ == "__main__":
    main()
