import pandas as pd

# Step 2: Read the CSV file
file_path = 'output.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Step 3: Drop rows where 'area' is missing
df = df.dropna(subset=['area'])

# Step 4: Save the DataFrame back to a CSV file
df.to_csv('output.csv', index=False)
