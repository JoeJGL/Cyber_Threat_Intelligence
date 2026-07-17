# test_cleaner.py
from app.services.cleaners.basic_text_cleaner import RegexTextCleanerService

def test_text_cleaner():
    # 1. Texte bruité simulant un document PDF mal extrait
    noisy_text = """
    TLP:CLEAR
    This is an active cyber threat-
    intelligence report [1, 2]. 
    The threat actor group was seen using malicious tools. 
    More details can be found on https://malicious-domain.com/payload.exe
    
    1/12
    """

    print("=== TEST NETTOYAGE TEXTE ===")
    print("--- Texte d'origine (bruité) :")
    print(noisy_text)
    print("-" * 30)

    # 2. Initialisation et exécution du service
    cleaner = RegexTextCleanerService()
    cleaned_text = cleaner.clean(noisy_text)

    print("--- Texte après passage dans le RegexTextCleanerService :")
    print(cleaned_text)
    print("-" * 30)

    # 3. Assertions simples pour valider le résultat
    assert "TLP:CLEAR" not in cleaned_text, "Le tag TLP:CLEAR aurait dû être retiré."
    assert "1/12" not in cleaned_text, "La pagination aurait dû être retirée."
    assert "[1, 2]" not in cleaned_text, "Les références inline auraient dû être retirées."
    assert "https://" not in cleaned_text, "L'URL aurait dû être retirée."
    
    print("[+] Test réussi avec succès ! Toutes les regex ont fonctionné.")

if __name__ == "__main__":
    test_text_cleaner()