import sys
import requests

# Configuration de l'API NLP
API_URL = "http://127.0.0.1:8000/analyze"

# Spécifiez ici le rapport PDF que vous souhaitez analyser
PDF_REPORT_PATH = "data/cleaned_text_pypdf.pdf" 


def run_connector():
    """Simule le comportement d'un connecteur d'ingestion CTI."""
    print(f"[*] Lecture du rapport : {PDF_REPORT_PATH}")
    
    try:
        # 1. Ouverture et lecture du fichier PDF local
        with open(PDF_REPORT_PATH, "rb") as file_data:
            files = {"file": (PDF_REPORT_PATH, file_data, "application/pdf")}
            
            print("[*] Envoi du document à l'API NLP pour analyse...")
            # 2. Requête HTTP POST vers votre API FastAPI
            response = requests.post(API_URL, files=files)
            
    except FileNotFoundError:
        print(f"[!] Erreur : Le fichier '{PDF_REPORT_PATH}' n'a pas été trouvé.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"[!] Erreur : Impossible de contacter l'API sur {API_URL}. Est-elle démarrée ?")
        sys.exit(1)

    # 3. Traitement de la réponse de l'API
    if response.status_code == 200:
        data = response.json()
        entities = data.get("entities", [])
        
        print(f"[+] Analyse réussie ! {len(entities)} entités identifiées.\n")
        print("=" * 60)
        print(f"{'TEXTE':<30} | {'TYPE':<15} | {'INDEX (DEB-FIN)':<10}")
        print("=" * 60)
        
        # 4. Affichage des entités structurées retournées par l'API
        for ent in entities:
            pos = f"{ent['start']}-{ent['end']}"
            print(f"{ent['text']:<30} | {ent['label']:<15} | {pos:<10}")
        print("=" * 60)
        
        # 5. Simulation de la transmission à OpenCTI
        print("\n[*] Étape suivante (Simulation) : Conversion des entités au format STIX 2.1")
        print("[*] Envoi des bundles STIX à la plateforme OpenCTI... [OK]")
        
    else:
        print(f"[!] L'API a retourné une erreur {response.status_code} :")
        print(response.json())


if __name__ == "__main__":
    run_connector()