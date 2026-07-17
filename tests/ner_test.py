# test_ner.py
from app.models.domain import ParsedDocument
from app.services.ner_extractors.Spacy_extractor import SpacyNERService

# 1. Simuler un document déjà parsé avec différents types d'IOCs à détecter
sample_text = """
The threat actor APT29 (also known as Cozy Bear) was observed deploying malware.
Command and Control (C2) servers were identified at 192.168.1.1 and 10.0.0.2.
The binary has the SHA256 hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
They exploited CVE-2021-44228 to gain initial access.
"""

parsed_doc = ParsedDocument(
    filename="mock_report.txt",
    text=sample_text
)

# 2. Instancier et lancer le service NER
ner_service = SpacyNERService()
result = ner_service.extract_entities(parsed_doc)

# 3. Vérifier les résultats
print("=== TEST NER ===")
print(f"Nombre d'entités trouvées : {len(result.entities)}")
for entity in result.entities:
    print(f"- [{entity.label}] {entity.text} (Positions: {entity.start}-{entity.end})")