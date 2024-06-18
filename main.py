import os
import requests
import json
import logging
from modules.format_answers import output_csv, rework_json

def import_files(file_path):
  with open(file_path, 'r') as file:
    # Read content of txt file
    content = file.read()
    return content


def api_call(content):
   # Set up logging to a file
  logging.basicConfig(filename="app.log", level=logging.DEBUG)
  logger = logging.getLogger(__name__)

  headers = {
      'Content-Type': 'application/json',
  }

  data = {"model": "llama3:70b-text",
          "prompt":'''<s>[INST] <<SYS>> 
                      Comportes-toi comme un codeur médical, ton objectif est de clasissifier du texte et me retourner SEULEMENT et UNIQUEMENT un objet JSON structuré avec: 
                        ```json
                        {
                            \"ICD10\": \"La localisation du cancer selon ICD10, seulement le code. Il ne faut absolument pas l'inventer, la précision de cet indicateur est très importante pour la survie du patient. Si tu ne trouves pas, simplement retourne: NA\",
                            \"Latéralité\": \"De quel côté est situé le cancer, gauche ou droite. Si tu ne trouves pas, retourne: NA\",
                            \"ICDO\": "La morphologie du cancer selon ICDO, seulement le code. Si tu ne trouves pas, retourne: NA.\",
                            \"ER\": \"La valeur du récepteur oestrogene, le mot clé ER peut t'aider à trouver l'information, seulement la valeur en %. Si tu ne trouves pas, retourne: NA.\",
                            \"PR\": "La valeur du récepteur progesterone, le mot clé PR peut t'aider à trouver l'information, seulement la valeur en %. Si tu ne trouves pas, retourne: NA.\",
                            \"Grade\": \"La valeur du grade sans les chiffres entre parenthèses. Je ne veux pas que tu retournes les parenthèses et son contenu. Seulement un chiffre. Si tu ne trouves pas, retourne: NA.\",
                            \"Score\": \"Le score selon Eston & Ellis. Si tu ne trouves pas, retourne: NA.\"
                        } ```
                      <</SYS>>

                           
                    </s>
                    <s>[INST]
                    ''',
          "stream":'false',
          "format": "json",
          "stream": False,
          "options": {"temperature": 0, "top_p": 0.95, "num_ctx": 16384, "num_predict": 100}
          }


  data["prompt"] += "Voici le texte à analyser, ce texte est issu d'une extraction de plusieurs PDFs qui ont été anonymisés, les données personnelles ont été remplacés par des tags, il faut uniquement aller chercher les informations demandés par SYSTEM : "+content
  data["prompt"] += '''
                    [/INST]'''
  response = requests.post("http://GPU_IP_ADDRESS:11434/api/generate", json=data, stream=False)
  json_data = json.loads(response.text)
  return response



def main(directory_path, output_dir):
  """The main function that executes the core application logic."""
  i=0
  for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
      i += 1
      file_path = os.path.join(directory_path, filename)
      content = import_files(file_path)
      print(f"Processing {filename} number {i}")
      llm_answer = api_call(content)
      # # Store API response in a JSON file
      output_filename = filename.replace(".txt", "_response.json")
      output_path = os.path.join(output_dir, output_filename)
      with open(output_path, 'w') as output_file:
        json.dump(llm_answer.json(), output_file, indent=4)

      print(f"Processed {filename} and stored response in {output_filename}")

  rework_json(output_dir)
  output_csv(output_dir)


# Execute the main function if this script is run directly
if __name__ == "__main__":

  directory_path = "data/Lot_2"
  output_dir = "results/Lot_2"
  main(directory_path, output_dir)