import os
from pathlib import Path

# Dossier racine du projet (deux niveaux au-dessus de ce fichier)
BASE_DIR = Path(__file__).resolve().parent.parent

# Chemin d'accès par défaut vers les données
DATA_DIR = BASE_DIR / "data"

# Chemins des ressources configurables via des variables d'environnement (idéal pour Docker/GitHub)
THREAT_ACTORS_JSON_PATH = Path(
    os.getenv("THREAT_ACTORS_PATH", str(DATA_DIR / "threat_actors.json"))
)

# Modèle spaCy utilisé
SPACY_MODEL_NAME = os.getenv("SPACY_MODEL_NAME", "en_core_web_trf")