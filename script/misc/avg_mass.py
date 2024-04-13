import pandas as pd

# Replace 'your_file.csv' with the actual name of your CSV file
file_name = 'output.csv'

# Read the CSV data into a DataFrame
df = pd.read_csv(file_name)

# Group the data by 'object_id' and calculate the average mass for each group
average_mass = df.groupby('object_id')['mass'].mean().reset_index()
# Rename the columns for clarity
average_mass.columns = ['object_id', 'average_mass']

# Display the average mass of each food item
print(average_mass)
