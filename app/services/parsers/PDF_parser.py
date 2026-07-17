import io
from pypdf import PdfReader
from app.models.domain import Document, ParsedDocument
from app.services.base import BaseParserService


class PyPDFParserService(BaseParserService):
    """Implémentation concrète du parseur de PDF utilisant la bibliothèque pypdf.
    
    Cette classe lit le contenu binaire d'un document PDF en mémoire,
    en extrait le texte page par page et retourne un ParsedDocument.
    """

    def parse(self, document: Document, path) -> ParsedDocument:
        """Extrait le texte d'un document PDF stocké en mémoire sous forme d'octets.
        
        Args:
            document (Document): Le document binaire.
            
        Returns:
            ParsedDocument: Le modèle contenant le texte extrait.
        """
        
        reader = PdfReader(path)
        extracted_text_chunks = []

        # Extraction page par page
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text_chunks.append(page_text)
                
        # Jointure des pages avec un saut de ligne
        full_text = "\n".join(extracted_text_chunks)

        return ParsedDocument(
            filename=document.filename,
            text=full_text
        )