from fastapi import FastAPI, UploadFile, File, HTTPException, status

from app.models.domain import Document
from app.models.api import ExtractionResponse
from app.services.parsers.PDF_parser import PyPDFParserService
from app.services.cleaners.basic_text_cleaner import RegexTextCleanerService
from app.services.ner_extractors.Spacy_extractor import SpacyNERService


path_txt = r"C:\Users\Agee\OneDrive\Bureau\Work_dir\Filigran\cti_projects\Cyber_Threat_Intelligence\data\CERTFR-2025-CTI-007.pdf"

# Initialisation de l'API
app = FastAPI(title="Cyber Threat Intelligence NLP API")

# Instanciation de nos trois services au démarrage
parser_service = PyPDFParserService()
cleaner_service = RegexTextCleanerService()
ner_service = SpacyNERService()


@app.post("/analyze", response_model=ExtractionResponse)
def analyze_pdf(file: UploadFile = File(...)):
    """Reçoit un PDF, extrait le texte, le nettoie et renvoie les entités trouvées."""
    
    # 1. Validation de l'extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers PDF sont acceptés."
        )

    # 2. Lecture du contenu binaire
    content = file.file.read()
    file.file.close()

    # 3. Pipeline de traitement
    document = Document(
        filename=file.filename,
        content_type=file.content_type or "application/pdf",
        content=content
    )
    
    # Étape A : Extraction du texte brut du PDF
    parsed_doc = parser_service.parse(document, path_txt)
    
    # Étape B : Nettoyage et normalisation du texte extrait
    parsed_doc.text = cleaner_service.clean(parsed_doc.text)
    
    # Étape C : Extraction des entités nommées (NER)
    extraction_result = ner_service.extract_entities(parsed_doc)

    # 4. Retour du résultat
    return ExtractionResponse(entities=extraction_result.entities)