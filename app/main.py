from fastapi import FastAPI, UploadFile, File, HTTPException, status

from app.models.domain import Document
from app.models.api import ExtractionResponse
from app.services.parsers.PDF_parser import PyPDFParserService
from app.services.ner_extractors.Spacy_extractor import SpacyNERService

# Initialisation de l'API
app = FastAPI(title="Cyber Threat Intelligence NLP API")

# Instanciation directe des services au démarrage du script (V1 simple)
parser_service = PyPDFParserService()
ner_service = SpacyNERService()


@app.post("/analyze", response_model=ExtractionResponse)
def analyze_pdf(file: UploadFile = File(...)):
    """Reçoit un PDF, extrait le texte et renvoie les entités trouvées."""
    
    # 1. Validation de l'extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers PDF sont acceptés."
        )

    # 2. Lecture du contenu binaire
    content = file.file.read()
    file.file.close()

    # 3. Passage par nos modèles de domaine et nos services
    document = Document(
        filename=file.filename,
        content_type=file.content_type or "application/pdf",
        content=content
    )
    
    # Parsing
    parsed_doc = parser_service.parse(document)
    
    # Extraction NER
    extraction_result = ner_service.extract_entities(parsed_doc)

    # 4. Retour du résultat (sérialisé automatiquement par FastAPI)
    return ExtractionResponse(entities=extraction_result.entities)