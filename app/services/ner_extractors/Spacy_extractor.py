import json
import ipaddress
import logging
import spacy
from spacy.language import Language
from spacy.tokens import Span

from app.config import THREAT_ACTORS_JSON_PATH, SPACY_MODEL_NAME
from app.models.domain import ParsedDocument, ExtractionResult, Entity
from app.services.base import BaseNERService

logger = logging.getLogger("cti_pipeline")

# =====================================================================
# Composants Personnalisés SpaCy (définis au niveau module)
# =====================================================================

@Language.component("ip_detector")
def ip_detector(doc):
    """Composant personnalisé pour valider et extraire IPv4/IPv6."""
    new_ents = list(doc.ents)
    for token in doc:
        try:
            ip = ipaddress.ip_address(token.text)
            label = "IPv4" if ip.version == 4 else "IPv6"
            span = Span(doc, token.i, token.i + 1, label=label)
            new_ents.append(span)
        except ValueError:
            pass
    doc.ents = spacy.util.filter_spans(new_ents)
    return doc


@Language.component("normalize_cve")
def normalize_cve(doc):
    """Composant de normalisation pour forcer les CVE en majuscules."""
    for ent in doc.ents:
        if ent.label_ == "VULNERABILITY":
            ent._.set("normalized", ent.text.upper())
    return doc


# Initialisation de l'extension personnalisée spaCy
if not Span.has_extension("normalized"):
    Span.set_extension("normalized", default=None)


# =====================================================================
# Service Principal d'Extraction
# =====================================================================

class SpacyNERService(BaseNERService):
    """Implémentation concrète de l'extracteur d'entités CTI utilisant spaCy."""

    def __init__(self) -> None:
        """Initialise le modèle spaCy et configure le pipeline NLP."""
        logger.info(f"Chargement du modèle spaCy : {SPACY_MODEL_NAME}...")
        self.nlp = spacy.load(SPACY_MODEL_NAME)

        # 1. Ajout de l'EntityRuler
        self.ruler = self.nlp.add_pipe(
            "entity_ruler",
            before="ner",
            config={"overwrite_ents": False}
        )

        # 2. Chargement et configuration des patterns
        self._load_pipeline_patterns()

        # 3. Ajout des étapes de post-traitement personnalisées
        self.nlp.add_pipe("ip_detector", after="entity_ruler")
        self.nlp.add_pipe("normalize_cve", last=True)
        logger.info("Pipeline NLP CTI initialisé avec succès.")

    def _load_pipeline_patterns(self) -> None:
        """Définit les expressions régulières et charge les Threat Actors."""
        patterns = [
            # CVE
            {
                "label": "VULNERABILITY",
                "pattern": [{"TEXT": {"REGEX": r"(?i)^CVE-\d{4}-\d{4,7}$"}}]
            },
            # Hachages
            {"label": "SHA256", "pattern": [{"TEXT": {"REGEX": r"^[A-Fa-f0-9]{64}$"}}]},
            {"label": "SHA1", "pattern": [{"TEXT": {"REGEX": r"^[A-Fa-f0-9]{40}$"}}]},
            {"label": "MD5", "pattern": [{"TEXT": {"REGEX": r"^[A-Fa-f0-9]{32}$"}}]},
            # Réseau / IOCs
            {"label": "EMAIL", "pattern": [{"TEXT": {"REGEX": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"}}]},
            {"label": "DOMAIN", "pattern": [{"TEXT": {"REGEX": r"^(?:[a-zA-Z0-9-]+\.)+[A-Za-z]{2,}$"}}]},
            {"label": "URL", "pattern": [{"TEXT": {"REGEX": r"^(?:https?|hxxps?)://.*"}}]}
        ]

        # Chargement dynamique des Threat Actors depuis le fichier JSON configuré
        try:
            with open(THREAT_ACTORS_JSON_PATH, "r", encoding="utf8") as f:
                actors = json.load(f)
            
            for actor in actors:
                tokens = actor.lower().split()
                patterns.append({
                    "label": "THREAT_ACTOR",
                    "pattern": [{"LOWER": t} for t in tokens]
                })
            logger.info(f"{len(actors)} Threat Actors chargés depuis le dictionnaire.")
        except FileNotFoundError:
            logger.warning(
                f"Fichier Threat Actors introuvable à l'adresse : {THREAT_ACTORS_JSON_PATH}. "
                "Le pipeline fonctionnera sans le dictionnaire des Threat Actors."
            )

        self.ruler.add_patterns(patterns)

    def extract_entities(self, parsed_document: ParsedDocument) -> ExtractionResult:
        """Analyse le texte du document et extrait les IOCs et entités nommées.
        
        Args:
            parsed_document (ParsedDocument): Le document d'entrée contenant le texte brut.
            
        Returns:
            ExtractionResult: La structure contenant la liste d'objets 'Entity' de notre domaine.
        """
        # Exécution du pipeline spaCy
        doc = self.nlp(parsed_document.text)
        
        extracted_entities = []
        for ent in doc.ents:
            # Mapping direct vers notre modèle de domaine Pydantic
            entity_domain = Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            )
            extracted_entities.append(entity_domain)

        return ExtractionResult(entities=extracted_entities)