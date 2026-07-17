import re
from app.services.base import BaseTextCleanerService


class RegexTextCleanerService(BaseTextCleanerService):
    """Implémentation concrète du nettoyeur de texte utilisant des expressions régulières."""

    def clean(self, text: str) -> str:
        """Nettoie le texte brut extrait des PDF (headers, pagination, césures...)."""
        if not text:
            return ""

        # 1. Retirer les headers/footers connus (ex: marquages TLP)
        text = text.replace("TLP:CLEAR", " ")
        text = text.replace("TLP:AMBER", " ")
        text = text.replace("TLP:RED", " ")

        # 2. Retirer la pagination (ex: "1/15", "12/20")
        text = re.sub(r"\b\d+/\d+\b", " ", text)

        # 3. Retirer les références de bas de page inline (ex: [1], [2, 3])
        text = re.sub(r"\[\s*\d+(?:,\s*\d+)*\s*\]", " ", text)

        # 4. Retirer les URLs pour éviter le bruit dans le texte brut
        text = re.sub(r"https?://\S+", " ", text)

        # 5. Retirer les césures PDF de fin de ligne (recolle les mots coupés)
        text = re.sub(r"-\n", "", text)

        # 6. Normalisation des espaces multiples et sauts de ligne en espaces simples
        text = re.sub(r"\s+", " ", text)

        return text.strip()