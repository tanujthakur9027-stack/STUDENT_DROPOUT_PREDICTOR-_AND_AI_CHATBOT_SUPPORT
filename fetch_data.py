import pandas as pd
from ucimlrepo import fetch_ucirepo 

print(" Fetching dataset from the cloud... Please wait.")

# This fetches the "Predict Students' Dropout and Academic Success" dataset (ID: 697)
student_dataset = fetch_ucirepo(id=697) 

# Extract features (X) and targets (y)
X = student_dataset.data.features 
y = student_dataset.data.targets 

# Combine them into one single spreadsheet (dataframe)
df = pd.DataFrame(X)
df['Final_Result'] = y

# Save it as a CSV file in your project folder
df.to_csv("student_data.csv", index=False)

print(" Success! The data has been saved as 'student_data.csv'")
print(f"Dataset shape: {df.shape} (Rows, Columns)")