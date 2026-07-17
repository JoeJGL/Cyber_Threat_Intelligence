from abc import ABC, abstractmethod
from app.models.domain import Document, ParsedDocument, ExtractionResult




class BaseTextCleanerService(ABC):
    """Interface abstraite pour tous les services de nettoyage et normalisation de texte.
    
    Permet de nettoyer le texte brut extrait des documents avant de l'envoyer au NER.
    """

    @abstractmethod
    def clean(self, text: str) -> str:
        """Nettoie et normalise un texte brut.

        Args:
            text (str): Le texte d'origine potentiellement bruité.

        Returns:
            str: Le texte nettoyé et prêt pour l'analyse NLP.
        """
        pass

    
class BaseRelationExtractorService(ABC) :
    pass


class BaseParserService(ABC):
    """Interface abstraite pour tous les services de parsing de documents.
    
    Chaque parseur concret (PDF, TXT, HTML, etc.) doit hériter de cette classe
    et implémenter la méthode 'parse'.
    """

    @abstractmethod
    def parse(self, document: Document) -> ParsedDocument:
        """Extrait le texte brut à partir d'un Document binaire.

        Args:
            document (Document): Le document d'origine contenant les octets bruts.

        Returns:
            ParsedDocument: Le document contenant le texte extrait et nettoyé.
        """
        pass


class BaseNERService(ABC):
    """Interface abstraite pour tous les services de reconnaissance d'entités nommées.
    
    Chaque moteur de NER (spaCy, Transformers, etc.) doit hériter de cette classe
    et implémenter la méthode 'extract_entities'.
    """

    @abstractmethod
    def extract_entities(self, parsed_document: ParsedDocument) -> ExtractionResult:
        """Extrait les entités nommées à partir d'un document textuel.

        Args:
            parsed_document (ParsedDocument): Le document contenant le texte extrait.

        Returns:
            ExtractionResult: La structure contenant la liste des entités trouvées.
        """
        pass