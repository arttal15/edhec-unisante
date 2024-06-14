import pandas as pd
from sklearn.metrics import accuracy_score

# Load CSV files
llm_output = pd.read_csv('output.csv')
truth = pd.read_csv('RVT_data_breast_2020_unique_TID.csv', sep=";")

# Filter relevant columns
llm_output = llm_output[['TID', 'ICD10', 'Latéralité', 'ICDO', 'ER', 'PR', 'Grade', 'Score']]
truth = truth[['TID', 'ICD10', 'Latéralité', 'ICDO', 'ER', 'PR', 'Grade', 'Score']]

# Merge dataframes on TID
merged_data = pd.merge(truth, llm_output, on='TID', suffixes=('_truth', '_llm_output'))


# Convert both columns to string for comparison
merged_data['ER_truth'] = merged_data['ER_truth'].apply(lambda x: int(float(x)))
merged_data['ER_llm_output'] = merged_data['ER_llm_output'].apply(lambda x: int(float(x)))

# Convert float representations to integers
merged_data['PR_truth'] = merged_data['PR_truth'].apply(lambda x: int(float(x)))
merged_data['PR_llm_output'] = merged_data['PR_llm_output'].apply(lambda x: int(float(x)))

# Convert both columns to string for comparison
merged_data['Grade_truth'] = merged_data['Grade_truth'].apply(lambda x: int(float(x)))
merged_data['Grade_llm_output'] = merged_data['Grade_llm_output'].apply(lambda x: int(float(x)))

# Convert columns to string type
merged_data = merged_data.astype(str)

# Calculate accuracy for each variable
accuracy_scores = {}
for column in ['ICD10', 'Latéralité', 'ICDO', 'ER', 'PR', 'Grade', 'Score']:
    accuracy_scores[column] = accuracy_score(merged_data[f"{column}_truth"], merged_data[f"{column}_llm_output"])

# Display or save results
for column, accuracy in accuracy_scores.items():
    print(f"Accuracy for {column}: {accuracy}")

# Compare ICD10 columns
# icd10_comparison = merged_data[['TID', 'ICD10_truth', 'ICD10_llm_output']]
# print(icd10_comparison)    

# Compare Grade columns
# Grade_comparison = merged_data[['TID', 'Grade_truth', 'Grade_llm_output']]
# print(Grade_comparison)    