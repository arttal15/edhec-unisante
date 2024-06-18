import requests
import json
import logging


def main():
  """The main function that executes the core application logic."""

  # Set up logging to a file
  logging.basicConfig(filename="app.log", level=logging.DEBUG)
  logger = logging.getLogger(__name__)

  headers = {
      'Content-Type': 'application/json',
  }

  data = {"model": "mixtral",
          "prompt":'''Comportes-toi comme un codeur médical, ton objectif est de clasissifier du texte et me retourner un objet JSON structuré avec: 
                        ```json
                        {
                            \"ICD10\": \"La localisation du cancer selon ICD10, seulement le code. Si tu ne trouves pas, retourne: NA\",
                            \"Latéralité\": \"De quel côté est situé le cancer, gauche ou droite. Si tu ne trouves pas, retourne: NA\",
                            \"ICDO\": "La morphologie du cancer selon ICDO, seulement le code. Si tu ne trouves pas, retourne: NA.\",
                            \"ER\": \"La valeur du récepteur oestrogene, le mot clé ER peut t'aider à trouver l'information, seulement la valeur en %. Si tu ne trouves pas, retourne: NA.\",
                            \"PR\": "La valeur du récepteur progesterone, le mot clé PR peut t'aider à trouver l'information, seulement la valeur en %. Si tu ne trouves pas, retourne: NA.\",
                            \"Grade\": \"La valeur du grade. Si tu ne trouves pas, retourne: NA.\",
                            \"Score\": \"Le score selon Eston & Ellis. Si tu ne trouves pas, retourne: NA.\"
                        } ```'''
                        
                        
                    '''Voici le texte, ce texte est issu d'une extraction de plusieurs PDFs qui ont été anonymisés, les données personnelles ont été remplacés par des tags, il faut les ignorer: 
                        DIAGNOSTIC : 

                        1)  Ganglion  lymphatique  axillaire  droit  sentinelle,  biopsie-exérèse  :  un  ganglion  lymphatique  sans  métastase  en 
                        coloration standard et en immunohistochimie (0/1).  

                        2) Sein droit, QSE, tumorectomie : carcinome invasif NST :  

                        - mesurant 0.6 x 0.5 x 0.5 cm ;  
                        - de grade 2 selon <PERSON> et Ellis (3+2+1, 7 mitoses pour 10 HPF) ; 
                        d'immunophénotype :  
                        - ER 0% (témoins interne et externe positifs, adéquats) ; 
                        - PR 0% (témoins interne et externe positifs, adéquats) ; 
                        - statut HER2 positif (score 3+ en immunohistochimie) ; 
                        - fraction de prolifération MIB1 30% ; 
                        - expression conservée de la cadhérine. 
                        - présence de quelques invasion lympho-vasculaires péri-tumorales ;  
                        - absence de neurotropisme ;  
                        infiltration inflammatoire lymphocytaire stromal (TILs) : inférieur à 1%;  
                        composante de carcinome canalaire in situ associée, péri-tumorale, multifocale, s'étendant sur une zone de 10 
                        cm  de  grand  axe,  de  grade  intermédiaire  à  élevé,  d'architecture  papillaire  cribriforme  et  micropapillaire,  sans 
                        nécrose, d'immunophénotype ER et PR: 0% et HER2 positif (score 3+).
                        - TS : le carcinome infiltrant est situé à :  
                        0.3 cm du plan superficiel ; 
                        plus de 1 cm des autres marges (plan profond, 12h, 3h, 9h, 6h) ; 
                        - TS : le carcinome canalaire in situ est situé à :  

                        - A 1 cm de la TS à 6h ; 
                        - moins de 0.1 cm du plan superficiel sur plusieurs foyers ; 
                        - moins de 0.1 cm du plan profond sur un front de 1.2 cm ; 

                        plus de 1 cm des autres marges (3h, 9h, 12h).  

                        3) Sein droit, recoupe de 7h à 11h : parenchyme mammaire sans lésion atypique ni carcinome. 

                        4)  Sein  gauche,  symétrisation  :  parenchyme  mammaire  avec  rares  foyers  d'hyperplasie  canalaire  simple,  sans  autre 
                        lésion notable. Peau sans lésion.  

                        5) Sein droit, résection complémentaire : parenchyme mammaire et peau sans lésion notable.  

                        Stade pathologique TNM (UICC 8ème édition 2017) : pT1b pN0 (sn) i- (0/1)''',
          "stream":'false',
          "format": "json",
          "stream": False,
          "options": {"temperature": 0, "top_p": 0.95, "top_k": 100}
          }

  #data_json = json.dumps(data, indent = 2) 
  response = requests.post("http://GPU_IP_ADDRESS:11434/api/generate", json=data, stream=False)
  json_data = json.loads(response.text)
#  print(json.dumps(json.loads(json_data["response"]), indent=2))
  print(json_data['response'])
#  print(response.text)

# Execute the main function if this script is run directly
if __name__ == "__main__":
  main()