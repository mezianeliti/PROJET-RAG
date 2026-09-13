"""Étape 2 du RAG : nettoyer le texte brut extrait d'un PDF."""

from pypdf import PdfReader

CHEMIN_PDF = "documents/situation-holding-azazga-2026-08-v1.pdf"


def extraire_texte(chemin):
    """Lit un PDF et renvoie tout son texte, pages mises bout à bout."""
    lecteur = PdfReader(chemin)
    morceaux = []
    for page in lecteur.pages:
        morceaux.append(page.extract_text() or "")
    return "\n".join(morceaux)


def nettoyer(texte):
    """Enlève les espaces parasites et les lignes vides en trop."""
    lignes_propres = []

    for ligne in texte.split("\n"):
        ligne = ligne.strip()

        # On saute une ligne vide si la précédente l'était déjà.
        if ligne == "" and (not lignes_propres or lignes_propres[-1] == ""):
            continue

        lignes_propres.append(ligne)

    return "\n".join(lignes_propres).strip()


if __name__ == "__main__":
    brut = extraire_texte(CHEMIN_PDF)
    propre = nettoyer(brut)

    print("=== COMPARAISON ===")
    print(f"Avant : {len(brut):5d} caractères, {len(brut.splitlines()):3d} lignes")
    print(f"Après : {len(propre):5d} caractères, {len(propre.splitlines()):3d} lignes")
    print(f"Gain  : {len(brut) - len(propre):5d} caractères supprimés")

    print("\n=== TEXTE NETTOYÉ ===")
    print(propre)
