# test_parser.py
from app.models.domain import Document
from app.services.parsers.PDF_parser import PyPDFParserService

path_txt = r"C:\Users\Agee\OneDrive\Bureau\Work_dir\Filigran\cti_projects\Cyber_Threat_Intelligence\data\CERTFR-2025-CTI-007.pdf"

# 1. Charger un PDF de test sous forme d'octets
with open(path_txt, "rb") as f:
    pdf_bytes = f.read()

# 2. Instancier le modèle de domaine Document
doc = Document(
    filename="CERTFR-2025-CTI-007.pdf",
    content_type="application/pdf",
    content=pdf_bytes
)

# 3. Tester le service de parsing
parser = PyPDFParserService()
parsed_document = parser.parse(doc, path_txt)

# 4. Assertions de validation de base
print("=== TEST PARSER ===")
print(f"Nom du fichier : {parsed_document.filename}")
print(f"Texte extrait (longueur) : {len(parsed_document.text)} caractères")
print("Contenu extrait :")
print(parsed_document.text[:300]) # Affiche les 300 premiers caractères