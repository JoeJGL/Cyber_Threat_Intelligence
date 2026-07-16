from pydantic import BaseModel, Field


class Document(BaseModel):
    """Représente le document brut initial avant tout traitement.

    Ce modèle sert de point d'entrée pour la phase de parsing. Il encapsule
    le fichier d'origine sous forme d'octets afin de ne pas dépendre du système
    de fichiers local.
    """

    filename: str = Field(..., description="Nom d'origine du fichier")
    content_type: str = Field(
        ..., description="Type MIME du document (ex: application/pdf)"
    )
    content: bytes = Field(..., description="Contenu brut du fichier en octets")


class ParsedDocument(BaseModel):
    """Représente le résultat textuel extrait du document initial.

    Ce modèle formalise la transition entre le document brut (binaire) et le
    texte brut nettoyé. C'est ce texte qui sera ensuite transmis au moteur NER (spaCy).
    """

    filename: str = Field(
        ..., description="Nom du fichier dont le texte est issu"
    )
    text: str = Field(..., description="Texte brut extrait du document")


class Entity(BaseModel):
    """Représente une entité nommée (ex: IP, Malware, Threat Actor) extraite par spaCy.

    Ce modèle stocke l'entité, sa classification (label) et ses indices de position
    (offsets) dans le texte d'origine. Ces offsets permettent de remonter à la source
    et de valider le contexte de l'extraction.
    """

    text: str = Field(..., description="Valeur textuelle de l'entité extraite")
    label: str = Field(
        ..., description="Type de l'entité (ex: 'IP', 'LOC', 'ORG')"
    )
    start: int = Field(
        ..., description="Indice de caractère de début dans le texte d'origine"
    )
    end: int = Field(
        ..., description="Indice de caractère de fin dans le texte d'origine"
    )


class ExtractionResult(BaseModel):
    """Conteneur regroupant l'ensemble des entités extraites d'un traitement.

    Ce modèle centralise les résultats du NER. Il offre une structure cohérente
    qui facilite le passage des données vers les étapes de traitement ultérieures
    (comme l'extraction de relations ou l'export).
    """

    entities: list[Entity] = Field(
        default_factory=list, description="Liste des entités extraites"
    )