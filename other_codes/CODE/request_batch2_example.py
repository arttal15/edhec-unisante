import os
import requests
import json
import logging

# Set up logging to a file
logging.basicConfig(filename="app.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to send content of txt file to API and store the response in a JSON file
def process_txt_files(directory_path, api_url, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                # Read content of txt file
                content = file.read()

                data = {
                    "temperature": 0.1,
                    "profile_type": "strict",
                    "model": "mixtral",
                    "messages": [
                        {
                            "content": '''Comportes-toi comme un codeur médical, ton objectif est de clasissifier du texte, tu dois me retourner un objet JSON structuré avec uniquement les clés suivantes sans explications: 
                                        ```json
                                        {
                                            \"ICD10\": \"La localisation du cancer selon ICD10 (seulement le code), tu dois utiliser les codes suivants: 
                                            Tumeur maligne du sein = C50
                                            Mamelon et aréole = C50.0	
                                            Région centrale du sein = C50.1	
                                            Quadrant supéro-interne du sein ou QSI = C50.2
                                            Quadrant inféro-interne du sein ou QII = C50.3
                                            Quadrant supéro-externe du sein ou QSE = C50.4	
                                            Quadrant inféro-externe du sein ou QIE = C50.5	
                                            Prolongement axillaire du sein = 50.6
                                            Lésion à localisations contiguës du sein ou JQS ou JQE ou JQInt ou JQInf = C50.8	
                                            Sein, sans précision = C50.9
                                            Carcinome in situ de la glande mammaire = D05	
                                            Tumeur du sein à comportement imprévisible ou inconnu = D48.6	
                                            . Si tu ne trouves pas, retourne: NA\",
                                            \"Latéralité\": \"De quel côté est situé le cancer, gauche ou droite. Si tu ne trouves pas, retourne: NA\",
                                            \"ICDO\": "La morphologie du cancer selon ICDO, seulement le code. Si tu ne trouves pas, retourne: NA.\",
                                            \"ER\": \"La valeur du récepteur oestrogènes, le mot clé ER ou RE peut t'aider à trouver l'information, seulement la valeur en % (sans le symbole). Si tu ne trouves pas, retourne: NA.\",
                                            \"PR\": "La valeur du récepteur progestérone, le mot clé PR ou RP peut t'aider à trouver l'information, seulement la valeur en % (sans le symbole). Si tu ne trouves pas, retourne: NA.\",
                                            \"Grade\": \"La valeur du grade. Si tu ne trouves pas, retourne: NA.\",
                                            \"Score\": \"Le score selon Elston & Ellis, souvent sous la forme (X+X+X), tu dois juste me retourner un entier qui est l'addition des chiffres entre parenthèses. Si tu ne trouves pas, retourne: NA.\"
                                        } ```''',
                            "role": "system"
                        },
                        {
                            "content": '''{ 
                                    }''',
                            "role": "user"
                        }    
                    ]   
                }

                headers = {
                    'Authorization': 'Bearer TOKEN',
                    'Content-Type': 'application/json',
                }

                data["messages"][1]["content"] = "Voici le texte, ce texte est issu d'une extraction de plusieurs PDFs qui ont été anonymisés, les données personnelles ont été remplacés par des tags, il faut les ignorer. Tu pourrais trouver un historique médical mais tu dois te concentrer sur le DIAGNOSTIC. : "+content

                data_json = json.dumps(data, indent = 2) 
                #print(type(data_json))

                response = requests.request("POST", url = api_url, data = data_json, headers = headers)

                # # Store API response in a JSON file
                output_filename = filename.replace(".txt", "_response.json")
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, 'w') as output_file:
                    json.dump(response.json(), output_file, indent=4)

                print(f"Processed {filename} and stored response in {output_filename}")

# Example usage
if __name__ == "__main__":
    # Directory containing txt files
    directory_path = "/Directory/To/The/TXT/Files/Lot_2"

    # API URL
    api_url = "https://api.infomaniak.com/2/llm/566/chat/completions"

    # Directory to store JSON responses
    output_dir = "/Directoty/To/Store/The/Answers/Lot_2_response"

    # Call function to process txt files
    process_txt_files(directory_path, api_url, output_dir)