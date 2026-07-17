# test_pipeline.py
import sys
from app.models.domain import Document
from app.services.parsers.PDF_parser import PyPDFParserService
from app.services.cleaners.basic_text_cleaner import RegexTextCleanerService
from app.services.ner_extractors.Spacy_extractor import SpacyNERService

PDF_TEST_PATH = r"C:\Users\Agee\OneDrive\Bureau\Work_dir\Filigran\cti_projects\Cyber_Threat_Intelligence\data\CERTFR-2025-CTI-007.pdf"


def test_full_pipeline():
    print("=== LANCEMENT DU TEST D'INTÉGRATION COMPLET (SANS API) ===")
    
    # 1. Lecture du fichier PDF
    try:
        with open(PDF_TEST_PATH, "rb") as f:
            pdf_bytes = f.read()
    except FileNotFoundError:
        print(f"[!] Erreur : Impossible de trouver le fichier {PDF_TEST_PATH} pour le test.")
        sys.exit(1)

    # 2. Instanciation du Document (Modèle de domaine d'entrée)
    document = Document(
        filename="test_report.pdf",
        content_type="application/pdf",
        content=pdf_bytes
    )
    print("[+] Étape 1 : Modèle Document initialisé.")

    # 3. Instanciation de tous nos services
    print("[*] Initialisation des services...")
    parser = PyPDFParserService()
    cleaner = RegexTextCleanerService()
    ner = SpacyNERService()
    print("[+] Étape 2 : Tous les services sont instanciés.")

    # 4. Exécution séquentielle du pipeline
    print("[*] Étape 3 : Début du traitement...")
    
    # Étape A : Parser
    parsed_doc = parser.parse(document, PDF_TEST_PATH)
    print(f"    -> PDF parsé. Caractères extraits : {len(parsed_doc.text)}")
    
    # Étape B : Cleaner
    raw_length = len(parsed_doc.text)
    parsed_doc.text = cleaner.clean(parsed_doc.text)
    clean_length = len(parsed_doc.text)
    print(f"    -> Texte nettoyé. Taille : {raw_length} -> {clean_length} caractères.")
    
    # Étape C : NER
    result = ner.extract_entities(parsed_doc)
    print(f"    -> NER terminé. {len(result.entities)} entités trouvées.")

    # 5. Affichage final des résultats
    print("\n=== RÉSULTATS DE L'EXTRACTION ===")
    print(f"{"TEXTE EXTRAIT":<35} | {"TYPE D'ENTITÉ":<15} | {"OFFSETS (DEB-FIN)":<15}")
    print("-" * 75)
    for ent in result.entities:
        offsets = f"{ent.start}-{ent.end}"
        print(f"{ent.text:<35} | {ent.label:<15} | {offsets:<15}")
    print("-" * 75)
    
    print("\n[+] TEST D'INTÉGRATION RÉUSSI ! Le moteur est 100% prêt pour l'exposition API.")


if __name__ == "__main__":
    test_full_pipeline()