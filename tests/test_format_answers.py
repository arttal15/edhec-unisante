import os
import json
import pandas as pd

def format_answers():
    input_folder = "results/lot_test"  # Update this with your folder path
    output_file = 'output.csv'  # Update this with your desired output CSV file name

    # Create an empty DataFrame to store the data
    columns=["TID", "ICD10", "Latéralité", "ICDO", "ER", "PR", "Grade", "Score"]
    df = pd.DataFrame(columns)

    # Iterate over each JSON file in the folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('_response.json'):
            tid = file_name.replace('_response.json', '')
            file_path = os.path.join(input_folder, file_name)
            print("Processing file:", file_name)  # Print file name for debugging
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    #content_str = data.get('content')
                    content_str = data
                    if content_str is None:
                        continue  # Skip files with missing content
                    # Extract the JSON-like content between "```json\n" and "\n```"
                    print(content_str)
                    start_index = content_str.find('{\n') + 2
                    end_index = content_str.find('\n}')
                    json_content = content_str[start_index:end_index]
                    print(json_content)
                    #content = json.loads(json_content)
                    content = json_content
                    content['TID'] = tid
                    for column in columns:
                        
                    df = df.append(content, ignore_index=True)
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")

    # Save the DataFrame to a CSV file with UTF-8 encoding
    df.to_csv(output_file, index=False, encoding='utf-8')

if __name__ == "__main__":
    format_answers()