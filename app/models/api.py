from pydantic import BaseModel, Field
from app.models.domain import Entity


class ExtractionRequest(BaseModel):
    """Modèle de requête pour soumettre un texte à l'analyse NER.

    Permet à un client d'envoyer directement du texte brut à l'API de CTI
    sans devoir encapsuler l'envoi dans un fichier binaire complexe.
    """

    text: str = Field(
        ...,
        min_length=1,
        description="Le texte brut à analyser pour l'extraction d'entités",
    )


class ExtractionResponse(BaseModel):
    """Modèle de réponse standard retourné par l'API après analyse NER.

    Ce schéma réutilise directement le modèle de domaine 'Entity' pour garantir
    la cohérence des données renvoyées sans dupliquer la définition d'une entité.
    """

    entities: list[Entity] = Field(
        ..., description="Liste des entités CTI identifiées dans le texte"
    )