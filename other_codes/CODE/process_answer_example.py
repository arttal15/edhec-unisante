import os
import json

def extract_content(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        content = data['response']
        return content

def main():
    input_folder = '/Directoty/Of/The/Answers/Lot_2_response'  # Update this with your folder path
    output_folder = '/Directoty/To/Store/The/Answers/Lot_2_response/content'  # Update this with your desired output folder

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

if __name__ == "__main__":
    main()
