import os
import json
import pandas as pd

def extract_content(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        content = data['response']
        return content

def rework_json(output_dir):
    input_folder = output_dir  # Update this with your folder path
    output_folder = output_dir + '/reworked'  # Update this with your desired output folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name)

            content = extract_content(input_file)

            # Creating a dictionary with just the content key
            content_dict = {"content": content}

            # Writing the content to a new JSON file
            with open(output_file, 'w') as f:
                json.dump(content_dict, f, indent=4)


def output_csv(input_path):
    input_folder = input_path + '/reworked' # Update this with your folder path
    output_file = 'output.csv'  # Update this with your desired output CSV file name

    # Create an empty DataFrame to store the data
    df = pd.DataFrame(columns=["TID", "ICD10", "Latéralité", "ICDO", "ER", "PR", "Grade", "Score"])

    # Iterate over each JSON file in the folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('_response.json'):
            tid = file_name.replace('_response.json', '')
            file_path = os.path.join(input_folder, file_name)
            print("Processing file:", file_name)  # Print file name for debugging
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content_str = data.get('content')
                    if content_str is None:
                        continue  # Skip files with missing content
                    # Extract the JSON-like content between "```json\n" and "\n```"
                    start_index = content_str.find('```json\n') + len('```json\n')
                    end_index = content_str.find('\n```', start_index)
                    json_content = content_str[start_index:end_index]
                    content = json.loads(content_str)
                    content['TID'] = tid
                    df = df._append(content, ignore_index=True)
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")

    # Save the DataFrame to a CSV file with UTF-8 encoding
    df.to_csv(output_file, index=False, encoding='utf-8')

if __name__ == "__main__":
    output_csv()
